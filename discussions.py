import csv
import json
import jq
from math import ceil
from stackapi import StackAPI
from helper import sort_by_answers, write_to_json_file, write_to_csv_file, convert_from_epoch, just_write
SITE = StackAPI('stackoverflow')

headers = ["forum", "type", "date_posted", "author_id", "author_username", "post_id", "parent_id", "parent_username", "title", "body"]
def get_questions():
    questions = SITE.fetch('search/advanced', sort="creation", order="desc", tagged="r", answers="11", pagesize="100")
    print(f'Retrieved {len(questions["items"])} questions')
    sorted_questions = sort_by_answers(questions["items"])
    print(f'Saving {len(sorted_questions[0:200])} questions')
    write_to_json_file(sorted_questions[0:200], 'question_file.json')

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

def format_rows(data, data_type):
    formatted_data = []
    for datum in data:
        post_id = datum.get('question_id') if data_type == "question" else datum.get('answer_id')
        print(f"post_id: {post_id} \n{data_type}")
        formatted_row = ["SO", data_type, convert_from_epoch(datum.get('creation_date')), datum.get('owner').get('user_id'), datum.get('owner').get('display_name'), post_id, datum.get('question_id'), datum.get('title'), datum.get('body')]
        formatted_data.append(formatted_row)
    return formatted_data

def get_comment_ids():
    comment_ids = []
    comments = SITE.fetch('questions/{ids}/comments', ids=[71213139, 71212278])
    for comment in comments["items"]:
        comment_ids.append(comment["comment_id"])
    print(comment_ids)

get_questions()

# with open('question_file.json', 'r') as questions:
#     # get_answers(json.load(questions))
#     formatted_questions = format_rows(json.load(questions), "question")
#     write_to_csv_file(headers, formatted_questions, 'stack_overflow.csv')

# with open('answers.json', 'r') as answers:
#     formatted_answers = format_rows(json.load(answers), "answer")
#     just_write(formatted_answers, 'stack_overflow.csv')