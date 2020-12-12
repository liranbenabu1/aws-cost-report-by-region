#!/usr/bin/env python3

import argparse
import boto3
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--days', type=int, default=30)
parser.add_argument('--region', type=str, default="us-east-1")
args = parser.parse_args()
# set start and end date according the argument days.
now = datetime.datetime.utcnow()
start = (now - datetime.timedelta(days=args.days)).strftime('%Y-%m-%d')
end = now.strftime('%Y-%m-%d')
# create session to aws
session = boto3.session.Session(profile_name='default')
cd = session.client('ce', args.region)
results = []

token = None
while True:
    kwargs = {}
    if token:
        kwargs = {'NextPageToken': token}
    data = cd.get_cost_and_usage(
      TimePeriod={
        'Start': start, 'End':  end
        },
      Granularity='DAILY',
      Metrics=['UnblendedCost'],
      GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}], **kwargs)

    results += data['ResultsByTime']
    token = data.get('NextPageToken')
    if not token:
        break

print('\t'.join([ 'LinkedAccount', 'Service', 'Amount', 'Unit', 'Estimated']))
for result_by_time in results:
    for group in result_by_time['Groups']:
        amount = group['Metrics']['UnblendedCost']['Amount']
        unit = group['Metrics']['UnblendedCost']['Unit']
        print('\t'.join(group['Keys']), '\t', amount, '\t', unit, '\t', result_by_time['Estimated'])