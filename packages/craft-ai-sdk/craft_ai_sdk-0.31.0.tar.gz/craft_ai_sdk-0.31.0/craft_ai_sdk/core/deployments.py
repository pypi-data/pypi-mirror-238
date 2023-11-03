from ..constants import DEPLOYMENT_EXECUTION_RULES
from ..io import InputSource, OutputDestination
from ..sdk import BaseCraftAiSdk
from ..utils import log_func_result


@log_func_result("Deployment creation")
def create_deployment(
    sdk: BaseCraftAiSdk,
    pipeline_name,
    deployment_name,
    execution_rule,
    schedule=None,
    inputs_mapping=None,
    outputs_mapping=None,
    description=None,
):
    """Create a custom deployment associated to a given pipeline.

    Args:
        pipeline_name (:obj:`str`): Name of the pipeline.
        deployment_name (:obj:`str`): Name of the deployment.
        execution_rule(:obj:`str`): Execution rule of the deployment. Must
            be "endpoint" or "periodic". For convenience, members of the enumeration
            :class:`DEPLOYMENT_EXECUTION_RULES` could be used too.
        schedule (:obj:`str`, optional): Schedule of the deployment. Only
            required if ``execution_rule`` is "periodic". Must be a valid
            `cron expression <https://www.npmjs.com/package/croner>`.
            The deployment will be executed periodically according to this schedule.
            The schedule must follow this format:
            ``<minute> <hour> <day of month> <month> <day of week>``.
            Note that the schedule is in UTC time zone.
            '*' means all possible values.
            Here are some examples:

                * ``"0 0 * * *"`` will execute the deployment every day at
                  midnight.
                * ``"0 0 5 * *"`` will execute the deployment every 5th day of
                  the month at midnight.

        inputs_mapping(:obj:`list` of instances of :class:`InputSource`):
            List of input mappings, to map pipeline inputs to different
            sources (such as constant values, endpoint inputs, or environment
            variables). See :class:`InputSource` for more details.
            For endpoint rules, if an input of the step in the pipeline is not
            explicitly mapped, it will be automatically mapped to an endpoint
            input with the same name.
            For periodic rules, all inputs of the step in the pipeline must be
            explicitly mapped.
        outputs_mapping(:obj:`list` of instances of :class:`OutputDestination`):
            List of output mappings, to map pipeline outputs to different
            destinations. See :class:`OutputDestination` for more details.
            For endpoint rules, if an output of the step in the pipeline is not
            explicitly mapped, it will be automatically mapped to an endpoint
            output with the same name.
            For periodic rules, all outputs of the step in the pipeline must be
            explicitly mapped.
        description (:obj:`str`, optional): Description of the deployment.

    Returns:
        :obj:`dict[str, str]`: Created deployment represented as a dict with the
        following keys:

        * ``"name"`` (:obj:`str`): Name of the deployment.
        * ``"endpoint_token"`` (:obj:`str`): Token of the endpoint used to
          trigger the deployment. Note that this token is only returned if
          ``execution_rule`` is "endpoint".
        * ``"schedule"`` (:obj:`str`): Schedule of the deployment. Note that
          this schedule is only returned if ``execution_rule`` is "periodic".
        * ``"human_readable_schedule"`` (:obj:`str`): Human readable schedule
          of the deployment. Note that this schedule is only returned if
          ``execution_rule`` is "periodic".
    """

    if execution_rule not in set(DEPLOYMENT_EXECUTION_RULES):
        raise ValueError(
            "Invalid 'execution_rule', must be in ['endpoint', 'periodic']."
        )

    url = (
        f"{sdk.base_environment_api_url}/endpoints"
        if execution_rule == "endpoint"
        else f"{sdk.base_environment_api_url}/periodic-deployment"
    )

    data = {
        "pipeline_name": pipeline_name,
        "name": deployment_name,
        "description": description,
    }

    if schedule is not None:
        if execution_rule != "periodic":
            raise ValueError(
                "'schedule' can only be specified if 'execution_rule' is \
'periodic'."
            )
        else:
            data["schedule"] = schedule

    if inputs_mapping is not None:
        if any(
            [
                not isinstance(input_mapping_, InputSource)
                for input_mapping_ in inputs_mapping
            ]
        ):
            raise ValueError("'inputs' must be a list of instances of InputSource.")
        data["inputs"] = [input_mapping_.to_dict() for input_mapping_ in inputs_mapping]

    if outputs_mapping is not None:
        if any(
            [
                not isinstance(output_mapping_, OutputDestination)
                for output_mapping_ in outputs_mapping
            ]
        ):
            raise ValueError(
                "'outputs' must be a list of instances of OutputDestination."
            )
        data["outputs"] = [
            output_mapping_.to_dict() for output_mapping_ in outputs_mapping
        ]

    # filter optional parameters
    data = {k: v for k, v in data.items() if v is not None}

    return sdk._post(url, json=data)


def get_deployment(sdk: BaseCraftAiSdk, deployment_name):
    """Get information of a deployment.

    Args:
        deployment_name (:obj:`str`): Name of the deployment.

    Returns:
        :obj:`dict`: Deployment information represented as :obj:`dict` with the
        following keys:

        * ``"name"`` (:obj:`str`): Name of the deployment.
        * ``"pipeline"`` (:obj:`dict`): Pipeline associated to the deployment
          represented as :obj:`dict` with the following keys:

          * ``"name"`` (:obj:`str`): Name of the pipeline.

        * ``"inputs_mapping"`` (:obj:`list` of :obj:`dict`): List of inputs
          mapping represented as :obj:`dict` with the following keys:

          * ``"step_input_name"`` (:obj:`str`): Name of the step input.
          * ``"data_type"`` (:obj:`str`): Data type of the step input.
          * ``"description"`` (:obj:`str`): Description of the step input.
          * ``"constant_value"`` (:obj:`str`): Constant value of the step input.
            Note that this key is only returned if the step input is mapped to a
            constant value.
          * ``"environment_variable_name"`` (:obj:`str`): Name of the environment
            variable. Note that this key is only returned if the step input is
            mapped to an environment variable.
          * ``"endpoint_input_name"`` (:obj:`str`): Name of the endpoint input.
            Note that this key is only returned if the step input is mapped to an
            endpoint input.
          * ``"is_null"`` (:obj:`bool`): Whether the step input is mapped to null.
            Note that this key is only returned if the step input is mapped to
            null.
          * ``"datastore_path"`` (:obj:`str`): Datastore path of the step input.
            Note that this key is only returned if the step input is mapped to the
            datastore.
          * ``"is_required"`` (:obj:`bool`): Whether the step input is required.
            Note that this key is only returned if the step input is required.
          * ``"default_value"`` (:obj:`str`): Default value of the step input.
            Note that this key is only returned if the step input has a default
            value.

        * ``"outputs_mapping"`` (:obj:`list` of :obj:`dict`): List of outputs
          mapping represented as :obj:`dict` with the following keys:

          * ``"step_output_name"`` (:obj:`str`): Name of the step output.
          * ``"data_type"`` (:obj:`str`): Data type of the step output.
          * ``"description"`` (:obj:`str`): Description of the step output.
          * ``"endpoint_output_name"`` (:obj:`str`): Name of the endpoint output.
            Note that this key is only returned if the step output is mapped to an
            endpoint output.
          * ``"is_null"`` (:obj:`bool`): Whether the step output is mapped to null.
            Note that this key is only returned if the step output is mapped to
            null.
          * ``"datastore_path"`` (:obj:`str`): Datastore path of the step output.
            Note that this key is only returned if the step output is mapped to
            the datastore.

        * ``"endpoint_token"`` (:obj:`str`): Token of the endpoint. Note that this
          key is only returned if the deployment is an endpoint.
        * ``"schedule"`` (:obj:`str`): Schedule of the deployment. Note that this
          key is only returned if the deployment is a periodic deployment.
        * ``"human_readable_schedule"`` (:obj:`str`): Human readable schedule of
          the deployment. Note that this key is only returned if the deployment is
          a periodic deployment.
        * ``"created_at"`` (:obj:`str`): Date of creation of the deployment.
        * ``"created_by"`` (:obj:`str`): ID of the user who created the deployment.
        * ``"updated_at"`` (:obj:`str`): Date of last update of the deployment.
        * ``"updated_by"`` (:obj:`str`): ID of the user who last updated the
          deployment.
        * ``"last_execution_id"`` (:obj:`str`): ID of the last execution of the
          deployment.
        * ``"active"`` (:obj:`bool`): Whether the deployment is active.
        * ``"description"`` (:obj:`str`): Description of the deployment.
        * ``"execution_rule"`` (:obj:`str`): Execution rule of the deployment.
    """
    url = f"{sdk.base_environment_api_url}/deployments/{deployment_name}"
    return sdk._get(url)


def list_deployments(sdk: BaseCraftAiSdk):
    """Get the list of all deployments.

    Returns:
        :obj:`list` of :obj:`dict`: List of deployments represented as :obj:`dict`
        with the following keys:

        * ``"name"`` (:obj:`str`): Name of the deployment.
        * ``"pipeline_name"`` (:obj:`str`): Name of the pipeline associated to
          the deployment.
        * ``"version"`` (:obj:`str`): Version of the pipeline associated to the
          deployment.
        * ``"execution_count"`` (:obj:`int`): Number of times the deployment has
          been executed.
        * ``"type"`` (:obj:`str`): Type of the deployment. Can be "endpoint", "run"
          or "periodic".
    """
    url = f"{sdk.base_environment_api_url}/deployments"
    return sdk._get(url)


@log_func_result("Deployment deletion")
def delete_deployment(sdk: BaseCraftAiSdk, deployment_name):
    """Delete a deployment identified by its name.

    Args:
        deployment_name (:obj:`str`): Name of the deployment.

    Returns:
        :obj:`dict`: Deleted deployment represented as dict with the following
        keys:

        * ``"name"`` (:obj:`str`): Name of the deployment.
        * ``"type"`` (:obj:`str`): Type of the deployment. Can be "endpoint" or
          "periodic".
    """
    url = f"{sdk.base_environment_api_url}/deployments/{deployment_name}"
    return sdk._delete(url)
