import logging
import traceback
import boto3
import requests

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
xray_recorder.configure(sampling=False, context_missing='LOG_ERROR')
patch_all()

logger = logging.getLogger(__name__)
logging.getLogger("aws_xray_sdk").setLevel(logging.CRITICAL)

s3 = boto3.resource('s3')
TMP_FILE = "/tmp/badge.svg"


def lambda_handler(event, context):
    """ AWS Lambda handler """
    print(event)
    try:
        _download_badge()

    except Exception as err:  # pragma: no cover
        logger.error(str(err))
        traceback.print_exc()
        raise err
        # return {"statusCode": 500, "body": 'Internal Server Error'}

# def _check_badge_exists():

#     try:
#     except botocore.exceptions.ClientError as e:
#         if e.response['Error']['Code'] == "404":
#             # The object does not exist.
#             ...
#         else:
#             # Something else has gone wrong.
#             raise
#     else:
#         # The object does exist.
#         ...


def _download_badge():
    # Given an Internet-accessible URL, download the image and upload it to S3,
    # without needing to persist the image to disk locally
    req_for_image = requests.get(
        "https://img.shields.io/badge/pipeline-succes-brightgreen.svg", stream=True)
    file_object_from_req = req_for_image.raw
    req_data = file_object_from_req.read()

    # Do the actual upload to s3
    s3.Bucket('{{ cookiecutter.project_name.lower().replace(' ', ' -
              ') }}-{{ cookiecutter.cloudformation_resource_suffix.lower() }}-cfn').put_object(
        Key='country.svg', Body=req_data)
