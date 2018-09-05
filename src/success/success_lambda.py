import decimal
import logging
import simplejson as json
import os
import time
from copy import deepcopy
from datetime import datetime

import boto3
from botocore.exceptions import ProfileNotFound

AWS_REGION = os.environ['AWS_REGION']
TABLE_NAME = os.environ['TABLE_NAME']


# os.environ['AWS_PROFILE'] = 'personal'
try:
    boto3.setup_default_session(profile_name='personal')
except ProfileNotFound:
    pass
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
    elif event['httpMethod'] == 'PUT':
        return put_handler(event, context)
    elif event['httpMethod'] == 'DELETE':
        return delete_handler(event, context)
    else:
        raise NotImplementedError()


def get_handler(event, context):
    logger.info("Starting lambda handler for GET request.")
    path_id = event['pathParameters'].get('ID')
    if path_id:
        path_id = int(path_id)
        db_response = table.get_item(Key={'id': path_id})
        item = db_response['Item']
        response = {
            'statusCode': db_response['ResponseMetadata']['HTTPStatusCode'],
            'body': json.dumps(item),
            'isBase64Encoded': False
        }
    else:
        db_response = table.scan()
        items = db_response['Items']
        response = {
            'statusCode': db_response['ResponseMetadata']['HTTPStatusCode'],
            'body': json.dumps(items),
            'isBase64Encoded': False
        }
    logger.info('DynamoDB response:{}'.format(db_response['ResponseMetadata']))
    return response


def post_handler(event, context):
    logger.info('Success POST request.')
    new_item = deepcopy(json.loads(event['body']))
    if not new_item.get('id'):
        new_item['id'] = int(round(time.time() * 1000))
    created_date = datetime.now().isoformat()
    new_item['created_date'] = created_date
    response = table.put_item(Item=new_item)
    logger.info('Success {} added to table.'.format(new_item['id']))
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def put_handler(event, context):
    logger.info('Success PUT request.')
    modified_item = deepcopy(json.loads(event['body']))
    path_id = event['pathParameters'].get('ID')
    if not modified_item.get('id'):
        modified_item['id'] = path_id
    response = table.put_item(Item=modified_item)
    logger.info('Success {} modified.'.format(modified_item['id']))
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def delete_handler(event, context):
    logger.info('Success DELETE request.')
    path_id = event['pathParameters'].get('ID')
    path_id = int(path_id)
    db_response = table.delete_item(Key={'id': path_id})
    response = {
        'statusCode': db_response['ResponseMetadata']['HTTPStatusCode'],
        'body': '',
        'isBase64Encoded': False
    }
    logger.info('Success {id} deleted.'.format(id=path_id))
    return response

