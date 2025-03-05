import json
import argparse
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, TwoFactorRequired
import sys
import os
import time
import random

if len(sys.argv) < 7:
    print("Usage: python main.py -u <username> -p <password> -f <path to the json file> [-2 <2fa_code>]")
    sys.exit()

parser = argparse.ArgumentParser(description='Script description')

parser.add_argument('-u', '--username', help='username', required=True)
parser.add_argument('-p', '--password', help='password', required=True)
parser.add_argument('-f', '--file', help='Path to the json file.', required=True)
parser.add_argument('-2', '--twofactor', help='2FA code', required=False)
args = parser.parse_args()

api = Client()

def LoadOldData():
    AlreadyUnfollowed = []
    if os.path.exists("done.txt"):
        with open('done.txt', 'r', encoding='utf-8') as f:
            data = f.readlines()
            for username in data:
                AlreadyUnfollowed.append(username.strip())
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
        except TwoFactorRequired as e:
            if args.twofactor:
                verification_code = args.twofactor
            else:
                verification_code = input("Enter 2FA code: ")
            
            try:
                cl.login(USERNAME, PASSWORD, verification_code=verification_code)
                print("[+]-> Logged in with 2FA successfully.")
                login_via_pw = True
            except Exception as e:
                print(f"[+]-> Couldn't login using 2FA: %s" % e)
        except Exception as e:
            print(f"[+]-> Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        print(f"[+]-> Couldn't login user with either password or session")
        sys.exit()

def Unfollow(username):
    UserID = api.user_info_by_username_v1(username).pk
    if api.user_unfollow(UserID):
        with open('done.txt', 'a', encoding='utf-8') as f:
            f.write(username + "\n")
        print(f"[+]-> {username} unfollowed successfully.")
    else:
        print(f"[+]-> An error occurred, with the user {username}")

def ExtractUsernames(filepath):
    OldData = LoadOldData()
    with open(filepath, 'r') as f:
        data = json.loads(f.read())
        for line in data[next(iter(data))]:
            username = line[list(line)[2]][0][list(line[list(line)[2]][0])[1]]
            if username not in OldData:
                Unfollow(username)
                RandomSleep = random.randint(38, 100)
                time.sleep(RandomSleep)
            else:
                print(f"[+]-> {username} already unfollowed")

if __name__ == "__main__":
    Login(api, args.username, args.password)
    api.dump_settings("session.json")
    ExtractUsernames(args.file)
