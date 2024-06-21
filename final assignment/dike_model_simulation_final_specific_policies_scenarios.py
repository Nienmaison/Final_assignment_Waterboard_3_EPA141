import pandas as pd
from ema_workbench import Model, MultiprocessingEvaluator, Policy, Scenario

from ema_workbench.em_framework.evaluators import perform_experiments
from ema_workbench.em_framework.samplers import sample_uncertainties
from ema_workbench.util import ema_logging, save_results
import time
from problem_formulation_project_final import get_model_for_problem_formulation

"""

This Python file is used to generate experiments for all 857 policies found by direct search and the five scenarios 
found by scenario discovery. This step is crucial before determining the Pareto optimal solutions among the policies 
found in the direct search. By evaluating each policy across all five scenarios, we mitigate the risk of accidentally 
excluding scenarios that may not be considered 'Pareto optimal' by the algorithm. In other words, each policy is tested
on all five scenarios, rather than just one scenario where the policy was found to be effective. 
By calculating the performance of each policy on all five scenarios and then averaging the results, we assess whether 
the policy is robust across all scenarios. Consequently, the Pareto optimal solutions derived from this approach 
will be robust across all scenarios.

For this analysis, we use problem formulation 8 as we are still refining the optimisation process and want to focus 
on the specific outcomes that are critical for Water Board 3.

"""

if __name__ == "__main__":
    ema_logging.log_to_stderr(ema_logging.INFO)

    # Load the 857 policies from a CSV file
    policies_df = pd.read_csv("data/857_policies_optimization.csv")

    # Use problem formulation 8
    dike_model, planning_steps = get_model_for_problem_formulation(8)

    # Load the five specific scenarios from a CSV file
    scenarios_df = pd.read_csv("data/final_scenarios_final.xls")

    # Convert the specific scenarios in scenarios_df to Scenario objects
    scenarios = []
    for index, row in scenarios_df.iterrows():
        scenario_dict = row.to_dict()
        scenarios.append(Scenario(f"scenario_{index + 1}", **scenario_dict))

    # Convert the policies in policies_df to Policy objects
    policies = []
    for index, row in policies_df.iterrows():
        policy_dict = row.to_dict()
        policy_name = f"policy_{index + 1}"
        policy_dict['policy_name'] = policy_name  # Add policy name to the dictionary
        policies.append(Policy(policy_name, **policy_dict))

    # Run experiments for each policy on the five specific scenarios
    all_results = []
    for policy in policies:
        results = perform_experiments(dike_model, scenarios=scenarios, policies=[policy])
        experiments, outcomes = results
        experiments_df = pd.DataFrame.from_dict(experiments)
        outcomes_df = pd.DataFrame.from_dict(outcomes)
        combined_df = pd.concat([experiments_df, outcomes_df], axis=1)
        combined_df['policy_name'] = policy.name
        all_results.append(combined_df)

    # Concatenate all results into a single DataFrame
    final_results_df = pd.concat(all_results, ignore_index=True)

    # Save the combined results to a single CSV file
    final_results_df.to_csv("dike_model_combined_results.csv", index=False)
