from flask import Flask, render_template, redirect, url_for, request
from bson.objectid import ObjectId
from pymongo import MongoClient
import os

host = os.environ.get('DB_URL')
client = MongoClient(host=host)
db = client.charityTracker
donations = db.donations
amounts = db.amounts
amount_sum = 0
sorted_donations = []
app = Flask(__name__)

def returnSum():
    amount_list =[]
    for donation in donations.find():
        donation_amount = donation.get('amount')
        if donation_amount != '':
            donation_amount = float(donation_amount)
            amount_list.append(donation_amount)
    # print(amount_list)
    amount_sum = sum(amount_list)
    print(amount_sum)

    return str(amount_sum)

def sortDonations(selected_category):
    sorted_donations=[]
    for donation in donations.find():
        donation_category = donation['category']
        if donation_category == selected_category:
            sorted_donations.append(donation)
    return sorted_donations


@app.route('/')
def index():
    amount_sum = returnSum()
    return render_template('donations_index.html', donations=donations.find(), amount_sum = amount_sum)

# creates a new donation
@app.route('/donations/new')
def donations_new():
    return render_template('donations_new.html', donation={}, title='New Donation')

# the form to make a new donation
@app.route('/donations', methods=['POST'])
def donations_submit():
    donation = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'amount': request.form.get('amount'),
        'category':request.form.get('category'),
        'date': request.form.get('date')
    }
    donations.insert_one(donation)
    return redirect (url_for('index'))

# shows a single donation
@app.route('/donations/<donation_id>')
def donations_show(donation_id):
    donation = donations.find_one({'_id': ObjectId(donation_id)})
    return render_template('donations_show.html', donation=donation)

# edit a donation
@app.route('/donations/<donation_id>/edit')
def donations_edit(donation_id):
    donation = donations.find_one({'_id': ObjectId(donation_id)})
    return render_template('donations_edit.html', donation=donation, title='Edit Donation')

# update a donation
@app.route('/donations/<donation_id>/', methods=['POST'])
def donations_update(donation_id):
    updated_donation = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'amount': request.form.get('amount'),
        'category':request.form.get('category'),
        'date': request.form.get('date')
    }
    # set the former playlist to the new one we just updated/edited
    donations.update_one(
        {'_id': ObjectId(donation_id)},
        {'$set': updated_donation})
    # take us back to the playlist's show page
    return redirect(url_for('donations_show', donation_id=donation_id))


# deletes a playlist
@app.route('/donations/<donation_id>/delete', methods=['POST'])
def donations_delete(donation_id):
    donations.delete_one({'_id': ObjectId(donation_id)})
    return redirect(url_for('index'))


@app.route('/donations/sort', methods=['GET','POST'])
def donations_sort():
    print("sort button clicked")
    selected_category = request.values.get('select-category')
    print(selected_category)
    sorted_donations = sortDonations(selected_category)
    return render_template('donations_sort.html', sorted_donations=sorted_donations)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))