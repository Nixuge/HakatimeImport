from mitmproxy import http
import json

# START BASE PATH
BASE_PATH = "/you_forgot_to_run_the_original_script"
# END BASE PATH

with open(f"{BASE_PATH}/cache/heartbeats_parsed.json", "r") as f:
    heartbeats: dict = json.load(f)

available_dates = list(heartbeats.keys())

with open(f"{BASE_PATH}/cache/all_user_agent_ids", "r") as f:
    known_uas: list = json.load(f)

with open(f"{BASE_PATH}/cache/default_user_agent", "r") as f:
    default_ua: str = f.read()


def fix_up_data(data):
    for heartbeat in data:
        for prop in ("cursorpos", "lineno"):
            val = heartbeat.get(prop)
            if val:
                heartbeat[prop] = str(val)

        if heartbeat["user_agent_id"] not in known_uas:
            heartbeat["user_agent_id"] = default_ua

    return data


def request(flow: http.HTTPFlow) -> None:
    # Check if the request URL matches the target URL
    url = flow.request.pretty_url
    if url.startswith("https://wakatime.com/api/v1/users/current/heartbeats?date="):
        date = url.split("?date=")[1].split("T")[0]
        print("Date:", date)

        if date not in available_dates:
            data = []
        else:
            data = fix_up_data(heartbeats[date])

        res = json.dumps({
            "data": data,
            "start": f"{date}T00:00:00Z", 
            "end": f"{date}T23:59:59Z", 
            "timezone": "Europe/Paris"
        })

        flow.response = http.Response.make(
            200,
            res,
            {"Content-Type": "application/json"}
        )
