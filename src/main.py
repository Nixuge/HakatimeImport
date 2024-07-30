import json
import os

from login.session import get_session
from utils.user_agent_parser import choose_user_agent, get_all_user_agents


print("Welcome to Hakatime's Wakatime archive importer.")

check_ua = True

if not os.path.exists("cache/"):
    os.makedirs("cache/")

if os.path.exists("cache/default_user_agent"):
    print("Would you like to re fetch user agents? This is recommended if you haven't in a while or if you've")
    check_ua = input("updated your system in any way (extension, os, ide). (Y/n): ").lower() not in ["n", "no", "non"]

if check_ua:
    sess = get_session()
    uas = get_all_user_agents(sess)

    with open("cache/all_user_agent_ids.json", "w") as f:
        json.dump([x["id"] for x in uas], f)

    choosed_ua = choose_user_agent(uas)

    with open("cache/default_user_agent", "w") as f:
        f.write(choosed_ua["id"])
        print("Wrote default user agent to cache/default_user_agent. You can remove this file to choose again.")


# Redoing the json thing every time as tbh it's not that bad on the cpu
print("Starting the json migration.")
path = "/home/"
while not os.path.isfile(path):
    path = input("Please enter the filepath for your exported heartbeats json: ")

with open(path, "r") as f:
    data: dict = json.load(f)

first_date = None
all_heartbeats = {}
for day in data["days"]:
    if first_date == None:
        first_date = day["date"]
    all_heartbeats[day["date"]] = day["heartbeats"]

print(f"The first date in the list is: {first_date}")

with open("cache/heartbeats_parsed.json", "w") as f:
    json.dump(all_heartbeats, f)

print("All done ! Now continue following the README.")
