from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
import flask

app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://accretioadmin:adminaccretio&2017@localhost:27017/topic_detection?authSource=admin"
mongo = PyMongo(app)


@app.route("/word-clouds/")
def read_topics():
    topics = mongo.db.topic.find({},{'_id': False})
    return flask.jsonify({"word-cloud":[topic["word-cloud"] for topic in topics]})

@app.route("/update_topic_name/<int:topic_id>/<topic_new_name>")
def update_topic(topic_id, topic_new_name):
    data = {"idtopic":topic_id, "assigned_name":topic_new_name}
    last_word = dict()
    for key in data.keys():
        print("key = ", key)
        last_word[f"word-cloud.$.{key}"] = data[key]
    mongo.db.topic.find_and_modify(
    query = {'idtopic': topic_id, 'word-cloud.idtopic':topic_id},
    update = { "$set": last_word })
    result = mongo.db.topic.update_one({'idtopic': topic_id}, {"$set": {'assigned_name':topic_new_name}})
    return result.raw_result



cors = CORS(app, resources={r"/*": {"origins": "*"}}) 


if __name__ == "__main__":
    app.run()
