# instagram follow request remover
## A simple python script that can extract usernames from pending_follow_requests.html and then remove them.

pending_follow_requests.html is a file you find in your instagram data after downloading it, and contains people you sent a follow request to them and they didn't accept or reject it, after that the script will start remove the follow requests
This script is time saving if you have a lot of pending follow requests because you won't spend hours removing one by one, just run the script and do your work.

## How to use the script

### 1: Copy pending_follow_requests.html to the script's folder
Download your instagram data and copy pending_follow_requests.html to the script's folder, you will find it in followers_and_following folder

### 2: Install requirements
pip install -r /requirements.txt

### 3: Update your login info in logininfo.py

### 4: Run the script
python Main.py
