#!/usr/bin/env python
import crowdai_api
import time

TOTAL_STEPS = 10
STEP_SLEEP = 0.2

predictions = []

########################################################################
# Instatiate Event Notifier
########################################################################
crowdai_events = crowdai_api.events.CrowdAIEvents()

########################################################################
# Register Evaluation Start event
########################################################################
crowdai_events.register_event(
            event_type=crowdai_events.CROWDAI_EVENT_INFO,
            message="evaluation_started",
            payload={ #Arbitrary Payload
                "type": "example_contractor:evaluation_started",
                "evaluation_state" : predictions
                }
            )

for step in range(TOTAL_STEPS):
    print("Current Step : ", step)
    ########################################################################
    # Register Evaluation Progress event
    ########################################################################
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_INFO,
                message="evaluation_progress : {}/{}".format(step, TOTAL_STEPS),
                payload={ #Arbitrary Payload
                    "type": "example_contractor:evaluation_progress",
                    "evaluation_state" : predictions
                    }
                )
    time.sleep(STEP_SLEEP)


########################################################################
# Register Evaluation Complete event
########################################################################
crowdai_events.register_event(
            event_type=crowdai_events.CROWDAI_EVENT_SUCCESS,
            message="evaluation_success",
            payload={ #Arbitrary Payload
                "type": "example_contractor:evaluation_complete",
                "evaluation_state" : predictions
                }
            )
