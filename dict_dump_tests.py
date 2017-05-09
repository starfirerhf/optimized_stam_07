import json
import os

testfile = "meta.json"

dict = {
"folder": "unknown",
"language": "EN",
"encoding": "UTF8",
"candidate-authors":
[
{"author-name": "candidate00001"},
{"author-name": "candidate00002"},
{"author-name": "candidate00003"}
],
"unknown-texts":
[
{"unknown-text": "unknown00001.txt"},
{"unknown-text": "unknown00002.txt"},
{"unknown-text": "unknown00003.txt"},
{"unknown-text": "unknown00004.txt"},
{"unknown-text": "unknown00005.txt"},
{"unknown-text": "unknown00006.txt"}
]
}

print(dict)

with open(testfile,'a',encoding="utf-8") as outfile:
    json.dump(dict,outfile,indent=4)