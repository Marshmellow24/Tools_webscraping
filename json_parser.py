# encoding: utf-8

import json
import re


with open(r"F:\UNI\Master WiInfo\Seminararbeit UM\instagram\lime\lime.json", encoding = "utf-8") as f:
    data = json.load(f)

o = open(r"F:\UNI\Master WiInfo\Seminararbeit UM\instagram\lime\comments.txt", "w", encoding = "utf-8")

print(type(data))

emoji_pattern = re.compile("["
        u"\U00002600-\U000026FF"  # hearts & misc 
        u"\U00002700-\U000027BF"  # dingbats 
        u"\U0001F600-\U0001F64F"  # emoticons 
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs 
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F900-\U0001F9FF"  # supplemental symbols & pictographs
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

at_pattern = re.compile(r"@\S*") # @s pattern


i = 1 # iterator for post
for d in data:
    if d["__typename"] == "GraphVideo" and not re.search(r"[g|G]iveaway", d["edge_media_to_caption"]["edges"][0]["node"]["text"]): # show only videos and filter out giveaways
        #print(d["shortcode"])
        #print(i)
        o.write(str(i) + "\n") # number of media
        o.write(d["shortcode"] + "\n\n" ) # shortcode of media post (instagram.com/p/{shortcode})
        
        for l in d["comments"]["data"]: 
            #print(emoji_pattern.sub(r" ", l["text"]))
            no_emoji = emoji_pattern.sub(r"", l["text"]) # filter emojis
            no_at = at_pattern.sub(r"", no_emoji) # filter @s
            stripped = no_at.strip() # @remove leading and trailing whitespaces
            print(stripped) 
            
            if not re.search(r"#.* ", stripped) and re.search(r"\s", stripped): # remove hashtag comments and single word lines ("\s" looks for strings with whitespaces)
                if no_at.strip(): # leere Zeilen nicht ausgeben
                #o.write(l["text"])
                    o.write(stripped)
                    o.write("\n")    
        o.write("\n*******************************\n") # delimiter  
        print("\n")
        i += 1


        