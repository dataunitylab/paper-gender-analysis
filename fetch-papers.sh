#!/bin/bash

mkdir -p data

for year in {2015..2020}; do
    wget -O data/SIGMOD-$year.json "https://dblp.org/search/publ/api?q=toc%3Adb/conf/sigmod/sigmod$year.bht%3A&h=1000&format=json"
    sleep 1
done

for vol in {25..29}; do
    wget -O data/VLDB-$vol.json "https://dblp.org/search/publ/api?q=toc%3Adb/journals/vldb/vldb$vol.bht%3A&h=1000&format=json"
    sleep 1
done
