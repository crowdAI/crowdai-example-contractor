#!/usr/bin/env python

import crowdai_api
import traceback
import logging
import json
import numpy as np

class CrowdAISubContractor:
    def __init__(self):
        self.agent_events = crowdai_api.events.CrowdAIEvents()
        self.oracle_events = crowdai_api.events.CrowdAIEvents(with_oracle=True)
        self.evaluation_state = {
            "steps": []
        }

    def handle_info_event(self, payload):
        if payload["event_type"] == "example_contractor:execution_started":
            self.evaluation_state["steps"] = []
            self.evaluation_state["state"] = "execution_started"
            self.oracle_events.register_event(
                event_type=self.oracle_events.CROWDAI_EVENT_INFO,
                payload=self.evaluation_state
            )

        elif payload["event_type"] == "example_contractor:execution_progress":
            _step = payload["step"]
            self.evaluation_state["steps"].append(_step)
            self.evaluation_state["state"] = "execution_progress"

            self.oracle_events.register_event(
                event_type=self.oracle_events.CROWDAI_EVENT_INFO,
                payload=self.evaluation_state
            )
        else:
            raise Exception("Unknown event_type")

    def handle_success_event(self, payload):
        self.evaluation_state["state"] = "execution_success"
        _score_object = {
            "score" : np.mean(self.evaluation_state["steps"]),
            "score_secondary" : np.median(self.evaluation_state["steps"])
        }
        self.evaluation_state["score"] = _score_object
        self.evaluation_state["state"] = "execution_success"
        self.oracle_events.register_event(
            event_type=self.oracle_events.CROWDAI_EVENT_SUCCESS,
            payload=self.evaluation_state
        )

    def handle_error_event(self, payload):
        self.evaluation_state["error"] = payload["error"]
        self.evaluation_state["state"] = "execution_error"
        self.oracle_events.register_event(
            event_type=self.oracle_events.CROWDAI_EVENT_ERROR,
            message="Error in Agent. Please refer to the logs.",
            payload=self.evaluation_state
        )

    def run(self):
        for _agent_event in self.agent_events:
            payload = _agent_event["payload"]
            if _agent_event["event_type"] == self.agent_events.CROWDAI_EVENT_INFO:
                self.handle_info_event(payload)
            elif _agent_event["event_type"] == self.agent_events.CROWDAI_EVENT_SUCCESS:
                self.handle_success_event(payload)
            elif _agent_event["event_type"] == self.agent_events.CROWDAI_EVENT_ERROR:
                self.handle_error_event(payload)
            else:
                raise Exception("Unknown event_type received")


if __name__ == "__main__":
    subcontractor = CrowdAISubContractor()
    try:
        subcontractor.run()
    except Exception as e:
        error = traceback.format_exc()
        print(error)
        subcontractor.oracle_events.register_event(
            event_type=subcontractor.oracle_events.CROWDAI_EVENT_ERROR,
            message=error
        )
