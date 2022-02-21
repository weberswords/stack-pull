from stackapi import StackAPI
import json
SITE = StackAPI('stackoverflow')

def get_questions():
    with open('comment_file.json', "x+") as file:
        questions = SITE.fetch('questions', order="desc", tagged="r", sort="hot")
        file.write(json.dumps(questions))

def get_answers():
    with open('answers.json', 'x+') as file:
        answers = SITE.fetch('questions/{ids}/answers', ids=[71213139, 71212278])
        file.write(json.dumps(answers))

def get_comment_ids():
    comment_ids = []
    comments = SITE.fetch('questions/{ids}/comments', ids=[71213139, 71212278])
    for comment in comments["items"]:
        comment_ids.append(comment["comment_id"])
    print(comment_ids)

get_comment_ids()