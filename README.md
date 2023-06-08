# Subreddit Blackout Tool
A Python script for sending blackout announcement posts and setting subreddits to private (or back to public) for a blackout. Useful if you moderate many subreddits.

Based on [reddit-post-scheduler by ibid-11962](https://github.com/ibid-11962/reddit-post-scheduler) and [PotRoastPotato's comment](https://www.reddit.com/r/ModCoord/comments/142rzna/a_bot_to_make_your_subreddit_private/jn7p4cc/).


![image](https://github.com/DerfJagged/subreddit-blackout-tool/assets/24844708/9fa40265-5634-4e1c-9f8e-35f6df30e344)

## Features
This app is designed to be run manually or scheduled using pythonanywhere (instructions below) or a cronjob.

- Takes in a list of subreddits specified in `variables.py`.
- Saves previous description, sets a temporary one, and reverts back when done.
- Ability to set a custom message for the posts.
- Options to sticky, distinguish, and lock the post (and its comment), and to set the suggested sort.

## Usage

### Setting up Reddit API Access

Go to your [app preferences](https://www.reddit.com/prefs/apps). Click the "Create app" or "Create another app" button. Fill out the form like so:

- **name:** BlackoutTool
- **App type:** Choose the **script** option
- **description:** A Python script for sending blackout announcement posts and automatically setting subreddits to private (or back to public) for a blackout.
- **about url:** [https://github.com/DerfJagged/subreddit-blackout-tool/](https://github.com/DerfJagged/subreddit-blackout-tool/)
- **redirect url:** http://localhost:8080

Hit the "create app" button. Make note of the client ID (under "personal use script") and client secret ("secret").

### Configuring

Edit `variables.py` to include your username, password, client ID, client secret, and subreddits to target. Optionally, set up another account and make it a developer and a moderator of the desired subreddits if you don't want to use your own account - though it runs the risk of the reddit site filter removing posts from new accounts. From a fresh copy, the only thing you MUST change is the subreddits being targeted.

The following properties are required depending on the type of posts:

- `subreddits` Subreddits to target.
- `title` Title of the post. Your subreddit name will be added to the front of it.
- `text` The body text. Required for all text-only posts (but not for link-only posts).
- `link` The url of the link. Required for all link-only posts (but not for text-only posts).

The following properties are optional:

- `dontnotify` Disable inbox notifications.
- `lock`  Lock post.
- `distinguish` Distinguish post.
- `sticky` Sticky post.
- `flairid` The uuid of the flair you want to use (string).
- `flairtext` The text of the flair you want to use (string).
- `collectionid` The uuid of the collection you want to post to (string).

## Running from pythonanywhere

If you do not have a server to run the script on, you can use pythonanywhere to run it for free.

- Make an account at https://www.pythonanywhere.com
- Naigate to the "Files" page.
- Click "Upload a File", and upload `blackout.py` and `variables.py`.
- Click on "Open Bash console here" and wait for the console to finish initilizing.
- Type in `python3 -m pip install praw -U --user`.
- Type in `python3 blackout.py` to run the script.
- OPTIONAL: Go back to Dashboard page, click "Tasks" button, and schedule a task to run the script at a certain time (UTC) and automatically execute a command with the following:
      python3 /home/Derf/blackout.py p
      OR
      python3 /home/Derf/blackout.py s
      OR
      python3 /home/Derf/blackout.py e

### Troubleshooting

Announcement posts were removed: Approve them manually. This is likely the reddit spam filter taking it down because of too much action or a new account.

*Disclaimer: I created this tool for myself because I moderate 100+ subreddits and I'm lazy. I am not liable if something goes wrong. Protest responsibly!*
