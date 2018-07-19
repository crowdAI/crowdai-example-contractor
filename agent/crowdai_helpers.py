#!/usr/bin/env python
import crowdai_api

########################################################################
# Instatiate Event Notifier
########################################################################
crowdai_events = crowdai_api.events.CrowdAIEvents()


def execution_start(execution_state):
    ########################################################################
    # Register Evaluation Start event
    ########################################################################
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_INFO,
                message="execution_started",
                payload={ #Arbitrary Payload
                    "type": "example_contractor:execution_started",
                    "execution_state" : execution_state
                    }
                )


def execution_progress(execution_state):
    steps = execution_state["steps"]
    TOTAL_STEPS = execution_state["TOTAL_STEPS"]
    ########################################################################
    # Register Evaluation Progress event
    ########################################################################
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_INFO,
                message="execution_progress : {}/{}".format(len(steps), TOTAL_STEPS),
                payload={ #Arbitrary Payload
                    "type": "example_contractor:execution_progress",
                    "execution_state" : execution_state
                    }
                )

def execution_success(execution_state):
    ########################################################################
    # Register Evaluation Complete event
    ########################################################################
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_SUCCESS,
                message="execution_success",
                payload={ #Arbitrary Payload
                    "type": "example_contractor:execution_success",
                    "execution_state" : execution_state
                    },
                blocking=True
                )

def execution_error(execution_state):
    ########################################################################
    # Register Evaluation Complete event
    ########################################################################
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_ERROR,
                message="execution_error",
                payload={ #Arbitrary Payload
                    "type": "example_contractor:execution_error",
                    "execution_state" : execution_state
                    },
                blocking=True
                )
