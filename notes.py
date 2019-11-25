
dynamodb_client = boto3.resource('dynamodb', region_name=AWS_REGION)
table = dynamodb_client.Table(TABLE_NAME)

table.get_item(Key={'id': path_id})
table.scan()
table.put_item(Item=new_item)
table.put_item(Item=modified_item)
table.delete_item(Key={'id': path_id})


get_total_time_saved
get_total_employee_salary_saved
get_days_active
get_total_cost_saved
get_all_statements


    {"id": 2, "innovation": "Archived data to reduce storage costs", "cost": 500, "duration": 0, "recurring": "monthly", "employee_multiplier": 0, "employee_salary": 0, "start_date": "2018-08-03T19:41:08Z"}
                 {"id": 3, "innovation": "Created automated tests to reduce manual testing", "cost": 0, "duration": 3600, "recurring": "weekly", "employee_multiplier": 0, "employee_salary": 0, "start_date": "2018-09-18T19:41:08Z"}
                 {"id": 4, "innovation": "Created library to eliminate need for 3rd party service", "cost": 10000, "duration": 0, "recurring": "once", "employee_multiplier": 2, "employee_salary": 50000, "start_date": "2018-10-01T19:41:08Z"}
                 {"id": 5, "innovation": "Created automated report to eliminate need of manual report creation", "cost": 0, "duration": 1800, "recurring": "daily", "employee_multiplier": 2, "employee_salary": 50000, "start_date": "2018-09-29T19:41:08Z"}
                 {"id": 6, "innovation": "Archived data to reduce storage costs", "cost": 500, "duration": 0, "recurring": "monthly", "employee_multiplier": 0, "employee_salary": 0, "start_date": "2018-04-05T19:41:08Z"}
                 {"id": 7, "innovation": "Created automated tests to reduce manual testing", "cost": 0, "duration": 3600, "recurring": "weekly", "employee_multiplier": 0, "employee_salary": 0, "start_date": "2018-08-28T19:41:08Z"}
                 {"id": 8, "innovation": "Created library to eliminate need for 3rd party service", "cost": 10000, "duration": 0, "recurring": "once", "employee_multiplier": 0, "employee_salary": 0, "start_date": "2018-09-02T19:41:08Z"} 
