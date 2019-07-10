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
parser.add_argument("-t", "--title", dest="title",
                    help="The title of the merge request", required=True)
parser.add_argument("-p", "--project", dest="project",
                    help="The project for which we want to create a MR", required=True)
args = parser.parse_args()

projectId = 'nkk%2F' + args.project
endpoint = 'http://' + args.servername + '/api/v4/projects/' + projectId + '/merge_requests'
header = { 'PRIVATE-TOKEN': args.token }
jsonData = {
    'id': projectId,
    'source_branch': args.sourcebranch,
    'target_branch': 'master',
    'title': args.title,
    'remove_source_branch': 'true'
}
response = requests.post(endpoint, json=jsonData, headers=header)
print(response.status_code)
print(response.json())
