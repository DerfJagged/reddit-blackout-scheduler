# Subreddit Blackout Tool
A Python script for sending blackout announcement posts and automatically setting subreddits to private (or back to public) for a blackout. Based on [reddit-post-scheduler by ibid-11962](https://github.com/ibid-11962/reddit-post-scheduler).

# Features
This app is designed to be run manually. 

- Takes in a list of subreddits specified in `variables.py`
- Asks you if you want to post an announcement to the subreddits, if you want to make them private (start blackout), or make them public (end blackout).
- Saves previous description, sets a temporary one, and reverts back when done
- Ability to set a custom message for the posts
- Options to sticky, distinguish, and lock the post (and its comment), and to set the suggested sort.

# Usage

## Setting up Reddit API Access

Go to your [app preferences](https://www.reddit.com/prefs/apps). Click the "Create app" or "Create another app" button. Fill out the form like so:

- **name:** BlackoutTool
- **App type:** Choose the **script** option
- **description:** A Python script for sending blackout announcement posts and automatically setting subreddits to private (or back to public) for a blackout.
- **about url:** [https://github.com/DerfJagged/subreddit-blackout-tool/](https://github.com/DerfJagged/subreddit-blackout-tool/)
- **redirect url:** http://localhost:8080

Hit the "create app" button. Make note of the client ID and client secret.

Edit the beginning of `variables.py` to include your username, password, client ID, and client secret.

## Configuring

Edit `variables.py` and change as necessary.

The following properties are required depending on the type of posts.

- `text` The body text. Required for all text posts. (but not for a title-only post)
- `link` The url of the link. Required for all link posts.

The following properties are optional strings.

- `flairid` The uuid of the flair you want to use.
- `flairtext` The text of the flair you want to use.
- `collectionid` The uuid of the collection you want to post to.

The following properties are also optional, but take booleans, not strings. These all default to False, so only include them if setting to True. Some need moderator permissions. 

- `dontnotify` Disable inbox notifications
- `lock` 
- `distinguish` 
- `sticky`

## Running from pythonanywhere

If you do not have a server to run the script on, you can use pythonanywhere to run it for free.

- Make an account at https://www.pythonanywhere.com
- Naigate to the "Files" page 
- Click "Upload a File", and upload `blackout.py` and `variables.py`.
- Click on "Open Bash console here" and wait for the console to finish initilizing.
- Type in `python3 -m pip install praw -U --user`.
- Type in `python3 blackout.py` to run the script.
