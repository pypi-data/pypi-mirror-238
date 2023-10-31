#
# # Copyright © 2023 Peak AI Limited. or its affiliates. All Rights Reserved.
# #
# # Licensed under the Apache License, Version 2.0 (the "License"). You
# # may not use this file except in compliance with the License. A copy of
# # the License is located at:
# #
# # https://github.com/PeakBI/peak-sdk/blob/main/LICENSE
# #
# # or in the "license" file accompanying this file. This file is
# # distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# # ANY KIND, either express or implied. See the License for the specific
# # language governing permissions and limitations under the License.
# #
# # This file is part of the peak-sdk.
# # see (https://github.com/PeakBI/peak-sdk)
# #
# # You should have received a copy of the APACHE LICENSE, VERSION 2.0
# # along with this program. If not, see <https://apache.org/licenses/LICENSE-2.0>
#
"""Contains the metadata for all the commands.

The metadata represents the following:
    - table_params: Parameters required for the table output formatting.
    - request_body_yaml_path: File containing the yaml file examples for the command.
"""
from typing import Any, Dict, List


def tag_parser(data: Any) -> str:
    tag_array = []
    for tag in data:
        tag_array.append(tag["name"])
    return ", ".join(tag_array)


command_metadata: Dict[str, Any] = {
    "list_images": {
        "table_params": {
            "output_keys": {
                "id": {
                    "label": "ID",
                },
                "name": {
                    "label": "Image Name",
                },
                "type": {
                    "label": "Type",
                },
                "scope": {
                    "label": "Scope",
                },
                "latestVersion.id": {
                    "label": "Latest Version ID",
                },
                "latestVersion.version": {
                    "label": "Latest Version",
                },
                "latestVersion.status": {
                    "label": "Latest Version Status",
                },
                "latestVersion.lastBuildStatus": {
                    "label": "Latest Version Build Status",
                },
                "latestVersion.tags": {
                    "label": "Tags",
                    "parser": tag_parser,
                },
            },
            "title": "Images",
            "data_key": "images",
            "subheader_key": "imageCount",
        },
    },
    "list_image_versions": {
        "table_params": {
            "output_keys": {
                "id": {
                    "label": "ID",
                },
                "version": {
                    "label": "Version",
                },
                "description": {
                    "label": "Description",
                },
                "status": {
                    "label": "Status",
                },
                "lastBuildStatus": {
                    "label": "Last Build Status",
                },
                "buildDetails": {
                    "label": "Build Details",
                },
                "tags": {
                    "label": "Tags",
                    "parser": tag_parser,
                },
            },
            "title": "Image Versions",
            "data_key": "versions",
            "subheader_key": "versionCount",
        },
    },
    "list_image_builds": {
        "table_params": {
            "output_keys": {
                "buildId": {
                    "label": "Build ID",
                },
                "versionId": {
                    "label": "Version ID",
                },
                "version": {
                    "label": "Version",
                },
                "status": {
                    "label": "Build Status",
                },
                "startedAt": {
                    "label": "Started At (UTC)",
                },
                "finishedAt": {
                    "label": "Finished At (UTC)",
                },
            },
            "title": "Image Builds",
            "data_key": "builds",
            "subheader_key": "buildCount",
        },
    },
    "list_workflows": {
        "table_params": {
            "output_keys": {
                "id": {
                    "label": "ID",
                },
                "name": {
                    "label": "Workflow Name",
                },
                "status": {
                    "label": "Status",
                },
                "triggers": {
                    "label": "Triggers",
                },
                "lastExecution.status": {
                    "label": "Last Execution Status",
                },
                "lastExecution.executedAt": {
                    "label": "Last Execution Time (UTC)",
                },
                "tags": {
                    "label": "Tags",
                    "parser": tag_parser,
                },
            },
            "title": "Workflows",
            "data_key": "workflows",
            "subheader_key": "workflowsCount",
        },
    },
    "list_workflow_executions": {
        "table_params": {
            "output_keys": {
                "executionId": {
                    "label": "Execution ID",
                },
                "status": {
                    "label": "Status",
                },
                "duration": {
                    "label": "Run Duration",
                },
                "executedAt": {
                    "label": "Execution Time (UTC)",
                },
            },
            "title": "Workflows Executions",
            "data_key": "executions",
            "subheader_key": "executionsCount",
        },
    },
    "get_execution_details": {
        "table_params": {
            "output_keys": {
                "name": {
                    "label": "Step Name",
                },
                "startedAt": {
                    "label": "Started At",
                },
                "finishedAt": {
                    "label": "Finished At",
                },
                "status": {
                    "label": "Status",
                },
                "stepType": {
                    "label": "Step Type",
                },
                "image": {
                    "label": "Image",
                },
                "output": {
                    "label": "Output",
                },
            },
            "title": "Execution Details",
            "data_key": "steps",
            "subheader_title": "Execution Status",
            "subheader_key": "status",
        },
    },
    "list_webapps": {
        "table_params": {
            "output_keys": {
                "id": {
                    "label": "ID",
                },
                "name": {
                    "label": "Name",
                },
                "status": {
                    "label": "Status",
                },
                "updatedBy": {
                    "label": "Updated By",
                },
                "updatedAt": {
                    "label": "Updated At (UTC)",
                },
                "tags": {
                    "label": "Tags",
                    "parser": tag_parser,
                },
            },
            "title": "Webapps",
            "data_key": "webapps",
            "subheader_key": "webappsCount",
        },
    },
    "list_artifacts": {
        "table_params": {
            "output_keys": {
                "id": {
                    "label": "ID",
                },
                "description": {
                    "label": "Description",
                },
                "name": {
                    "label": "Name",
                },
                "createdAt": {
                    "label": "Created At (UTC)",
                },
                "createdBy": {
                    "label": "Created By",
                },
            },
            "title": "Artifacts",
            "data_key": "artifacts",
            "subheader_key": "artifactCount",
        },
    },
    "list_specs": {
        "table_params": {
            "output_keys": {
                "id": {
                    "label": "ID",
                },
                "kind": {
                    "label": "Kind",
                },
                "metadata.name": {
                    "label": "Name",
                },
                "metadata.status": {
                    "label": "Status",
                },
                "latestRelease.version": {
                    "label": "Latest Release",
                },
                "metadata.tags": {
                    "label": "Tags",
                    "parser": tag_parser,
                },
            },
            "title": "Specs",
            "data_key": "specs",
            "subheader_key": "specCount",
        },
    },
    "list_release_deployments": {
        "table_params": {
            "output_keys": {
                "id": {
                    "label": "ID",
                },
                "kind": {
                    "label": "Kind",
                },
                "metadata.name": {
                    "label": "Name",
                },
                "metadata.status": {
                    "label": "Status",
                },
                "latestRevision.revision": {
                    "label": "Latest Revision",
                },
                "latestRevision.status": {
                    "label": "Latest Revision Status",
                },
                "metadata.tags": {
                    "label": "Tags",
                    "parser": tag_parser,
                },
            },
            "title": "Deployments for a Spec Release",
            "data_key": "deployments",
            "subheader_key": "deploymentCount",
        },
    },
    "list_deployments": {
        "table_params": {
            "output_keys": {
                "id": {
                    "label": "ID",
                },
                "kind": {
                    "label": "Kind",
                },
                "metadata.title": {
                    "label": "Title",
                },
                "metadata.status": {
                    "label": "Status",
                },
                "latestRevision.revision": {
                    "label": "Latest Revision",
                },
                "latestRevision.status": {
                    "label": "Latest Revision Status",
                },
                "metadata.tags": {
                    "label": "Tags",
                    "parser": tag_parser,
                },
            },
            "title": "Deployments",
            "data_key": "deployments",
            "subheader_key": "deploymentCount",
        },
    },
    "list_app_specs": {
        "table_params": {
            "output_keys": {
                "id": {
                    "label": "ID",
                },
                "kind": {
                    "label": "Kind",
                },
                "metadata.name": {
                    "label": "Name",
                },
                "metadata.status": {
                    "label": "Status",
                },
                "latestRelease.version": {
                    "label": "Latest Release",
                },
                "metadata.tags": {
                    "label": "Tags",
                    "parser": tag_parser,
                },
            },
            "title": "Specs",
            "data_key": "specs",
            "subheader_key": "specCount",
        },
    },
    "list_app_spec_releases": {
        "table_params": {
            "output_keys": {
                "id": {
                    "label": "ID",
                },
                "version": {
                    "label": "Version",
                },
                "notes": {
                    "label": "Notes",
                },
                "createdAt": {
                    "label": "Created At (UTC)",
                },
                "createdBy": {
                    "label": "Created By",
                },
            },
            "title": "Spec Releases",
            "data_key": "releases",
            "subheader_key": "releaseCount",
        },
    },
    "list_app_deployments": {
        "table_params": {
            "output_keys": {
                "id": {
                    "label": "ID",
                },
                "kind": {
                    "label": "Kind",
                },
                "metadata.title": {
                    "label": "Title",
                },
                "metadata.status": {
                    "label": "Status",
                },
                "latestRevision.revision": {
                    "label": "Latest Revision",
                },
                "latestRevision.status": {
                    "label": "Latest Revision Status",
                },
                "metadata.tags": {
                    "label": "Tags",
                    "parser": tag_parser,
                },
            },
            "title": "App Deployments",
            "data_key": "deployments",
            "subheader_key": "deploymentCount",
        },
    },
    "list_block_specs": {
        "table_params": {
            "output_keys": {
                "id": {
                    "label": "ID",
                },
                "kind": {
                    "label": "Kind",
                },
                "metadata.name": {
                    "label": "Name",
                },
                "metadata.status": {
                    "label": "Status",
                },
                "latestRelease.version": {
                    "label": "Latest Release",
                },
                "metadata.tags": {
                    "label": "Tags",
                    "parser": tag_parser,
                },
            },
            "title": "Block Specs",
            "data_key": "specs",
            "subheader_key": "specCount",
        },
    },
    "list_block_spec_releases": {
        "table_params": {
            "output_keys": {
                "id": {
                    "label": "ID",
                },
                "version": {
                    "label": "Version",
                },
                "notes": {
                    "label": "Notes",
                },
                "createdAt": {
                    "label": "Created At (UTC)",
                },
                "createdBy": {
                    "label": "Created By",
                },
            },
            "title": "Block Spec Releases",
            "data_key": "releases",
            "subheader_key": "releaseCount",
        },
    },
    "list_block_deployments": {
        "table_params": {
            "output_keys": {
                "id": {
                    "label": "ID",
                },
                "kind": {
                    "label": "Kind",
                },
                "metadata.title": {
                    "label": "Title",
                },
                "metadata.status": {
                    "label": "Status",
                },
                "latestRevision.revision": {
                    "label": "Latest Revision",
                },
                "latestRevision.status": {
                    "label": "Latest Revision Status",
                },
                "metadata.tags": {
                    "label": "Tags",
                    "parser": tag_parser,
                },
            },
            "title": "Block Deployments",
            "data_key": "deployments",
            "subheader_key": "deploymentCount",
        },
    },
    "list_tenant_instance_options": {
        "table_params": {
            "output_keys": {
                "id": {
                    "label": "ID",
                },
                "name": {
                    "label": "Instance Name",
                },
                "cpu": {
                    "label": "CPU",
                },
                "memory": {
                    "label": "Memory",
                },
                "gpu": {
                    "label": "GPU",
                },
                "gpuMemory": {
                    "label": "GPU Memory",
                },
                "provider": {
                    "label": "Provider",
                },
            },
            "title": "Instance Options",
            "data_key": "data",
        },
    },
    "create_artifact": {
        "request_body_yaml_path": "sample_yaml/resources/artifacts/create_artifact.yaml",
    },
    "update_artifact_metadata": {
        "request_body_yaml_path": "sample_yaml/resources/artifacts/update_artifact_metadata.yaml",
    },
    "create_artifact_version": {
        "request_body_yaml_path": "sample_yaml/resources/artifacts/create_artifact_version.yaml",
    },
    "create_image": {
        "request_body_yaml_path": "sample_yaml/resources/images/upload/create_image.yaml",
    },
    "create_image_version": {
        "request_body_yaml_path": "sample_yaml/resources/images/upload/create_image_version.yaml",
    },
    "update_version": {
        "request_body_yaml_path": "sample_yaml/resources/images/upload/update_version.yaml",
    },
    "create_or_update_image": {
        "request_body_yaml_path": "sample_yaml/resources/images/upload/create_or_update_image.yaml",
    },
    "create_workflow": {
        "request_body_yaml_path": "sample_yaml/resources/workflows/create_workflow.yaml",
    },
    "update_workflow": {
        "request_body_yaml_path": "sample_yaml/resources/workflows/update_workflow.yaml",
    },
    "create_or_update_workflow": {
        "request_body_yaml_path": "sample_yaml/resources/workflows/create_or_update_workflow.yaml",
    },
    "patch_workflow": {
        "request_body_yaml_path": "sample_yaml/resources/workflows/patch_workflow.yaml",
    },
    "execute_workflow": {
        "request_body_yaml_path": "sample_yaml/resources/workflows/execute_workflow.yaml",
    },
    "create_webapp": {
        "request_body_yaml_path": "sample_yaml/resources/webapps/create_webapp.yaml",
    },
    "update_webapp": {
        "request_body_yaml_path": "sample_yaml/resources/webapps/update_webapp.yaml",
    },
    "create_or_update_webapp": {
        "request_body_yaml_path": "sample_yaml/resources/webapps/create_or_update_webapp.yaml",
    },
    "create_app_spec": {
        "request_body_yaml_path": "sample_yaml/press/apps/specs/create_app_spec.yaml",
    },
    "update_app_spec_metadata": {
        "request_body_yaml_path": "sample_yaml/press/apps/specs/update_app_spec_metadata.yaml",
    },
    "create_app_spec_release": {
        "request_body_yaml_path": "sample_yaml/press/apps/specs/create_app_spec_release.yaml",
    },
    "create_app_deployment": {
        "request_body_yaml_path": "sample_yaml/press/apps/deployments/create_app_deployment.yaml",
    },
    "update_app_deployment_metadata": {
        "request_body_yaml_path": "sample_yaml/press/apps/deployments/update_app_deployment_metadata.yaml",
    },
    "create_block_spec": {
        "request_body_yaml_path": "sample_yaml/press/blocks/specs/create_block_spec.yaml",
    },
    "update_block_spec_metadata": {
        "request_body_yaml_path": "sample_yaml/press/blocks/specs/update_block_spec_metadata.yaml",
    },
    "create_block_spec_release": {
        "request_body_yaml_path": "sample_yaml/press/blocks/specs/create_block_spec_release.yaml",
    },
    "create_block_deployment": {
        "request_body_yaml_path": "sample_yaml/press/blocks/deployments/create_block_deployment.yaml",
    },
    "update_block_deployment_metadata": {
        "request_body_yaml_path": "sample_yaml/press/blocks/deployments/update_block_deployment_metadata.yaml",
    },
    "patch_block_parameters": {
        "request_body_yaml_path": "sample_yaml/press/blocks/deployments/patch_block_parameters.yaml",
    },
}

__all__: List[str] = ["command_metadata"]
