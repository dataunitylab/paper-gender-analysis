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
        mkdir -p data/$field
        [ -f "$outfile" ] || wget -O $outfile $url
    done

    sleep 1
}


### DB ###

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


### AI ###

get_dblp_json ai conf nips 1987 2019 0

get_dblp_json ai conf icml 1993 2020 0

get_dblp_json ai conf aaai 80 93 1900
# TODO Get weird years with -1 and -2 suffixes
get_dblp_json ai conf aaai 97 99 1900
get_dblp_json ai conf aaai 2000 2004 0 2
get_dblp_json ai conf aaai 2005 2020 0

get_dblp_json ai conf iclr 2013 2020 0

get_dblp_json ai conf ijcai 69 99 1900 2
get_dblp_json ai conf ijcai 2001 2015 0 2
get_dblp_json ai conf ijcai 2016 2020 0


### HCI ###

get_dblp_json hci conf chi 1989 1991 0
get_dblp_json hci conf chi 92 99 1900
get_dblp_json hci conf chi 2000 2020 0

get_dblp_json hci conf uist 1988 2020 0


### Networking ###

get_dblp_json networking conf sigcomm 1981 2020 0

get_dblp_json networking conf nsdi 2004 2020 0


### Systems ###

get_dblp_json systems conf osdi 94 96 1900 2
get_dblp_json systems conf osdi 99 99 1900
get_dblp_json systems conf osdi 2000 2018 0 2

get_dblp_json systems conf sosp 69 99 1900 2
get_dblp_json systems conf sosp 2001 2019 0 2

get_dblp_json systems conf eurosys 2006 2020 0

get_dblp_json systems conf fast 2002 2020 0

# TODO Get earlier years
get_dblp_json systems conf usenix 2009 2020 0
