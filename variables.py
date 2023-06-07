subreddits = ['DerfJagged','DerfCSS']
description = ' [is now private. Click here to find out why we have gone dark](https://old.reddit.com/r/Save3rdPartyApps/comments/13yh0jf/dont_let_reddit_kill_3rd_party_apps/)' 
post = [
{
  "title": " will go dark from 12-14 June in protest against Reddit API price changes",
  "link": "https://old.reddit.com/r/Save3rdPartyApps/comments/13yh0jf/dont_let_reddit_kill_3rd_party_apps/",
  "sticky": False,
  "distinguish": True
}
]
#Credentials
reddit = praw.Reddit(
	client_id='',          # From the app prefs page on reddit
	client_secret='',      # From the app prefs page on reddit
	password='',           # Password for account
	user_agent='blackout',
	username=''            # Username to perform action as - must be a moderator
)
