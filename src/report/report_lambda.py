import logging
import os
from datetime import datetime
import simplejson as json

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ProfileNotFound

AWS_REGION = os.environ['AWS_REGION']
TABLE_NAME = os.environ['TABLE_NAME']

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
    else:
        raise NotImplementedError()


def get_total_cost_saved(successes, end=datetime.now()):
    """Get total cost saved of successes to end date.

    Args:
        successes (list<dict>): List of successes.
        end (datetime): Results up to and including this end date.

    Returns
        int: Cost saved in cents.
    """
    total_cost_saved = 0
    for success in successes:
        days_active = get_days_active(success, end=datetime.now())
        cost_saved = float(success['cost']) * days_active
        total_cost_saved += cost_saved
    return total_cost_saved


def get_total_employee_salary_saved(successes, end=datetime.now()):
    """Get total cost of salary saved of successes to end date.

    Args:
        successes (list<dict>): List of successes.
        end (datetime): Results up to and including this end date.

    Returns
        int: Cost saved in cents.
    """
    total_employee_savings = 0
    for success in successes:
        if success['employee_multiplier'] and success['employee_salary']:
            days_active = get_days_active(success, end=datetime.now())
            time_saved = float(success['duration']) * days_active
            salary_per_day_in_cents = (float(success['employee_salary']) * 100) / 365
            employee_savings = salary_per_day_in_cents * float(success['employee_multiplier'])
            employee_savings *= time_saved
            total_employee_savings += employee_savings
    return round(total_employee_savings, 2)


def get_days_active(success, end=datetime.now()):
    """Gets the days success has been active.
    Based on how often it has occurred and the selected
    end date.

    Args:
        success (dict): A single success.
        end (datetime): Results up to and including this end date.

    Returns
        int: Days this success was active.

    """
    start_date = datetime.strptime(success['start_date'], '%Y-%m-%dT%H:%M:%S.%f')
    days_active = end - start_date
    days_active = days_active.days
    if success['recurring'] == 'once':
        days_active = 1
    elif success['recurring'] == 'weekly':
        days_active = days_active / 7
    elif success['recurring'] == 'monthly':
        days_active = days_active / 30
    elif success['recurring'] == 'yearly':
        days_active = days_active / 365
    return round(days_active, 2)


def get_total_time_saved(successes, end=datetime.now()):
    """Get total time saved of successes to end date.

    Args:
        successes (list<dict>): List of successes.
        end (datetime): Results up to and including this end date.

    Returns
        timedelta: Time saved in timedelta.
    """
    total_time_saved = 0
    for success in successes:
        days_active = get_days_active(success, end=datetime.now())
        time_saved = float(success['duration']) * days_active
        if success['employee_multiplier']:
            time_saved *= float(success['employee_multiplier'])
        total_time_saved += time_saved
    return total_time_saved


def get_all_statements(successes, end=datetime.now()):
    """Get statements of all successes to end date.

    Args:
        successes (list<dict>): List of successes.
        end (datetime): Results up to and including this end date.

    Returns
        List<str>: List of formatted strings.
    """
    statements = []
    for success in successes:
        statement = success['innovation']
        if success['cost']:
            cost = float(success['cost'])/100
            statement += ', saving ${cost} {recurring}.'.format(
                cost=cost, recurring=success['recurring'])
        if success['duration']:
            duration = round(float(success['duration']) / 60)
            statement += ', saving {duration} minutes {recurring}.'.format(
                duration=duration, recurring=success['recurring'])
            if success['employee_multiplier']:
                'This saved time for {employee_multiplier} employee(s).'.format(**success)
        statements.append(statement)
    return statements


def get_handler(event, context):
    logger.info('Starting lambda handler for GET request.')
    db_response = get_database_response(event)
    items = db_response['Items']
    response = {
        'statusCode': db_response['ResponseMetadata']['HTTPStatusCode'],
        'body': json.dumps(
            {
                'total_cost_saved': get_total_cost_saved(items),
                'total_time_saved': get_total_time_saved(items),
                'total_employee_salary_saved': get_total_employee_salary_saved(items),
                'statements': get_all_statements(items)
             }
        ),
        'isBase64Encoded': False
    }
    logger.info('DynamoDB response:{}'.format(db_response['ResponseMetadata']))
    return response


def get_database_response(event):
    query_string = event.get('queryStringParameters')
    start = query_string.get('start')
    end = query_string.get('end')
    limit = query_string.get('limit', 500)

    if not end:
        end = datetime.now().isoformat()
    if start:
        filter_exp = Key('start_date').between(start, end)
    else:
        filter_exp = Key('start_date').lte(end)

    return table.scan(FilterExpression=filter_exp, Limit=limit)
