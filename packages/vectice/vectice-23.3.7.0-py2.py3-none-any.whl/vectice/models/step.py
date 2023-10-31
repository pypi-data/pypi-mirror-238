# pyright: reportUnboundVariable=false
# this file is deprecated so we don't want to make changes because of type analysis
from __future__ import annotations

import logging
from io import BufferedReader, IOBase
from typing import TYPE_CHECKING, Any

from PIL.Image import Image

import vectice
from vectice.api.json.attachment import AttachmentOutput
from vectice.api.json.iteration import (
    IterationStatus,
    IterationStepArtifact,
    IterationStepArtifactInput,
    IterationStepArtifactType,
)
from vectice.api.json.step import StepType
from vectice.utils.common_utils import (
    check_string_sanity,
    ensure_correct_project_id_from_representation_objs,
    get_image_or_file_variables,
    set_dataset_attachments,
    set_model_attachments,
)
from vectice.utils.deprecation import deprecate
from vectice.utils.instance_helper import is_image_or_file
from vectice.utils.last_assets import (
    deprecated_comment_or_image_logging,
    deprecated_register_dataset_logging,
    deprecated_register_model_logging,
)

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.models import Iteration, Phase, Project, Workspace
    from vectice.models.model import Model
    from vectice.models.representation.dataset_version_representation import DatasetVersionRepresentation
    from vectice.models.representation.model_version_representation import ModelVersionRepresentation
    from vectice.models.step_dataset import StepDataset
    from vectice.models.step_model import StepModel
    from vectice.models.step_number import StepNumber
    from vectice.models.step_string import StepString

_logger = logging.getLogger(__name__)

MISSING_DATASOURCE_ERROR_MESSAGE = "Cannot create modeling dataset. Missing %s data source."


class Step:
    """Model a Vectice step.

    Steps define the logical sequence of steps required to complete
    the phase along with their expected outcomes.

    Steps belong to an Iteration. The steps created under a Phase are
    Step Definitions that are then re-used in Iterations.

    ```tree
    phase 1
        step definition 1
        step definition 2
        step definition 3
    ```

    ```tree
    iteration 1 of phase 1
        step 1
        step 2
        step 3
    ```

    If steps are added to a phase after iterations have been created
    and completed, these steps won't appear in these iterations.

    NOTE: **Phases and Steps Definitions are created in the Vectice App,
    Iterations are created from the Vectice Python API.**

    To access the step and assign a value, you must use the "slug" of the step:
    the slug is the name of the step, transformed to fit Python's naming rules,
    and prefixed with `step_`. For example, a step called "Clean Dataset" can
    be accessed with `my_iteration.step_clean_dataset`.

    Therefore, to assign a value to a step:

    ```python
    my_clean_dataset = ...
    my_iteration.step_clean_dataset = my_clean_dataset
    ```

    You can assign a [`Model`][vectice.models.model.Model],
    [`Dataset`][vectice.models.dataset.Dataset], comments or files to any step.
    """

    def __init__(
        self,
        id: int,
        iteration: Iteration,
        name: str,
        index: int,
        slug: str,
        description: str | None = None,
        artifacts: list[IterationStepArtifact] | None = None,
        step_type: StepType = StepType.Step,
    ):
        self._id = id
        self._iteration: Iteration = iteration
        self._name = name
        self._index = index
        self._description = description
        self._client = self._iteration._client  # pyright: ignore[reportPrivateUsage]
        self._artifacts = artifacts or []
        self._slug = slug
        self._type: StepType = step_type
        self._model: Model | None = None

        self._iteration_read_only = self._iteration._status in {  # pyright: ignore[reportPrivateUsage]
            IterationStatus.Completed,
            IterationStatus.Abandoned,
        }
        if self._iteration_read_only:
            _logger.debug(f"Step {self.name}, iteration is {self._iteration.status} and is read-only!")

    def __repr__(self):
        return f"Step(name={self.name!r}, slug={self.slug!r}, id={self.id!r})"

    def __eq__(self, other: object):
        if not isinstance(other, Step):
            return NotImplemented
        return self.id == other.id

    @deprecate(
        warn_at="23.4",
        fail_at="24.1",
        remove_at="24.2",
        reason="This method is deprecated. Please use iteration.log() instead",
    )
    def __iadd__(self, value: Any):
        # TODO cyclic import
        from vectice.models.dataset import Dataset
        from vectice.models.model import Model
        from vectice.models.representation.dataset_representation import DatasetRepresentation
        from vectice.models.representation.dataset_version_representation import DatasetVersionRepresentation
        from vectice.models.representation.model_representation import ModelRepresentation
        from vectice.models.representation.model_version_representation import ModelVersionRepresentation
        from vectice.models.step_dataset import StepDataset
        from vectice.models.step_image import StepImage
        from vectice.models.step_model import StepModel
        from vectice.models.step_number import StepNumber
        from vectice.models.step_string import StepString

        ensure_correct_project_id_from_representation_objs(self.project.id, value)

        if is_image_or_file(value):
            artifact_input, filename = self._create_image_or_file_artifact(value)
            artifact = IterationStepArtifact(
                entity_file_id=artifact_input.id, type=IterationStepArtifactType.EntityFile
            )
            step = StepImage(self, value)
            self._iadd_comment_or_image(value, artifact)(self, _logger, filename)
        elif isinstance(value, (int, float, str)):
            if isinstance(value, str):
                check_string_sanity(value)
            artifact_input = IterationStepArtifactInput(text=str(value), type="Comment")
            artifact = IterationStepArtifact(text=value, type=IterationStepArtifactType.Comment)
            step = StepString(self, value) if isinstance(value, str) else StepNumber(self, value)
            self._client.add_iteration_step_artifact(self._id, artifact_input)
            self._iadd_comment_or_image(value, artifact)(self, _logger)
        elif (
            isinstance(value, Model)
            or isinstance(value, ModelRepresentation)
            or isinstance(value, ModelVersionRepresentation)
        ):
            if isinstance(value, Model):
                code_version_id = self._get_code_version_id()
                model_data = self._client.deprecated_register_model(
                    model=value,
                    project_id=self.project.id,
                    phase=self.phase,
                    iteration=self.iteration,
                    code_version_id=code_version_id,
                )
                attachments_output = set_model_attachments(self._client, value, model_data.model_version)
                model_artifact = IterationStepArtifact(
                    modelVersionId=model_data["modelVersion"]["vecticeId"], type="ModelVersion"
                )
            elif isinstance(value, ModelRepresentation):
                model_data = {
                    "useExistingModel": True,
                    "modelVersion": {"vecticeId": value.version.id, "name": value.version.name},
                }
                model_artifact = IterationStepArtifact(
                    modelVersionId=value.version.id,
                    type=IterationStepArtifactType.ModelVersion.name,
                )
                attachments_output = self._get_version_attachments(value.version)

            elif isinstance(value, ModelVersionRepresentation):  # pyright: ignore[reportUnnecessaryIsInstance]
                model_data = {
                    "useExistingModel": True,
                    "modelVersion": {"vecticeId": value.id, "name": value.name},
                }
                model_artifact = IterationStepArtifact(
                    modelVersionId=value.id,
                    type=IterationStepArtifactType.ModelVersion.name,
                )
                attachments_output = self._get_version_attachments(value)

            attachments = (
                [IterationStepArtifact(entityFileId=attach.fileId, type="EntityFile") for attach in attachments_output]
                if attachments_output
                else []
            )
            self.artifacts.extend([model_artifact, *attachments])
            copy_artifacts = self.artifacts.copy()
            self._keep_artifacts_and_update_step(StepType.StepModel, value)
            step = StepModel(self, model_artifact, value)  # type: ignore
            deprecated_register_model_logging(
                self, model_data, value, self.name, attachments_output, _logger, copy_artifacts
            )
        elif (
            isinstance(value, Dataset)
            or isinstance(value, DatasetRepresentation)
            or isinstance(value, DatasetVersionRepresentation)
        ):
            if isinstance(value, Dataset):
                code_version_id = self._get_code_version_id()
                dataset_output = self._client.deprecated_register_dataset_from_source(
                    dataset=value,
                    project_id=self.project.id,
                    phase_id=self.phase.id,
                    iteration_id=self.iteration.id,
                    code_version_id=code_version_id,
                )
                dataset_artifact = IterationStepArtifact(
                    datasetVersionId=dataset_output["datasetVersion"]["vecticeId"],
                    type=IterationStepArtifactType.DataSetVersion.name,
                )
                attachments_output = set_dataset_attachments(self._client, value, dataset_output.dataset_version)
            elif isinstance(value, DatasetRepresentation):
                dataset_output = {
                    "useExistingDataset": True,
                    "useExistingVersion": True,
                    "datasetVersion": {"vecticeId": value.version.id, "name": value.version.name},
                }
                dataset_artifact = IterationStepArtifact(
                    datasetVersionId=value.version.id,
                    type=IterationStepArtifactType.DataSetVersion.name,
                )
                attachments_output = self._get_version_attachments(value.version)
            elif isinstance(value, DatasetVersionRepresentation):  # pyright: ignore[reportUnnecessaryIsInstance]
                dataset_output = {
                    "useExistingDataset": True,
                    "useExistingVersion": True,
                    "datasetVersion": {"vecticeId": value.id, "name": value.name},
                }
                dataset_artifact = IterationStepArtifact(
                    datasetVersionId=value.id,
                    type=IterationStepArtifactType.DataSetVersion.name,
                )
                attachments_output = self._get_version_attachments(value)

            copy_artifacts = self.artifacts.copy()
            self.artifacts.append(dataset_artifact)
            attachments = (
                [IterationStepArtifact(entityFileId=attach.fileId, type="EntityFile") for attach in attachments_output]
                if attachments_output
                else []
            )
            self.artifacts += attachments
            self._keep_artifacts_and_update_step(StepType.StepDataset, value)
            step = StepDataset(self, dataset_artifact)
            deprecated_register_dataset_logging(
                self, dataset_output, value, attachments_output, _logger, copy_artifacts
            )
        else:
            raise TypeError(f"Expected Comment, Dataset or a Model, got {type(value)}")

        self._iteration._steps[self.name] = step  # pyright: ignore[reportPrivateUsage]

    def _iadd_comment_or_image(self, value: Any, artifact: IterationStepArtifact):
        self.artifacts.append(artifact)
        self._warn_step_change(value)
        return deprecated_comment_or_image_logging

    def _keep_artifacts_and_update_step(self, step_type: StepType, value: Any) -> None:
        artifacts = list(
            filter(
                self._filter_non_empty_artifact,
                self._client.get_step_by_name(self.name, self._iteration.id).artifacts,
            )
        )

        def _get_artifact_id(artifact: IterationStepArtifact) -> int | str | None:
            if artifact.model_version_id:
                return artifact.model_version_id
            if artifact.dataset_version_id:
                return artifact.dataset_version_id
            if artifact.entity_file_id:
                return artifact.entity_file_id

            return None

        def _maintain_and_add_artifacts(
            session_artifacts: list[IterationStepArtifactInput], existing_artifacts: list[IterationStepArtifactInput]
        ):
            # Ensure we don't keep adding an instances artifacts to the step
            maintain_artifacts = existing_artifacts
            for ia, art in enumerate(session_artifacts):
                if len(maintain_artifacts) >= ia + 1:
                    existing_art = maintain_artifacts[ia]
                    if (art.id is not None and existing_art.id == art.id) or (
                        art.text is not None and existing_art.text == art.text
                    ):
                        continue
                    maintain_artifacts += [art]
                else:
                    maintain_artifacts += [art]
            return maintain_artifacts

        # These are artifacts that exist in the current instance
        filtered_artifacts = list(filter(self._filter_non_empty_artifact, self.artifacts))
        session_artifacts: list[IterationStepArtifactInput] = [
            IterationStepArtifactInput(
                id=_get_artifact_id(artifact),
                type=artifact.type.value,
                text=str(artifact.text) if artifact.text is not None else None,
            )
            for artifact in filtered_artifacts
        ]
        # These are artifacts in Vectice
        existing_artifacts: list[IterationStepArtifactInput] = [
            IterationStepArtifactInput(
                id=_get_artifact_id(artifact),
                type=artifact.type.value,
                text=str(artifact.text) if artifact.text is not None else None,
            )
            for artifact in artifacts
        ]
        # Ensure no crossover or duplicates
        maintain_artifacts = _maintain_and_add_artifacts(session_artifacts, existing_artifacts)
        self._client.update_iteration_step_artifact(self.id, step_type, artifacts=maintain_artifacts)
        self._warn_step_change(value)

    def _flush_artifacts(self, step_type: StepType):
        self._client.update_iteration_step_artifact(step_id=self.id, step_type=step_type, artifacts=[])
        self.artifacts = []

    @deprecate(
        warn_at="23.4",
        fail_at="24.1",
        remove_at="24.2",
        reason="This method is deprecated. Please use iteration.log() instead",
    )
    def step_factory_and_update(self, value: Any) -> Step | StepString | StepNumber | StepDataset | StepModel:
        # TODO cyclic imports
        from vectice.models.dataset import Dataset
        from vectice.models.model import Model
        from vectice.models.representation.dataset_representation import DatasetRepresentation
        from vectice.models.representation.dataset_version_representation import DatasetVersionRepresentation
        from vectice.models.representation.model_representation import ModelRepresentation
        from vectice.models.representation.model_version_representation import ModelVersionRepresentation
        from vectice.models.step_dataset import StepDataset
        from vectice.models.step_image import StepImage
        from vectice.models.step_model import StepModel
        from vectice.models.step_number import StepNumber
        from vectice.models.step_string import StepString

        ensure_correct_project_id_from_representation_objs(self.project.id, value)

        if isinstance(value, (int, float)):
            self._update_iteration_step(StepType.StepNumber, value)
            return StepNumber(step=self, number=value)

        img_value = is_image_or_file(value)
        if img_value:
            self._update_iteration_step(StepType.StepImage, img_value, True)
            return StepImage(self, img_value)

        if isinstance(value, str):
            check_string_sanity(value)
            self._update_iteration_step(StepType.StepString, value)
            return StepString(self, string=value)

        if (
            isinstance(value, Model)
            or isinstance(value, ModelRepresentation)
            or isinstance(value, ModelVersionRepresentation)
        ):
            data: dict[str, Any] = {}
            if isinstance(value, Model):
                code_version_id = self._get_code_version_id()
                data = self._client.deprecated_register_model(
                    model=value,
                    project_id=self.project.id,
                    phase=self.phase,
                    iteration=self.iteration,
                    code_version_id=code_version_id,
                )
                attachments_output = set_model_attachments(self._client, value, data.model_version)
            elif isinstance(value, ModelRepresentation):
                data = {
                    "useExistingModel": True,
                    "modelVersion": {"vecticeId": value.version.id, "name": value.version.name},
                }
                attachments_output = self._get_version_attachments(value.version)
            elif isinstance(value, ModelVersionRepresentation):  # pyright: ignore[reportUnnecessaryIsInstance]
                data = {
                    "useExistingModel": True,
                    "modelVersion": {"vecticeId": value.id, "name": value.name},
                }
                attachments_output = self._get_version_attachments(value)
            else:
                attachments_output = None

            artifacts = self._get_version_artifacts(data, attachments_output)
            self._client.update_iteration_step_artifact(
                self.id,
                StepType.StepModel,
                artifacts,
            )
            deprecated_register_model_logging(self, data, value, self.name, attachments_output, _logger)
            self.artifacts = [
                IterationStepArtifact(modelVersionId=data["modelVersion"]["vecticeId"], type="ModelVersion")
            ]
            self._warn_step_change(value)
            return StepModel(self, self.artifacts[0], value)  # type: ignore

        elif (
            isinstance(value, Dataset)
            or isinstance(value, DatasetRepresentation)
            or isinstance(value, DatasetVersionRepresentation)
        ):
            dataset: dict[str, Any] = {}
            if isinstance(value, Dataset):
                code_version_id = self._get_code_version_id()
                dataset = self._client.deprecated_register_dataset_from_source(
                    dataset=value,
                    project_id=self.project.id,
                    phase_id=self.phase.id,
                    iteration_id=self.iteration.id,
                    code_version_id=code_version_id,
                )
                attachments_output = set_dataset_attachments(self._client, value, dataset.dataset_version)
            elif isinstance(value, DatasetRepresentation):
                dataset = {
                    "useExistingDataset": True,
                    "useExistingVersion": True,
                    "datasetVersion": {"vecticeId": value.version.id, "name": value.version.name},
                }
                attachments_output = self._get_version_attachments(value.version)
            elif isinstance(value, DatasetVersionRepresentation):  # pyright: ignore[reportUnnecessaryIsInstance]
                dataset = {
                    "useExistingDataset": True,
                    "useExistingVersion": True,
                    "datasetVersion": {"vecticeId": value.id, "name": value.name},
                }
                attachments_output = self._get_version_attachments(value)
            else:
                attachments_output = None

            artifacts = self._get_version_artifacts(dataset, attachments_output)
            self._client.update_iteration_step_artifact(
                self.id,
                StepType.StepDataset,
                artifacts,
            )
            deprecated_register_dataset_logging(self, dataset, value, attachments_output, _logger)
            self.artifacts = [
                IterationStepArtifact(datasetVersionId=dataset["datasetVersion"]["vecticeId"], type="DataSetVersion")
            ]
            self._warn_step_change(value)
            return StepDataset(self, dataset_version=self.artifacts[0])

        return self

    def _get_version_attachments(self, value: ModelVersionRepresentation | DatasetVersionRepresentation):
        return self._client.list_version_representation_attachments(version=value).list

    def _get_version_artifacts(
        self, data: Any, attachments_output: list[AttachmentOutput] | None = None
    ) -> list[IterationStepArtifactInput]:
        attachments = None
        if attachments_output:
            attachments = (
                [IterationStepArtifactInput(id=attach.fileId, type="EntityFile") for attach in attachments_output]
                if attachments_output
                else None
            )
        if "modelVersion" in data:
            artifact = IterationStepArtifactInput(
                id=data["modelVersion"]["vecticeId"],
                type=IterationStepArtifactType.ModelVersion.name,
            )
        else:
            artifact = IterationStepArtifactInput(
                id=data["datasetVersion"]["vecticeId"],
                type=IterationStepArtifactType.DataSetVersion.name,
            )
        artifacts = [artifact]
        artifacts += attachments if attachments else []
        return artifacts

    def _create_image_or_file_artifact(
        self, value: str | IOBase | Image, flush_step_artifacts: bool = False
    ) -> tuple[IterationStepArtifactInput, str]:
        if flush_step_artifacts is True:
            self._flush_artifacts(step_type=StepType.StepImage)

        image_or_file, filename = get_image_or_file_variables(value)
        try:
            artifact, *_ = self._client.deprecated_create_iteration_attachments(
                [("file", (filename, image_or_file))], self.iteration.id, step_id=self.id
            )
            if isinstance(image_or_file, BufferedReader):
                image_or_file.close()
            return (
                IterationStepArtifactInput(id=artifact.fileId, type=IterationStepArtifactType.EntityFile.name),
                filename,
            )
        except Exception as error:
            raise ValueError("Check the provided image.") from error

    def _update_iteration_step(self, type: StepType, value: Any, flush_step_artifacts: bool = False):
        filename: str | None = None
        if type is StepType.StepImage:
            _, filename = self._create_image_or_file_artifact(value=value, flush_step_artifacts=flush_step_artifacts)
            self._warn_step_change(StepType.StepImage)
        elif isinstance(value, (str, int, float)):
            self._client.update_iteration_step_artifact(
                self.id,
                type,
                [IterationStepArtifactInput(type="Comment", text=str(value))],
            )
            self._warn_step_change(value)

        deprecated_comment_or_image_logging(self, _logger, filename)

    def _warn_step_change(self, value: Any):
        # TODO: cyclic import
        from vectice.models.dataset import Dataset
        from vectice.models.model import Model
        from vectice.models.representation.dataset_representation import DatasetRepresentation
        from vectice.models.representation.dataset_version_representation import DatasetVersionRepresentation
        from vectice.models.representation.model_representation import ModelRepresentation
        from vectice.models.representation.model_version_representation import ModelVersionRepresentation

        if self._type is StepType.Step:
            return
        elif self._type is not StepType.StepModel and (
            isinstance(value, Model)
            or isinstance(value, ModelRepresentation)
            or isinstance(value, ModelVersionRepresentation)
        ):
            _logger.debug(f"Step type changed from {self._type.name} to StepModel")
        elif self._type is not StepType.StepDataset and (
            isinstance(value, Dataset)
            or isinstance(value, DatasetRepresentation)
            or isinstance(value, DatasetVersionRepresentation)
        ):
            _logger.debug(f"Step type changed from {self._type.name} to StepDataset")
        elif self._type is not StepType.StepImage and StepType.StepImage is value:
            _logger.debug(f"Step type changed from {self._type.name} to StepImage")
        elif self._type is not StepType.StepNumber and isinstance(value, (int, float)):
            _logger.debug(f"Step type changed from {self._type.name} to StepNumber")
        elif self._type is not StepType.StepString and isinstance(value, str):
            _logger.debug(f"Step type changed from {self._type.name} to StepString")

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> int:
        """The step's id.

        Returns:
            The step's id.
        """
        return self._id

    @id.setter
    def id(self, step_id: int):
        self._id = step_id

    @property
    def index(self) -> int:
        """The step's index.

        Returns:
            The step's index.
        """
        return self._index

    @property
    def slug(self) -> str:
        """The step's slug.

        Returns:
            The step's slug.
        """
        return self._slug

    @property
    def properties(self) -> dict:
        """The step's name, id, and index.

        Returns:
            A dictionary containing the `name`, `id` and `index` items.
        """
        return {"name": self.name, "id": self.id, "index": self.index}

    @property
    def artifacts(self) -> list[IterationStepArtifact]:
        return self._artifacts

    @artifacts.setter
    def artifacts(self, artifacts: list[IterationStepArtifact]):
        self._artifacts = artifacts

    @property
    def connection(self) -> Connection:
        """The connection to which this step belongs.

        Returns:
            The connection to which this step belongs.
        """
        return self._iteration.connection

    @property
    def workspace(self) -> Workspace:
        """The workspace to which this step belongs.

        Returns:
            The workspace to which this step belongs.
        """
        return self._iteration.workspace

    @property
    def project(self) -> Project:
        """The project to which this step belongs.

        Returns:
            The project to which this step belongs.
        """
        return self._iteration.project

    @property
    def phase(self) -> Phase:
        """The phase to which this step belongs.

        Returns:
            The phase to which this step belongs.
        """
        return self._iteration.phase

    @property
    def iteration(self) -> Iteration:
        """The iteration to which this step belongs.

        Returns:
            The iteration to which this step belongs.
        """
        return self._iteration

    def _get_code_version_id(self):
        # TODO: cyclic imports
        from vectice.models.git_version import check_code_source, inform_if_git_repo

        if vectice.code_capture:
            return check_code_source(self._client, self.project.id, _logger)
        else:
            inform_if_git_repo()
            return None

    @property
    def model(self) -> Model | None:
        return self._model

    def _filter_non_empty_artifact(self, artifact: IterationStepArtifact) -> str | int | float | None:
        return artifact.model_version_id or artifact.dataset_version_id or artifact.entity_file_id or artifact.text
