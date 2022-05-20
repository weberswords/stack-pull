import json
from math import ceil
from venv import create
from stackapi import StackAPI
from helper import get_count_of_json, get_next_page, sort_by_answers, write_to_json_file, write_to_csv_file, convert_from_epoch, just_write
with open('secrets.json', 'r') as raw_secrets:
    secrets = json.load(raw_secrets)
    key = secrets.get('key')
    access_token = secrets.get('access_token')
SITE = StackAPI('stackoverflow', key=key, access_token=access_token)

def test_connection():
    response = SITE.fetch('me')
    print(response)

headers = ["forum", "type", "date_posted", "author_id", "author_username", "post_id", "parent_question_user_id", "parent_question_username", "title", "body"]
def get_questions():
    questions = SITE.fetch('search/advanced', sort="creation", order="desc", tagged="r", answers="11", pagesize="100", filter="withbody")
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
    answers = call_for_answers(ids)
    print(f"Answers collected: {len(answers)}")
    write_to_json_file(answers, 'answers.json')

def create_batches(ids, pagesize):
    print(f"Count for ids: {len(ids)}")
    total_batches = ceil(len(ids)/pagesize)
    print(f"Calculated batches: {total_batches}")
    return total_batches

def get_all_answers_for_single_batch(ids):
    print(f"Ids being processed are: {ids[:5]}...{ids[-5:]}")
    first_fetch = SITE.fetch('questions/{ids}/answers', ids=ids, filter="withbody", pagesize=100)
    has_more = first_fetch.get('has_more')
    message = "But wait there's more!" if has_more is True else "That's all folks!"
    print(message)
    page = first_fetch.get('page')
    print(f"The current page is {page}")
    current_answers = first_fetch.get('items')
    while has_more is True:
        next_page = get_next_page(page)
        print(f"Getting next page {next_page}")
        next_fetch = SITE.fetch('questions/{ids}/answers', ids=ids, page=next_page, pagesize=100, filter="withbody")
        print(f"Adding to current_answers: {next_fetch.get('items')}")
        current_answers += next_fetch.get('items')
        has_more = next_fetch.get('has_more')
        print(f"Do we have more? {has_more}")
        print(message)
        print(f"Current count is {len(current_answers)}")
        if has_more is True:
            page = next_fetch.get('page')
    print(f"Total answers returned for ids {ids[:5]}...{ids[-5:]}: {len(current_answers)}")
    return current_answers

def call_for_answers(ids):
    all_answers = []
    if len(ids) > 100:
        batches_to_process = create_batches(ids, 100)
        print(f"Batches we expect to process {batches_to_process}")
    id_start = 0
    id_end = 99
    end_of_list = len(ids) - 1
    should_end = False
    while should_end is False:
        should_end = True if id_end == end_of_list else False
        print(f"Processing {id_start} to {id_end}")
        batch_answers = get_all_answers_for_single_batch(ids[id_start:id_end])
        all_answers += batch_answers
        if should_end is False:
            id_start += 100
            id_end += 100
            if id_end > end_of_list:
                id_end = end_of_list
    return all_answers

def locate_question_author(question_id):
    with open('question_file.json', 'r') as raw_questions:
        questions = json.load(raw_questions)
        # print(f'Looking for {question_id}')
        for question in questions:
            if question.get('question_id') == question_id:
                # print("Question ID found!")
                # print(f"Owner: {question['owner']['display_name']}\nUser ID: {question['owner']['user_id']}")
                return (question.get('owner').get('user_id'), question.get('owner').get('display_name'))

def format_rows(data, data_type):
    print(f"Data received.\nType: {data_type}\nItem Count: {len(data)}")
    formatted_data = []
    for datum in data:
        if data_type == "answer":
            parent_user_id, parent_display_name = locate_question_author(datum.get('question_id'))
        else:
            parent_user_id = datum.get('owner').get('user_id')
            parent_display_name = datum.get('owner').get('display_name')
        post_id = datum.get('question_id') if data_type == "question" else datum.get('answer_id')
        # print(f"post_id: {post_id}\n{data_type}")
        formatted_row = ["SO", 
            data_type, 
            convert_from_epoch(datum.get('creation_date')), 
            datum.get('owner').get('user_id'), 
            datum.get('owner').get('display_name'), 
            post_id,
            parent_user_id,
            parent_display_name,
            datum.get('question_id'), 
            datum.get('title'), 
            datum.get('body')]
        formatted_data.append(formatted_row)
    return formatted_data

# with open('question_file.json', 'r') as raw_questions:
#     questions = json.load(raw_questions)
#     get_answers(questions)

with open('question_file.json', 'r') as raw_questions:
    questions = json.load(raw_questions)
    formatted_questions = format_rows(questions, "question")
    write_to_csv_file(headers, formatted_questions, 'stack_overflow.csv')

with open('answers.json', 'r') as answers:
    formatted_answers = format_rows(json.load(answers), "answer")
    just_write(formatted_answers, 'stack_overflow.csv')

# test_connection()

get_count_of_json("answers.json")
