#main.py
import props
import requests
import json

url = "https://"+props.hostname+"/rest/api/1.0/repos?limit="+props.limit
headers = {
    'Authorization': 'Basic ' + props.auth_token
}

#get all bitbucket repos
response = requests.request("GET", url, headers=headers)
repos = response.json()['values']

#will store repo info here
sizes = []

for repo in repos:
    repoName = repo['name']
    #grab the repo url and build the url to get repo size
    repoURL = repo['links']['self'][0]['href'].replace('/browse', '/sizes')
    #get repo size
    response = requests.request("GET", repoURL, headers=headers).json()
    #convert size to MB
    repoSize = (response['repository'] + response['attachments']) / 1024 / 1024
    newRepo = {
        "name": repoName,
        "url": repo['links']['self'][0]['href'],
        "size": round(repoSize,2)
    }
    #add new repo to array
    sizes.append(newRepo)

#sort repos by size
sizes = sorted(sizes,key=lambda x : x['size'],reverse=True)
print("repos: " + str(len(sizes)))

with open('repos.json','w') as outfile:
  json.dump(sizes,outfile,indent=4)