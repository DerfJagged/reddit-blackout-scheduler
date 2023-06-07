# Subreddit Blackout Tool
# WIP - IN TESTING, DO NOT USE
A Python script for sending blackout announcement posts and automatically setting subreddits to private (or back to public) for a blackout. Based on [reddit-post-scheduler](https://github.com/ibid-11962/reddit-post-scheduler).

# Features

- Ability to set a custom message for the posts
- Saves previous description, sets a temporary one, and reverts back when done
- Options to sticky, distinguish, and lock the post (and its comment), and to set the suggested sort.

# Setup

Go to your [app preferences](https://www.reddit.com/prefs/apps). Click the "Create app" or "Create another app" button. Fill out the form like so:

- **name:** BlackoutTool
- **App type:** Choose the **script** option
- **description:** A Python script for sending blackout announcement posts and automatically setting subreddits to private (or back to public) for a blackout.
- **about url:** [https://github.com/ibid-11962/reddit-post-scheduler](https://github.com/DerfJagged/reddit-blackout-scheduler/)
- **redirect url:** http://localhost:8080

Hit the "create app" button. Make note of the client ID and client secret.

Edit the beginning of `variables.py` to include your username, password, client ID, and client secret.

# Using for a Blackout

This app is designed to be scheduled to run on the day you wish to post an announcement and the day you'd like to toggle the subreddit to private or public.

Any posts that you would like to schedule should go in `variables.py`. The format is pretty straightfoward and some examples are already there.

The following properties are required depending on the type of posts.

- `date` The date you want the post to go up on. Needs to be in "M,D" format. Required for all posts and comments. 
- `text` The body text. Required for all text posts. (but not for a title-only post)
- `link` The url of the link. Required for all link posts.

The following properties are optional strings. (some need moderator permissions)

- `flairid` The uuid of the flair you want to use.
- `flairtext` The text of the flair you want to use.
- `collectionid` The uuid of the collection you want to post to.

The following properties are also optional, but take booleans, not strings. These all default to False, so only include them if setting to True. Some need moderator permissions. 

- `dontnotify` Disable inbox notifications
- `lock` 
- `distinguish` 
- `sticky` 
- `stickycomment`
- `wait` If the ratelimit is reached, wait the ten minutes and try again.

# Setting this up with pythonanywhere

If you do not have a server, this can be set up for free on pythonanwhere. It meets their daily limits. 

- Make an account at https://www.pythonanywhere.com
- Naigate to the "Files" page 
- Click "Upload a File", and upload `blackout.py` and `variables.py`.
- Click on "Open Bash console here" and wait for the console to finish initilizing.
- Type in `python3 -m pip install praw -U --user`.
- Navigate to the tasks page.
- Start a new daily task with the command `python3 blackout.py` set to run at the time that you want your stuff to post. (Note that the server time listed on the page may be different from your own time.)
