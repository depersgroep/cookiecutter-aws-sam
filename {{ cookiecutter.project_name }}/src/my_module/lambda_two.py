import logging
import traceback
import boto3
import json

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
xray_recorder.configure(sampling=False, context_missing='LOG_ERROR')
patch_all()

logger = logging.getLogger(__name__)
logging.getLogger("aws_xray_sdk").setLevel(logging.CRITICAL)

session = boto3.Session()


def lambda_handler(event, context):
    """ AWS Lambda handler """
    try:
        message = {
            'status': 'ok'
        }
        # raise Exception('Simulate error')
        return {"statusCode": 200, "body": json.dumps(message)}

    except Exception as err:  # pragma: no cover
        logger.error(str(err))
        traceback.print_exc()
        raise err
        # return {"statusCode": 500, "body": 'Internal Server Error'}
