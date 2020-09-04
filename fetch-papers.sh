#!/bin/bash

mkdir -p data

function get_dblp_json() {
    local type=$1
    local key=$2
    local start=$3
    local end=$4

    # Loop over the range of parameters
    # (typically years or journal volume numbers)
    for param in $(seq $start $end); do
        # Find the output filename
        local outfile="data/$key-$param.json"

        # Download the file if does not exist
        url="https://dblp.org/search/publ/api?q=toc%3Adb/$type/$key/$key$param.bht%3A&h=1000&format=json"
        [ -f "$outfile" ] || wget -O $outfile $url
    done

    sleep 1
}

get_dblp_json conf edbt $year 2010 2020
get_dblp_json conf icde $year 2010 2020
get_dblp_json conf kdd $year 2010 2020
get_dblp_json conf sigir $year 2010 2020
get_dblp_json conf sigmod $year 2010 2020
get_dblp_json journals pvldb $vol 3 13
