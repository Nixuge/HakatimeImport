import json
from rauth import OAuth2Session


def get_all_user_agents(session: OAuth2Session):
    all_user_agents: list = []
    res = json.loads(session.get("users/current/user_agents?page=1").text)
    all_user_agents += res["data"]

    # Due to a bug in Hakatime, ONLY THE FIRST PAGE USER AGENTS ARE GRABBED, hence why an util for this is required.
    # This has the effect that old user agents aren't grabbed, and any heartbeat using one of those will fail on add.
    # max_page = res["total_pages"]
    # for i in range(1, max_page+1):
    #     new_res = json.loads(session.get(f"users/current/user_agents?page={i}").text)
    #     all_user_agents += new_res["data"]
    #     print(f"Done grabbing user agents for page {i}")
    
    all_user_agents.reverse() # latest last 
    return all_user_agents

def choose_user_agent(uas: list):
    for i, ua in enumerate(uas):
        print(f"{i+1}: {ua['value']} ({ua['created_at']}->{ua['last_seen_at']})")
    print("Please choose your prefeered user agent. Order is a bit weird, but should be from last (bottom) to first (top).")
    i = 0
    while True:
        try:
            i = int(input("Enter your prefeered user agent: "))
            if i > 0 and i <= len(uas):
                break
        except: pass
        print("Please choose a valid id.")
    
    return uas[i-1]