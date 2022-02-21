from stackapi import StackAPI
import json
SITE = StackAPI('stackoverflow')

with open('comment_file.json', "x+") as file:
    questions = SITE.fetch('questions', order="desc", tagged="r", sort="hot")
    file.write(json.dumps(questions))