#!/usr/bin/python

'''
This script creates a list with all the repos within a github organization and the attribute Private.
Useful if your organization has a bunch of repos and you want to list them. 
In my case, I was interested on the private attribute because our billing plan has a limitation per number of private repos.
It will make just the required api calls to gather all repos.
'''
import sys
import requests
import json
import argparse

repos = 100
lastpage = 50
repo_counter = 0
# User to input the organization name
'''orgname = raw_input("Introduce your organization's name: (Case sensitive) \n")
if len(orgname) == 0 :
	print "Error: This is not a Github organization name.\n"
	exit()
'''
parser = argparse.ArgumentParser(description='Introducing the Github organization name')
parser.add_argument('--org', nargs=1,  help='Introduce your Github organizations name')
args = parser.parse_args()
orgname = args.org[0]

#User to define where to export the repos list
results_path = raw_input("Where do you want to export the repos list? (Introduce the path):\n")
if len(results_path) == 0 :
	results_path = ("/tmp/results_repos.txt")
else:
	pass

print "Your file will be stored in " + results_path + " \n"

#User to define where the github access token file is located
token_path = raw_input("Where is your Git access token located? (Introduce the path):\n")
if len(token_path) == 0 :
	token_path = ("/Users/carto/token1")
else:
	pass

with open(token_path) as file:
	token = file.read()
results_file = open(results_path, "a+")
 
for page in range(1, lastpage+1):
	
	api_call= "https://api.github.com/orgs/" + orgname + "/repos?per_page=" + str(repos) + "&page=" + str(page) + "&access_token=" + token
	response = requests.get(api_call)
	response_data = json.loads(response.text)
	print(response.url)
	# If we get a response code different than 200, exit
	if response.status_code != 200 :
		exit()
	else: 
		# Convert response data into a list
		repos_per_response = len(response_data)
		repo_counter_per_response = 0

		for repo in range(0, repos_per_response):
			#This gets the attribute full name and removes the Org part (orgname/)from it
			name = response_data[repo]['full_name']
			organization = orgname + "/"
			info = name.replace(organization, "")
			results_file.write(info + "\n")
			repo_counter = repo_counter+1
			repo_counter_per_response = repo_counter_per_response+1
			while (repo_counter_per_response != 100 and repo_counter_per_response == repos_per_response) :
				print "Total number of repos: " + str(repo_counter) + "\n" + str(repo_counter_per_response)
				results_file.close()
				exit()

