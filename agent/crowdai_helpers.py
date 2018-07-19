#!/usr/bin/env python
import crowdai_api

########################################################################
# Instatiate Event Notifier
########################################################################
crowdai_events = crowdai_api.events.CrowdAIEvents()


def evaluation_start(evaluation_state):
    ########################################################################
    # Register Evaluation Start event
    ########################################################################
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_INFO,
                message="evaluation_started",
                payload={ #Arbitrary Payload
                    "type": "example_contractor:evaluation_started",
                    "evaluation_state" : evaluation_state
                    }
                )


def evaluation_progress(evaluation_state):
    step = evaluation_state["step"]
    TOTAL_STEPS = evaluation_state["TOTAL_STEPS"]
    ########################################################################
    # Register Evaluation Progress event
    ########################################################################
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_INFO,
                message="evaluation_progress : {}/{}".format(step, TOTAL_STEPS),
                payload={ #Arbitrary Payload
                    "type": "example_contractor:evaluation_progress",
                    "evaluation_state" : evaluation_state
                    }
                )

def evaluation_success(evaluation_state):
    ########################################################################
    # Register Evaluation Complete event
    ########################################################################
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_SUCCESS,
                message="evaluation_success",
                payload={ #Arbitrary Payload
                    "type": "example_contractor:evaluation_complete",
                    "evaluation_state" : evaluation_state
                    },
                blocking=True
                )
