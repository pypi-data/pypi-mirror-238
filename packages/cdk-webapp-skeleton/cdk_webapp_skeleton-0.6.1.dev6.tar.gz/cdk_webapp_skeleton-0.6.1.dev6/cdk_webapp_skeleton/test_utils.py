import json
from typing import cast

from _pytest.fixtures import FixtureRequest
from aws_cdk import assertions


def print_template(template: assertions.Template) -> None:
    print(json.dumps(template.to_json(), indent=4))


def get_branch_name_from_mark(request: FixtureRequest) -> str:
    marker = request.node.get_closest_marker("branch_name")
    assert marker is not None
    branch_name = marker.args[0]
    return cast(str, branch_name)
