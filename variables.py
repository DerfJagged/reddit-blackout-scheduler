#Subreddits to post announcement to / blackout
subreddits = ['DerfJagged','DerfCSS']

#Temporary description users see when they visit during the blackout
description = ' is now private. Find out why we have gone dark: https://old.reddit.com/r/Save3rdPartyApps/comments/13yh0jf/dont_let_reddit_kill_3rd_party_apps/' 

#Announcement Post
post = {
  "title": " will go dark from June 12-14 in protest against Reddit API price changes",
  "link": "https://old.reddit.com/r/Save3rdPartyApps/comments/13yh0jf/dont_let_reddit_kill_3rd_party_apps/",
  "sticky": False,
  "distinguish": True,
  "lock": False
}

#Credentials
reddit = praw.Reddit(
	client_id='',          # From the app prefs page on reddit
	client_secret='',      # From the app prefs page on reddit
	password='',           # Password for account to use
	user_agent='blackout',
	username=''            # Username to perform action as - must be a moderator
)
