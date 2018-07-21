#!/usr/bin/env python

import os
from jinja2 import Environment, FileSystemLoader
import uuid

class CrowdAIRenderer:
    def __init__(self, challenge_config, templates_folder=False):
        self.challenge_config = challenge_config
        if templates_folder:
            self.templates_folder = templates_folder
        else:
            self.templates_folder = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "templates"
            )
        self.file_loader = FileSystemLoader(self.templates_folder)
        self.jinja_env = Environment(loader=self.file_loader)

    def render_pod_spec(self, params):
        template = self.jinja_env.get_template("pod_spec/pod_spec.yaml")
        return template.render(
            challenge_config=self.challenge_config,
            params=params
            )

if __name__ == "__main__":

    challenge_config = {}
    challenge_config["subcontractor_image"] = "crowdaidocker/example-subcontractor"
    challenge_config["resources"] = {
        "redis" : {
            "requests": {
                "cpu" : 1,
                "memory" : "2048Mi"
                },
            "limits" : {
                "cpu" : 1,
                "memory" : "2048Mi"
            }
        },
        "subcontractor" : {
            "requests": {
                "cpu" : 1,
                "memory" : "2048Mi",
                "gpu" : 0
                },
            "limits" : {
                "cpu" : 1,
                "memory" : "2048Mi",
                "gpu" : 0
            }
        },
        "agent" : {
            "requests": {
                "cpu" : 1,
                "memory" : "2048Mi",
                "gpu" : 0
                },
            "limits" : {
                "cpu" : 2,
                "memory" : "4096Mi",
                "gpu" : 0
            }
        }
    }

    params = {}
    params["pod_name"] = "example-pod-name"
    params["app_name"] = params["pod_name"]

    agent_communication_channel = str(uuid.uuid4())
    params["agents"] = []
    _agent = {
        "name" : "agent",
        "image" : "crowdaidocker/example-agent",
        "communication_channel" : agent_communication_channel,
        "blocking_response_channel" : str(uuid.uuid4()),
        "id": "agent-{}".format(str(uuid.uuid4())),
        "gpu" : True
    }
    params["agents"].append(_agent)

    params["subcontractor_communication_channel"] = agent_communication_channel
    params["subcontractor_oracle_communication_channel"] = str(uuid.uuid4())
    params["subcontractor_blocking_response_channel"] = str(uuid.uuid4())
    params["subcontractor_id"] = "subcontractor-{}".format(str(uuid.uuid4()))

    renderer = CrowdAIRenderer(challenge_config=challenge_config)

    pod_spec_yaml = renderer.render_pod_spec(params=params)
    print(pod_spec_yaml)
