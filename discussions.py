import json
from math import ceil
from stackapi import StackAPI
from helper import write_to_json_file, sort_by_views
SITE = StackAPI('stackoverflow')

headers = ["forum", "type", "date_posted", "author_id", "author_username", "question_id", "parent_id", "title"]
def get_questions():
    questions = SITE.fetch('questions', order="desc", tagged="r", pagesize="50", pages="4")
    sorted_questions = sort_by_views(questions["items"])
    print(f"Retrieved {len(sorted_questions)} questions")
    print(f"Sorted: {sorted_questions[0]}")
    write_to_json_file(sorted_questions, 'question_file.json')

def get_answers(questions):
    ids = []
    answers = []
    answers_count = 0
    for question in questions:
        answer_count = question.get('answer_count')
        if answer_count > 0:
            answers_count += answer_count
            ids.append(question.get('question_id'))
    print(f"Expecting {answers_count} answers.")
    total_batches = ceil(answers_count / 100)
    batch_count = 1
    print(f"Batch started\n{total_batches} batches will be processed.\nCurrent batch count {batch_count}")
    while batch_count < total_batches:
        batch_start = batch_count*100 - 100
        batch_end = batch_count*100-1
        batch_ids = ids[batch_start:batch_end]
        batch_answers = SITE.fetch('questions/{ids}/answers', ids=batch_ids, filter="!nKzQURF6Y5", pagesize=50, pages=2)
        print(f"Batch count: {batch_count}\n{batch_answers.get('items')}")
        for item in batch_answers.get('items'):
            answers.append(item)
        batch_count += 1
    print(f"Expected {answers_count} answers. Total is {len(answers)} answers.")
    write_to_json_file(answers, 'answers.json')

def format_rows(data, type):
    return

def get_comment_ids():
    comment_ids = []
    comments = SITE.fetch('questions/{ids}/comments', ids=[71213139, 71212278])
    for comment in comments["items"]:
        comment_ids.append(comment["comment_id"])
    print(comment_ids)

# get_questions()
with open("question_file.json", "r") as questions:
    get_answers(json.load(questions))