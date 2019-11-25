from datetime import datetime, timedelta

import simplejson as json
import uuid

import pytest

from src.report import report_lambda
from src.report.report_lambda import get_total_cost_saved, get_days_active, get_total_time_saved, get_all_statements, \
    get_total_employee_salary_saved
from src.success import success_lambda


class MockLambdaContext:

    def __init__(self):
        self.aws_request_id = uuid.uuid4()


@pytest.fixture()
def achievement():
    return {
        'id': 1,
        'innovation': 'Created script to reduce database costs.',
        'cost': 500,
        'duration': 0,
        'recurring': 'monthly',
        'statement': 'Created script to reduce database costs by $5/month.',
        'employee_multiplier': 0,
        'employee_salary': 0
    }

@pytest.fixture()
def achievements():
    now = datetime.now()
    return [
        {
            'id': 2,
            'innovation': 'Archived data to reduce storage costs',
            'cost': 500,
            'duration': 0,
            'recurring': 'monthly',
            'employee_multiplier': 0,
            'employee_salary': 0,
            'start_date': (now - timedelta(days=2*30)).isoformat()},
        {
            'id': 3,
            'innovation': 'Created automated tests to reduce manual testing',
            'cost': 0,
            'duration': 60 * 60,
            'recurring': 'weekly',
            'employee_multiplier': 0,
            'employee_salary': 0,
            'start_date': (now - timedelta(days=2 * 7)).isoformat()},
        {
            'id': 4,
            'innovation': 'Created library to eliminate need for 3rd party service',
            'cost': 10000,
            'duration': 0,
            'recurring': 'once',
            'employee_multiplier': 2,
            'employee_salary': 50000,
            'start_date': (now - timedelta(days=1)).isoformat()},
        {
            'id': 5,
            'innovation': 'Created automated report to eliminate need of manual report creation',
            'cost': 0,
            'duration': 60 * 30,
            'recurring': 'daily',
            'employee_multiplier': 2,
            'employee_salary': 50000,
            'start_date': (now - timedelta(days=3)).isoformat()},
        {
            'id': 6,
            'innovation': 'Archived data to reduce storage costs',
            'cost': 500,
            'duration': 0,
            'recurring': 'monthly',
            'employee_multiplier': 0,
            'employee_salary': 0,
            'start_date': (now - timedelta(days=6 * 30)).isoformat()},
        {
            'id': 7,
            'innovation': 'Created automated tests to reduce manual testing',
            'cost': 0,
            'duration': 60 * 60,
            'recurring': 'weekly',
            'employee_multiplier': 0,
            'employee_salary': 0,
            'start_date': (now - timedelta(days=5 * 7)).isoformat()},
        {
            'id': 8,
            'innovation': 'Created library to eliminate need for 3rd party service',
            'cost': 10000,
            'duration': 0,
            'recurring': 'once',
            'employee_multiplier': 0,
            'employee_salary': 0,
            'start_date': (now - timedelta(days=30)).isoformat()},
        {
            'id': 9,
            'innovation': 'Created automated report to eliminate need of manual report creation',
            'cost': 0,
            'duration': 60 * 30,
            'recurring': 'daily',
            'employee_multiplier': 1,
            'employee_salary': 50000,
            'start_date': (now - timedelta(days=7)).isoformat()}
    ]


@pytest.fixture()
def api_gateway_post_event():
    """API Gateway Event."""
    return {
        "body": "{\"test\":\"body\"}",
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": None,
                "userArn": None,
                "cognitoAuthenticationType": None,
                "caller": None,
                "userAgent": "Custom User Agent String",
                "user": None,
                "cognitoIdentityPoolId": None,
                "cognitoIdentityId": None,
                "cognitoAuthenticationProvider": None,
                "sourceIp": "127.0.0.1",
                "accountId": None
            },
            "stage": "prod"
        },
        "queryStringParameters": {
            "foo": "bar"
        },
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch"
        },
        "pathParameters": {
            "proxy": "success"
        },
        "httpMethod": "POST",
        "stageVariables": {
            "baz": "qux"
        },
        "path": "/success"
    }


class TestSuccessLambda:

    def test_success_lambda_post_returns_200(self, api_gateway_post_event, achievement):
        context = MockLambdaContext()
        api_gateway_post_event['body'] = json.dumps(achievement)
        response = success_lambda.lambda_handler(api_gateway_post_event, context)
        assert response['statusCode'] == 200

    def test_success_lambda_get_with_id_returns_success(self, api_gateway_post_event, achievement):
        # POST
        context = MockLambdaContext()
        api_gateway_post_event['body'] = json.dumps(achievement)
        success_lambda.lambda_handler(api_gateway_post_event, context)

        # GET
        api_gateway_post_event['path'] = '/successes/{id}'.format(**achievement)
        api_gateway_post_event['pathParameters'] = {'ID': achievement['id']}
        api_gateway_post_event['httpMethod'] = 'GET'
        response = success_lambda.lambda_handler(api_gateway_post_event, context)
        return_body = json.loads(response['body'])
        assert response['statusCode'] == 200
        assert return_body['id'] == api_gateway_post_event['pathParameters']['ID']

    def test_success_lambda_get_all_returns_success(self, api_gateway_post_event, achievement):
        # POST
        context = MockLambdaContext()
        api_gateway_post_event['body'] = json.dumps(achievement)
        success_lambda.lambda_handler(api_gateway_post_event, context)

        # GET
        api_gateway_post_event['path'] = '/successes'
        api_gateway_post_event['httpMethod'] = 'GET'
        response = success_lambda.lambda_handler(api_gateway_post_event, context)
        return_body = json.loads(response['body'])
        assert response['statusCode'] == 200
        assert return_body[0]['id'] == 1

    def test_success_lambda_put_handler_returns_200(self, api_gateway_post_event, achievement):
        # POST
        context = MockLambdaContext()
        api_gateway_post_event['body'] = json.dumps(achievement)
        success_lambda.lambda_handler(api_gateway_post_event, context)
        api_gateway_post_event['path'] = '/successes/{id}'.format(**achievement)
        api_gateway_post_event['pathParameters'] = {'ID': achievement['id']}
        api_gateway_post_event['httpMethod'] = 'PUT'
        api_gateway_post_event['body'] = json.dumps({'cost': 600})

        # PUT
        results = success_lambda.lambda_handler(api_gateway_post_event, context)
        assert results['statusCode'] == 200

        # GET
        api_gateway_post_event['httpMethod'] = 'GET'
        results = success_lambda.lambda_handler(api_gateway_post_event, context)
        return_body = json.loads(results['body'])
        assert return_body['cost'] == 600

        # DELETE
        api_gateway_post_event['httpMethod'] = 'DELETE'
        results = success_lambda.lambda_handler(api_gateway_post_event, context)
        assert results['statusCode'] == 200

    def test_success_lambda_with_id_handler_returns_200(self, api_gateway_post_event, achievement):
        # POST
        context = MockLambdaContext()
        api_gateway_post_event['body'] = json.dumps(achievement)
        success_lambda.lambda_handler(api_gateway_post_event, context)

        # DELETE
        api_gateway_post_event['path'] = '/successes/{id}'.format(**achievement)
        api_gateway_post_event['path'] = '/successes/{id}'.format(**achievement)
        api_gateway_post_event['pathParameters'] = {'ID': achievement['id']}
        api_gateway_post_event['httpMethod'] = 'DELETE'
        results = success_lambda.lambda_handler(api_gateway_post_event, context)
        assert results['statusCode'] == 200


class TestReportLambda:

    def test_get_total_cost_saved(self, achievements):
        total_cost_saved = get_total_cost_saved(achievements)
        expected_total_cost_saved = 24000.0
        assert total_cost_saved == expected_total_cost_saved

    def test_get_days_active(self, achievements):
        days_active_list = []
        for achievement in achievements:
            days_active_list.append(get_days_active(achievement))
        assert days_active_list == [1.97, 1.86, 1, 2, 5.97, 4.86, 1, 6]

    def test_get_total_time_saved(self, achievements):
        expected_total_time_saved = 48600.0
        total_time_saved = get_total_time_saved(achievements)
        assert total_time_saved == expected_total_time_saved

    def test_get_all_statements(self, achievements):
        expected_statements = [
            'Archived data to reduce storage costs, saving $5.0 monthly.',
            'Created automated tests to reduce manual testing, saving 60 minutes weekly.',
            'Created library to eliminate need for 3rd party service, saving $100.0 once.',
            'Created automated report to eliminate need of manual report creation, saving 30 minutes daily.']
        assert get_all_statements(achievements[:4]) == expected_statements

    def test_get_total_employee_salary_saved(self, achievements):
        expected_total_employee_salary_saved = 15565.13
        total_employee_salary_saved = get_total_employee_salary_saved(achievements)
        assert total_employee_salary_saved == expected_total_employee_salary_saved

    def test_report_lambda_get_db_response_returns_ids(self, api_gateway_post_event, achievements):
        context = MockLambdaContext()
        for achievement in achievements:
            api_gateway_post_event['body'] = json.dumps(achievement)
            response = success_lambda.lambda_handler(api_gateway_post_event, context)
            assert response['statusCode'] == 200
        now = datetime.now()
        api_gateway_post_event['path'] = '/report'
        api_gateway_post_event['httpMethod'] = 'GET'

        # 1 Week
        expected_item_ids = [4, 5]
        week_ago = now - timedelta(days=7)
        api_gateway_post_event['queryStringParameters'] = {'start': week_ago.isoformat()}
        response = report_lambda.get_database_response(api_gateway_post_event)
        item_ids = sorted([int(i['id']) for i in response['Items']])
        assert item_ids == expected_item_ids

        # 6 Months
        expected_item_ids = [2, 3, 4, 5, 7, 8, 9]
        six_months_ago = now - timedelta(days=30 * 6)
        api_gateway_post_event['queryStringParameters'] = {'start': six_months_ago.isoformat()}
        response = report_lambda.get_database_response(api_gateway_post_event)
        item_ids = sorted([int(i['id']) for i in response['Items']])
        assert item_ids == expected_item_ids

        # 6 Months Ago to 1 Month
        expected_item_ids = [2, 7, 8]
        one_month_ago = now - timedelta(days=30)
        six_months_ago = now - timedelta(days=30 * 6)
        query_string = {'start': six_months_ago.isoformat(), 'end': one_month_ago.isoformat()}
        api_gateway_post_event['queryStringParameters'] = query_string
        response = report_lambda.get_database_response(api_gateway_post_event)
        item_ids = sorted([int(i['id']) for i in response['Items']])
        assert item_ids == expected_item_ids

    def test_report_lambda_get_returns_200(self, api_gateway_post_event, achievements):
        context = MockLambdaContext()

        for achievement in achievements:
            api_gateway_post_event['body'] = json.dumps(achievement)
            response = success_lambda.lambda_handler(api_gateway_post_event, context)
            assert response['statusCode'] == 200
        now = datetime.now()

        api_gateway_post_event['path'] = '/report'
        api_gateway_post_event['httpMethod'] = 'GET'

        # 1 Week
        expected_response = {
            'statusCode': 200,
            'body':
                '{"total_cost_saved": 10000.0, "total_time_saved": 10800.0,'
                ' "total_employee_salary_saved": 7183.91, '
                '"statements": ["Created library to eliminate need for 3rd party service, saving $100.0 once.",'
                ' "Created automated report to eliminate need of manual report creation, saving 30 minutes daily."]}',
            'isBase64Encoded': False}
        week_ago = now - timedelta(days=7)
        api_gateway_post_event['queryStringParameters'] = {'start': week_ago.isoformat()}
        response = report_lambda.lambda_handler(api_gateway_post_event, context)
        assert response == expected_response