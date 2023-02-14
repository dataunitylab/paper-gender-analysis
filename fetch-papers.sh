#!/bin/bash

mkdir -p data

function get_dblp_json() {
    local OPTIND

    local field pub_type start_idx end_idx offset skip label parts group suffix

    offset=0
    skip=1

    while getopts "f:t:k:s:e:o:n:l:p:g:x:" opt; do
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

            n)  # The number to skip on increment (e.g. 2 for alternate years)
                skip="$OPTARG";;

            l)  # The label to be stored under (if different than key)
                label="$OPTARG";;

            p)  # Number of parts for multipart proceedings
                parts="$OPTARG";;

            g)  # The first part of the path after /{conf,journal}
                group="$OPTARG";;

            x)  # A suffix which should be added to the URL, but not saved
                suffix="$OPTARG";;
        esac
    done

    # Default the label to the key
    if [ -z "$label" ]; then label="$key"; fi

    # Default the group to the key
    if [ -z "$group" ]; then group="$key"; fi

    # Loop over the range of parameters
    # (typically years or journal volume numbers)
    for param in $(seq $start_idx $skip $end_idx); do
        for part in $(seq 1 $parts); do
            # Find the output filename
            if [ -z "$parts" ]; then
                # Exclude the part entirely for single part proceedings
                local outfile="data/$field/$label-$(($param+$offset)).json"
                local url="https://dblp.org/search/publ/api?q=toc%3Adb/$pub_type/$group/$key$param$suffix.bht%3A&h=1000&format=json"
            else
                # XXX For now, we need to fetch the HTML and parse later
                local outfile="data/$field/$label-$(($param+$offset))-$part.html"
                local url="https://dblp.org/db/$pub_type/$group/$key$param$suffix-$part.html"
                # local outfile="data/$field/$label-$(($param+$offset))-$part.json"
                # local url="https://dblp.org/search/publ/api?q=toc%3Adb/$pub_type/$group/$key$param$suffix-$part.bht%3A&h=1000&format=json"
            fi

            # Download the file if does not exist
            mkdir -p data/$field
            [ -f "$outfile" ] || wget -O $outfile $url
        done
    done

    sleep 1
}

### DB ###
# XXX Any conferences added here should be removed when
#     comparing fields to match the CS Rankings list

get_dblp_json -f DB -t conf -k cidr -s 2003 -e 2022 -n 2

get_dblp_json -f DB -t conf -k edbt -s 88 -e 99 -o 1900
get_dblp_json -f DB -t conf -k edbt -s 2000 -e 2023

get_dblp_json -f DB -t conf -k icde -s 84 -e 99 -o 1900
get_dblp_json -f DB -t conf -k icde -s 2000 -e 2022

get_dblp_json -f DB -t conf -k sigmod -s 75 -e 99 -o 1900
get_dblp_json -f DB -t conf -k sigmod -s 2000 -e 2022

get_dblp_json -f DB -t journals -k vldb -s 1 -e 32 -o 1991 -l vldbj

# VLDB is fragmented on DBLP but we collect the data together
get_dblp_json -f DB -t conf -k vldb -s 75 -e 99 -o 1900
get_dblp_json -f DB -t conf -k vldb -s 2000 -e 2007
get_dblp_json -f DB -t journals -k pvldb -s 1 -e 16 -o 2007 -l vldb

# XXX Thsi breaks the pattern of having the year as part of the file name
get_dblp_json -f DB -t journals -k dke -s 1 -e 130

get_dblp_json -f DB -t conf -k dasfaa -s 89 -e 99 -o 1900
get_dblp_json -f DB -t conf -k adbis -s 2000 -l dasfaa
get_dblp_json -f DB -t conf -k dasfaa -s 2001 -e 2009
get_dblp_json -f DB -t conf -k dasfaa -s 2010 -e 2019 -p 2
get_dblp_json -f DB -t conf -k dasfaa -s 2020 -e 2022 -p 3

get_dblp_json -f DB -t conf -k pods -s 82 -e 99 -o 1900
get_dblp_json -f DB -t conf -k pods -s 2000 -e 2022

get_dblp_json -f DB -t journals -k tkde -s 1 -e 35 -o 1988

# get_dblp_json DB journals tods 1 45 1975
#get_dblp_json DB conf kdd 2010 2020 0
#get_dblp_json DB conf sigir 2010 2020 0


### AI ###

#get_dblp_json -f ai -t conf -k nips -s 1987 -e 2019

#get_dblp_json -f ai -t conf -k icml -s 1993 -e 2020

get_dblp_json -f AI -t conf -k aaai -s 80 -e 93 -o 1900
get_dblp_json -f AI -t conf -k aaai -s 94 -e 96 -o 1900 -n 2 -p 2
get_dblp_json -f AI -t conf -k aaai -s 97 -e 99 -o 1900
get_dblp_json -f AI -t conf -k aaai -s 2000 -e 2004 -n 2
get_dblp_json -f AI -t conf -k aaai -s 2005 -e 2020

#get_dblp_json -f AI -t conf -k iclr -s 2013 -e 2020

get_dblp_json -f AI -t conf -k ijcai -s 69 -e 77 -o 1900 -n 2
get_dblp_json -f AI -t conf -k ijcai -s 1979 -e 1979
get_dblp_json -f AI -t conf -k ijcai -s 81 -e 99 -o 1900 -n 2
get_dblp_json -f AI -t conf -k ijcai -s 2001 -e 2015 -n 2
get_dblp_json -f AI -t conf -k ijcai -s 2016 -e 2020


### HCI ###

get_dblp_json -f HCI -t conf -k chi -s 1989 -e 1991
get_dblp_json -f HCI -t conf -k chi -s 92 -e 99 -o 1900
get_dblp_json -f HCI -t conf -k chi -s 2000 -e 2020

get_dblp_json -f HCI -t conf -k uist -s 1988 -e 2020

get_dblp_json -f HCI -t conf -k huc -s 1999 -e 2000 -l ubicomp
get_dblp_json -f HCI -t conf -g huc -k ubicomp -s 2001 -e 2019

get_dblp_json -f HCI -t conf -k pervasive -s 2002 -e 2012

get_dblp_json -f HCI -t journals -k imwut -s 1 -e 4 -o 2016

### Networking ###

get_dblp_json -f Networking -t conf -k sigcomm -s 1981 -e 2020

get_dblp_json -f Networking -t conf -k nsdi -s 2004 -e 2020


### Operating Systems ###

get_dblp_json -f Operating_Systems -t conf -k osdi -s 94 -e 96 -o 1900 -n 2
get_dblp_json -f Operating_Systems -t conf -k osdi -s 99 -e 99 -o 1900
get_dblp_json -f Operating_Systems -t conf -k osdi -s 2000 -e 2018 -n 2

get_dblp_json -f Operating_Systems -t conf -k sosp -s 69 -e 99 -o 1900 -n 2
get_dblp_json -f Operating_Systems -t conf -k sosp -s 2001 -e 2019 -n 2

get_dblp_json -f Operating_Systems -t conf -k eurosys -s 2006 -o 2020

get_dblp_json -f Operating_Systems -t conf -k fast -s 2002 -e 2020

get_dblp_json -f Operating_Systems -t conf -k usenix -s 96 -e 97 -o 1900
get_dblp_json -f Operating_Systems -t conf -k usenix -s 1998
get_dblp_json -f Operating_Systems -t conf -k usenix -s 1999 -e 2006 -x g
get_dblp_json -f Operating_Systems -t conf -k usenix -s 2007 -e 2020


### Algorithms ###

get_dblp_json -f Algorithms -t conf -k focs -s 60 -e 99 -o 1900
get_dblp_json -f Algorithms -t conf -k focs -s 2000 -e 2020

get_dblp_json -f Algorithms -t conf -k soda -s 90 -e 99 -o 1900
get_dblp_json -f Algorithms -t conf -k soda -s 2000 -e 2020

get_dblp_json -f Algorithms -t conf -k stoc -s 69 -e 92 -o 1900
get_dblp_json -f Algorithms -t conf -k stoc -s 1993 -e 2020
