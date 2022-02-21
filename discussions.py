from stackapi import StackAPI
import json
SITE = StackAPI('stackoverflow')

with open('comment_file.json', "x+") as file:
    comments = SITE.fetch('comments')
    file.write(json.dumps(comments))