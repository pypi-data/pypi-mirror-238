from __future__ import annotations

import logging
from contextlib import suppress
from io import BufferedReader, IOBase
from textwrap import dedent
from typing import TYPE_CHECKING, Any, ClassVar

from PIL.Image import Image
from rich.table import Table

import vectice
from vectice.api.http_error_handlers import ArtifactVersionIdExistingError, NoStepsInPhaseError, VecticeException
from vectice.api.json.iteration import (
    IterationInput,
    IterationOutput,
    IterationStatus,
    IterationStepArtifactInput,
    IterationStepArtifactType,
)
from vectice.models.step import Step
from vectice.utils.common_utils import (
    check_read_only,
    check_string_sanity,
    ensure_correct_project_id_from_representation_objs,
    get_image_or_file_variables,
    get_step_type,
    set_dataset_attachments,
    set_model_attachments,
    temp_print,
)
from vectice.utils.deprecation import deprecate
from vectice.utils.instance_helper import is_image_or_file
from vectice.utils.last_assets import (
    assign_asset_version_logging,
    comment_or_image_logging,
    register_dataset_logging,
    register_model_logging,
)
from vectice.utils.logging_utils import get_iteration_status

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.api import Client
    from vectice.models import Phase, Project, Workspace
    from vectice.models.dataset import Dataset
    from vectice.models.model import Model
    from vectice.models.representation.dataset_representation import DatasetRepresentation
    from vectice.models.representation.dataset_version_representation import DatasetVersionRepresentation
    from vectice.models.representation.model_representation import ModelRepresentation
    from vectice.models.representation.model_version_representation import ModelVersionRepresentation

    TAssetType = ModelRepresentation | ModelVersionRepresentation | DatasetRepresentation | DatasetVersionRepresentation

_logger = logging.getLogger(__name__)


class Iteration:
    """Represent a Vectice iteration.

    Iterations reflect the development and test cycles completed
    by data scientists until a fully functional algorithm is ready for
    deployment. Each iteration can be organised into sections for clarity.

    Typical usage example:

    ```python
    # Create a new iteration within a phase
    iteration = phase.create_iteration()

    # Log a dataset to the iteration
    iteration.log(my_dataset)

    # Log a model to the iteration with optional section assignment
    iteration.log(my_model, section="Modeling")
    ```

    NOTE: **You can create sections dynamically using the API.**

    To create a new iteration:

    ```python
    iteration = phase.create_iteration()
    ```
    """

    __slots__: ClassVar[list[str]] = [
        "_id",
        "_index",
        "_phase",
        "_status",
        "_client",
        "_steps",
        "__dict__",
    ]

    def __init__(
        self,
        output: IterationOutput,
        phase: Phase,
        client: Client,
    ):
        self.__dict__ = {}
        self._id = output.id
        self._index = output.index
        self._phase = phase
        self._status = output.status
        self._client = client
        self._steps = self._populate_steps()

    def __repr__(self):
        return f"Iteration (index={self._index}, status={self._status}"

    def __eq__(self, other: object):
        if not isinstance(other, Iteration):
            return NotImplemented
        return self.id == other.id

    def _populate_steps(self) -> dict[str, Step]:
        with suppress(NoStepsInPhaseError):
            step_output = self._client.list_steps(self.id, True).list
            steps = [get_step_type(step_output=item, iteration=self) for item in step_output]
            check = {step.slug: step for step in steps}
            return check
        return {}

    def __getattr__(self, item: str) -> Step:
        if item in self.__dict__:
            return self.__dict__[item]
        if item in super().__getattribute__("_steps"):
            step_item = self._steps[item]
            step = self._client.get_step_by_name(step_item.name, self.id)
            return get_step_type(step_output=step, iteration=self)
        raise AttributeError(f"The attribute '{item}' does not exist.")

    def __setattr__(self, attr_name: str, attr_value: Any):
        if hasattr(self, "_steps") and attr_name in super().__getattribute__("_steps"):
            self._steps[attr_name] = self._steps[attr_name].step_factory_and_update(value=attr_value)
        elif hasattr(self, "__dict__") and attr_name not in self.__slots__:
            raise AttributeError(f"The attribute '{attr_name}' does not exist.")
        else:
            super().__setattr__(attr_name, attr_value)

    @property
    def id(self) -> str:
        """The iteration's identifier.

        Returns:
            The iteration's identifier.
        """
        return self._id

    @id.setter
    def id(self, iteration_id: str):
        """Set the iteration's identifier.

        Parameters:
            iteration_id: The identifier.
        """
        check_read_only(self)
        self._id = iteration_id

    @property
    def index(self) -> int:
        """The iteration's index.

        Returns:
            The iteration's index.
        """
        return self._index

    @property
    def status(self) -> str:
        """The iteration's status.

        Returns:
            The iteration's status.
        """
        return get_iteration_status(self._status)

    @property
    def completed(self) -> bool:
        """Whether this iteration is completed.

        Returns:
            Whether the iteration is completed.
        """
        return self._status is IterationStatus.Completed

    @property
    def properties(self) -> dict[str, int | str]:
        """The iteration's identifier and index.

        Returns:
            A dictionary containing the `id` and `index` items.
        """
        return {"id": self.id, "index": self.index}

    def list_phase_requirements(self) -> None:
        """Prints a list of phase requirements in a tabular format, limited to the first 10 requirements. A link is provided to view the remaining requirements.

        Returns:
            None
        """
        paged_requirements = self._client.list_step_definitions(self.phase.id)

        rich_table = Table(expand=True, show_edge=False)

        rich_table.add_column("Title", justify="left", no_wrap=True, min_width=5, max_width=40)
        rich_table.add_column("Description", justify="left", no_wrap=True, min_width=5, max_width=35)

        for requirement in paged_requirements.list:
            description = requirement.description.strip() if requirement.description else None
            rich_table.add_row(requirement.name, description)

        description = f"""There are {paged_requirements.total} requirements in the phase {self.phase.name!r} and a maximum of 10 requirements are displayed in the table below:"""
        link = dedent(
            f"""
                For quick access to the phase requirements in the Vectice web app, visit:
                {self._client.auth.api_base_url}/phase/{self.phase.id}/requirements
            """
        ).lstrip()

        temp_print(description)
        temp_print(table=rich_table)
        temp_print(link)

    def list_sections(self) -> None:
        """Prints a list of sections belonging to the iteration in a tabular format, limited to the first 10 sections. A link is provided to view the remaining sections.

        Returns:
            None
        """
        iteration_output = self._client.list_sections(self.id)

        rich_table = Table(expand=True, show_edge=False)

        rich_table.add_column("Name", justify="left", no_wrap=True, min_width=5, max_width=40)
        rich_table.add_column("Assets (count)", justify="left", no_wrap=True, min_width=5, max_width=15)

        if iteration_output.artifacts_count > 0:
            rich_table.add_row("None ('Assets without section')", str(iteration_output.artifacts_count))

        for section in iteration_output.sections.list:
            rich_table.add_row(section.name, str(section.artifacts_count))

        description = f"""There are {iteration_output.sections.total} sections in the iteration {self.index!r} and a maximum of 10 sections are displayed in the table below:"""
        link = dedent(
            f"""
                >> To log an asset to a specific section, use iteration.log()
                For quick access to the iteration in the Vectice web app, visit:
                {self._client.auth.api_base_url}/browse/iteration/{self.id}
            """
        ).lstrip()

        temp_print(description)
        temp_print(table=rich_table)
        temp_print(link)

    @deprecate(
        warn_at="23.4",
        fail_at="24.1",
        remove_at="24.2",
        reason="Steps are deprecated. Please use iteration.list_sections() instead.",
    )
    def list_steps(self) -> None:
        """WARNING: **DEPRECATED** To list the sections of your iteration, use list_sections() instead.

        Prints a list of steps belonging to the iteration in a tabular format, limited to the first 10 steps. A link is provided to view the remaining steps.

        Returns:
            None
        """
        steps_output = self._client.list_steps(self.id, populate=False)

        rich_table = Table(expand=True, show_edge=False)

        rich_table.add_column("Shortcut", justify="left", no_wrap=True, min_width=5, max_width=20)
        rich_table.add_column("Registered items (count)", justify="left", no_wrap=True, min_width=5, max_width=15)
        rich_table.add_column("Description", justify="left", no_wrap=True, min_width=5, max_width=35)

        if steps_output.total == 0:
            _logger.info(
                "The list of steps is empty. Use iteration.log() to log an asset to vectice.\n"
                "The += syntax is deprecated, if you still want to use it, close that iteration and create a new one with steps."
            )
            return

        for step in steps_output.list:
            description = step.description.strip() if step.description else None
            rich_table.add_row(step.slug, str(step.artifacts_count), description)
        description = f"""There are {steps_output.total} steps in Iteration '{self.index!r}' and a maximum of 10 steps are displayed in the table below:"""
        tips = dedent(
            """
        To access a specific step, use the step shortcut \033[1iiteration\033[0m.step_my_step_name
        The step reference is referred to as shortcut"""
        ).lstrip()
        link = dedent(
            f"""
        For quick access to the list of steps in the Vectice web app, visit:
        {self._client.auth.api_base_url}/browse/iteration/{self.id}"""
        ).lstrip()

        temp_print(description)
        temp_print(table=rich_table)
        temp_print(tips)
        temp_print(link)

    def cancel(self) -> None:
        """Cancel the iteration."""
        iteration_input = IterationInput(status=IterationStatus.Abandoned.name)
        self._client.update_iteration(self.id, iteration_input)
        self._status = IterationStatus.Abandoned
        _logger.info(f"Iteration with index {self.index} cancelled.")

    def complete(self) -> None:
        """Mark the iteration as completed."""
        iteration_input = IterationInput(status=IterationStatus.Completed.name)
        self._client.update_iteration(self.id, iteration_input)
        self._status = IterationStatus.Completed
        logging_output = dedent(
            f"""
                        Iteration with index {self.index} completed.

                        For quick access to the Iteration in the Vectice web app, visit:
                        {self._client.auth.api_base_url}/browse/iteration/{self.id}"""
        ).lstrip()
        _logger.info(logging_output)

    def delete(self) -> None:
        """Permanently deletes the iteration."""
        self._client.delete_iteration(self.id)
        _logger.info(f"Iteration with index {self.index} was deleted.")

    @property
    def connection(self) -> Connection:
        """The connection to which this iteration belongs.

        Returns:
            The connection to which this iteration belongs.
        """
        return self._phase.connection

    @property
    def workspace(self) -> Workspace:
        """The workspace to which this iteration belongs.

        Returns:
            The workspace to which this iteration belongs.
        """
        return self._phase.workspace

    @property
    def project(self) -> Project:
        """The project to which this iteration belongs.

        Returns:
            The project to which this iteration belongs.
        """
        return self._phase.project

    @property
    def phase(self) -> Phase:
        """The phase to which this iteration belongs.

        Returns:
            The phase to which this iteration belongs.
        """
        return self._phase

    def log(self, asset: Any, section: str | None = None) -> None:
        """Log an asset to an iteration. Assets can be organized into sections for improved clarity within the iteration.

        ```python
        from vectice import Model
        my_model = Model(name="my_model")
        iteration.log(my_model)
        iteration.log("my note")
        ```

        Parameters:
            asset: The asset to log to an iteration. Assets can include notes, images, Vectice datasets, or Vectice models.
            section (Optional): The iteration's section where the asset will be displayed in the Vectice App. Assets without sections are logged in the iteration itself.

        """
        # TODO: cyclic imports
        from vectice.models.dataset import Dataset
        from vectice.models.model import Model
        from vectice.models.representation.dataset_representation import (
            DatasetRepresentation,
            DatasetVersionRepresentation,
        )
        from vectice.models.representation.model_representation import ModelRepresentation, ModelVersionRepresentation

        self._client.assert_feature_flag_or_raise("iteration-improvements")

        ensure_correct_project_id_from_representation_objs(self.project.id, asset)

        if section:
            section = section.strip()

        if section is not None and len(section) > 60:
            raise VecticeException("section: name must be shorter than or equal to 60 characters")

        if is_image_or_file(asset):
            self._log_image_or_file(asset, section)

        elif isinstance(asset, (int, float, str)):
            self._log_comment(asset, section)

        elif isinstance(
            asset,
            (ModelRepresentation, ModelVersionRepresentation, DatasetRepresentation, DatasetVersionRepresentation),
        ):
            self._assign_version_representation(asset, section)

        elif isinstance(asset, Model):
            self._log_model(asset, section)

        elif isinstance(asset, Dataset):
            self._log_dataset(asset, section)
        else:
            raise TypeError(f"Expected Image, Comment, Dataset or a Model, got {type(asset)}")

    def _create_image_or_file_artifact(
        self, value: str | IOBase | Image, section: str | None = None
    ) -> tuple[IterationStepArtifactInput, str]:
        is_image_or_file, filename = get_image_or_file_variables(value)
        try:
            artifact, *_ = self._client.create_iteration_attachments(
                files=[("file", (filename, is_image_or_file))], iteration_id=self.id, step_name=section
            )
            if isinstance(is_image_or_file, BufferedReader):
                is_image_or_file.close()
            return (
                IterationStepArtifactInput(id=artifact.fileId, type=IterationStepArtifactType.EntityFile.name),
                filename,
            )
        except Exception as error:
            raise ValueError("Check the provided image.") from error

    def _get_code_version_id(self):
        # TODO: cyclic imports
        from vectice.models.git_version import check_code_source, inform_if_git_repo

        if vectice.code_capture:
            return check_code_source(self._client, self.project.id, _logger)
        else:
            inform_if_git_repo()
            return None

    def _log_image_or_file(self, asset: str | IOBase | Image, section: str | None = None):
        _, filename = self._create_image_or_file_artifact(asset, section)
        comment_or_image_logging(self, _logger, section, filename)

    def _log_comment(self, asset: int | float | str, section: str | None = None):
        if isinstance(asset, str):
            check_string_sanity(asset)
        artifact_inp: list[IterationStepArtifactInput] = [IterationStepArtifactInput(type="Comment", text=str(asset))]
        self._client.add_iteration_artifacts(iteration_id=self._id, artifacts=artifact_inp, section=section)
        comment_or_image_logging(self, _logger, section)

    def _assign_version_representation(
        self,
        asset: TAssetType,
        section: str | None = None,
    ):
        from vectice.models.representation.dataset_representation import DatasetRepresentation
        from vectice.models.representation.model_representation import ModelRepresentation

        asset_type = self._get_asset_type_from_asset_representation(asset)

        artifact_inp = [
            IterationStepArtifactInput(
                type=asset_type,
                id=asset.version.id if isinstance(asset, (ModelRepresentation, DatasetRepresentation)) else asset.id,
            )
        ]
        already_assigned: bool = False
        try:
            self._client.add_iteration_artifacts(iteration_id=self._id, artifacts=artifact_inp, section=section)
        except ArtifactVersionIdExistingError:
            already_assigned = True
        assign_asset_version_logging(
            iteration=self,
            value=asset,
            _logger=_logger,
            already_assigned=already_assigned,
            section=section,
        )

    def _log_model(self, asset: Model, section: str | None = None):
        code_version_id = self._get_code_version_id()
        model_data = self._client.register_model(
            model=asset,
            phase=self.phase,
            iteration=self,
            code_version_id=code_version_id,
            section=section,
        )
        attachments_output = set_model_attachments(self._client, asset, model_data.model_version)
        register_model_logging(self, model_data, asset, attachments_output, _logger, section)

    def _log_dataset(self, asset: Dataset, section: str | None = None):
        code_version_id = self._get_code_version_id()
        dataset_output = self._client.register_dataset_from_source(
            dataset=asset,
            iteration_id=self.id,
            code_version_id=code_version_id,
            section=section,
        )
        attachments_output = set_dataset_attachments(self._client, asset, dataset_output.dataset_version)
        register_dataset_logging(self, dataset_output, asset, attachments_output, _logger, section)

    def _get_asset_type_from_asset_representation(
        self,
        asset: TAssetType,
    ):
        from vectice.models.representation.dataset_representation import (
            DatasetRepresentation,
            DatasetVersionRepresentation,
        )
        from vectice.models.representation.model_representation import ModelRepresentation, ModelVersionRepresentation

        if isinstance(asset, (ModelRepresentation, ModelVersionRepresentation)):
            return "ModelVersion"
        if isinstance(
            asset, (DatasetRepresentation, DatasetVersionRepresentation)
        ):  # pyright: ignore[reportUnnecessaryIsInstance]
            return "DataSetVersion"

        raise ValueError(f"Asset type '{type(asset)!s}' is unsupported")
