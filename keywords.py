import collections
import json
import re


keywords = {
    "semi-structured": [
        "graph",
        "graphs",
        "rdf",
        "social network",
        "subgraph",
        "sparql",
        "temporal",
        "stream",
        "streams",
        "semistructured",
        "xml",
        "json",
        "xpath",
        "xquery",
        "spatial",
        "key-value",
        "document",
    ],
    "core": [
        "information",
        "system",
        "systems",
        "transaction",
        "query",
        "querying",
        "queries",
        "query processing",
        "query optimization",
        "storage",
        "index",
        "indexing",
        "data model",
        "semantics",
        "query language",
        "algebra",
        "calculus",
        "deadlock",
        "relational",
        "search",
        "management",
        "data",
        "database",
        "databases",
    ],
    "new": [
        "machine learning",
        "data science",
        "visualization",
        "human",
        "interactive",
        "user",
        "crowdsourcing",
        "p2p",
        "integration",
        "mining",
        "analytics",
        "linkage",
        "skyline",
        "top-k",
        "responsible",
    ],
    "performance": [
        "performance",
        "scalable",
        "distributed",
        "parallel",
        "hardware",
        "realtime",
        "concurrency",
        "scaling",
        "multicore",
        "benchmark",
        "efficient",
    ],
}

paper_cats = {}
titles = {}

for line in open('scopus.json'):
    jsonl = json.loads(line)

    # Try to get the first ID of the first paper from this line
    try:
        eid = jsonl["search-results"]["entry"][0]["eid"]
    except KeyError:
        continue

    paper_cats[eid] = set()

    # Try to get the title of the paper
    title = jsonl["search-results"]["entry"][0].get("dc:title").lower()
    if not title:
        continue
    titles[eid] = title

    # Check the paper for the given keywords corresponding to a category
    for (cat, kws) in keywords.items():
        for kw in kws:
            if re.search(r"\b" + kw + r"\b", title):
                paper_cats[eid].add(cat)
                break


# Count the number of papers assigned to 1, 2, 3, ... categories
cat_counts = collections.Counter()
for (eid, p) in paper_cats.items():
    cat_counts[len(p)] += 1
print(cat_counts)
