#/usr/bin/env python3
# TODO:
# - Need to make sure we don't keep saying "you're prime!" when we've already told the user
#   ex. I just passed 400 users, and my 401st follower was already notified, I gained followers
#   and then lost some, and now back to 401, and the bot said thank you again.
# - Need to keep track of how many followers they had when we notified them, and then count
#   how many since we last notified them.

import tweepy
import logging
import json
from config import create_api
# from playing import playtime
import time

def is_prime(a):
    # this function determines if the number you provided is prime or not
    # TODO: Eat catfood
    for i in range(2,a):
        if a%i==0:
            return False

    return True


def check_user(api, users):
    # this will check a user's follower count and determine if it is a prime number or not
    print(f"Going to loop through these users:\n{users}")
    for username in users:
        print("-" * 30)
        try:
            # get information about the user
            user = api.get_user(username)

            # get the follower account
            user_fc = user.followers_count

            follower_diff = user_fc - users[username]
            print(f"User details:\t@{username}\nFollowers:\t{user_fc} (diff:{follower_diff})")

            # update the follower account for the user, but only if the follower
            # count that we know about is less than their current follower count
            if users[username] < user_fc:
                users[username] = user_fc

            # save our user dictionary
            save_users(users)



            # if the follower account is prime
            if is_prime(user_fc):

                # if the follower count is greater than what we already know
                if user_fc > users[username]:
                    # get the last user who followed our user
                    last_follower = user.followers()
                    print("Prime:\tYes")
                    # print('Last follower:', last_follower[0].name,'@%s' % last_follower[0].screen_name)
                    print(f"Last follower:\t{last_follower[0].name} - @{last_follower[0].screen_name}")

                    # craft the tweet
                    message = f"Hey @{username}! Your follower count is a PRIME number ({user_fc})!\nYour latest follower is @{last_follower[0].screen_name}\n\nI'm a bot.\n Reply with !primefollower followed by either:\n addme  to be notifed too.\n stop   to stop notification."

                    try:
                        # send the tweet
                        api.update_status(message)

                        print("Notified:\tTweet Sent")
                    except tweepy.TweepError:
                        print(e)
                        # there was probably an error
                        print("[ERROR] Problem sending notification tweet!!!")
                else:
                    print(f"Prime:\t\tYes\nNotified:\tYes")
                # save_already_notified(notifications)
                users[username] = user_fc

            else:
                print(f"Prime:\t\tNo")

        except:
            print(f"[ERROR] User {username} not found...")


def check_mentions(api, users):
    # this checks to see if anyone has mentioned our trigger word
    # and if so, check to see if it's a bot command or not

    # grab the tweets we know about
    known_tweets = load_known_tweets()
    # print(f"Loaded these->{known_tweets}")
    print('Checking to see if anyone mentions !primefollower\n')

    # cycle through all the tweets that twitter returns for us, looking for mentions and commands
    for tweet in api.search(q="!primefollower", rpp=100, tweet_mode='extended'):  # limits to 100, commented out to get all
        # who said it
        tweet_user = tweet.user.screen_name

        # tweet ID
        tweet_id = tweet.id

        # check to see if we've already seen this tweet
        if tweet_id not in known_tweets:
            print(f"Have not seen this tweet before.\n{tweet_id}")
            print(f"{tweet_user} said:\n{tweet.full_text}")
            bot_command = str(tweet.full_text).split()

            # cycle through the tweet, looking for !primefollower and the word that follows it
            for idx, a in enumerate(bot_command):

                if a == "!primefollower" and idx < len(bot_command):

                    # the bot saw that it was invoked, and need to check the next input.
                    command = bot_command[idx+1]

                    print(f'  Bot command ({command})received from {tweet_user}')
                    if command == "addme":
                        print(f'  Bot instructed to add {tweet_user}\n')
                        if tweet_user not in users:
                            #users.append(tweet_user)
                            users[tweet_user] = 0
                            save_users(users)

                            # reply to their tweet
                            message = f"Done @{tweet_user}! I'll monitor your follower count and let you know when it's prime.\nDoot Doot: Mr_Hobbits is not a bot, but his bot replied on his behalf."
                            api.update_status(message, in_reply_to_status_id=tweet_id)
                        else:
                            print(f"  User {tweet_user} is already being monitored")

                    elif command == "stop":
                        print('  Bot instructed to stop monitoring %s\n' % tweet_user)

                        message = "Done @" + tweet_user + "! I have removed you from my monitoring queue. Thank you for using me!\nDoot Doot: Mr_Hobbits is not a bot, but his bot replied to this."

                        try:
                            api.update_status(message, in_reply_to_status_id=tweet_id)
                        except Exception as e:
                            if e.api_code == 187:
                                print("[ERROR] Tweet notifying user we're going to stop is a duplicate.")

                        #users.remove(tweet_user)
                        del users[tweet_user]
                        save_users(users)

                    else:
                        print('  Invalid bot command. Bot command not found\n')

            # add tweet to known tweets
            known_tweets.append(tweet_id)

            # save it
            save_known_tweets(known_tweets)


    return True

def load_users():
    # this will load the usernames we need to check for follower counts
    with open('users.log', 'r') as f:
        return json.load(f)

def save_users(users):
    # this will save our list of users
    with open('users.log', 'w') as f:
        json.dump(users, f)

def load_known_tweets():
    # this will load tweets from our logfile into 'known tweets'
    with open('tweets.log', 'r') as f:
        return json.load(f)

def save_known_tweets(known_tweets):
    # this will save the tweets we know about into a logfile as JSON
    with open('tweets.log', 'w') as f:
        json.dump(known_tweets, f)

def load_already_notified():
    with open('notified.log','r') as f:
        return json.load(f)

def save_already_notified(notifications):
    with open('notified.log','w') as f:
        json.dump(notifications, f)

def main():
    # playground
    #playtime()

    # used to stop the app
    #return True
    print("-" * 50)
    print("\n\nScript started:", time.asctime(time.localtime(time.time())),"\n")


    print("Authenticating to Twitter API...")
    try:
        api = create_api()
        print("Authentication OK")

    except:
        print("Something went wrong authenticating you.")

    try:
        # load users
        users = load_users()


        # playtime after authentication!
        #playtime()
        #return True

        # send a test message
        # api.update_status("Testing the bot, disregard.")

        # run actual bot functions
        if check_mentions(api, users):
            print("Mention check complete.\n\n")

        if check_user(api, users):
            print("User check complete.\n\n")
    except tweepy.TweepError as e:
        with open('bot_logging.log', 'w') as f:
            json.dump(e, f)
    except Exception as e:
        with open('bot_logging.log', 'w') as f:
            json.dump(e, f)

        pass
        #if e.api_code == 187:
        #    print("[ERROR] We already tweeted this (duplicate)")
        #else:
        #    print(e)



    print("\nBot Run Complete.\n")


if __name__ == "__main__":
    main()
