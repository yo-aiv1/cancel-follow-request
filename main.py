import json
import argparse
from instagrapi import Client
from instagrapi.exceptions import LoginRequired 
import sys
import os
import time


if len(sys.argv) != 7:
    print("Usage: python main.py -u <username> -p <password> -f <path to the json file>")
    sys.exit()

parser = argparse.ArgumentParser(description='Script description')

parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password')
parser.add_argument('-f', '--file', help='Path to the json file.')
args = parser.parse_args()


api = Client()

def LoadOldData():
    AlreadyUnfollowed = []
    if os.path.exists("done.txt"):
        with open('done.txt', 'r', encoding='utf-8') as f:
            data = f.readlines()
            for username in data:
                AlreadyUnfollowed.append(username[:-1])
    return AlreadyUnfollowed

def Login(cl: Client, USERNAME: str, PASSWORD: str):
    session = cl.load_settings("session.json") if os.path.exists("session.json") else None

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)

            try:
                cl.get_timeline_feed()
            except LoginRequired:
                print(f"[+]-> Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(USERNAME, PASSWORD)
            login_via_session = True
        except Exception as e:
            print(f"[+]-> Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            print(f"[+]-> Attempting to login via username and password. username: %s" % USERNAME)
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
        except Exception as e:
            print(f"[+]-> Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        print(f"[+]-> Couldn't login user with either password or session")
        sys.exit()

def Unfollow(username):
    user_id = api.user_id_from_username(username)
    if api.user_unfollow(user_id):
        with open('done.txt', 'a', encoding='utf-8') as f:
            f.write(username + "\n")
        print(f"[+]-> {username} unfollowed successfully.")
    else:
        print(f"[+]-> an error has occurred.")
        sys.exit()

def ExtractUsernames(filepath):
    OldData = LoadOldData()
    with open(filepath, 'r') as f:
        data = json.loads(f.read())
# i can use the below code but in case the key's names were different it wont work:
#        for line in data["relationships_follow_requests_sent"]:
#            username = line["string_list_data"][0]["value"]
# thats why i used method below:
        for line in data[next(iter(data))]:
            username = line[list(line)[2]][0][list(line[list(line)[2]][0])[1]]
            if username not in OldData:
                Unfollow(username)
                time.sleep(2)
            else:
                print(f"[+]-> {username} already unfollowed")

if __name__ == "__main__":
    Login(api, args.username, args.password)
    api.dump_settings("session.json")
    ExtractUsernames(args.file)