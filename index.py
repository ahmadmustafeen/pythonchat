from types import MethodType
from flask import Flask, jsonify, request
import sys

from flask.templating import render_template
import aiml
import os
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

KNOWN_SYMPTOMS = ['Nausea', 'vomiting', 'Rash', 'eye pain', 'muscle pain', 'bone pain',
                  'Belly pain', 'tenderness', 'Vomiting', 'Bleeding', 'Vomiting', 'Feeling tired', 'restless']


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
                "message": symtopms
            })
        response = (kernal.respond(userMessage)).upper()
        listorwords = response.split(" ")
        if(True):
            if(len(listorwords) < 3):
                return "False"
            elif((listorwords[3]) == "SYMPTOMS"):
                symtopms.append((listorwords[5]))
                for x in range(len(symtopms)):
                    print(symtopms[x])
            return jsonify({
                "status": 200,
                "response": True,
                "message": str(kernal.respond(userMessage))
            })


if __name__ == "__main__":
    app.run(debug=True)
