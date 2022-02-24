from helper import write_to_json_file
import requests

def get_topic_posts(category):
    page = 0
    paramaters = {"detail": 1, "filter": 1}
    response = requests.get(f'https://scratchdb.lefty.one/v3/forum/category/topics/{category}/{page}', params=paramaters)
    write_to_json_file(response.text, 'scratch_posts.json')

get_topic_posts("Help with Scripts")