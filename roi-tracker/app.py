from datetime import datetime
import os

import boto3 as boto3
import simplejson as json
import time
import logging

from botocore.exceptions import ProfileNotFound

AWS_REGION = os.environ['AWS_REGION']
TABLE_NAME = os.environ['TABLE_NAME']

try:
    boto3.setup_default_session(profile_name='personal')
except ProfileNotFound:
    pass

dynamodb_client = boto3.resource('dynamodb', region_name=AWS_REGION)
table = dynamodb_client.Table(TABLE_NAME)


from chalice import Chalice, Response

app = Chalice(app_name='roi-tracker')

#
# @app.route('/')
# def index():
#     return {'hello': 'world'}


@app.route('/successes', methods=['POST', 'GET'])
def successes():
    app.log.info('Success POST request.')
    request = app.current_request
    if request.method == 'POST':
        new_item = request.json_body
        if not new_item.get('id'):
            new_item['id'] = int(round(time.time() * 1000))
        if not new_item.get('start_date'):
            start_date = datetime.now().isoformat()
            new_item['start_date'] = start_date
        response = table.put_item(Item=new_item)
        logger.info('Success {} added to table.'.format(new_item['id']))
        return Response(body=response,
                        status_code=200,
                        headers={'Content-Type': 'application/json'})

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
