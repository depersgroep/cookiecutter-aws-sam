from __future__ import print_function  # Python 2/3 compatibility
import logging
import traceback
import boto3
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def handler(event, context):
    """Scrape an account for EC2 vulnerabilities"""

    deploymentId = event["DeploymentId"]
    lifecycleEventHookExecutionId = event["LifecycleEventHookExecutionId"]

    is_ok = False
    try:
        lambda_client = boto3.client('lambda')
        function_name = 'lambda-one-cfn'
        event = {}
        response = lambda_client.invoke(
            FunctionName=function_name,
            Payload=json.dumps(event)
        )
        data = json.loads(response['Payload'].read())
        if data['statusCode'] == 200:
            is_ok = True
            logger.info("Integration tests Passed.")

    except Exception as err:  # pragma: no cover
        logger.error(str(err))
        traceback.print_exc()

    response = boto3.client('codedeploy').put_lifecycle_event_hook_execution_status(
        deploymentId=deploymentId,
        lifecycleEventHookExecutionId=lifecycleEventHookExecutionId,
        status='Succeeded' if is_ok else 'Failed'
    )
    logger.info("Event hook executed with status [%s]." % ('Succeeded' if is_ok else 'Failed'))

    return response["lifecycleEventHookExecutionId"]
