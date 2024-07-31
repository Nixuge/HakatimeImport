# HakatimeImport
A tool to import all of your exported Wakatime heartbeats into Hakatime.

# Before anything else
You can do this in a self hosted wakapi in a way less jank way.

Self host using https://github.com/muety/wakapi, then on the web panel simply go to Settings/Integrations and paste in your Wakatime API Key.

Once you've done that, you should have the option to "Import Data" (may take a bit of time to load)

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
  
   