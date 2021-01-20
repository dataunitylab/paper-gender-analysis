#!/bin/bash
JQ_FILTER="{cells: [.cells[] | del(.metadata)], metadata: .metadata}"
diff -u <(git show HEAD:cs-paper-gender-analysis.ipynb | jq "$JQ_FILTER") <(jq "$JQ_FILTER" cs-paper-gender-analysis.ipynb)
exit $?
