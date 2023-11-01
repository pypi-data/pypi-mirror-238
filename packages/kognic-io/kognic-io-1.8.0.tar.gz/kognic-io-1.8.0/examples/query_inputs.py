from typing import List, Optional

import kognic.io.client as IOC
from kognic.io import model as IAM


def run(client: IOC.KognicIOClient, project: Optional[str] = None, scene_uuids: Optional[List[str]] = None) -> List[IAM.Input]:
    print("Listing inputs...")
    return client.input.query_inputs(project=project, scene_uuids=scene_uuids)


if __name__ == "__main__":
    client = IOC.KognicIOClient()

    # Project - Available via `client.project.get_projects()`
    project = "Project-identifier"
    scene_uuids = ["scene-identifier"]
    run(client, project=project, scene_uuids=scene_uuids)
