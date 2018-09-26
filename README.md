# ROI Tracker

This a tool to track your successes over time and provide business reports.
It runs on AWS and can be deployed to run on your own account.

## Prerequisites

* [Python 3.6](https://www.python.org/downloads/)
* [Pipenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

##### Create a new virtualenv in the roi-tracker directory and activate it. Pipenv will output the virtualenv location.
```bash
cd roi-tracker
pipenv --python 3.6
pipenv shell
```
##### Install AWS CLI, AWS SAM CLI and Docker
```bash
pip install awscli
pip install aws-sam-cli
brew cask install docker
```
##### Create IAM user with the following permissions to deploy.

<details>
  <summary>Click to expand the policy</summary>

  ```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "NotAction": [
                "iam:*",
                "organizations:*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:CreateServiceLinkedRole",
                "iam:DeleteServiceLinkedRole",
                "iam:GetRole",
                "iam:ListRoles",
                "iam:CreateRole",
                "iam:PutRolePolicy",
                "iam:AttachRolePolicy",
                "iam:DetachRolePolicy",
                "iam:PassRole",
                "organizations:DescribeOrganization"
            ],
            "Resource": "*"
        }
    ]
}
```
</details>
<br />

#### Config access
To deploy to AWS, you need to provide an access and secret key.
In order to deploy as different users or to different accounts you can use profiles. In this example the profile is tracker, but it can be called anything.

```bash
~/.aws/config
[tracker]
region=us-east-1
output=json

~/.aws/credentials 
[tracker]
aws_access_key_id=$KEY
aws_secret_access_key=$SECRET

export AWS_PROFILE=tracker
```

#### Deploying

* Create an S3 bucket.

```bash
aws s3 mb s3://mbrenner-roi-tracker
```

* Package roi-tracker and send to bucket

```bash
sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket mbrenner-roi-tracker
```

* Create the Cloudformation stack.

```bash
sam deploy --template-file packaged.yaml --stack-name roi-tracker --capabilities CAPABILITY_IAM
```

### Using ROI Tracker

Now that your tracker is deployed. Time to add successes. 