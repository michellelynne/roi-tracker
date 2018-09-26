#!/usr/bin/env bash

sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket mbrenner-roi-tracker
sam deploy --template-file packaged.yaml --stack-name roi-tracker --capabilities CAPABILITY_IAM
