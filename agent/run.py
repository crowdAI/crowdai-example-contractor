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

def run():
    TOTAL_STEPS = 10
    STEP_SLEEP = 0.2

    """
        Register Prediction Start
    """
    crowdai_helpers.execution_start()

    for step in range(TOTAL_STEPS):
        print("Current Step : ", step)
        """
            Register Event Start
        """
        _progress_payload = {}
        _progress_payload["step"] = step
        crowdai_helpers.execution_progress(_progress_payload) # Can be any arbitrary data
        time.sleep(STEP_SLEEP)

    crowdai_helpers.execution_success()

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        error = traceback.format_exc()
        crowdai_helpers.execution_error(error)
