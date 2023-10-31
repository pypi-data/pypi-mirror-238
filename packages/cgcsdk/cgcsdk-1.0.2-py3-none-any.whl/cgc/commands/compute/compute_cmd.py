import json
import click

from cgc.commands.compute.compute_models import EntityList, GPUsList
from cgc.commands.compute.compute_responses import (
    compute_create_filebrowser_response,
    compute_create_response,
    compute_list_response,
)
from cgc.commands.compute.compute_utills import compute_create_payload
from cgc.utils.prepare_headers import get_api_url_and_prepare_headers
from cgc.utils.response_utils import retrieve_and_validate_response_send_metric
from cgc.utils.click_group import CustomGroup, CustomCommand
from cgc.utils.requests_helper import call_api, EndpointTypes
from cgc.commands.resource.resource_cmd import resource_delete


@click.group(name="compute", cls=CustomGroup)
def compute_group():
    """
    Management of compute resources.
    """


@click.group(name="filebrowser", cls=CustomGroup)
def filebrowser_group():
    """
    Management of filebrowser.
    """


@filebrowser_group.command("create", cls=CustomCommand)
@click.option("-u", "--puid", "puid", type=click.INT, required=False, default=0)
@click.option("-g", "--pgid", "pgid", type=click.INT, required=False, default=0)
def compute_filebrowser_create(puid: int, pgid: int):
    """Create a filebrowser service"""
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/filebrowser_create"
    metric = "compute.create_filebrowser"
    __payload = {"puid": puid, "pgid": pgid}
    __res = call_api(
        request=EndpointTypes.post,
        url=url,
        headers=headers,
        data=json.dumps(__payload),
    )
    click.echo(
        compute_create_filebrowser_response(
            retrieve_and_validate_response_send_metric(__res, metric)
        )
    )


@filebrowser_group.command("delete", cls=CustomCommand)
def compute_filebrowser_delete():
    """Delete a filebrowser service"""
    resource_delete("filebrowser")


@compute_group.command("create", cls=CustomCommand)
@click.argument("entity", type=click.Choice(EntityList.get_list()))
@click.option("-n", "--name", "name", type=click.STRING, required=True)
@click.option(
    "-g",
    "--gpu",
    "gpu",
    type=click.INT,
    default=0,
    help="How much GPU cards app will use",
)
@click.option(
    "-gt",
    "--gpu-type",
    "gpu_type",
    type=click.Choice(GPUsList.get_list(), case_sensitive=False),
    default="A5000",
    help="Graphic card used by the app",
)
@click.option(
    "-c",
    "--cpu",
    "cpu",
    type=click.INT,
    default=1,
    help="How much CPU cores app can use",
)
@click.option(
    "-m",
    "--memory",
    "memory",
    type=click.INT,
    default=2,
    help="How much Gi RAM app can use",
)
@click.option(
    "-v",
    "--volume",
    "volumes",
    multiple=True,
    help="List of volume names to be mounted with default mount path",
)
@click.option(
    "-d",
    "--resource-data",
    "resource_data",
    multiple=True,
    help="List of optional arguments to be passed to the app, key=value format",
)
def compute_create(
    entity: str,
    gpu: int,
    gpu_type: str,
    cpu: int,
    memory: int,
    volumes: list[str],
    resource_data: list[str],
    name: str,
):
    """
    Create an app in user namespace.
    \f
    :param entity: name of entity to create
    :type entity: str
    :param gpu: number of gpus to be used by app
    :type gpu: int
    :param cpu: number of cores to be used by app
    :type cpu: int
    :param memory: GB of memory to be used by app
    :type memory: int
    :param volumes: list of volumes to mount
    :type volumes: list[str]
    :param resource_data: list of optional arguments to be passed to the app
    :type resource_data: list[str]
    :param name: name of app
    :type name: str
    """
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/create"
    metric = "compute.create"
    __payload = compute_create_payload(
        name=name,
        entity=entity,
        cpu=cpu,
        memory=memory,
        gpu=gpu,
        volumes=volumes,
        resource_data=resource_data,
        gpu_type=gpu_type,
    )
    # Extra keys allowed for payload:
    # 1.
    # template_specific_data: TemplateSpecificData
    #   TemplateSpecificData -> resource_data: dict [str, str]
    # --- example: ---
    #   "template_specific_data": {
    #     "resource_data": {
    #       "postgre_host": "postgresql",
    #       "postgre_password": "password",
    #       "postgre_name": "db",
    #       ...
    #     }
    #   }
    # currently available for label-studio
    # 2.
    # config_maps_data: dict [dict [str, str]]]
    # NOTE: filebrowser creation is NOT ALLOWED via this endpoint
    # NOTE: only valid config map names will be proceed
    # NOTE: only str values are allowed, otherwise config map will not be created and app might not start
    # ex.: config_maps_data = {"filebrowser-permissions-config": {
    #     "puid": "123",
    #     "pgid": "456",
    # }}
    # How to update payload with custom values?
    # payload["template_specific_data"] = dict(...)
    # payload["config_maps_data"] = dict(...)
    __res = call_api(
        request=EndpointTypes.post,
        url=url,
        headers=headers,
        data=json.dumps(__payload),
    )
    click.echo(
        compute_create_response(
            retrieve_and_validate_response_send_metric(__res, metric)
        )
    )


@compute_group.command("delete", cls=CustomCommand)
@click.argument("name", type=click.STRING)
def compute_delete_cmd(name: str):
    """
    Delete an app from user namespace.
    \f
    :param name: name of app to delete
    :type name: str
    """
    resource_delete(name)


compute_group.add_command(filebrowser_group)


@compute_group.command("list", cls=CustomCommand)
@click.option(
    "-d", "--detailed", "detailed", type=click.BOOL, is_flag=True, default=False
)
def resource_list(detailed: bool):
    """
    List all apps for user namespace.
    """
    api_url, headers = get_api_url_and_prepare_headers()
    url = f"{api_url}/v1/api/resource/list?resource_type=compute"
    metric = "compute.list"
    __res = call_api(
        request=EndpointTypes.get,
        url=url,
        headers=headers,
    )
    table = compute_list_response(
        detailed,
        retrieve_and_validate_response_send_metric(__res, metric),
    )

    click.echo(table)
