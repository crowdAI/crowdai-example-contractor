#!/usr/bin/env python
import crowdai_helpers
import time

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

TOTAL_STEPS = 10
STEP_SLEEP = 0.2

evaluation_state = {}

"""
    Register Event Start
"""
crowdai_helpers.evaluation_start(evaluation_state)

for step in range(TOTAL_STEPS):
    print("Current Step : ", step)
    time.sleep(STEP_SLEEP)
    crowdai_helpers.evaluation_progress(evaluation_state)

crowdai_helpers.evaluation_success(evaluation_state)
