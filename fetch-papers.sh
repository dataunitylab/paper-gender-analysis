#!/bin/bash

mkdir -p data

function get_dblp_json() {
    local OPTIND

    local field pub_type start_idx end_idx offset skip label

    offset=0
    skip=1

    while getopts "f:t:k:s:e:o:p:l:" opt; do
        case "$opt" in
            f)  # Field of the publication
                field="$OPTARG";;

            t)  # Publication type (journal/conf)
                pub_type="$OPTARG";;

            k)  # The key of the publication (used in the URL)
                key="$OPTARG";;

            s)  # The numerical index to start retrieval
                start_idx="$OPTARG";;

            e)  # The numerical index to end retrieval
                end_idx="$OPTARG";;

            o)  # The offset between the numerical index and the year
                offset="$OPTARG";;

            p)  # The number to skip on increment (e.g. 2 for alternate years)
                skip="$OPTARG";;

            l)  # The label to be stored under (if different than key)
                label="$OPTARG";;
        esac
    done

    # Default the label to the key
    if [ -z "$label" ]; then label="$key"; fi

    # Loop over the range of parameters
    # (typically years or journal volume numbers)
    for param in $(seq $start_idx $skip $end_idx); do
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

get_dblp_json -f db -t conf -k cidr -s 2003 -e 2020 -p 2

get_dblp_json -f db -t conf -k edbt -s 88 -e 99 -o 1900
get_dblp_json -f db -t conf -k edbt -s 2000 -e 2020

get_dblp_json -f db -t conf -k icde -s 84 -e 99 -o 1900
get_dblp_json -f db -t conf -k icde -s 2000 -e 2020

get_dblp_json -f db -t conf -k sigmod -s 75 -e 99 -o 1900
get_dblp_json -f db -t conf -k sigmod -s 2000 -e 2020

get_dblp_json -f db -t journals -k vldb -s 1 -e 29 -o 1991 -l vldbj

# VLDB is fragmented on DBLP but we collect the data together
get_dblp_json -f db -t conf -k vldb -s 75 -e 99 -o 1900
get_dblp_json -f db -t conf -k vldb -s 2000 -e 2007
get_dblp_json -f db -t journals -k pvldb -s 1 -e 13 -o 2007 -l vldb

# get_dblp_json db journals tods 1 45 1975
#get_dblp_json db conf kdd 2010 2020 0
#get_dblp_json db conf sigir 2010 2020 0


### AI ###

get_dblp_json -f ai -t conf -k nips -s 1987 -e 2019

get_dblp_json -f ai -t conf -k icml -s 1993 -e 2020

get_dblp_json -f ai -t conf -k aaai -s 80 -e 93 -o 1900
# TODO Get weird years with -1 and -2 suffixes
get_dblp_json -f ai -t conf -k aaai -s 97 -e 99 -o 1900
get_dblp_json -f ai -t conf -k aaai -s 2000 -e 2004 -p 2
get_dblp_json -f ai -t conf -k aaai -s 2005 -e 2020

get_dblp_json -f ai -t conf -k iclr -s 2013 -e 2020

get_dblp_json -f ai -t conf -k ijcai -s 69 -e 99 -o 1900 -p 2
get_dblp_json -f ai -t conf -k ijcai -s 2001 -e 2015 -p 2
get_dblp_json -f ai -t conf -k ijcai -s 2016 -e 2020


### HCI ###

get_dblp_json -f hci -t conf -k chi -s 1989 -e 1991
get_dblp_json -f hci -t conf -k chi -s 92 -e 99 -o 1900
get_dblp_json -f hci -t conf -k chi -s 2000 -e 2020

get_dblp_json -f hci -t conf -k uist -s 1988 -e 2020


### Networking ###

get_dblp_json -f networking -t conf -k sigcomm -s 1981 -e 2020

get_dblp_json -f networking -t conf -k nsdi -s 2004 -e 2020


### Systems ###

get_dblp_json -f systems -t conf -k osdi -s 94 -e 96 -o 1900 -p 2
get_dblp_json -f systems -t conf -k osdi -s 99 -e 99 -o 1900
get_dblp_json -f systems -t conf -k osdi -s 2000 -e 2018 -p 2

get_dblp_json -f systems -t conf -k sosp -s 69 -e 99 -o 1900 -p 2
get_dblp_json -f systems -t conf -k sosp -s 2001 -e 2019 -p 2

get_dblp_json -f systems -t conf -k eurosys -s 2006 -o 2020

get_dblp_json -f systems -t conf -k fast -s 2002 -e 2020

# TODO Get earlier years
get_dblp_json -f systems -t conf -k usenix -s 2009 -e 2020
