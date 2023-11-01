import dataclasses
from typing import ClassVar

from pyspark.sql import SparkSession

from curia.infra.task import TaskDefinition
from curia.infra.types import TaskType, DatabricksTaskCodeSourceType


@dataclasses.dataclass
class DatabricksTaskDefinition(TaskDefinition):  # pylint: disable=too-many-instance-attributes
    """
    Task definition for a task executed through a databricks job
    """
    code_src_type: DatabricksTaskCodeSourceType = DatabricksTaskCodeSourceType.S3WHEEL
    code_src_cfg: dict = dataclasses.field(default_factory=dict)
    min_workers: int = 2
    max_workers: int = 4
    task_type: ClassVar[TaskType] = TaskType.DATABRICKS

    # pylint: disable=arguments-differ
    def run(self,
            task_execution_id: str,
            api_token: str,
            api_endpoint: str,
            spark: SparkSession,
            dbutils: 'DBUtils') -> None:
        """
        Run the analytics task flow definition
        :param task_execution_id: The task execution ID
        :param api_token: The API key to use to retrieve the task inputs from the Curia API
        :param api_endpoint: The API endpoint to use to retrieve the task inputs from the Curia API
        :return: The result
        """
        assert self._function is not None, "TaskDefinition must decorate a function"
        resolved_args = self.resolve_arguments(task_execution_id, api_token, api_endpoint)
        results = self._function(**resolved_args, spark=spark, dbutils=dbutils)
        self.upload_results(task_execution_id, api_token, api_endpoint, results)

    def build_task_type_specific_input_arguments(self, context: dict):
        if "databricks_job_id" not in context:
            raise ValueError("Databricks job ID must be provided to DatabricksTaskDefinition")
        databricks_job_id = context["databricks_job_id"]
        return {
            "jobId": {
                "default": databricks_job_id,
                "required": False
            }
        }