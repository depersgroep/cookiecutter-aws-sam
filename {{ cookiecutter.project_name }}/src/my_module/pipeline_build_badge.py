import logging
import traceback
import boto3
import botocore
import requests

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
xray_recorder.configure(sampling=False, context_missing='LOG_ERROR')
patch_all()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.getLogger("aws_xray_sdk").setLevel(logging.CRITICAL)

s3 = boto3.resource('s3')
TMP_FILE = "/tmp/badge.svg"


def lambda_handler(event, context):
    """ AWS Lambda handler """

    logger.info("Build badge lambda triggered.")

    try:

        if 'detail' not in event:
            raise Exception('Invalid CodePipeline event')

        detail = event['detail']
        if detail['pipeline'] == '{{ cookiecutter.project_name.lower().replace(' ', ' - ') }}-pipeline-{{ cookiecutter.cloudformation_resource_suffix.lower() }}-cfn':

            logger.info("Build badge trigger for pipeline [%s]." % detail['pipeline'])

            bucket = '{{ cookiecutter.project_name.lower().replace(' ', ' - ') }}-{{ cookiecutter.cloudformation_resource_suffix.lower() }}-cfn'

            state = detail['state'].lower()
            badge = state + '.svg'

            _assure_badge_exists(bucket, state, badge)

            copy_source = {
                'Bucket': bucket,
                'Key': 'badges/' + badge
            }
            extra_args = {
                'ACL': 'public-read'
            }
            s3.Bucket(bucket).copy(copy_source, 'badges/current_state.svg', ExtraArgs=extra_args)

            logger.info("Current pipline state successfully linked to badge [%s]." % badge)

    except Exception as err:  # pragma: no cover
        logger.error(str(err))
        traceback.print_exc()
        raise err


def _get_badge_color(state):
    if state == 'canceled':
        return 'lightgrey'
    if state == 'failed':
        return 'red'
    if state == 'resumed':
        return 'yellow'
    if state == 'started':
        return 'yellow'
    if state == 'succeeded':
        return 'brightgreen'
    if state == 'superseded':
        return 'orange'


def _assure_badge_exists(bucket, state, badge):

    try:
        s3.Object(bucket, 'badges/' + badge).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # Given an Internet-accessible URL, download the image and upload it to S3,
            # without needing to persist the image to disk locally
            url = 'https://img.shields.io/badge/'
            filename = 'pipeline-' + state + '-' + _get_badge_color(state) + '.svg'
            req_for_image = requests.get(url + filename, stream=True)
            file_object_from_req = req_for_image.raw
            req_data = file_object_from_req.read()

            # Do the actual upload to s3
            s3.Bucket(bucket).put_object(
                ACL='public-read',
                CacheControl='no-cache',
                ContentEncoding='gzip',
                ContentDisposition='inline',
                ContentType='image/svg+xml',
                Key='badges/' + badge,
                Body=req_data)

            logger.info("Badge [%s] generated and stored on S3." % badge)
        else:
            raise
    else:
        logger.info("Badge [%s] already exists." % badge)
