#!/usr/bin/env python
import crowdai_helpers
import time

TOTAL_STEPS = 10
STEP_SLEEP = 0.2

evaluation_state = {}

crowdai_helpers.evaluation_start(evaluation_state)

for step in range(TOTAL_STEPS):
    print("Current Step : ", step)
    time.sleep(STEP_SLEEP)
    crowdai_helpers.evaluation_progress(evaluation_state)

crowdai_helpers.evaluation_success(evaluation_state)
