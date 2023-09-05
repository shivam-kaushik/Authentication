import logging

from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from Tables.TableImagePair import getimagePair, insertTableImagePairs
from Tables.TableImages import getImageidFromTableImages
from Tables.TableUserKeyPoints import getDataFromTableUserKeyPoints, getDataFromTableUsers, getKeyPointsFromTableUserKeyPoints, insertTableUserKeyPoints, insertTableUser

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    return render_template('new_signup.html')

@app.route('/login_token', methods=['POST', 'GET'])
def login():
    username = session.get('username')  # Retrieve username from session
    if username:
        selected_imagesfromhtml = request.json['images']
        allimages = request.json['gridimages']
        selected_images = []
        keypoint_images = []
        compare_images = []
        for i in range(len(selected_imagesfromhtml)-1, -1,-1):
            j = selected_imagesfromhtml[i].strip("http://127.0.0.1:5000/")
            j = j.replace("static/", "..\static\\")
            id = getImageidFromTableImages(j)
            selected_images.append(id)
            
        oldKeyPointsList = getKeyPointsFromTableUserKeyPoints(username)
        print(oldKeyPointsList)
                  
        old_images = []            
        for i in oldKeyPointsList:
            i = int(i)
            if i < 4:
                image_index = i-1
                old_images.append(allimages[image_index]) 
            else:
                if i >= 4: 
                    image_index = i  
                    old_images.append(allimages[image_index])  
                    
        for i in old_images:
            j = i.strip("http://127.0.0.1:5000/")
            j = j.replace("static/", "..\static\\")
            id = getImageidFromTableImages(j)
            keypoint_images.append(id)

        for i in keypoint_images:
            compare_images.append(getimagePair(username, i))

        if selected_images == compare_images:
            jsonify({'success': 'Login is successful!'})
        else:
            return jsonify({'error': 'Login is not successful!'})
        
    #   select imageid2 from ImagePairs where username='myuser1' and imageid1=4 UNION select imageid1 from ImagePairs where username='myuser1' and imageid2=4
    return jsonify({'error': 'User not found'})

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    result = getDataFromTableUsers(username)
    if result == '1':
        getDataFromTableUsers(username)
    else:
        insertTableUser(username)
    session['username'] = username  # Store username in session
    return redirect(url_for('enrollment'))

@app.route('/enrollment')
def enrollment():
    return render_template('new_enrollment.html')

@app.route('/home', methods=['GET', 'POST'])
def home_page():
    return render_template('login_successful.html')

@app.route('/store_key_position', methods=['GET', 'POST'])
def store_key_position():
    username = session.get('username')  # Retrieve username from session
    if username:
        keyPoint = list(request.form.get('keyPoint', ''))
        insertTableUserKeyPoints(username, keyPoint)

        # Create image pairs from the grid
        grid_items = request.form.getlist('gridItem')
        image_pairs = []
        for i in range(0, len(grid_items), 2):
            image_pair = (grid_items[i], grid_items[i+1])
            image_pairs.append(image_pair)

        # Store image pairs in the database
        for image_pair in image_pairs:
             image1 = image_pair[0]
             image2 = image_pair[1]
             image1_id = getImageidFromTableImages(image1)
             image2_id = getImageidFromTableImages(image2)

            # Insert image pairs into the "imagepairs" table
             insertTableImagePairs(username, image1_id, image2_id)

        return render_template('login_token.html')
    else:
        return jsonify({'error': 'User not found'})

if __name__ == '__main__':
    app.run(debug=True)
