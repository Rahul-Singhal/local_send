#!/bin/bash

mkdir /usr/share/local_send
sudo mv server.py client.py local_send.sh /usr/share/local_send/
sudo chmod +x local_send.sh
sudo ln -s /usr/bin/bar /opt/foo