import json
from typing import Any, List

from numerous.grpc import spm_pb2
from numerous.grpc.spm_pb2_grpc import SPMStub


def load_target_scenario_data_and_set_job_id(
    spm_stub: SPMStub, project_id: str, scenario: dict[str, Any]
) -> List[Any]:
    target_scenario_id = scenario["optimizationTargetScenarioID"]
    target_scenario_request = spm_pb2.Scenario(
        project=project_id, scenario=target_scenario_id
    )
    target_scenario_response = spm_stub.GetScenario(target_scenario_request)
    target_scenario = json.loads(target_scenario_response.scenario_document)

    if not isinstance(target_scenario, dict):
        raise TypeError(f"Received invalid target scenario data: {target_scenario}")

    target_job_id = next(
        job_id
        for job_id, job in target_scenario["jobs"].items()
        if job.get("isMain", False)
    )
    return [target_scenario, target_job_id]
