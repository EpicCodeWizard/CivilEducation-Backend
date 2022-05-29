from markdown2html import markdown2html
from cohere.classify import Example
from cors import crossdomain
from replit import db
from flask import *
import cohere
import json
import uuid

app = Flask(__name__, template_folder="", static_folder="")
co = cohere.Client("2H7QHvLLgO1HK4kzz6w7EBLpoEHVJnYOTH0UbGF5")
dataset = [Example(x.split("\t")[1], x.split("\t")[0]) for x in open("preds.txt", "r").read().split("\n")]

@crossdomain(origin="*")
@app.route("/posts/all", methods=["GET"])
def all_posts():
  return jsonify(json.loads(db.get_raw("posts")))

@crossdomain(origin="*")
@app.route("/posts/add", methods=["POST"])
def add_post():
  data = request.json
  tempuuid = str(uuid.uuid4())
  data["id"] = tempuuid
  data["content"] = markdown2html(data["content"])
  data["comments"] = []
  db["posts"].append(data)
  return ""

@crossdomain(origin="*")
@app.route("/posts/get/<post_id>", methods=["GET"])
def get_post(post_id):
  for ind, post in enumerate(json.loads(db.get_raw("posts"))):
    if post["id"] == post_id:
      return json.loads(db.get_raw("posts"))[ind]

@crossdomain(origin="*")
@app.route("/posts/comments/<post_id>", methods=["POST"])
def add_comment(post_id):
  classifications = co.classify(model="medium", taskDescription="The following is a sentiment classifier regarding comments for our civil education application", outputIndicator="this is:", inputs=[request.json["content"]], examples=dataset).classifications
  for x in classifications:
    if x.prediction == "positive":
      for ind, post in enumerate(json.loads(db.get_raw("posts"))):
        if post["id"] == post_id:
          db["posts"][ind]["comments"].append(request.json)
    else:
      return jsonify({"nlp": "Our NLP processor recognized this as a negative comment. It said your comment was " + str(round(x.confidence[0].confidence*100, 2)) + "% negative. Please rephrase your comment."})
    return ""

@crossdomain(origin="*")
@app.route("/blogs/all", methods=["GET"])
def all_blogs():
  blogs = json.loads(db.get_raw("blogs"))
  blogs.sort(key=lambda info: info["rating"], reverse=True)
  return jsonify(blogs)

@crossdomain(origin="*")
@app.route("/blogs/add", methods=["POST"])
def add_blogs():
  data = request.json
  tempuuid = str(uuid.uuid4())
  data["id"] = tempuuid
  data["content"] = markdown2html(data["content"])
  data["rating"] = 0
  db["blogs"].append(data)
  return ""

@crossdomain(origin="*")
@app.route("/blogs/get/<blog_id>", methods=["GET"])
def get_blog(blog_id):
  for ind, blog in enumerate(json.loads(db.get_raw("blogs"))):
    if blog["id"] == blog_id:
      return json.loads(db.get_raw("blogs"))[ind]

@crossdomain(origin="*")
@app.route("/blogs/rate/<blog_id>", methods=["GET"])
def add_rate(blog_id):
  for ind, blog in enumerate(json.loads(db.get_raw("blogs"))):
    if blog["id"] == blog_id:
      db["blogs"][ind]["rating"] += 1
  return ""

app.run(host="0.0.0.0")
