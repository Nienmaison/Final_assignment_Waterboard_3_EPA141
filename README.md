This read me guides you through the folder with our files and provides explanation as to which files we have used and created.

Structure of created and edited files in final assignment folder:

Notebooks for analysis;

global_sensitivity_analysis_final.ipynb,

open_exploration_final.ipynb,

directed_search_final.ipynb,

robustness_analysis_final.ipynb,

Python files for simulation/optimization;

optimization.py (just for some minor bugs),

problem_formulation_project_final.py (adjusted problem formulations for simulation and optimization),

dike_model_simulation_final_0policy.py (simulation file used for the scenario discovery based on a 'zero policy'),

dike_model_optimization_project_final.py (Optimization of policies with our 5 picked scenarios from scenario discovery),

dike_model_simulation_final_specific_policies_scenarios.py (857 found policies in optimization simulated times the 5 found scenarios to create experiments of each policy over every scenario),

dike_model_simulation_final_specific_policies.py (Final simulation of 5 policies, each simulated 20.000 times over random scenarios to further analyze robustness),

CSV- and output files:

dike_model_results_100k_experiments_id_7_plus_casualties.tar.gz (output: dike_model_simulation_final_0policy.py --- input: scenario_discovery_final.ipynb),

final_scenarios_final.xls (output:scenario_discovery_final.ipynb),

final_assignment/data/directed_search/ -- optimization files: optimization_results_seed_0_scenario_0.csv -- seed 0 through 4 and scenario 0 through 4 -- 5x5= 25 files in total.

final_assignment/data/directed_search/convergence/ -- convergence files: convergence_data_seed_0_scenario_0.csv -- seed 0 through 4 and scenario 0 through 4 -- 5x5= 25 files in total.

final_assignment/data/directed_search/metrics/ -- metrics_seed_0.csv up until metrics_seed_4.csv,

857_policies_optimization.csv (Input: dike_model_simulation_final_specific_policies_scenarios.py),

dike_model_combined_results.csv (output: dike_model_simulation_final_specific_policies_scenarios.py input: directed_search_final.ipynb),

5_best_policies.csv (output: directed_search_final.ipynb input: dike_model_simulation_final_specific_policies.py),

output of: dike_model_simulation_final_specific_policies.py input for: robustness_analysis_final.ipynb,

dike_model_results_policy_policy_13.tar.gz

dike_model_results_policy_policy_34.tar.gz

dike_model_results_policy_policy_133.tar.gz

dike_model_results_policy_policy_138.tar.gz

dike_model_results_policy_policy_157.tar.gz


The rest of the files in the folder are untouched and directly pulled from: https://github.com/quaquel/epa141A_open/tree/master/final%20assignment
