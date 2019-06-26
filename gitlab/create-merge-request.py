#!/usr/bin/env python3

from argparse import ArgumentParser
import requests

parser = ArgumentParser()
parser.add_argument("-s", "--gitlab-server", dest="servername",
                    help="e.g. example.gitlab.com", required=True)
parser.add_argument("-b", "--source-branch", dest="sourcebranch",
                    help="The branch to create a merge request from", required=True)
parser.add_argument("-a", "--auth-token", dest="token",
                    help="The personal access token for Gitlab", required=True)
parser.add_argument("-t", "--title", dest="token",
                    help="The title of the merge request", required=True)
args = parser.parse_args()

response = requests.get(
    'https://' + args.servername + '/api/v4/merge_requests')
