'''
# Assignment
## Goal: create a microservice, which has two functions:
- merge the datastructures from the external interfaces into one single structure.
- act as a caching layer for the external interfaces.


## Data
Posts: http://jsonplaceholder.typicode.com/posts
Comments: http://jsonplaceholder.typicode.com/comments


## Plan of Approach
Let's start as simple as possible, by fetching the resources and merging them, thus focussing on going from two datastructures to one. From there we can build upon it, to create a caching middleware microservice.


Feel free to use any resource (Google, libraries, etc.) as you need.
'''
from itertools import groupby
from json import JSONEncoder
from typing import List, Dict
import json

from flask import Flask

import requests

url_posts = "http://jsonplaceholder.typicode.com/posts"
url_comments = "http://jsonplaceholder.typicode.com/comments"

app = Flask(__name__)

data = {}

class MyEncoder(JSONEncoder):
    def default(self, o):
        return json.dump({"id": o.post["id"], "comments": o.comments})

class Post:

    def __init__(self, post: Dict):
        self.post = post
        self.comments = []

    def add_comments(self, comments):
        self.comments += comments



def merge(posts: List[Dict], comments: List[Dict]) -> Dict:
    global data
    data = {post["id"]: Post(post) for post in posts}
    grouped_posts = groupby(comments, lambda c: c["postId"])
    for key, group in grouped_posts:
        data[key].add_comments(group)
    return data


def load() -> Dict:
    responce_posts = requests.get(url_posts)
    responce_comments = requests.get(url_comments)

    posts = responce_posts.json() if responce_posts else []
    comments = responce_comments.json() if responce_comments else []

    return merge(posts, comments)


@app.route("/")
def hello():
    return MyEncoder.encode(data)


def main():
    data = load()
    app.run()

if __name__ == '__main__':
    main()
