import praw
import config
import time
import datetime


# Logging in
def bot_login():
    print("Authenticating...")
    reddit = praw.Reddit(client_id=config.client_id,
                        client_secret=config.client_secret,
                        password=config.password,
                        user_agent="Ban Bot v1 by u/reddit_user",
                        username=config.username)
    print("Logged in!")
    return reddit


def main():
    reddit = bot_login()
    while True:
        run_bot(reddit)


def run_bot(reddit):
    subreddit = reddit.subreddit("[enter name of subreddit where bans will happen here]")
    if not subreddit.user_is_moderator:
        print("You are not a moderator of this subreddit. Please login as a moderator")
    # open and read existing file
    # Reading file of existing banned users to compare
    with open("user_list.txt", "r") as r:
        user_list = r.read()
        user_list = user_list.split("\n")
    print("Defining subreddits...")
    with open("banned_sub.txt", "r") as b:
        banned_sub = b.read()
        banned_sub = banned_sub.split("\n")
        for i, v in enumerate(banned_sub):
            submissions = reddit.subreddit(str(v)).new(limit=10)
            comments = reddit.subreddit(str(v)).comments(limit=100)
            # search posts/comments function
            search_subs = f"SEARCHING POSTS IN /r/{v}..."
            print(search_subs)
            for submission in submissions:
                sub_name = submission.author
                if not submission.author:
                    continue

                if sub_name not in user_list:
                    user_list.append(submission.author)
                    # Ban Happens Here
                    subreddit.banned.add(str(sub_name), ban_reason="Rule 4. Account History - r/" + v,
                                        ban_message="You have been banned for Violation of Rule 4. Account History")
                    subreddit.muted.add(sub_name)
                    with open("user_list.txt", "a") as w:
                        w.write(str(submission.author) + "\n")
                        print(str(sub_name) + " banned for POSTING in r/" + str(v))
                        w.close()
                        time.sleep(1)

            print("SEARCHING COMMENTS IN /r/" + str(v) + "...")
            for comment in comments:
                com_name = comment.author
                if not comment.author:
                    continue
                if com_name not in user_list:
                    user_list.append(comment.author)
                    subreddit.banned.add(str(com_name), ban_reason="Rule 4. Account History - r/" + v,
                                        ban_message="You have been banned for Violation of Rule 4. Account History")
                    subreddit.muted.add(com_name)
                    with open("user_list.txt", "a") as wc:
                        wc.write(str(comment.author) + "\n")
                        print(str(com_name) + " banned for COMMENTING in r/" + str(v))
                        wc.close()
                        time.sleep(1)
    now = datetime.datetime.now()
    print("Done Scanning At " + now.strftime("%Y-%m-%d %H:%M \n\n"))
    time.sleep(14400)

if __name__ == "__main__":
    main()
