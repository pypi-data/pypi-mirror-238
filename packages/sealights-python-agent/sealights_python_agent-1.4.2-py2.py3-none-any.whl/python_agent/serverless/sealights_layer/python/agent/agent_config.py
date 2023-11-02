import json
import os
import uuid

__version__ = "1.0.0"


class AgentConfig(object):
    def __init__(self):
        self.appName = ""
        self.buildName = ""
        self.branchName = ""
        self.buildSessionId = ""
        self.collectorUrl = ""
        self.labId = ""
        self.agentId = ""
        self.agentVersion = __version__
        self.agentType = "PythonLambdaAgent"

    def load_from_env_or_file(self, filename):
        # Load from environment or set to default values from the file
        with open(filename, "r") as f:
            file_data = json.load(f)

        self.appName = os.environ.get('SL_APP_NAME', file_data.get('appName', ''))
        self.buildName = os.environ.get('SL_BUILD_NAME', file_data.get('buildName', ''))
        self.branchName = os.environ.get('SL_BRANCH_NAME', file_data.get('branchName', ''))
        self.buildSessionId = os.environ.get('SL_BUILD_SESSION_ID', file_data.get('buildSessionId', ''))
        self.collectorUrl = os.environ.get('SL_COLLECTOR_URL', file_data.get('collectorUrl', ''))
        self.labId = os.environ.get('SL_LAB_ID', self.buildSessionId)
        self.agentId = os.environ.get('AGENT_ID', uuid.uuid4().hex)

    def validate(self):
        attributes = vars(self)
        for attr, value in attributes.items():
            if not value:
                raise ValueError(f"Agent config Error: The attribute '{attr}' cannot be empty or None.")

    def __str__(self):
        return str(self.__dict__)
