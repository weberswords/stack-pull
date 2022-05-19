import csv
import json
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
    answer_count = 0
    for question in questions:
        answer_count += question.get('answer_count')
        ids.append(question.get('question_id'))
    print(f"Expecting {answer_count} answers.")
    first_batch_answers = SITE.fetch('questions/{ids}/answers', ids=ids[0:100], filter="withbody")
    second_batch_answers = SITE.fetch('questions/{ids}/answers', ids=ids[101:200], filter="withbody")
    batch_answers = { **first_batch_answers, **second_batch_answers }
    for item in batch_answers.get('items'):
        answers.append(item)
    write_to_json_file(answers, 'answers.json')

def locate_question_author(question_id):
    with open('question_file.json', 'r') as raw_questions:
        questions = json.load(raw_questions)
        # print(f'Looking for {question_id}')
        for question in questions:
            if question['question_id'] == question_id:
                # print("Question ID found!")
                # print(f"Owner: {question['owner']['display_name']}\nUser ID: {question['owner']['user_id']}")
                return question['owner']['user_id'], question['owner']['display_name']

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

# questions = get_questions()
locate_question_author(1097367)
# with open('question_file.json', 'r') as questions:
#     get_answers(json.load(questions))
#   formatted_questions = format_rows(json.load(questions), "question")
#   write_to_csv_file(headers, formatted_questions, 'stack_overflow.csv')

# with open('answers.json', 'r') as answers:
#     formatted_answers = format_rows(json.load(answers), "answer")
#     just_write(formatted_answers, 'stack_overflow.csv')