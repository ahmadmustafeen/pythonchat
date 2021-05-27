import os
import aiml
from flask.templating import render_template
from types import MethodType
from flask import Flask, jsonify, request
import sys
import numpy as np
from tensorflow import keras
import difflib
# import mimetypes
# import logging
# from console_log import ConsoleLog
# mimetypes.add_type('application/javascript', '.mjs')
# console = logging.getLogger('console')
# console.setLevel(logging.DEBUG)
kernal = aiml.Kernel()
# for filename in os.listdir("brain"):
#     if filename.endswith(".aiml"):
#         kernal.learn("brain/"+filename)
# kernal.learn("brain/biography.aiml")
# kernal.learn("brain/badanswer.aiml")
kernal.learn("brain/basic_chat.aiml")
# kernal.learn("brain/client_profile.aiml")
# kernal.learn("brain/computers.aiml")


app = Flask(__name__)
symtopms = []


# @app.route("/", methods=["POST", "GET"])
# def home():
#     return "ASDA"

KNOWN_SYMPTOMS = ['Nausea', 'vomiting', 'Rash', 'eye_pain', 'muscle_pain', 'bone_pain',
                  'Belly_pain', 'tenderness', 'Vomiting', 'Bleeding', 'Vomiting', 'Feeling_tired', 'restless']
POSITIVE_DENGUE = "You may be suffering from Dengue"
NEGATIVE_DENGUE = "Atleast you are not suffering from Dengue but take care or consult a doctor"


User_Symptoms = np.zeros(13).tolist()


def responseApi(response, message, extra):
    return jsonify({
        "response": response,
        "message": message,
        "things": extra
    })


# def runModel():
#     return float((model.predict([User_Symptoms])[0][0]))


MODEL = keras.models.load_model('./')
Symptoms_TOLD = 0


@app.route("/", methods=["POST", "GET"])
def home():
    # enabling the use of global variables
    global Symptoms_TOLD
    if (request.method == "POST"):
        # inputs from form
        userMessage = str(request.form["message"]).lower()
        if (userMessage == "say"):
            responseMessage = "You are suffering from: "+str(Symptoms_TOLD)
            return responseApi(True, symtopms, responseMessage)
        response = (kernal.respond(userMessage)).upper()
        if((Symptoms_TOLD) > 2):
            correct_symptoms = 0
            for i in range(len(User_Symptoms)):
                # print(User_Symptoms[i])
                if(int(User_Symptoms[i]) == 1):
                    correct_symptoms += 1
            if(Symptoms_TOLD-correct_symptoms > 2):
                modelResponse = MODEL.predict([User_Symptoms])[0][0]
                if(str(round(modelResponse)) == '1'):
                    message = POSITIVE_DENGUE+", Confidence Level: " + \
                        str(MODEL.predict([User_Symptoms])[0][0]*100) + " % "
                else:
                    message = NEGATIVE_DENGUE
                return responseApi(True, message, str(modelResponse))
        listorwords = response.split(" ")
        if((userMessage).lower() == "model"):
            modelResponse = MODEL.predict([User_Symptoms])[0][0]
            if(str(round(modelResponse)) == '1'):
                message = POSITIVE_DENGUE+", Confidence Level: " + \
                    str(MODEL.predict([User_Symptoms])[0][0]*100) + " % "
            else:
                message = NEGATIVE_DENGUE
            return responseApi(True, message, str(modelResponse))

        if(True):
            related_words = [""]
            perfect_match = False
            if(len(listorwords) < 3):
                return responseApi(False, str(kernal.respond(userMessage)), "")
            elif((listorwords[3]) == "SYMPTOMS"):
                for symptom in KNOWN_SYMPTOMS:
                    if(listorwords[5].upper() != symptom.upper()):
                        Symptoms_TOLD += 1
                symtopms.append((listorwords[5]))
                related_words = difflib.get_close_matches(
                    listorwords[5].lower(), KNOWN_SYMPTOMS)
                for x in range(len(symtopms)):
                    for i in range(len(KNOWN_SYMPTOMS)):
                        if(str(symtopms[x]).upper() == str(KNOWN_SYMPTOMS[i]).upper()):
                            User_Symptoms[i] = 1
                            perfect_match = True
                        if(perfect_match != True):
                            return responseApi(True, "Kindly Type one or two", related_words)
            return responseApi(True, str(kernal.respond(userMessage)), related_words)


if __name__ == "__main__":
    app.run(debug=True)
