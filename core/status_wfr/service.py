# -*- coding: utf-8 -*-

import boto3


def handler(event, context):
    arn = event['executionArn']
    # see if task is running and kill it
    client = boto3.client('stepfunctions', region_name='us-east-1')
    run_details = client.describe_execution(
            executionArn=arn
        )

    if run_details.get('startDate'):
        run_details['startDate'] = str(run_details['startDate'])
    if run_details.get('stopDate'):
        run_details['stopDate'] = str(run_details['stopDate'])
    return run_details

if __name__ == "__main__":
    handler({'executionArn': 'arn:aws:states:us-east-1:643366669028:execution:tibanna_pony-dev:test'}, 1)
