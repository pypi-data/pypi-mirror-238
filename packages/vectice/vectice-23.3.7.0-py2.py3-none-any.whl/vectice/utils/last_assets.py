from __future__ import annotations

import os
from textwrap import dedent
from typing import TYPE_CHECKING, Any, List

from PIL import Image

from vectice.api.json.attachment import AttachmentOutput
from vectice.models.representation.dataset_representation import DatasetRepresentation, DatasetVersionRepresentation
from vectice.models.representation.model_representation import ModelRepresentation, ModelVersionRepresentation
from vectice.utils.automatic_link_utils import deprecated_existing_dataset_logger, deprecated_existing_model_logger

if TYPE_CHECKING:
    from logging import Logger

    from vectice.api import Client
    from vectice.api.json.dataset_register import DatasetRegisterOutput
    from vectice.api.json.model_register import ModelRegisterOutput
    from vectice.models.dataset import Dataset
    from vectice.models.iteration import Iteration
    from vectice.models.model import Model
    from vectice.models.step import Step


def get_last_user_and_default_workspace(client: Client) -> tuple[str, str | None]:
    asset = client.get_user_and_default_workspace()
    workspace_id = str(asset["defaultWorkspace"]["vecticeId"]) if asset["defaultWorkspace"] else None
    return asset["user"]["name"], workspace_id


def connection_logging(_logger: Logger, user_name: str, host: str, workspace_id: str | None):
    from vectice.utils.logging_utils import CONNECTION_LOGGING

    if workspace_id:
        logging_output = f"For quick access to your default workspace in the Vectice web app, visit:\n{host}/browse/workspace/{workspace_id}"
        _logger.info(CONNECTION_LOGGING.format(user=user_name, logging_output=logging_output))
        return
    logging_output = f"For quick access to the list of workspaces in the Vectice web app, visit:\n{host}/workspaces"
    _logger.info(CONNECTION_LOGGING.format(user=user_name, logging_output=logging_output))


def deprecated_register_dataset_logging(
    step: Step,
    data: dict[str, Any],
    value: Any,
    attachments: List[AttachmentOutput] | None,
    _logger: Logger,
    step_artifacts: Any | None = None,
):
    iteration_id = step.iteration.id
    url = step._client.auth.api_base_url  # pyright: ignore[reportPrivateUsage] OK to ignore deprecated code
    hyper_link = f"{url}/browse/iteration/{iteration_id}"

    # check if exists
    existing_logging = deprecated_existing_dataset_logger(data, value.name, _logger)
    # check if attached to step
    check_artifacts = step_artifacts if step_artifacts else step.artifacts
    match = next(filter(lambda x: x.dataset_version_id == data["datasetVersion"]["vecticeId"], check_artifacts), None)
    attachments_output = None
    if attachments:
        attachments_output = ", ".join([attach.fileName for attach in attachments])
    logging_output = None
    if existing_logging and match:
        logging_output = dedent(
            f"""
                                Existing Dataset: {value.name!r} and Version: {data['datasetVersion']['name']!r} already linked to Step: {step.name}
                                Attachments: {attachments_output}
                                Link to Step: {hyper_link}
                                """
        ).lstrip()
    if existing_logging and not match:
        logging_output = dedent(
            f"""
                    New Version: {data['datasetVersion']['name']!r} of Dataset: {value.name!r} added to Step: {step.name}
                    Attachments: {attachments_output}
                    Link to Step: {hyper_link}
                    """
        ).lstrip()
    if not existing_logging:
        logging_output = dedent(
            f"""
                                    New Dataset: {value.name!r} Version: {data['datasetVersion']['name']!r} added to Step: {step.name}
                                    Attachments: {attachments_output}
                                    Link to Step: {hyper_link}
                                    """
        ).lstrip()
    if logging_output:
        _logger.info(logging_output)
    else:
        _logger.debug("Logging failed for register dataset at step, check _register_dataset_logging.")


def deprecated_get_image_or_file_artifact_reference(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    pillow_extensions = {exten for exten in Image.registered_extensions()}
    return "Image" if (ext in pillow_extensions and ext != ".pdf") else "File"


def deprecated_comment_or_image_logging(step: Step, _logger: Logger, filename: str | None = None):
    iteration_id = step.iteration.id
    url = step._client.auth.api_base_url  # pyright: ignore[reportPrivateUsage] OK to ignore deprecated code
    hyper_link = f"{url}/browse/iteration/{iteration_id}"
    if filename:
        asset_type_log = deprecated_get_image_or_file_artifact_reference(filename)
        artifact_reference = f"{asset_type_log}: {filename!r}"
    else:
        artifact_reference = "Comment"
    logging_output = dedent(
        f"""
        Added {artifact_reference} to Step: {step.name}

        Link to Step: {hyper_link}
        """
    ).lstrip()

    _logger.info(logging_output)


def deprecated_register_model_logging(
    step: Step,
    data: dict[str, Any],
    value: Any,
    step_name: str,
    attachments: List[AttachmentOutput] | None,
    _logger: Logger,
    step_artifacts: Any | None = None,
):
    iteration_id = step.iteration.id
    url = step._client.auth.api_base_url  # pyright: ignore[reportPrivateUsage] OK to ignore deprecated code
    hyper_link = f"{url}/browse/iteration/{iteration_id}"

    # check if exists
    existing_logging = deprecated_existing_model_logger(data, value.name, _logger)
    # check if attached to step already
    check_artifacts = step_artifacts if step_artifacts else step.artifacts
    match = next(filter(lambda x: x.model_version_id == data["modelVersion"]["vecticeId"], check_artifacts), None)
    attachments_output = None
    if attachments:
        attachments_output = ", ".join([attach.fileName for attach in attachments])
    logging_output = None
    if existing_logging and match:
        logging_output = dedent(
            f"""
                                Existing Model: {value.name!r} and Version: {data['modelVersion']['name']!r} already linked to Step: {step_name}
                                Attachments: {attachments_output}
                                Link to Step: {hyper_link}
                                """
        ).lstrip()
    if existing_logging and not match:
        logging_output = dedent(
            f"""
                    New Version: {data['modelVersion']['name']!r} of Model: {value.name!r} added to Step: {step_name}
                    Attachments: {attachments_output}
                    Link to Step: {hyper_link}
                    """
        ).lstrip()
    if not existing_logging and not match:
        logging_output = dedent(
            f"""
                                    New Model: {value.name!r} Version: {data['modelVersion']['name']!r} added to Step: {step_name}
                                    Attachments: {attachments_output}
                                    Link to Step: {hyper_link}
                                    """
        ).lstrip()

    if logging_output:
        _logger.info(logging_output)
    else:
        _logger.debug("Logging failed for register model at step, check _register_model_logging.")


def _get_iteration_log(iteration: Iteration, section: str | None = None, existing_asset: bool = False):
    iteration_id = iteration.id
    url = iteration._client.auth.api_base_url  # pyright: ignore[reportPrivateUsage] OK to ignore deprecated code
    hyper_link = f"{url}/browse/iteration/{iteration_id}"
    assignment_type = "reassigned to" if existing_asset else "in"
    to_section = f", {assignment_type} section: {section!r}." if section else "."
    return f"to iteration: {iteration.index}{to_section}", f"Link to iteration: {hyper_link}"


def _get_image_or_file_artifact_reference(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    pillow_extensions = {exten for exten in Image.registered_extensions()}
    return "image" if (ext in pillow_extensions and ext != ".pdf") else "file"


def comment_or_image_logging(
    iteration: Iteration,
    _logger: Logger,
    section: str | None,
    filename: str | None = None,
):
    artifact_reference = "comment"
    if filename:
        asset_type_log = _get_image_or_file_artifact_reference(filename)
        artifact_reference = f"{asset_type_log}: {filename!r}"

    assignment_log, iteration_link_log = _get_iteration_log(iteration, section)
    logging_output = dedent(
        f"""
            Added {artifact_reference} {assignment_log}
            {iteration_link_log}
        """
    ).lstrip()

    _logger.info(logging_output)


def _get_full_asset_log(
    asset_log: str,
    iteration: Iteration,
    section: str | None,
    attachments: list[AttachmentOutput] | None,
    existing_asset: bool = False,
):
    attachments_output = ", ".join([attach.fileName for attach in attachments]) if attachments else "None"
    assignment_log, iteration_link_log = _get_iteration_log(iteration, section, existing_asset)
    return dedent(
        f"""
            {asset_log} {assignment_log}
            Attachments: {attachments_output}
            {iteration_link_log}
        """
    ).lstrip()


def _get_register_dataset_log(data: DatasetRegisterOutput, value: Dataset) -> str:
    dsv_name = data.dataset_version.name
    if data.use_existing_version:
        return f"Existing dataset: {value.name!r} and version: {dsv_name!r} already linked"
    if data.use_existing_dataset:
        return f"New version: {dsv_name!r} of dataset: {value.name!r} added"

    return f"New dataset: {value.name!r} version: {dsv_name!r} added"


def register_dataset_logging(
    iteration: Iteration,
    data: DatasetRegisterOutput,
    value: Dataset,
    attachments: list[AttachmentOutput] | None,
    _logger: Logger,
    section: str | None = None,
):
    asset_log = _get_register_dataset_log(data, value)
    extisting_asset: bool = True if data.use_existing_version else False
    logging_output = _get_full_asset_log(asset_log, iteration, section, attachments, extisting_asset)
    _logger.info(logging_output)


def register_model_logging(
    iteration: Iteration,
    data: ModelRegisterOutput,
    value: Model,
    attachments: list[AttachmentOutput] | None,
    _logger: Logger,
    section: str | None = None,
):
    mv_name = data.model_version.name
    asset_log = (
        f"New version: {mv_name!r} of model: {value.name!r} added"
        if data.use_existing_model
        else f"New model: {value.name!r} version: {mv_name!r} added"
    )
    logging_output = _get_full_asset_log(asset_log, iteration, section, attachments)
    _logger.info(logging_output)


def _get_asset_parent_name(value: ModelVersionRepresentation | DatasetVersionRepresentation):
    return value.model_name if isinstance(value, ModelVersionRepresentation) else value.dataset_name


def assign_asset_version_logging(
    iteration: Iteration,
    value: ModelRepresentation | ModelVersionRepresentation | DatasetRepresentation | DatasetVersionRepresentation,
    _logger: Logger,
    already_assigned: bool = False,
    section: str | None = None,
):
    assignment_log, iteration_link_log = _get_iteration_log(iteration=iteration, section=section, existing_asset=True)
    asset_info = "model" if isinstance(value, (ModelVersionRepresentation, ModelRepresentation)) else "dataset"
    link = "already linked" if already_assigned else "linked"

    is_parent = isinstance(value, (ModelRepresentation, DatasetRepresentation))
    asset_id = value.version.id if is_parent else value.id
    asset_name = value.name if is_parent else _get_asset_parent_name(value)

    logging_output = dedent(
        f"""
            Existing {asset_info} version: {asset_id!r} of {asset_info}: {asset_name!r} {link} {assignment_log}
            {iteration_link_log}
        """
    ).lstrip()
    _logger.info(logging_output)
