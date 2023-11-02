import sys

import requests
import argparse
import os
from _datetime import datetime, timezone
from tabulate import tabulate
from dateutil.parser import parse
import re

DOCKERHUB_BASE = "https://hub.docker.com"
SEMVER_PATTERN = re.compile(r"^v?\d+\.\d+\.\d+$")

def headers(token):
  return {
    "Authorization": f"JWT {token}"
  }

def should_delete(last_pulled, last_pushed, max_days):
    age = tag_age(last_pulled, last_pushed)
    return age > max_days


def tag_age(last_pulled, last_pushed):
  last_pushed_days = days_since(parse(last_pushed))
  if last_pulled is None:
    return last_pushed_days
  else:
    last_pulled_days = days_since(parse(last_pulled))
    return min(last_pulled_days, last_pushed_days)


def days_since(time):
  today = datetime.now(timezone.utc)
  duration = today - time
  days = duration.days
  return days


def get_token(user, password):
  print(f"Getting token for user '{user}'")
  resp = requests.post(f"{DOCKERHUB_BASE}/v2/users/login/",
                       json={'username': user, 'password': password},
                       headers={'Content-Type': 'application/json'})
  if (resp.status_code != 200):
    raise f"Invalid credentials supplied. Service responded with {resp.status_code}"

  print("Token received")

  return resp.json()["token"]


def get_tags(token, repo):
  url = f"{DOCKERHUB_BASE}/v2/repositories/{repo}/tags/?page_size=100"
  resp = requests.get(url, headers=headers(token))
  json = resp.json()
  tags = json['results']

  while json.get('next') is not None:
    next = json['next']
    resp = requests.get(next, headers=headers(token))
    json = resp.json()
    tags.extend(json['results'])
  return tags


def is_semver(tag):
  return bool(SEMVER_PATTERN.match(tag))

def prune():
  parser = argparse.ArgumentParser()
  parser.add_argument('-u', '--user',
                      required=True,
                      help='The user to log into the service'
                      )

  parser.add_argument('-r', '--repo',
                      required=True,
                      help='The repository to check for images to delete'
                      )

  parser.add_argument('-d', '--days',
                      required=False,
                      default=180,
                      type=int,
                      help='How many days an images can stay without pull before it is deleted'
                      )

  parser.add_argument('-a', '--activate',
                      action='store_true',
                      help='Do the actual deletion rather than just a dry run'
                      )

  parser.add_argument('--keep-semver',
                      required=False,
                      default=True,
                      type=bool,
                      help='Should tags that are a sematic version (MAJOR.MINOR.PATCH) also be deleted or kept'
                      )

  args = parser.parse_args()

  pw = os.environ["CONTAINER_REGISTRY_PASSWORD"]
  repo = args.repo
  days = args.days

  token = get_token(args.user, pw)

  tags = get_tags(token, repo)
  tags_to_delete = []

  table = [["Tag", "Last pushed", "Last pulled", "Last activity (days ago)", "To be deleted"]]
  for tag in tags:
    last_pushed = tag['tag_last_pushed']
    last_pulled = tag['tag_last_pulled']

    delete = should_delete(last_pulled, last_pushed, days)
    if(args.keep_semver):
      delete = not is_semver(tag['name'])

    age = tag_age(last_pulled, last_pushed)
    row = [tag['name'], last_pushed, last_pulled, age, delete]
    table.append(row)
    if delete:
      tags_to_delete.append(tag['name'])

  print("")
  print(f"Checking repo {repo} on {DOCKERHUB_BASE} for tags that haven't been pulled in the last {days} days")
  print("")
  print(tabulate(table, headers="firstrow"))

  if args.activate:

    for tag in tags_to_delete:

      url = f"{DOCKERHUB_BASE}/v2/repositories/{repo}/tags/{tag}"
      print(f"Deleting tag {tag}")
      resp = requests.delete(url, headers=headers(token))

      if resp.status_code != 204:
        print(resp)
        raise "error"

  else:
    print("Not deleting anything. Use --activate to force actual deletion.")

if __name__ == "__main__":
    prune()
