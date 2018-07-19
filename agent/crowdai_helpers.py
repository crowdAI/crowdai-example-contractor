#!/usr/bin/env python
import crowdai_api

########################################################################
# Instatiate Event Notifier
########################################################################
crowdai_events = crowdai_api.events.CrowdAIEvents()


def execution_start():
    ########################################################################
    # Register Evaluation Start event
    ########################################################################
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_INFO,
                message="execution_started",
                payload={ #Arbitrary Payload
                    "type": "example_contractor:execution_started"
                    }
                )


def execution_progress(progress_payload):
    step = progress_payload["step"]
    ########################################################################
    # Register Evaluation Progress event
    ########################################################################
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_INFO,
                message="execution_progress : {}".format(step),
                payload={ #Arbitrary Payload
                    "type": "example_contractor:execution_progress",
                    "step" : step
                    }
                )

def execution_success():
    ########################################################################
    # Register Evaluation Complete event
    ########################################################################
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_SUCCESS,
                message="execution_success",
                payload={ #Arbitrary Payload
                    "type": "example_contractor:execution_success",
                    },
                blocking=True
                )

def execution_error(error):
    ########################################################################
    # Register Evaluation Complete event
    ########################################################################
    crowdai_events.register_event(
                event_type=crowdai_events.CROWDAI_EVENT_ERROR,
                message="execution_error",
                payload={ #Arbitrary Payload
                    "type": "example_contractor:execution_error",
                    "error" : error
                    },
                blocking=True
                )
