import json
import uuid


class LambdaConfig(object):
    def __init__(self, app_name, build_name, branch_name, build_session_id, collector_url):
        self.appName = app_name
        self.buildName = build_name
        self.branchName = branch_name
        self.buildSessionId = build_session_id
        self.collectorUrl = collector_url
        self.agentId = uuid.uuid4().hex

    # save config file to json with the workspace path
    def save_to_file(self, file_path):
        with open(file_path, 'w') as f:
            json.dump(self.__dict__, f)
