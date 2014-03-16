#!/bin/bash

args=""
if [[ $# == 0 ]]
then
	python /usr/share/local_send/indicator_local_send.py &
else
	for var in "$@"
	do
	    args="$args"" $var"
	done
	python /usr/share/local_send/client.py $args &
fi