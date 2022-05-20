import json
from math import ceil
from auth import get_site
from helper import calculate_next_page, sort_by_answers, write_to_json_file, write_to_csv_file, convert_from_epoch, just_write

SITE = get_site()
headers = ["forum", "type", "date_posted", "author_id", "author_username", "post_id", "parent_question_user_id", "parent_question_username", "parent_question_id", "title", "body"]
def get_200_most_answered_questions(tags):
    questions = SITE.fetch('search/advanced', sort="creation", order="desc", tagged=tags, answers="11", pagesize="100", filter="withbody")
    print(f'Retrieved {len(questions["items"])} questions')
    sorted_questions = sort_by_answers(questions["items"])
    print(f'Saving {len(sorted_questions[0:200])} questions')
    write_to_json_file(sorted_questions[0:200], 'question_file.json')

def get_answers(questions, pagesize):
    ids = []
    answers = []
    answer_count = 0
    for question in questions:
        answer_count += question.get('answer_count')
        ids.append(question.get('question_id'))
    print(f"Expecting {answer_count} answers.")
    answers = call_for_answers(ids, pagesize)
    print(f"Answers collected: {len(answers)}")
    write_to_json_file(answers, 'answers.json')

def create_batches(ids, pagesize):
    print(f"Count for ids: {len(ids)}")
    total_batches = ceil(len(ids)/pagesize)
    print(f"Calculated batches: {total_batches}")
    return total_batches

def get_all_answers_for_single_batch(ids, pagesize):
    print(f"Ids being processed are: {ids[:5]}...{ids[-5:]}")
    first_fetch = fetch_next_page(ids, 1, pagesize)
    has_more = first_fetch.get('has_more')
    message = "But wait there's more!" if has_more is True else "That's all folks!"
    print(message)
    page = first_fetch.get('page')
    print(f"The current page is {page}")
    current_answers = first_fetch.get('items')
    while has_more is True:
        next_page = calculate_next_page(page)
        next_fetch = fetch_next_page(ids, next_page, pagesize)
        temp_answers = append_new_answers(current_answers, next_fetch.get('items'))
        current_answers = temp_answers
        has_more = next_fetch.get('has_more')
        print(message)
        print(f"Current count is {len(current_answers)}")
        if has_more is True:
            page = next_fetch.get('page')
    print(f"Total answers returned for ids {ids[:5]}...{ids[-5:]}: {len(current_answers)}")
    return current_answers

def append_new_answers(current_answers, new_answers):
    print(f"Adding to current_answers: {new_answers}")
    all_answers = current_answers + new_answers
    return all_answers

def fetch_next_page(ids, next_page, pagesize):
    return SITE.fetch('questions/{ids}/answers', ids=ids, page=next_page, pagesize=pagesize, filter="withbody")

def calculate_next_page(page):
    next_page = calculate_next_page(page)
    print(f"Getting next page {next_page}")
    return next_page

def call_for_answers(ids, pagesize):
    all_answers = []
    if len(ids) > pagesize:
        batches_to_process = create_batches(ids, pagesize)
        print(f"Batches we expect to process {batches_to_process}")
    id_start = 0
    id_end = pagesize - 1
    end_of_list = len(ids) - 1
    should_end = False
    while should_end is False:
        should_end = True if id_end == end_of_list else False
        print(f"Processing {id_start} to {id_end}")
        batch_answers = get_all_answers_for_single_batch(ids[id_start:id_end])
        all_answers += batch_answers
        if should_end is False:
            id_start, id_end = calculate_id_start_stop(id_start, id_end, end_of_list, pagesize)
    return all_answers

def calculate_id_start_stop(id_start, id_end, end_of_list, pagesize):
    id_start += pagesize
    id_end += pagesize
    if id_end > end_of_list:
        id_end = end_of_list
    return (id_start, id_end)

def locate_question_author(question_id):
    with open('question_file.json', 'r') as raw_questions:
        questions = json.load(raw_questions)
        for question in questions:
            if question.get('question_id') == question_id:
                return (question.get('owner').get('user_id'), question.get('owner').get('display_name'))

def format_rows(posts, post_type):
    print(f"Data received.\nType: {post_type}\nItem Count: {len(posts)}")
    formatted_data = []
    for post in posts:
        if post_type == "answer":
            parent_user_id, parent_display_name = locate_question_author(post.get('question_id'))
        else:
            parent_user_id = post.get('owner').get('user_id')
            parent_display_name = post.get('owner').get('display_name')
        post_id = post.get('question_id') if post_type == "question" else post.get('answer_id')
        formatted_row = [
                "SO", 
                post_type, 
                convert_from_epoch(post.get('creation_date')), 
                post.get('owner').get('user_id'), 
                post.get('owner').get('display_name'), 
                post_id,
                parent_user_id,
                parent_display_name,
                post.get('question_id'), 
                post.get('title'), 
                post.get('body')
            ]
        formatted_data.append(formatted_row)
    return formatted_data

get_200_most_answered_questions("r")

with open('question_file.json', 'r') as raw_questions:
    questions = json.load(raw_questions)
    get_answers(questions)

with open('question_file.json', 'r') as raw_questions:
    questions = json.load(raw_questions)
    formatted_questions = format_rows(questions, "question")
    write_to_csv_file(headers, formatted_questions, 'stack_overflow.csv')

with open('answers.json', 'r') as answers:
    formatted_answers = format_rows(json.load(answers), "answer")
    just_write(formatted_answers, 'stack_overflow.csv')

