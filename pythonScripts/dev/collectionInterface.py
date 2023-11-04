# encoding=utf-8
"""in response to https://community.notepad-plus-plus.org/topic/NNNNNN/

other notes go here
"""
from Npp import *
import urllib2  # .urlopen() returns stream
import json     # .load(f) => load from stream; .loads(s) => load from string; .dump(o) => dump to stream; .dumps(o) => dump to string

f = urllib2.urlopen("https://raw.githubusercontent.com/notepad-plus-plus/userDefinedLanguages/master/udl-list.json")
udl_object = json.load(f)

f = urllib2.urlopen("https://github.com/notepad-plus-plus/userDefinedLanguages/tree/master/autoCompletions")
auto_str = f.read()

console.clear();
console.write(json.dumps({ "udls": udl_object , "autoCompletions": auto_str}, sort_keys=True, indent=2, separators=(',',':')))
console.write("\n")

"""
from HTMLParser import HTMLParser
import urllib

class AnchorParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
            if tag =='a':
                    for key, value in attrs.iteritems()):
                            if key == 'href':
                                    print value

parser = AnchorParser()
data = urllib.urlopen('http://somewhere').read()
parser.feed(data)
"""
# from HTMLParser import HTMLParser
# class MyGitHubLinkParser(HTMLParser):
#     def handle_starttag(self, tag, attrs):
#         if tag == 'a':
#             console.write("{:s} => '{:s}'\n".format(tag, attrs));
#             for name, value in attrs:
#                 console.write("\t{:s} => {:s}\n".format(name, value))
#
#             # for key, value in attrs.iteritems():
#             #     if key == 'href':
#             #         console.write("{:-20s} => {}".format(key, value))
#
# parser = MyGitHubLinkParser()
# parser.feed(auto_str)
