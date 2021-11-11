from flask import Flask, render_template, redirect, url_for, request
from bson.objectid import ObjectId
from pymongo import MongoClient
import os

host = os.environ.get('DB_URL')
client = MongoClient(host=host)
db = client.charityTracker
donations = db.donations


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('donations_index.html', donations=donations.find())

# creates a new donation
@app.route('/donations/new')
def donations_new():
    return render_template('donations_new.html', donation={}, name='New Playlist')

# the form to make a new donation
@app.route('/donations', methods=['POST'])
def donations_submit():
    donation = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
    }
    donations.insert_one(donation)
    return redirect (url_for('index'))

# shows a single donation
@app.route('/donations/<donation_id>')
def donations_show(donation_id):
    donation = donations.find_one({'_id': ObjectId(donation_id)})
    return render_template('donations_show.html', donation=donation)

# deletes a playlist
@app.route('/donations/<donation_id>/delete', methods=['POST'])
def donations_delete(donation_id):
    donations.delete_one({'_id': ObjectId(donation_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))