import requests
import base64
from config import API_WORDPRESS, EMAIL_WORDPRESS, WEB_URL
from datetime import datetime
from GetTranscript import get_transcript

transcripts = get_transcript()
content = transcripts[1]
title = transcripts[2][6:]
print(title)

now = datetime.now()
date_string = now.strftime("%Y-%m-%dT%H:%M:%S")

username = EMAIL_WORDPRESS
password = API_WORDPRESS

creds = username + ":" + password
cred_token = base64.b64encode(creds.encode())

header = {'Authorization': 'Basic ' + cred_token.decode('utf-8')}

url = WEB_URL

post = {
 'title' : title,
 'content' : content,
 'status' : 'publish', 
 'categories': 7, 
 'date' : date_string
}

blog = requests.post(url + '/posts', headers = header, json = post)
print(blog)