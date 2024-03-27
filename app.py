from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://ajengadiar1:sparta@cluster0.1xoa3iw.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_recive = request.form['bucket_give']
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {
        'num': num, 
        'bucket': bucket_recive, 
        'done': 0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    sample_receive = request.form['sample_give']
    print(sample_receive)
    return jsonify({'msg': 'POST /bucket/done request!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets = list(db.bucket.find({}, {'_id': 0}))
    return jsonify({'buckets': buckets})

@app.route("/delete", methods=["POST"])
def delete_item():
    num = request.form.get('num_give')
    if num is None:
        return jsonify({'msg': 'Error: Missing num parameter'}), 400
    
    try:
        num = int(num)
    except ValueError:
        return jsonify({'msg': 'Error: Invalid num parameter'}), 400

    result = db.bucket.delete_one({'num': num})
    if result.deleted_count == 0:
        return jsonify({'msg': f'Error: Item with num {num} not found'}), 404

    return jsonify({'msg': f'Item with num {num} deleted successfully'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)