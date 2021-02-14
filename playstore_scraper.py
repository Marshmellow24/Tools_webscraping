# encoding: utf-8

from google_play_scraper import app
from google_play_scraper.features.reviews import reviews_all
import re
import json

result = reviews_all(
    "com.tier.app",
    sleep_milliseconds=0,
    lang="de",
    country="de",
    )

#print(result)



#result_string = ",".join(result)
#print(type(result[0]))
i = 0

while i < len(result):
    for k in result[i]:
        if re.match("content", k):
            print(i)
            print(result[i][k])
    i += 1
#re.findall("'content': '.*'", result_string)