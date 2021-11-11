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
def playlists_new():
    return render_template('donations_new.html', donation={}, name='New Playlist')

# Note the methods parameter that explicitly tells the route that this is a POST
@app.route('/donations', methods=['POST'])
def playlists_submit():
    donation = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
    }
    donations.insert_one(donation)
    return redirect (url_for('index'))

@app.route('/donations/<donation_id>')
def playlists_show(donation_id):
    """Show a single playlist."""
    donation = donations.find_one({'_id': ObjectId(donation_id)})
    return render_template('donations_show.html', donation=donation)

@app.route('/donations/<donation_id>/delete', methods=['POST'])
def playlists_delete(donation_id):
    """Delete one playlist."""
    donations.delete_one({'_id': ObjectId(donation_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))