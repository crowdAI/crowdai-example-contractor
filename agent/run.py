#!/usr/bin/env python
import crowdai_helpers
import time
import traceback

"""
Note that, if you do not already have an established protocol for
communication with the components in the sub-contractor
(like in the case of multiplayer games, or a REST API accessible through local host),
then you can use these functions to establish communication with the sub contractor.
These calls can very well be abstacted away in your custom library for the challenge.

In any case, no messages or events sent from the agent are directly related to
the oracle (crowdai-contractor), and instead the main events used by the crowdai-contractor
are the ones relayed to it by the crowdai-subcontractor.
"""
execution_state = {}

def run():
    TOTAL_STEPS = 10
    STEP_SLEEP = 0.2

    execution_state["steps"] = []
    execution_state["TOTAL_STEPS"] = TOTAL_STEPS

    """
        Register Prediction Start
    """
    crowdai_helpers.execution_start(execution_state)

    for step in range(TOTAL_STEPS):
        print("Current Step : ", step)
        execution_state["steps"].append(step)

        """
            Register Event Start
        """
        crowdai_helpers.execution_progress(execution_state)
        time.sleep(STEP_SLEEP)

    crowdai_helpers.execution_success(execution_state)

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        error = traceback.format_exc()
        print(error)
        execution_state["errors"] = [error]
        crowdai_helpers.execution_error(execution_state)
