import logging

import traceback
import boto3
import json
import uuid
import random

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
xray_recorder.configure(sampling=False, context_missing='LOG_ERROR')
patch_all()

logger = logging.getLogger(__name__)
logging.getLogger("aws_xray_sdk").setLevel(logging.CRITICAL)

session = boto3.Session()


@xray_recorder.capture('handler')
def lambda_handler(event, context):
    """
        AWS Lambda handler
        This method is invoked by the API Gateway: /Prod/first/{proxy+} endpoint.
    """
    xray_subsegment = xray_recorder.current_subsegment()
    xray_subsegment.put_annotation('application', '{{ cookiecutter.project_name.lower().replace(' ',' - ') }}')
    xray_subsegment.put_metadata('event', event, '{{ cookiecutter.project_name.lower().replace(' ',' - ') }}')

    try:
        subsegment = xray_recorder.begin_subsegment('message')
        message = {
            'Id': uuid.uuid4().hex,
            'Count': random.random() * 100,
        }
        subsegment.put_metadata('message', message, '{{ cookiecutter.project_name.lower().replace(' ',' - ') }}')
        xray_recorder.end_subsegment()

        return {"statusCode": 200, "body": json.dumps(message)}

    except Exception as err:  # pragma: no cover
        logger.error(str(err))
        traceback.print_exc()
        raise err
        # return {"statusCode": 500, "body": 'Internal Server Error'}
