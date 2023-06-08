from flask import Flask, render_template, redirect, url_for,request,send_file
import random
import string
from PIL import Image, ImageDraw, ImageFont
import os
from flask_login import login_required
app = Flask(__name__)
# Set the secret key for encrypting session data
app.secret_key = 'your-secret-key'
# Set the upload folder path
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Set the download folder path
app.config['DOWNLOAD_FOLDER'] = 'static/downloads/'

@app.route('/')
def index():
    return render_template('form.html')
@app.route("/cancer")
@login_required
def cancer():
    return render_template("cancer.html")
# Function to generate a 6 digit unique ID
def generate_id():
    return ''.join(random.choices(string.digits, k=6))

# Route to handle form submission for health card
@app.route('/submit', methods=['POST'])
def submit_form():
    # Get form data
    name = request.form['name']
    dob = request.form['dob']
    address = request.form['address']
    gender = request.form['gender']
    contact = request.form['contact']
    bloodgroup = request.form['bloodgroup']
    profile_pic = request.files['profile_pic']

    # Generate a unique health ID
    health_id = generate_id()
   
    # Save the uploaded profile picture
    filename = profile_pic.filename
    filename=filename.split('.')
    filename=health_id+'.'+filename[1]
    profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    # Create a new PIL Image object for the health card
    card_width = 700
    card_height = 500
    card_color = (250, 251, 255)
    card_image = Image.new('RGB', (card_width, card_height), color=card_color)

    # Draw the profile picture on the health card
    profile_pic_width = 200
    profile_pic_height = 200
    profile_pic_border = 5
    profile_pic_margin = 50
    profile_pic_image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)).resize((profile_pic_width, profile_pic_height))
    card_image.paste(profile_pic_image, (profile_pic_margin, profile_pic_margin))
    draw = ImageDraw.Draw(card_image)
    draw.rectangle((profile_pic_margin - profile_pic_border, profile_pic_margin - profile_pic_border, 
                    profile_pic_margin + profile_pic_width + profile_pic_border, profile_pic_margin + profile_pic_height + profile_pic_border), 
                    outline=(0, 0, 0), width=profile_pic_border)
    
    # Draw the patient details on the health card
    text_color = (0, 0, 0)
    text_margin = 300
    text_font = ImageFont.truetype('arial.ttf', size=30)
    draw.text((text_margin, profile_pic_margin), f"Name: {name}", fill=text_color, font=text_font)
    draw.text((text_margin, profile_pic_margin+50), f"Date of Birth: {dob}", fill=text_color, font=text_font)
    draw.text((text_margin, profile_pic_margin+150), f"Gender: {gender}", fill=text_color, font=text_font)
    draw.text((text_margin, profile_pic_margin+200), f"Contact: {contact}", fill=text_color, font=text_font)
    draw.text((text_margin, profile_pic_margin+250), f"Address: {address}", fill=text_color, font=text_font)
    draw.text((text_margin, profile_pic_margin+300), f"Blood Group: {bloodgroup}", fill=text_color, font=text_font)
    draw.text((text_margin, profile_pic_margin+350), f"Health ID: {health_id}", fill=text_color, font=text_font)

# Save the health card image
    card_filename = f"{health_id}.png"
    card_filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], card_filename)
    card_image.save(card_filepath)

# Render the form result template and pass the health ID and card URL
    return render_template('form_result.html', health_id=health_id,name=name,dob=dob,gender=gender,contact=contact,address=address,bloodgroup=bloodgroup,profile_pic_image=profile_pic_image,card_url=card_filename)
@app.route('/result', methods=['GET'])
def display_result():
# Get health ID from query parameters
    health_id = request.args.get('health_id')
    
    card_filepath = os.path.join(app.config['DOWNLOAD_FOLDER'], f"{health_id}.png")
    
    return send_file(card_filepath, as_attachment=True)
# @app.route('/get_profile_pic/<health_id>')
# def get_profile_pic(health_id):
#     filename = health_id + '.jpg'
#     return send_file(app.config['UPLOAD_FOLDER'], filename)
if __name__ == '__main__':
	app.run(debug=True)