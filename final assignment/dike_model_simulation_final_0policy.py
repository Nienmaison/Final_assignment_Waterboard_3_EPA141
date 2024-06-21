from ema_workbench import Model, MultiprocessingEvaluator, Policy, Scenario

from ema_workbench.em_framework.evaluators import perform_experiments
from ema_workbench.em_framework.samplers import sample_uncertainties
from ema_workbench.util import ema_logging, save_results
import time
from problem_formulation_project_final import get_model_for_problem_formulation

"""

This Python file is used to randomly generate 100000 scenarios with a zero policy.
The zero policy means that no policies are implemented, so no dike investment, no room for the river,  
and no prior warnings are given. 

This results in a total of 100000 experiments used for scenario discovery. 

"""

if __name__ == "__main__":
    ema_logging.log_to_stderr(ema_logging.INFO)

    # Use problem formulation 7
    dike_model, planning_steps = get_model_for_problem_formulation(7)

    # Build a user-defined scenario and policy:
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

    # This is the zero policy where no policy measures are implemented,
    # in other words no dike increase, no warning, none of the rfr.
    zero_policy = {"DaysToThreat": 0}
    zero_policy.update({f"DikeIncrease {n}": 0 for n in planning_steps})
    zero_policy.update({f"RfR {n}": 0 for n in planning_steps})
    pol0 = {}

    for key in dike_model.levers:
        s1, s2 = key.name.split("_")
        pol0.update({key.name: zero_policy[s2]})

    policy0 = Policy("Policy 0", **pol0)

    # Call random 100.000 scenarios and policies:
    scenarios = sample_uncertainties(dike_model, 100000)

    # Generate 100.000 experiments
    results = perform_experiments(dike_model, scenarios=scenarios, policies=policy0)

    # Save results to a file
    save_results(results, "dike_model_results_100k_experiments_id_7_plus_casualties.tar.gz")