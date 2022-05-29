from markdown2html import markdown2html
from cors import crossdomain
from replit import db
from flask import *
import json
import uuid

app = Flask(__name__, template_folder='', static_folder='')

@crossdomain(origin="localhost")
@app.route("/posts/all", methods=["GET"])
def all_posts():
  return jsonify(json.loads(db.get_raw("posts")))

@crossdomain(origin="localhost")
@app.route("/posts/add", methods=["POST"])
def add_post():
  data = request.json
  tempuuid = str(uuid.uuid4())
  data["id"] = tempuuid
  data["content"] = markdown2html(data["content"])
  data["comments"] = []
  db["posts"].append(data)
  return ""

@crossdomain(origin="localhost")
@app.route("/posts/comments/<post_id>", methods=["POST"])
def add_comment(post_id):
  for ind, post in enumerate(json.loads(db.get_raw("posts"))):
    if post["id"] == post_id:
      db["posts"][ind]["comments"].append(request.json)
  return ""

@crossdomain(origin="localhost")
@app.route("/blogs/all", methods=["GET"])
def all_blogs():
  blogs = json.loads(db.get_raw("blogs"))
  blogs.sort(key=lambda info: info["rating"], reverse=True)
  return jsonify(blogs)

@crossdomain(origin="localhost")
@app.route("/blogs/add", methods=["POST"])
def add_blogs():
  data = request.json
  tempuuid = str(uuid.uuid4())
  data["id"] = tempuuid
  data["content"] = markdown2html(data["content"])
  data["rating"] = 0
  db["blogs"].append(data)
  return ""

@crossdomain(origin="localhost")
@app.route("/blogs/rate/<blog_id>", methods=["POST"])
def add_rate(blog_id):
  for ind, blog in enumerate(json.loads(db.get_raw("blogs"))):
    if blog["id"] == blog_id:
      db["blogs"][ind]["rating"] += 1
  return ""

app.run(host='0.0.0.0')
