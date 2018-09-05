#!/usr/bin/env bash

#aws cloudformation delete-stack --stack-name roi-tracker
#sleep 45
sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket mbrenner-roi-tracker
sam deploy --template-file packaged.yaml --stack-name roi-tracker --capabilities CAPABILITY_IAM
rm logs
aws cloudformation describe-stack-events --stack-name roi-tracker >> logs