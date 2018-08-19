import json
import uuid

import pytest

from src.success import success_lambda


class MockLambdaContext:

    def __init__(self):
        self.aws_request_id = uuid.uuid4()


@pytest.fixture()
def achievement():
    return {
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

    def test_success_lambda_post_handler(self, achievement, api_gateway_post_event):
        context = MockLambdaContext()
        api_gateway_post_event['body'] = achievement
        response = success_lambda.lambda_handler(api_gateway_post_event, context)
        assert response['statusCode'] == 200
