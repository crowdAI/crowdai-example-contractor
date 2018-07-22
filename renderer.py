#!/usr/bin/env python

import os
from jinja2 import Environment, FileSystemLoader
import uuid
import json
import yaml
import time

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

        # Render Cache settings
        self.last_note_text = ""
        self.global_issue_update_frequency = 5
        self.last_issue_note_update_time = time.time()

    def render_pod_spec(self, params):
        template = self.jinja_env.get_template("pod_spec/pod_spec.yaml")
        pod_spec = yaml.load(template.render(
            challenge_config=self.challenge_config,
            params=params
            ))
        return pod_spec

    def render_evaluation_state(self, evaluation_state):
        _evaluation_state = {
            "state" : "execution_pending",
            "steps" : [],
        }
        _evaluation_state.update(evaluation_state)
        return """
```

        {}

```
        """.format(json.dumps(evaluation_state, indent=4))
        # template = self.jinja_env.get_template(
        #     "evaluation_state/evaluation_state.yaml"
        #     )
        # return template.render(
        #     evaluation_state=_evaluation_state
        # )

    def update_evaluation_log(self, evaluation_state, gl_note, force_update=False):
        if force_update or (time.time() - self.last_issue_note_update_time > self.global_issue_update_frequency):
            note_text = self.render_evaluation_state(evaluation_state)
            if note_text != self.last_note_text and note_text.strip() != "":
                gl_note.body = note_text
                gl_note.save()
                self.last_issue_note_update_time = time.time()
                self.last_note_text = note_text


if __name__ == "__main__":

    challenge_config = json.loads(open("config.json").read())

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
