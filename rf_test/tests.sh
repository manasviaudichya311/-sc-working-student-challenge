#!/usr/bin/env sh

# Hint: Add something here to wait until the server is ready
# taken from https://stackoverflow.com/a/23157343
until $(curl --output /dev/null --silent --head --fail 'http://server:80/ready');
do
    sleep 10
done

mkdir -p results

robot -d results test-server.robot
