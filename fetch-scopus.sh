#!/bin/env bash
set -o allexport; source .env; set +o allexport

jq -c '.result.hits.hit[]' data/DB/*.json 2> /dev/null | jq -r '.info.doi' 2> /dev/null | grep -v '^null$' | sort | uniq | head -5 | while read doi; do
    curl -s -H "X-ELS-ApiKey: $SCOPUS_API_KEY" -G https://api.elsevier.com/content/search/scopus --data-urlencode 'subj=COMP' --data-urlencode "query=DOI(\"$doi\")" | jq -c .
    sleep 1
done > scopus.json
