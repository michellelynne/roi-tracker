import decimal
import logging
import json
import os
import time
from copy import deepcopy

import boto3

AWS_REGION = os.environ['AWS_REGION']
TABLE_NAME = os.environ['TABLE_NAME']
os.environ['AWS_PROFILE'] = 'personal'

boto3.setup_default_session(profile_name='personal')
dynamodb_client = boto3.resource('dynamodb', region_name=AWS_REGION)
table = dynamodb_client.Table(TABLE_NAME)

logger = logging.getLogger()
logHandler = logging.StreamHandler()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Success Lambda function

    This lambda is invoked by GET or POST API request,
    it adds/reads info into DynamoDB table.

    Arguments:
        event LambdaEvent -- Lambda Event received from Invoke API.
        context LambdaContext -- Lambda Context runtime methods and attributes.

    Returns:
        dict -- {'statusCode': int, 'body': dict}
    """
    if event['httpMethod'] == 'GET':
        return get_handler(event, context)
    elif event['httpMethod'] == 'POST':
        return post_handler(event, context)
    else:
        raise NotImplementedError()


def get_handler(event, context):
    logger.info("Starting lambda handler for GET request.")

    response = table.get_item(
        Key={
            'id': 'test_id'
        }
    )
    logger.info('DynamoDB response:')
    logger.info(response)
    item = response['Item']

    return {
        'statusCode': 200,
        'body': json.dumps({'test':'test'})
    }


def post_handler(event, context):
    #TODO: Add created date
    logger.info('Success POST request.')
    new_item = deepcopy(event['body'])
    new_item['id'] = int(round(time.time() * 1000))
    response = table.put_item(Item=new_item)
    logger.info('Success {} added to table.'.format(new_item['id']))
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
