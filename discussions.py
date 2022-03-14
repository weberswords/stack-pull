from stackapi import StackAPI
from helper import write_to_json_file, sort_by_views
SITE = StackAPI('stackoverflow')

def get_questions():
    questions = SITE.fetch('questions', order="desc", tagged="r")
    sorted_questions = sort_by_views(questions["items"])
    print(f"Sorted: {sorted_questions[0]}")
    write_to_json_file(sorted_questions, 'question_file.json')

def get_answers():
    answers = SITE.fetch('questions/{ids}/answers', ids=[71213139, 71212278])
    write_to_json_file(answers, 'answers.json')

def get_comment_ids():
    comment_ids = []
    comments = SITE.fetch('questions/{ids}/comments', ids=[71213139, 71212278])
    for comment in comments["items"]:
        comment_ids.append(comment["comment_id"])
    print(comment_ids)

get_questions()