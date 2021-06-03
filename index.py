import os
import aiml
from flask.templating import render_template
from types import MethodType
from flask import Flask, jsonify, request
import sys
import numpy as np
from tensorflow import keras
import difflib
kernal = aiml.Kernel()
# for filename in os.listdir("brain"):
#     if filename.endswith(".aiml"):
#         kernal.learn("brain/"+filename)
kernal.learn("brain/basic_chat.aiml")


app = Flask(__name__)
symtopms = []
get = False
last_Keyword = ""

# @app.route("/", methods=["POST", "GET"])
# def home():
#     return "ASDA"

KNOWN_SYMPTOMS = ['Nausea', 'vomiting', 'Rash', 'eye_pain', 'muscle_pain', 'bone_pain',
                  'Belly_pain', 'tenderness', 'Vomiting', 'Bleeding', 'Vomiting', 'Feeling_tired', 'restless']


# JUST CAPITALIZING THE ENTIRE LIST (LATER TO BE CONVERTED INTO FUNCTION)
temp = []
for symptoms in range(len(KNOWN_SYMPTOMS)):
    temp.append(KNOWN_SYMPTOMS[symptoms].upper())
KNOWN_SYMPTOMS = temp


# CONSTANT MESSAGES
POSITIVE_DENGUE = "You may be suffering from Dengue"
NEGATIVE_DENGUE = "Atleast you are not suffering from Dengue but take care or consult a doctor"


# USERSYPMTOMS
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

        response = (kernal.respond(userMessage)).upper()
        print(userMessage + "userMessage")

       # HARD CODED TO GET THE DATA USING WORD "SAY" IN API
        if (userMessage.upper() == "SAY"):
            responseMessage = "You are suffering from: "+str(Symptoms_TOLD)
            return responseApi(User_Symptoms, symtopms, responseMessage)

        # HARD CODED TO RUN THE MODEL USING WORD "MODEL" IN API
        if((userMessage).upper() == "MODEL"):
            modelResponse = MODEL.predict([User_Symptoms])[0][0]
            if(str(round(modelResponse)) == '1'):
                message = POSITIVE_DENGUE+", Confidence Level: " + \
                    str(MODEL.predict([User_Symptoms])[0][0]*100) + " % "
            else:
                message = NEGATIVE_DENGUE + " Chances of Dengue are: " + \
                    str(MODEL.predict([User_Symptoms])[0][0]*100) + " % "
            return responseApi(True, message, str(modelResponse))

        # THIS HERE KNOWS SYMPTOMS TOLD IF ARE MORE THAN 2 THAN IT WILL RUN THE MODEL AUTOMATICALLY
            # KEEPING IN MIND THAT SYMPTOMS ARE COUNTED WHICH ARE NOT AVAILABLE IN  KNOWN FUNCTIONS
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
                    message = NEGATIVE_DENGUE + " Chances of Dengue are: " + \
                        str(MODEL.predict([User_Symptoms])[0][0]*100) + " % "
                return responseApi(True, message, str(modelResponse))
        List_Of_Words_ = response.split(" ")

        if(True):
            matched_sypmtoms = 0
            related_words = [""]

            # HERE WE ARE GOING TO TAKE RESPONSE OF OUR MATCHING SYMPTOMS
            if(get == True):
                return responseApi("GREATE", "GREATE", "GREATE")

            # HERE WE WILL CHECK WHETHER USER TYPED SYMPTOMS ARE DEFINED OR HE HAVE MISTYPED
            if (List_Of_Words_[5]).upper() in KNOWN_SYMPTOMS:
                print("sad")
            else:
                response = "Following " + \
                    List_Of_Words_[5] + \
                    " is not found in our known dictionary "
                # IF THERE IS  SUGGESTION IN THE KNOWN SYMPTOMS THEN USER IS REQUESTED TO ENTER THE NUMBER IN CHOICE OF IN TEXT AGAIN
                if(len(related_words) > 0):
                    response += "but we have following choices kindly choose: "
                    predicted_symptoms = difflib.get_close_matches(
                        List_Of_Words_[5].upper(), KNOWN_SYMPTOMS)
                    for i in range(len(predicted_symptoms)):
                        response = response + \
                            str(i+1) + ") " + str(predicted_symptoms[i]) + " "
                    return responseApi(response, predicted_symptoms, " ")

                # SINCE THERE IS NO ELSE SO IF THERE IS NO SUGGESTION USERS SYMPTOMS WILL BE RECORDED

            # HAVING A GRAPH NOW HOW MUCH TOTAL SYMPTOMS ARE MATCHED IN OUR KNOWN
            for i in range(len(User_Symptoms)):
                if(User_Symptoms[i] == 1):
                    matched_sypmtoms += 1

            # IF  RESPONSE IS LESS THAN 3 WORDS THEN WILL RETURN AS FALSE BUT API WILL WORK FINE.
            if(len(List_Of_Words_) < 3):
                return responseApi(False, str(kernal.respond(userMessage)), "")

            # CHECKING IF 4TH WORD IS SYMPTOMS SO WE CAN USE THIS CONCEPT TO EXCLUDE INFORMATION FROM THE AIML
            elif((List_Of_Words_[3]) == "SYMPTOMS"):

                # THIS CHECKS WHERE MIS-MATCHED SYMPTOMS ARE MORE THAN 3 AND THEN RUNS THE MODEL AND GIVES OUTPUT
                if(len(symtopms) >= 3):
                    modelResponse = MODEL.predict([User_Symptoms])[0][0]

                # WE HAVE A ROUNDOFF FUNCTION THEN IF IT'S 1 IT GIVE POSITIVE DENGUE
                    if(str(round(modelResponse)) == '1'):
                        message = POSITIVE_DENGUE+", Confidence Level: " + \
                            str(MODEL.predict([User_Symptoms])[
                                0][0]*100) + " % "

                # ELSE GIVE NEGATIVE DENGUE
                    else:
                        message = NEGATIVE_DENGUE + " Chances of Dengue are: " + \
                            str(MODEL.predict([User_Symptoms])[
                                0][0]*100) + " % "
                    return responseApi(True, message, str(modelResponse))

                # CHECKING IF ENTERED SYMPTOMS ALREADY KNOWN SYMPTOM OF USER OR NOT
                if List_Of_Words_[5].upper() in symtopms:
                    print(symtopms.index(List_Of_Words_[5].upper()))

                # IF NOT ALREADY KNOWN
                else:

                    # THEN WE MATCH THAT SYMPTOMS IN DENGUE SYMPTOMS
                    if List_Of_Words_[5] in KNOWN_SYMPTOMS:
                        for i in range(len(KNOWN_SYMPTOMS)):
                            # IF SYMPTOMS IS IN DENGUE SYMPTOMSIT MAKES IT 1 IN USER_SYMPTOMS ELSE OTHERS ARE 0
                            if(List_Of_Words_[5].upper() == str(KNOWN_SYMPTOMS[i]).upper()):
                                User_Symptoms[i] = 1
                    # IF THEY ARE NOT IN KNOWN SYMPTOMS, WE SIMPLY ADD THEM IN USER KNOWN SYMPTOMS
                    else:
                        symtopms.append((List_Of_Words_[5]))

                related_words = difflib.get_close_matches(
                    List_Of_Words_[5].lower(), KNOWN_SYMPTOMS)
            return responseApi(True, str(kernal.respond(userMessage)), related_words)


if __name__ == "__main__":
    app.run(debug=True)
