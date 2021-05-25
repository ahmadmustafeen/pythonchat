import os
import aiml
from flask.templating import render_template
from types import MethodType
from flask import Flask, jsonify, request
import sys
import numpy as np
from tensorflow import keras
model = keras.models.load_model('./')
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
kernal.learn("brain/biography.aiml")
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


User_Symptoms = np.zeros(13).tolist()


@app.route("/", methods=["POST", "GET"])
def home():
    if (request.method == "POST"):
        userMessage = str(request.form["nm"])
        if ((userMessage).lower() == "say"):
            response = "You are suffering from: "
            for x in range(len(symtopms)):
                response = response + "<br>" + (symtopms[x])
            return jsonify({
                "response": True,
                "message": symtopms,
                "things": User_Symptoms
            })
        response = (kernal.respond(userMessage)).upper()
        listorwords = response.split(" ")
        if((userMessage).lower() == "model"):
            return jsonify({
                "response": True,
                "message": "You may be suffering from Dengue" if(str(round(model.predict([User_Symptoms])[0][0])) == '1') else "Atleast you are not suffering from Dengue but take care or consult a doctor",
                "things": str((model.predict([User_Symptoms])[0][0]))
            })
        if(True):
            if(len(listorwords) < 3):
                return "False"
            elif((listorwords[3]) == "SYMPTOMS"):
                symtopms.append((listorwords[5]))
                for x in range(len(symtopms)):
                    for i in range(len(KNOWN_SYMPTOMS)):
                        if(str(symtopms[x]).upper() == str(KNOWN_SYMPTOMS[i]).upper()):
                            User_Symptoms[i] = 1
            return jsonify({
                "status": 200,
                "response": True,
                "message": str(kernal.respond(userMessage))
            })


if __name__ == "__main__":
    app.run(debug=True)
