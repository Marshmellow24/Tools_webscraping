# encoding: utf-8

import json
import re


class IGJsonParser:
    """
    Parses through json file, that is generated with instagram-scraping package.
    Removes Emojis, as well as @'s and extracts comments.
    Also filters out comments from posts that are Giveaways.
    """

    def __init__(self, json_file, output_path, output=False):
        self.json_file = json_file
        self.output_path = output_path
        self.output = output  # if true output file is generated

    def switch_output(self):
        if self.output:
            self.output = False
            print("Output to file disabled ")
        else:
            self.output = True
            print("Output switched to active: ")
            print(self.output_path)

    def parse(self, split=True):
        """
        If IGJsonParser parameter 'output' is true
        this class gives out a .txt file at the output location.

        :param split: prints delimiter, post shortcode and post number if True
        :return: the comments as string
        """
        with open(file=self.json_file, encoding="utf-8") as f:
            data = json.load(f)

        if self.output:
            o = open(self.output_path, "w", encoding="utf-8")

        emoji_pattern = re.compile("["
                                   u"\U00002600-\U000026FF"  # hearts & misc 
                                   u"\U00002700-\U000027BF"  # dingbats 
                                   u"\U0001F600-\U0001F64F"  # emoticons 
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs 
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F900-\U0001F9FF"  # supplemental symbols & pictographs
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U0001F100-\U0002FA1F"  # other symbols
                                   "]+", flags=re.UNICODE)
        at_pattern = re.compile(r"@\S*")  # @s pattern
        line_pattern = re.compile(r"\n")  # remove \n in comments

        i = 1  # iterator for post
        output_list = []  # buffer list for comments

        for d in data:
            # show only videos and filter out giveaways
            if d["__typename"] == "GraphVideo" and not \
                    re.search(r"[g|G]iveaway", d["edge_media_to_caption"]["edges"][0]["node"]["text"]):

                shortcode = d["shortcode"] + "\n\n"
                number = str(i) + "\n"
                delimiter = "\n*******************************\n"

                if self.output:  # only write to file if param output true
                    o.write(number)  # number of media post
                    o.write(shortcode)  # shortcode of media post (instagram.com/p/{shortcode})
                if split:
                    output_list.extend([number, shortcode])  # extend, not append or else list will be added to list

                for comment in d["comments"]["data"]:
                    process = emoji_pattern.sub(r"", comment["text"])  # filter emojis
                    process = at_pattern.sub(r"", process)  # filter @s
                    process = line_pattern.sub(r" ", process)  # replace \n with whitespace
                    process = process.strip()  # @remove leading and trailing whitespaces

                    # remove hashtag comments and single word lines ("\s" looks for strings with whitespaces)
                    if not re.search(r"#.* ", process) and re.search(r"\s", process):
                        if process.strip():  # don't add empty lines
                            if self.output:  # only write to file if param output true
                                o.write(process)
                                o.write("\n")
                            output_list.extend([process, "\n"])  # extend comments list
                if self.output:
                    o.write(delimiter)  # delimiter
                if split:
                    output_list.extend(delimiter)

                i += 1  # increase number per loop

        output_str = "".join(output_list)  # transform list of comments to string

        return output_str
