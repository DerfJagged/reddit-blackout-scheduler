#!/usr/bin/python3
import praw
import time
from praw.exceptions import APIException

f = open("blackoutbot.log","a+")

#Credentials
reddit = praw.Reddit(
	client_id='',          # From the app prefs page on reddit
	client_secret='',      # From the app prefs page on reddit
	password='',           # Password for account
	user_agent='blackout',
	username=''            # Username to perform action as - must be a moderator
)

from variables import subreddits
from variables import description
from variables import posts

###############################################################################
###############################################################################
###############################################################################

def submit_post(sub, title, text, link, image, video, parent, flairid, flairtext, collectionid, sort, commenttext, spoiler, nsfw, lock, contest, dontnotify, distinguish, sticky, lockcomment, distinguishcomment, stickycomment, wait):
	if parent == None:
		try:
			if image == None and video == None:
				submission = reddit.subreddit(sub).submit(title, selftext=text, url=link, flair_id=flairid, flair_text=flairtext, send_replies=not(dontnotify), nsfw=nsfw, spoiler=spoiler, collection_id=collectionid)	
			else:
				if video == None:
					submission = reddit.subreddit(sub).submit_image(title, image_path=image, flair_id=flairid, flair_text=flairtext, send_replies=not(dontnotify), nsfw=nsfw, spoiler=spoiler, collection_id=collectionid)
				else:
					submission = reddit.subreddit(sub).submit_video(title, video_path=video, thumbnail_path=image, flair_id=flairid, flair_text=flairtext, send_replies=not(dontnotify), nsfw=nsfw, spoiler=spoiler, collection_id=collectionid)
					
			f.write("\n\nPosted --  "+ tolink(submission.permalink))
			
		except APIException as e:
			if e.field=="ratelimit":
				if wait==True:
					msg = e.message.lower()
					index=msg.find("minute")
					minutes = int(msg[index - 2]) + 1 if index != -1 else 1
					f.write("\n\nRatelimit reached. Waiting "+str(minutes)+" minutes before retrying.")
					time.sleep(minutes*60)
					return 5
				else:
					f.write("\n\nError posting submission -- "+str(e))
		except Exception as e:
			f.write("\n\nError posting submission -- "+str(e))
		try:
			if distinguish:
				submission.mod.distinguish()
				f.write("\nDistinguished")
			if sticky:
				submission.mod.sticky()
				f.write("\nStickied")
			if lock:
				submission.mod.lock()
				f.write("\nLocked")
			if contest:
				submission.mod.contest_mode()
				f.write("\nEnabled Contest Mode")
			if sort != None:
				submission.mod.suggested_sort(sort)
				f.write("\nSet suggested sort to "+sort)
		except Exception as e:
			f.write("\n\nError attributing submission. (Are you a moderator?) -- "+str(e))
	else:
		submission = reddit.comment(parent)
		try:
			submission.body
		except Exception as e:
			submission = reddit.submission(parent)
			
	if commenttext == None:
		return 2
		
	try:
		comment = submission.reply(commenttext)
		f.write("\n\tCommented --  "+ tolink(comment.permalink))
	except Exception as e:
		f.write("\n\tError posting comment -- "+str(e))
	try:
		if stickycomment:
			comment.mod.distinguish(how='yes', sticky=True)
			f.write("\n\tDistinguished and Stickied")
		elif distinguishcomment:
			comment.mod.distinguish(how='yes')
			f.write("\n\tDistinguished")
		if lockcomment:
			comment.mod.lock()
			f.write("\n\tLocked")
	except Exception as e:
		f.write("\n\tError attributing comment. (Are you a moderator?) -- "+str(e))
	return 0

def tolink(permalink):
	return "https://reddit.com" + permalink

def blackout(subreddit):
	if subreddit.mod.settings["subreddit_type"] != 'private':
		description_file = open(subreddit+"_saved_description.log","a+")
		description_file.write(subreddit.mod.settings['public_description'])
		description_file.close()
		
		new_settings = {
		'subreddit_type': 'private',
		'disable_contributor_requests': 'True',
		'public_description': '/r/' + subreddit + description
		}
		subreddit.mod.update(**new_settings)
		f.write(subreddit+" blackout started")
	
def end_blackout(subreddit):
	if subreddit.mod.settings["subreddit_type"] == 'private':
		description_file = open(subreddit+"_saved_description.log","a+")
		saved_description = description_file.read()
		description_file.close()
		
		new_settings = {
		'subreddit_type': 'public',
		'disable_contributor_requests': 'True',
		'public_description': saved_description
		}
		subreddit.mod.update(**new_settings)
		f.write(subreddit+" blackout ended")

#Main
if __name__ == "__main__":
	f.write("\n---------------------\nStarted")
	f.write(subreddits)
	print("Targeted subreddits: "+subreddits+"\n")
	response = input("Enter 'P' to post announcement\nEnter 'S' to start blackout (set subreddits to private).\nEnter 'E' to end blackout (set subreddits to public): ")
	
	if (response == 'P'):
		for post in posts:	
			postspecs = {"sub": "test", "title": "test", "text": "", "link": None, "image": None, "video": None, "parent": None, "flairid": None, "flairtext": None, "collectionid": None, "sort": None, "commenttext": None, "spoiler": False, "nsfw": False, "lock": False, "contest": False, "dontnotify": False, "distinguish": False, "sticky": False, "lockcomment": False, "distinguishcomment": False, "stickycomment": False, "wait": False}
			postspecs.update(post)
			if postspecs["link"] != None:
				postspecs["text"] = None
			err = submit_post(sub=postspecs["sub"], title=postspecs["title"], text=postspecs["text"], link=postspecs["link"], image=postspecs["image"], video=postspecs["video"], parent=postspecs["parent"], flairid=postspecs["flairid"], flairtext=postspecs["flairtext"], collectionid=postspecs["collectionid"], sort=postspecs["sort"], commenttext=postspecs["commenttext"], spoiler=postspecs["spoiler"], nsfw=postspecs["nsfw"], lock=postspecs["lock"], contest=postspecs["contest"], dontnotify=postspecs["dontnotify"], distinguish=postspecs["distinguish"], sticky=postspecs["sticky"], lockcomment=postspecs["lockcomment"], distinguishcomment=postspecs["distinguishcomment"], stickycomment=postspecs["stickycomment"], wait=postspecs["wait"])
			if err == 5:
				submit_post(sub=postspecs["sub"], title=postspecs["title"], text=postspecs["text"], link=postspecs["link"], image=postspecs["image"], video=postspecs["video"], parent=postspecs["parent"], flairid=postspecs["flairid"], flairtext=postspecs["flairtext"], collectionid=postspecs["collectionid"], sort=postspecs["sort"], commenttext=postspecs["commenttext"], spoiler=postspecs["spoiler"], nsfw=postspecs["nsfw"], lock=postspecs["lock"], contest=postspecs["contest"], dontnotify=postspecs["dontnotify"], distinguish=postspecs["distinguish"], sticky=postspecs["sticky"], lockcomment=postspecs["lockcomment"], distinguishcomment=postspecs["distinguishcomment"], stickycomment=postspecs["stickycomment"], wait=postspecs["wait"])
	elif (response == 'S'):
		for i in range(len(subreddits)):
			if (len(subreddits) >= 30):
				time.sleep(2) # Avoid rate limit
			subreddit = reddit.subreddit(subreddits[i])
			blackout(subreddit)
	elif (response == 'E'):
		for i in range(len(subreddits)):
			if (len(subreddits) >= 30):
				time.sleep(2) # Avoid rate limit
			subreddit = reddit.subreddit(subreddits[i])
			end_blackout(subreddit)
	
	f.write("\n\nFinished\n---------------------\n")
	f.close()
