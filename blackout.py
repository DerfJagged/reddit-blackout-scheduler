#!/usr/bin/python3
import sys
import time

from praw.exceptions import APIException

from variables import subreddits
from variables import description
from variables import post
from variables import reddit

f = open("subreddit-blackout-tool.log", "a+")


###############################################################################
###############################################################################
###############################################################################

def submit_post(sub, title, text, link, image, video, parent, flair_id, flair_text, collection_id, sort, comment_text, spoiler, nsfw, lock, contest,
                dont_notify, distinguish, sticky, lock_comment, distinguish_comment, sticky_comment, wait):
    if not parent:
        try:
            if not image and not video:
                submission = reddit.subreddit(sub).submit(title, selftext=text, url=link, flair_id=flair_id, flair_text=flair_text,
                                                          send_replies=not dont_notify, nsfw=nsfw, spoiler=spoiler, collection_id=collection_id)
            else:
                if not video:
                    submission = reddit.subreddit(sub).submit_image(title, image_path=image, flair_id=flair_id, flair_text=flair_text,
                                                                    send_replies=not dont_notify, nsfw=nsfw, spoiler=spoiler,
                                                                    collection_id=collection_id)
                else:
                    submission = reddit.subreddit(sub).submit_video(title, video_path=video, thumbnail_path=image, flair_id=flair_id,
                                                                    flair_text=flair_text, send_replies=not dont_notify, nsfw=nsfw, spoiler=spoiler,
                                                                    collection_id=collection_id)

            f.write(f"\n\nPosted -- {to_link(submission.permalink)}")

        except APIException as e:
            if e.field == "ratelimit":
                if wait:
                    msg = e.message.lower()
                    index = msg.find("minute")
                    minutes = int(msg[index - 2]) + 1 if index != -1 else 1
                    f.write(f"\n\nRatelimit reached. Waiting {minutes} minutes before retrying.")
                    time.sleep(minutes * 60)
                    return 5
                else:
                    f.write(f"\n\nError posting submission -- {str(e)}")
        except Exception as e:
            f.write(f"\n\nError posting submission -- {str(e)}")
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
            if sort is not None:
                submission.mod.suggested_sort(sort)
                f.write(f"\nSet suggested sort to {sort}")
            print(f"{sub} - announcement posted!")
        except Exception as e:
            f.write(f"\n\nError attributing submission. (Are you a moderator?) -- {str(e)}")
    else:
        submission = reddit.comment(parent)
        try:
            submission.body
        except Exception:
            submission = reddit.submission(parent)

    if not comment_text:
        return 2

    try:
        comment = submission.reply(comment_text)
        f.write(f"\n\tCommented --  {to_link(comment.permalink)}")
    except Exception as e:
        f.write(f"\n\tError posting comment -- {str(e)}")
    try:
        if sticky_comment:
            comment.mod.distinguish(how='yes', sticky=True)
            f.write("\n\tDistinguished and Stickied")
        elif distinguish_comment:
            comment.mod.distinguish(how='yes')
            f.write("\n\tDistinguished")
        if lock_comment:
            comment.mod.lock()
            f.write("\n\tLocked")
    except Exception as e:
        f.write(f"\n\tError attributing comment. (Are you a moderator?) -- {str(e)}")
    return 0


def to_link(permalink):
    return f"https://reddit.com{permalink}"


def blackout(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    if subreddit.mod.settings()["subreddit_type"] != 'private':
        description_file = open(subreddit_name + "_saved_description.log", "a+")
        description_file.write("\n" + subreddit.mod.settings()['public_description'])
        description_file.close()

        new_settings = {
            'subreddit_type': 'private',
            'disable_contributor_requests': 'True',
            'public_description': '/r/' + subreddit_name + description
        }
        subreddit.mod.update(**new_settings)
        f.write("\n" + subreddit_name + " blackout started")
        print(f"{subreddit_name} blackout started")


def end_blackout(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    if subreddit.mod.settings()["subreddit_type"] == 'private':
        description_file = open(subreddit_name + "_saved_description.log", "r")
        saved_description = description_file.read()
        description_file.close()

        new_settings = {
            'subreddit_type': 'public',
            'disable_contributor_requests': 'True',
            'public_description': saved_description
        }
        subreddit.mod.update(**new_settings)
        f.write(f"\n{subreddit_name} blackout ended")
        print(f"{subreddit_name} blackout ended")


# Main
if __name__ == "__main__":
    f.write("\n---------------------\nStarted")
    response = None
    if len(sys.argv) > 1:
        response = str(sys.argv[1])

    if not response:
        response = input(
            "\n== Subreddit Blackout Tool ==\n\nEnter 'P' to post announcement\nEnter 'S' to start blackout (set subreddits to private)\nEnter 'E' to end blackout (set subreddits to public)\nEnter 'Q' to quit\n> ")

    response = response.lower()

    if response == 'p':
        print("")
        for i in range(len(subreddits)):
            postspecs = {"sub": "test", "title": "test", "text": "", "link": None, "image": None, "video": None, "parent": None, "flairid": None,
                         "flairtext": None, "collectionid": None, "sort": None, "commenttext": None, "spoiler": False, "nsfw": False, "lock": False,
                         "contest": False, "dontnotify": False, "distinguish": False, "sticky": False, "lockcomment": False,
                         "distinguishcomment": False, "stickycomment": False, "wait": False}
            postspecs.update(post)
            postspecs["sub"] = subreddits[i]
            postspecs["title"] = "/r/" + subreddits[i] + postspecs["title"]
            if postspecs["link"] != None:
                postspecs["text"] = None
            err = submit_post(sub=postspecs["sub"], title=postspecs["title"], text=postspecs["text"], link=postspecs["link"],
                              image=postspecs["image"], video=postspecs["video"], parent=postspecs["parent"], flair_id=postspecs["flairid"],
                              flair_text=postspecs["flairtext"], collection_id=postspecs["collectionid"], sort=postspecs["sort"],
                              comment_text=postspecs["commenttext"], spoiler=postspecs["spoiler"], nsfw=postspecs["nsfw"], lock=postspecs["lock"],
                              contest=postspecs["contest"], dont_notify=postspecs["dontnotify"], distinguish=postspecs["distinguish"],
                              sticky=postspecs["sticky"], lock_comment=postspecs["lockcomment"], distinguish_comment=postspecs["distinguishcomment"],
                              sticky_comment=postspecs["stickycomment"], wait=postspecs["wait"])
            if err == 5:
                submit_post(sub=postspecs["sub"], title=postspecs["title"], text=postspecs["text"], link=postspecs["link"], image=postspecs["image"],
                            video=postspecs["video"], parent=postspecs["parent"], flair_id=postspecs["flairid"], flair_text=postspecs["flairtext"],
                            collection_id=postspecs["collectionid"], sort=postspecs["sort"], comment_text=postspecs["commenttext"],
                            spoiler=postspecs["spoiler"], nsfw=postspecs["nsfw"], lock=postspecs["lock"], contest=postspecs["contest"],
                            dont_notify=postspecs["dontnotify"], distinguish=postspecs["distinguish"], sticky=postspecs["sticky"],
                            lock_comment=postspecs["lockcomment"], distinguish_comment=postspecs["distinguishcomment"],
                            sticky_comment=postspecs["stickycomment"], wait=postspecs["wait"])
    elif response == 's':
        print("")
        for i in range(len(subreddits)):
            if len(subreddits) >= 30:
                time.sleep(2)  # Avoid rate limit
            blackout(subreddits[i])
        print("Blackout started, thanks for participating!")
    elif response == 'e':
        print("")
        for i in range(len(subreddits)):
            if len(subreddits) >= 30:
                time.sleep(2)  # Avoid rate limit
            end_blackout(subreddits[i])
        print("Blackout ended, thanks for participating!")
    elif response == 'q':
        print("\nQuitting")
    else:
        print("\nInvalid response")

    f.write("\n\nFinished\n---------------------\n")
    f.close()
