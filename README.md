# cancel instagram follow request you sent
after the update the only way to see the people you sent follow request to them is by downloading your follow and follwing data from insatgram.
in the folder there's a file named pending_follow_requests.json, it contains the username of users who didnt either canceled follow or accepted it.
this script can cancel the follow request sent by you, after extracting them from pending_follow_requests.json and saving the unfollowed usernames in a text file named done.txt so if the script stops for any reason you can just run it again and it will look in the file if the username already been unfollowed and if it is it'll pass it.

## How to use the script
watch the [video](https://youtu.be/Kg_D-GSRqgU) or follow the steps

### 1: Get the file.
Download your instagram data and get path to the pending_follow_requests.json to the script file, you will find it in followers_and_following folder.

### 2: Install requirements
pip install -r /requirements.txt

### 4: Run the script
python main.py -u "username" -p "password" -f "the path to pending_follow_requests.json" 


for any issues or ideas to improvement the script please open an issue.