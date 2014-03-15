#!/bin/bash

sudo rm /usr/share/local_send /usr/bin/local_send -rf
sudo rm /usr/share/pixmaps/local_send_*.png -rf

sudo mkdir /usr/share/local_send
sudo cp images/* /usr/share/pixmaps
sudo cp messenger_icon.png /usr/share/pixmaps
sudo cp server.py client.py local_send.sh indicator_local_send.py /usr/share/local_send/
sudo chmod +x local_send.sh
sudo ln -s /usr/share/local_send/local_send.sh /usr/bin/local_send
echo "DONE"