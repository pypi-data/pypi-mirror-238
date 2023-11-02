"""
This file holds all of the CLI commands for the "anyscale machines" path.
"""
from typing import Optional

import click
from rich import print_json
import tabulate

from anyscale.controllers.machine_controller import MachineController


@click.group(
    "machine", help="Commands to interact with machines in Anyscale.",
)
def machine_cli() -> None:
    pass


@machine_cli.command(name="list", help="List machines registered to Anyscale.")
@click.option("--cloud", type=str, help="Provide a cloud name.")
@click.option("--cloud-id", type=str, help="Provide a cloud ID.")
@click.option(
    "--format",
    "format_",
    type=click.Choice(["table", "json"]),
    default="table",
    help="The format to return results in.",
)
def list_machines(cloud: Optional[str], cloud_id: Optional[str], format_: str) -> None:

    if not cloud and not cloud_id:
        raise ValueError("One of {'cloud', 'cloud-id'} must be provided.")

    machines_controller = MachineController()
    output = machines_controller.list_machines(cloud=cloud, cloud_id=cloud_id)

    if format_ == "json":
        rows = []
        for m in output.machines:
            rows.append(
                {
                    "machine_id": m.machine_id,
                    "hostname": m.hostname,
                    "machine_shape": m.machine_shape,
                    "connection_state": m.connection_state,
                    "allocation_state": m.allocation_state,
                    "cluster_id": m.cluster_id,
                    "cluster_creator_name": m.cluster_creator_name,
                    "cluster_name": m.cluster_name,
                }
            )
        print_json(data=rows)
    elif format_ == "table":
        table = []
        columns = [
            "MACHINE",
            "HOSTNAME",
            "SHAPE",
            "HEALTHY",
            "STATUS",
            "OWNER",
            "CLUSTER ID",
            "CLUSTER NAME",
        ]
        for m in output.machines:
            table.append(
                [
                    m.machine_id,
                    m.hostname,
                    m.machine_shape,
                    "Yes" if m.connection_state == "connected" else "No",
                    m.allocation_state.title(),
                    m.cluster_creator_name,
                    m.cluster_id,
                    m.cluster_name,
                ]
            )

        print(
            tabulate.tabulate(table, tablefmt="plain", headers=columns, stralign="left")
        )
