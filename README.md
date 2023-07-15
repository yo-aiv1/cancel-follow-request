# instagram follow request remover
## A simple python script that can extract usernames from pending_follow_requests.html and then remove them.

pending_follow_requests.html is a file you find in your instagram data after downloading it, and it contains people you sent a follow request to them and they didn't either accept or reject you :3, after that the script will start removing them for you one by one This script is time saving if you have a lot of pending follow requests because (ya lmdlol :3 ) you won't spend hours removing one by one, just run the script and leave it in the background.

## How to use the script

### 1: Copy pending_follow_requests.html to the script's folder
Download your instagram data and copy pending_follow_requests.html to the script's folder, you will find it in followers_and_following folder

### 2: Install requirements
pip install -r /requirements.txt

### 4: Run the script
python main.py -u <username> -p <password> -f <the path to pending_follow_requests.html>

## Updates

### 1: Removed the  logininfo.py now you can enter username and password using arguments -u for username and -p for password and -f for the path for the pending_follow_requests.html
