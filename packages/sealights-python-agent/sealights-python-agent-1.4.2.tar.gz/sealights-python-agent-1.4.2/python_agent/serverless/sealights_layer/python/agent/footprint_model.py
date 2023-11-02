from typing import List, Optional

from agent_config import AgentConfig


class TechSpecificInfo:
    # Assuming the structure of TechSpecificInfo, since it wasn't provided
    pass


class AgentInfo:
    # Assuming the structure of AgentInfo, since it wasn't provided
    pass


class MachineInfo:
    # Assuming the structure of MachineInfo, since it wasn't provided
    pass


class AgentMetadata:
    def __init__(self,
                 tech_specific_info: Optional[TechSpecificInfo] = None,
                 agent_info: Optional[AgentInfo] = None,
                 machine_info: Optional[MachineInfo] = None):
        self.tech_specific_info = tech_specific_info
        self.agent_info = agent_info
        self.machine_info = machine_info


class Intervals:
    def __init__(self, timed_footprints_collection_interval_seconds: int):
        self.timed_footprints_collection_interval_seconds = timed_footprints_collection_interval_seconds


class FootprintMeta:
    def __init__(self, agent_config: AgentConfig):
        self.agentMetadata = {}
        self.agentConfig = agent_config
        self.agentId = agent_config.agentId
        self.labId = agent_config.labId
        self.intervals = {
            "timedFootprintsCollectionIntervalSeconds": 10
        }


class FootprintExecutionHit(object):
    def __init__(self, methods: List[int], start_time: int, end_time: int):
        self.start = start_time
        self.end = end_time
        self.methods = methods


class FootprintExecution(object):
    def __init__(self, indexes: List[int], start_time: int, end_time: int):
        self.executionId = ""
        self.hits = []
        self.hits.append(FootprintExecutionHit(indexes, start_time, end_time))


class FootprintModel(object):
    def __init__(self, agent_config: AgentConfig, methods: List[str], start_time: int, end_time: int):
        self.formatVersion = "6.0"
        self.methods = []
        self.executions = []
        self.meta = FootprintMeta(agent_config)
        self.methods.extend(methods)
        indexes = [index for index, _ in enumerate(methods)]
        self.executions.append(FootprintExecution(indexes, start_time, end_time))
