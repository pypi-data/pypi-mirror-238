"""
This file holds all of the CLI commands for the "anyscale machines" path.
"""
from typing import Optional

import click
from rich import print_json
from rich.console import Console
from rich.table import Table

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
                }
            )
        print_json(data=rows)
    elif format_ == "table":
        table = Table()
        table.add_column("Machine ID", overflow="fold")
        table.add_column("Host Name", overflow="fold")
        table.add_column("Machine Shape", overflow="fold")
        table.add_column("Connection State", overflow="fold")
        table.add_column("Allocation State", overflow="fold")
        table.add_column("Cluster ID", overflow="fold")
        for m in output.machines:
            table.add_row(
                m.machine_id,
                m.hostname,
                m.machine_shape,
                m.connection_state,
                m.allocation_state,
                m.cluster_id,
            )

        console = Console()
        console.print(table)
