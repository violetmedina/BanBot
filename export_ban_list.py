import praw
import config
import time


# Logging in
def bot_login():
    print("Logging in...")
    reddit = praw.Reddit(client_id=config.client_id,
                        client_secret=config.client_secret,
                        password=config.password,
                        user_agent='Ban Bot v1 by u/reddit_user',
                        username=config.username)
    print("Logged in!")
    time.sleep(2)
    return reddit


def main():
    reddit = bot_login()
    run_bot(reddit)


def run_bot(reddit):
    # print("Searching subreddit...")
    for ban in reddit.subreddit("[enter name of subreddit where list of banned user will come from]").banned(limit=9999):
        with open("banned_users_export.txt", "r") as a:
            banned_list = a.read()
            banned_list = banned_list.split("\n")

        with open("banned_users_export.txt", "a") as b:
            if ban not in banned_list:
                print(f"{ban}: {ban.id}")
                b.write(f"{ban}" + "\n")

        print("Done!")


if __name__ == '__main__':
    main()
