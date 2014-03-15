#!/bin/bash

args=""
for var in "$@"
do
	echo $var
    args="$args"" $var"
done

python /usr/share/local_send/client.py $args