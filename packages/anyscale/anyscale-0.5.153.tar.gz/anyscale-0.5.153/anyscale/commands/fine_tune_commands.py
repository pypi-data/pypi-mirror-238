from typing import Optional

import click

from anyscale.controllers.fine_tune_controller import FineTuneController
from anyscale.models.fine_tune_model import FineTuneConfig


@click.group(
    "fine-tune", help="Interact with fine-tuning jobs running on Anyscale.", hidden=True
)
def fine_tune_cli() -> None:
    pass


@fine_tune_cli.command(name="submit")
@click.argument("base-model", required=True)
@click.option("--train-file", required=True, help="The path of the training file.")
@click.option(
    "--valid-file",
    required=False,
    default=None,
    help="The path of the validation file.",
)
@click.option("--cloud-id", required=True, help="The id of the cloud")
@click.option(
    "--suffix",
    required=False,
    default=None,
    help="The suffix of the fine-tuned model.",
)
def submit(
    base_model: str,
    train_file: str,
    valid_file: Optional[str],
    cloud_id: str,
    suffix: Optional[str],
) -> None:
    """
    Submits a fine-tuning job.

    Example usage:

        anyscale fine-tuning submit --model meta-llama/Llama-2-7b-chat-hf --train-file train.jsonl --cloud-id CLOUD_ID
    """
    fine_tune_controller = FineTuneController()
    config = FineTuneConfig(
        base_model=base_model,
        train_file=train_file,
        valid_file=valid_file,
        cloud_id=cloud_id,
        suffix=suffix,
    )
    fine_tune_controller.fine_tune(config=config)
