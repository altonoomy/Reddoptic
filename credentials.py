import praw
import json

with open('auth.json', "r") as authfile:
	creds = json.loads(authfile.read())

reddit = praw.Reddit(
	client_id = creds.get('ID'),
	client_secret = creds.get('SECRET'),
	password = 	creds.get('PASSWORD'),
	user_agent = creds.get('AGENT'),
	username = creds.get('USERNAME'),
	)


