#!/usr/bin/python

'''
This script creates a list with all the repos within a github organization and the attribute Private.
Useful if your organization has a bunch of repos and you want to list them. 
In my case, I was interested on the private attribute because our billing plan has a limitation per number of private repos.
It will return an exception after the last one but the list will be generated anyway. I still need to fix it.
'''
import sys
import requests
import json

listado = list()
repo_counter = 0
private_counter = 0
# User to input the organization name
orgname = raw_input("Introduce your organization's name: (Case sensitive) \n")
if len(orgname) == 0 :
	print "Error: This is not a Github organization name.\n"
	exit()

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

#You can gather up to 100 repos per page/API call.
repos = input("How many repos per page do you want to gather? (Max=100 & Default=100)\n")
if not repos in range(0, 100):
	repos = 100
else:
	pass
#Each page means 1 API call.
lastpage = input("How many pages you want to display? (Default is 1).\n")
if not lastpage in range(0, 10):
	lastpage = 1
else:
	pass

with open(token_path) as file:
	token = file.read()
results_file = open(results_path, "a")
 
for page in range(1, lastpage+1):
	#print "\nThere are a total of " + str(repo_counter) + ", and " + str(private_counter) + " of them are Private.\n"
	api_call= "https://api.github.com/orgs/" + orgname + "/repos?per_page=" + str(repos) + "&page=" + str(page) + "&access_token=" + token
	response = requests.get(api_call)
	print(response.url)
	#print "API Call Status code " + str(response.status_code)
	if response.status_code != 200 :
		exit()
	else: 
		
		data = json.loads(response.text)
		for repo in range(1, repos):
			if len(data[repo]['full_name']) == 0 :
				break
			else:
				pass
			#This gets the attribute full name and removes the Org part (orgname/)from it
			name = data[repo]['full_name']
			organization = orgname + "/"

			#This writes if the repo is private or public by checking the private attribute given in the response
			if data[repo]['private'] is True :
				priv = "Private"
			else:
				priv = "Public"
			info = name.replace(organization, "") + " is " + str(priv) + "\n"
			results_file.write(info)
			repo_counter = repo_counter+1
			if priv == True :
				private_counter = private_counter+1

results_file.close()
