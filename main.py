from rich.console import Console
from bs4 import BeautifulSoup
from instagram_private_api import Client
import logininfo

def extract_ig_usernames(html):
    soup = BeautifulSoup(html, 'html.parser')
    a_tags = soup.find_all('a')
    usernames = [a_tag.get_text() for a_tag in a_tags]
    return usernames

console = Console()
tasks = ["Extract usernames from pending_follow_requests.html", "Remove follow requests"]

with console.status("[bold green]Working on tasks...") as status:
    while tasks:
        task = tasks.pop(0)
        if task == "Extract usernames from pending_follow_requests.html":
            console.log("Extracting usernames from pending_follow_requests.html file...")
            with open('pending_follow_requests.html', 'r') as f:
                html = f.read()
            usernames = extract_ig_usernames(html)
            console.log("Writing usernames to file...")
            with open('igs.txt', 'w') as f:
                for username in usernames:
                    f.write(username + '\n')
            console.log(f"{task} complete")
        elif task == "Remove follow requests":
            console.log("Connecting to Instagram API...")
            api = Client(logininfo.username, logininfo.password)
            console.log("Reading usernames from file...")
            f = open("igs.txt", "r").read().split("\n")

            i=0
            console.log("Removing follow requests...")
            for x in f:
              if bool(x):
                  user_info = api.username_info(x)
                  uid = user_info['user']['pk']
                  api.friendships_destroy(uid)
                  i+=1
                  ig_usr = x
                  console.log("The follow request N" + str(i)+ " has been removed successfully | username: " +ig_usr)
            console.log(f"{task} complete")
