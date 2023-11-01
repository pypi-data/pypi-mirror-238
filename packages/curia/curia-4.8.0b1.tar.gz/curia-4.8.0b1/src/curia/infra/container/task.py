import dataclasses
from typing import Optional, ClassVar

from curia.infra.task import TaskDefinition
from curia.infra.types import TaskType
from curia.utils.s3 import AWSIoContext, AWSConfig


@dataclasses.dataclass
class ContainerTaskDefinition(TaskDefinition):  # pylint: disable=too-many-instance-attributes
    """
    Task definition for a task executed through a container
    """
    task_type: ClassVar[TaskType] = TaskType.CONTAINER

    # pylint: disable=arguments-differ
    def run(self,
            task_execution_id: str,
            api_token: str,
            api_endpoint: str,
            aws_config: Optional[AWSConfig] = None) -> None:
        """
        Run the analytics task flow definition
        :param task_execution_id: The task execution ID
        :param api_token: The API key to use to retrieve the task inputs from the Curia API
        :param api_endpoint: The API endpoint to use to retrieve the task inputs from the Curia API
        :param aws_config: The AWS region to use for S3
        :return: The result
        """
        if aws_config is None:
            aws_config = AWSConfig()

        with AWSIoContext(
                **aws_config.to_kwargs()
        ):
            assert self._function is not None, "TaskDefinition must decorate a function"
            resolved_args = self.resolve_arguments(task_execution_id, api_token, api_endpoint)
            results = self._function(**resolved_args)
            self.upload_results(task_execution_id, api_token, api_endpoint, results)

    def build_task_type_specific_input_arguments(self, context: dict):
        if "ecs_task_family" not in context:
            raise ValueError("ECS task family must be provided to ContainerTaskDefinition")
        return {
            "taskDefinition": {
                "default": context["ecs_task_family"],
                "required": False
            }
        }
