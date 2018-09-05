import simplejson as json
import uuid

import pytest

from src.success import success_lambda


class MockLambdaContext:

    def __init__(self):
        self.aws_request_id = uuid.uuid4()


@pytest.fixture()
def achievement():
    return {
        'id': 1,
        'innovation': 'Created script to reduce database costs.',
        'cost': '500',
        'duration': 0,
        'recurring': 'monthly',
        'statement': 'Created script to reduce database costs by $5/month.',
        'employee_multiplier': 0,
        'employee_salary': 0
    }


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
