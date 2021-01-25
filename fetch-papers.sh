#!/bin/bash

mkdir -p data

function get_dblp_json() {
    local field=$1
    local type=$2
    local key=$3
    local start=$4
    local end=$5
    local offset=$6
    local skip=$7
    local label="${8:-$key}"

    # Loop over the range of parameters
    # (typically years or journal volume numbers)
    for param in $(seq $start $skip $end); do
        # Find the output filename
        local outfile="data/$field/$label-$(($param+$offset)).json"

        # Download the file if does not exist
        url="https://dblp.org/search/publ/api?q=toc%3Adb/$type/$key/$key$param.bht%3A&h=1000&format=json"
        [ -f "$outfile" ] || wget -O $outfile $url
    done

    sleep 1
}

get_dblp_json db conf cidr 2003 2020 0 2

get_dblp_json db conf edbt 88 99 1900
get_dblp_json db conf edbt 2000 2020 0

get_dblp_json db conf icde 84 99 1900
get_dblp_json db conf icde 2000 2020 0

get_dblp_json db conf sigmod 75 99 1900
get_dblp_json db conf sigmod 2000 2020 0

get_dblp_json db journals vldb 1 29 1991 1 vldbj

# VLDB is fragmented on DBLP but we collect the data together
get_dblp_json db conf vldb 75 99 1900
get_dblp_json db conf vldb 2000 2007 0
get_dblp_json db journals pvldb 1 13 2007 1 vldb

# get_dblp_json db journals tods 1 45 1975
#get_dblp_json db conf kdd 2010 2020 0
#get_dblp_json db conf sigir 2010 2020 0
