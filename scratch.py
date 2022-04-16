from asyncore import write
from helper import write_to_json_file
import requests
import json

def get_forum_topics(category):
    page = 0
    paramaters = {"detail": 1, "filter": 1}
    response = requests.get(f'https://scratchdb.lefty.one/v3/forum/category/topics/{category}/{page}', params=paramaters)
    write_to_json_file(response.json(), 'forum_topics_list.json')
    # return response.json()

def get_post_info(post_id):
    response = requests.get(f"https://scratchdb.lefty.one/v3/forum/post/info/{int(post_id)}")
    write_to_json_file(response.json(), 'example_post_info.json')
    # return response.json()

def get_topic_post_list(forum_topic):
    response = requests.get(f"https://scratchdb.lefty.one/v3/forum/topic/posts/{forum_topic['id']}/")
    write_to_json_file(response.json(), 'topic_list.json')
    #return response.json()

def get_data():
    forum_topics = get_forum_topics("Help with Scripts")
    for topic in forum_topics:
        print(f"Topic ID: {topic['id']}")
    i = 1
    topic_posts = []
    while i < 4:
        topic_post_list = get_topic_post_list(forum_topics[i])
        print(f"Posts acquired: {len(topic_post_list)} posts for topic {forum_topics[i]['id']}")
        topic_posts.append(topic_post_list)
        i += 1
    write_to_json_file(topic_posts, 'topic_posts.json')

get_forum_topics("Help with Scripts")