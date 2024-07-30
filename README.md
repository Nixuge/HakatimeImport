# HakatimeImport
A tool to import all of your exported Wakatime heartbeats into Hakatime.

# Requirements
- mitmproxy
- docker (with docker-compose)
- python >=3.9

# Usage
- Run main.py and follow the instructions.
- Run `mitmweb --mode regular@8082 -s <PATH_TO_MITMPROXY/REDIRECTOR.PY>` (replace the path with yours)
- Grab your `mitmproxy-ca-cert.pem`, which is usually located at `~/.mitmproxy/mitmproxy-ca-cert.pem` and copy it to the `docker` folder.
- `cd` to the `docker` folder, then run the following:
- - `docker build -t custom-hakatime .`
- - `docker-compose -f ./new_compose.yml up`
- Open localhost:8080, register, then click on your profile picture and click on "Import Data"
- Select a date range (you should've had your earliest valid date printed in the first step)
- Submit and done.
  
   