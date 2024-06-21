from ema_workbench import (
    Model,
    MultiprocessingEvaluator,
    ScalarOutcome,
    IntegerParameter,
    optimize,
    Scenario,
    HypervolumeMetric,
    GenerationalDistanceMetric,
    EpsilonIndicatorMetric,
    InvertedGenerationalDistanceMetric,
    SpacingMetric,
)
from ema_workbench.em_framework.optimization import EpsilonProgress, to_problem, epsilon_nondominated, ArchiveLogger
from ema_workbench.util import ema_logging
from problem_formulation_project_final import get_model_for_problem_formulation
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import shutil

"""

This script is used for direct search.

The five scenarios identified in the open exploration step are used here to generate possible policies. First, 
a function is created to generate possible policies for a given scenario and seed. This function is then used in the 
code below to iterate over the five scenarios.

The last part of the code is designed to plot convergence metrics needed to check if an NFE
 (Number of Function Evaluations) of 20000 is sufficient to converge to a set of policies.

The code uses problem formulation 8. This formulation is specifically designed for optimization, aiming to minimize 
all outcomes and focusing only on the outcomes that are critical for Water Board 3.

"""

def run_optimization_with_scenario(experiment_values, seed):
    ema_logging.log_to_stderr(ema_logging.INFO)

    # Use problem formulation 8
    model, steps = get_model_for_problem_formulation(8)

    # Create a scenario based on the provided experiment values
    scen = {}
    for key in model.uncertainties:
        scen.update({key.name: experiment_values[key.name]})
    scenario = Scenario("experiment_based", **scen)

    # # Ensure the archives directory exists and is empty
    archives_dir = "./archives"

    # Set convergence metrics, epsilon values and nfe for optimization over levers and outcomes
    convergence_metrics = [
        ArchiveLogger(
            archives_dir,
            [l.name for l in model.levers],
            [o.name for o in model.outcomes],
            base_filename=f"{seed}.tar.gz",
        ),
        EpsilonProgress(),
    ]
    epsilon = [0.1] * len(model.outcomes) # For each outcome the epsilon is set to 0.1
    nfe = 20000  # The number of function evaluations is here set to 20000

    # Run the optimization
    with MultiprocessingEvaluator(model) as evaluator:
        result, convergence = evaluator.optimize(
            nfe=nfe,
            searchover="levers",
            epsilons=epsilon,
            convergence=convergence_metrics,
            reference=scenario,
        )
    print("exited optimizer")

    return result, convergence

if __name__ == "__main__":

# This code iterates over the five scenarios and optimizes for each seed x scenario combination.

    # Load the dataframe with the five scenarios found during open exploration
    experiments_df = pd.read_csv('data/final_scenarios_final.xls')

    model, steps = get_model_for_problem_formulation(8)

    # Iterate over each experiment and perform the optimization, we do this for 5 seeds.
    results = []
    convergences = []

    for seed in range(5):  # run for 5 seeds
        for index, experiment in experiments_df.iterrows():
            experiment_values = experiment.to_dict()
            result, convergence = run_optimization_with_scenario(experiment_values, seed)

            result_df = pd.DataFrame(result)
            #result_df['seed'] = seed
            result_file_name = f'optimization_results_seed_{seed}_scenario_{index}.csv'
            result_df.to_csv(result_file_name, index=False)

            convergence_df = pd.DataFrame(convergence.epsilon_progress)
            #convergence_df['seed'] = seed
            convergence_file_name = f'convergence_data_seed_{seed}_scenario_{index}.csv'
            convergence_df.to_csv(convergence_file_name, index=False)

            results.append(result_df)
            convergences.append(convergence_df)

# Here starts the code for the convergence metrics.

    # Load the archives into memory
    all_archives = []
    for i in range(5):
        archives = ArchiveLogger.load_archives(f"./archives/{i}.tar.gz")
        for key in archives:
            if 'Unnamed: 0' in archives[key].columns:
                archives[key].drop(columns=['Unnamed: 0'], inplace=True)
        all_archives.append(archives)

    problem = to_problem(model, searchover="levers")

    # Define metrics
    epsilon = [0.05] * len(model.outcomes)
    reference_set = epsilon_nondominated(results, epsilon, problem)

    hv = HypervolumeMetric(reference_set, problem)
    gd = GenerationalDistanceMetric(reference_set, problem, d=1)
    ei = EpsilonIndicatorMetric(reference_set, problem)
    ig = InvertedGenerationalDistanceMetric(reference_set, problem, d=1)
    sm = SpacingMetric(problem)

    # Calculate metrics for each archive and store results
    metrics_by_seed = []
    for archives in all_archives:
        metrics = []
        for nfe, archive in archives.items():
            scores = {
                "generational_distance": gd.calculate(archive),
                "hypervolume": hv.calculate(archive),
                "epsilon_indicator": ei.calculate(archive),
                "inverted_gd": ig.calculate(archive),
                "spacing": sm.calculate(archive),
                "nfe": int(nfe),
            }
            metrics.append(scores)
        metrics = pd.DataFrame.from_dict(metrics)

        # Sort metrics by number of function evaluations
        metrics.sort_values(by="nfe", inplace=True)
        metrics_by_seed.append(metrics)

    # Save the metrics
    for seed, metrics in enumerate(metrics_by_seed):
        metrics_file_name = f'metrics_seed_{seed}.csv'
        metrics.to_csv(metrics_file_name, index=False)


