from typing import List, Dict, Any, Optional
from ..types.cortex_file import CortexFile
from ..types.cortex_pipeline import CortexPipeline
from .api_resource import APIResource


class Pipelines(APIResource):
    """
    Cortex Repos API.
    """
    @classmethod
    def get(
        cls, 
        resource_id: Optional[str] = None
    ) -> CortexPipeline| List[CortexPipeline]:
        """
        Gets one or many pipelines.

        Args:
            resource_id (str, optional):
            The ID of the repo to retrieve. If None, retrieves all repo.

        Returns:
            CortexPipeline or list[CortexPipeline]: 
            If resource_id is provided, returns a single CortexPipeline object.
            If resource_id is None, returns a list of CortexPipeline objects.
        """
        return cls._generic_get(
            path        = f'/pipelines/{resource_id or ""}',
            return_type = CortexPipeline
        )

    @classmethod
    def create(
        cls,
        model_id:   str,
        git_branch: str,
        git_hash:   str
    ):
        """
        Creates a new pipeline.

        Args:
            model_id (str):
            The id of the model.

            git_branch (str):
            The name of the Git branch.

            git_hash (str):
            The commit hash.
        """
        return cls._generic_post(
            path = '/pipelines',
            json = {
                'modelId':   model_id,
                'gitBranch': git_branch,
                'gitHash':   git_hash
            }
        )

    @classmethod
    def create_steps(
        cls,
        pipeline_id: str,
        steps: Dict[str, Any]
    ):
        """
        Creates a new pipeline.

        Args:
            model_id (str):
            The id of the model.

            git_branch (str):
            The name of the Git branch.

            git_hash (str):
            The commit hash.
        """
        return cls._generic_post(
            path = f'/pipelines/{pipeline_id}/steps',
            json = {
                'stepsConfig': steps
            }
        )

    @classmethod
    def run(
        cls,
        pipeline_id: str,
        model_id:    str
    ):
        """
        Creates a new pipeline.

        Args:
            model_id (str):
            The id of the model.

            git_branch (str):
            The name of the Git branch.

            git_hash (str):
            The commit hash.
        """
        return cls._generic_post(
            path = f'/pipelines/{pipeline_id}/run',
            json = {
                'modelId': model_id
            }
        )
