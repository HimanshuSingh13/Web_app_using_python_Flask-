from flask import Flask,render_template,request,redirect
import speech_recognition as sr
from flask_cors import cross_origin
import pyttsx3
import requests
#import os
import uuid
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
   return render_template("index.html")
@app.route('/result',methods=["post","GET"])
@cross_origin()
def result():
    if request.method == 'POST':
        mytext = request.form['speech']
        gender = request.form['voices']
        engine=pyttsx3.init()
        engine.say(mytext)
        engine.runAndWait()
        return render_template('SPEECHTOTEXT.html')
    else:
        return render_template('SPEECHTOTEXT.html')
@app.route("/STT", methods=["GET", "POST"])
def STT():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)

    return render_template('STT.html', transcript=transcript)

@app.route('/ST', methods=['GET'])
def ST():
	return render_template('ST.html')


# code
@app.route('/ST', methods=['POST'])
def ST_post():
	# Read the values from the form
	original_text = request.form['text']
	target_language = request.form['language']

	# Load the values from .env
	key = "dc56b8aa751646459acd64805ed3a801"
	endpoint = "https://api.cognitive.microsofttranslator.com/"
	location = "centralindia"

	# Indicate that we want to translate and the API
	# version (3.0) and the target language
	path = '/translate?api-version=3.0'

	# Add the target language parameter
	target_language_parameter = '&to=' + target_language

	# Create the full URL
	constructed_url = endpoint + path + target_language_parameter

	# Set up the header information, which includes our
	# subscription key
	headers = {
		'Ocp-Apim-Subscription-Key': key,
		'Ocp-Apim-Subscription-Region': location,
		'Content-type': 'application/json',
		'X-ClientTraceId': str(uuid.uuid4())
	}

	# Create the body of the request with the text to be
	# translated
	body = [{'text': original_text}]

	# Make the call using post
	translator_request = requests.post(
		constructed_url, headers=headers, json=body)

	# Retrieve the JSON response
	translator_response = translator_request.json()

	# Retrieve the translation
	translated_text = translator_response[0]['translations'][0]['text']

	# Call render template, passing the translated text,
	# original text, and target language to the template
	return render_template(
		'STresults.html',
		translated_text=translated_text,
		original_text=original_text,
		target_language=target_language
	)

if __name__ == '__main__':
   app.run(debug = True)