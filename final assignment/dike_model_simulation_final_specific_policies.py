import pandas as pd
from ema_workbench import Model, MultiprocessingEvaluator, Policy, Scenario

from ema_workbench.em_framework.evaluators import perform_experiments
from ema_workbench.em_framework.samplers import sample_uncertainties
from ema_workbench.util import ema_logging, save_results
import time
from problem_formulation_project_final import get_model_for_problem_formulation

"""

This Python script is designed to randomly generate 20000 scenarios and evaluate them against five specific policies. 
This process helps to assess the robustness of the policies identified in the direct search. Robust policies are 
expected to reduce the occurrence of unfavourable scenarios within our problem space.

In this analysis, problem formulation 7 is used to explore the entire uncertainty space for these five specific 
policies. This approach ensures that no critical outcomes are overlooked, similar to the open exploration phase.

Ultimately, this script runs a total of 100000 experiments (5 policies * 20000 scenarios) for scenario discovery.

"""

if __name__ == "__main__":
    ema_logging.log_to_stderr(ema_logging.INFO)

    # Load the five policies from a CSV file
    policies_df = pd.read_csv("data/5_best_policies.csv")

    # Use problem formulation 7
    dike_model, planning_steps = get_model_for_problem_formulation(7)

    # Build a user-defined scenario
    reference_values = {
        "Bmax": 175,
        "Brate": 1.5,
        "pfail": 0.5,
        "ID flood wave shape": 4,
        "planning steps": 2,
    }
    reference_values.update({f"discount rate {n}": 3.5 for n in planning_steps})
    scen1 = {}

    for key in dike_model.uncertainties:
        name_split = key.name.split("_")
        if len(name_split) == 1:
            scen1.update({key.name: reference_values[key.name]})
        else:
            scen1.update({key.name: reference_values[name_split[1]]})

    ref_scenario = Scenario("reference", **scen1)

    # Convert the five policies in policies_df to Policy objects
    policies = []
    for index, row in policies_df.iterrows():
        policy_dict = row.to_dict()
        policy_name = policy_dict.pop('policy_name')
        policies.append(Policy(policy_name, **policy_dict))

    # Sample 20000 scenarios randomly
    scenarios = sample_uncertainties(dike_model, 20000)

    # Run experiments for each policy
    # Separate csv files are generated for each policy. We will use these files for scenario discovery.
    all_results = []
    for policy in policies:
        results = perform_experiments(dike_model, scenarios=scenarios, policies=policy)
        all_results.append(results)
        save_results(results, f"dike_model_results_policy_{policy.name}.tar.gz")