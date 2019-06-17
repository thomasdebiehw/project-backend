# Project Alarmostat backend
This is the backend for my alarmostat project. It's written in Python 3.5 and meant to be run on a Raspberry Pi.
The program can be controlled via the hardware or with a webinterface that connects via Flask.

Link to frontend: https://github.com/thomasdebiehw/project-frontend

Instructions to build the Alarmostat can be found here: https://www.instructables.com/id/Alarmostat/

To run this program on startup make a new service file with the following contents:
```
$:  sudo nano /lib/systemd/system/alarmostat.service
```

```
[Unit]
Description=Alarmostat service
Wants=network-online.target
After=network-online.target

[Service]
Type=idle
ExecStart=/usr/bin/python3.5 /home/dp-user/project-backend/app.py -u -m flask run --host=0.0.0.0

[Install]
WantedBy=multi-user.target
```
Replace the ExecStart path with the path to your file, save and run these commands:
```
$:  sudo chmod 644 /lib/systemd/system/alarmostat.service
$:  sudo systemctl daemon-reload
$:  sudo systemctl enable alarmostat.service
```


The database file contains the needed values already, you shoudl add a insert a new user with an rfidtag though.
You might have to create a new user though. In the program these credentials are used:

user: project

password: ditwachtwoordmagjezekerweten

You could also change these in the program instead.
