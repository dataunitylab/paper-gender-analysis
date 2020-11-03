#!/bin/bash

mkdir -p data

function get_dblp_json() {
    local type=$1
    local key=$2
    local start=$3
    local end=$4
    local offset=$5
    local skip=$6

    # Loop over the range of parameters
    # (typically years or journal volume numbers)
    for param in $(seq $start $skip $end); do
        # Find the output filename
        local outfile="data/$key-$(($param+$offset)).json"

        # Download the file if does not exist
        url="https://dblp.org/search/publ/api?q=toc%3Adb/$type/$key/$key$param.bht%3A&h=1000&format=json"
        [ -f "$outfile" ] || wget -O $outfile $url
    done

    sleep 1
}

get_dblp_json conf cidr 2003 2020 0 2
get_dblp_json conf edbt 1988 2020 0
get_dblp_json conf icde 1984 2020 0
get_dblp_json conf sigmod 1975 2020 0
get_dblp_json journals pvldb 1 13 2007
get_dblp_json journals tods 1 45 1975

#get_dblp_json conf kdd 2010 2020 0
#get_dblp_json conf sigir 2010 2020 0
