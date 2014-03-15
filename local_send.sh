#!/bin/bash

args=""
for var in "$@"
do
	echo $var
    args="$args"" $var"
done

python client.py $args