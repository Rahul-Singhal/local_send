#!/bin/bash

sudo mkdir /usr/share/local_send
sudo cp server.py client.py local_send.sh /usr/share/local_send/
sudo chmod +x local_send.sh
sudo ln -s /usr/share/local_send/local_send.sh /usr/bin/local_send
echo "DONE"