#!/bin/bash

while [ $(date "+%H") -lt 24 ]; do
    echo "Time Now: `date +%H:%M:%S`"
    echo "Sleeping for 10 seconds"
    sleep 10
    sudo sntp -sS ntp0.cornell.edu
    # sudo sntp -sS time.nist.gov
done
