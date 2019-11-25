#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import textwrap


def get_args():
    description = textwrap.dedent('''
    Access roi tracker to view, create, modify and delete successes.
    Review reports of successes. 
    
    Examples: 
    
    Basic run to disburse to one or more locations:
        python scripts/test_disbursement.py -r 1
        python scripts/test_disbursement.py -r 1,16,2050

    To accept submitted status orders prior to running disbursement:
        python scripts/test_disbursement.py -r 1 --accept-orders

    To reschedule the disbursement time for location to a specific time (in UTC):
        python scripts/test_disbursement.py -r 1 -t '2016-11-18 00:00:00'
    ''')
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    return parser.parse_args()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #TODO: If adding, needs required fields.
    parser.add_argument('-a', '--add', help='Add a success.')
    parser.add_argument('-l', '--list', help='List all successes.')
    parser.add_argument('-r', '--report', help='Report of successes. Use start/end and interval for more options.')

    args = parser.parse_args()