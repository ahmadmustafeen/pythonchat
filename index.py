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
for filename in os.listdir("brain"):
    if filename.endswith(".aiml"):
        kernal.learn("brain/"+filename)
# kernal.learn("brain/basic_chat.aiml")
# kernal.learn("brain/basicinfo.aiml")
# kernal.learn("brain/topicRedirecting.aiml")
# kernal.learn("brain/medicationInfo.aiml")
# kernal.learn("brain/SymtpomsTackling.aiml")


app = Flask(__name__)
symtopms = []
get = False
last_Keyword = ""

# @app.route("/", methods=["POST", "GET"])
# def home():
#     return "ASDA"

KNOWN_SYMPTOMS = [
    'nausea', 'nausea_s', 'rash','rash_s', 'eye_pain', 'eye_pain_s', 'muscle_pain', 'muscle_pain_s',
    'bone_pain', 'bone_pain_s', 'belly_pain', 'belly_pain_s', 'tendernes', 'tendernes_s', 'bleeding', 'bleeding_s', 'vomiting', 'vomiting_s', 'feeling_tired', 'feeling_tired_s', 'restles', 'restless_S', 'prognosis'
]


# JUST CAPITALIZING THE ENTIRE LIST (LATER TO BE CONVERTED INTO FUNCTION)
temp = []
for symptoms in range(len(KNOWN_SYMPTOMS)):
    temp.append(KNOWN_SYMPTOMS[symptoms].upper())
KNOWN_SYMPTOMS = temp


# CONSTANT MESSAGES
POSITIVE_DENGUE = "You may be suffering from Dengue"
NEGATIVE_DENGUE = "Atleast you are not suffering from Dengue but take care or consult a doctor"


# USERSYPMTOMS
User_Symptoms = np.zeros(22).tolist()


def responseApi(response, message, extra):
    return jsonify({
        "response": response,
        "message": message,
        "things": extra
    })


# def runModel():
#     return float((model.predict([User_Symptoms])[0][0]))

def renderAIML(userMessage):
    return str(kernal.respond(userMessage)).upper()


MODEL = keras.models.load_model('./')
Symptoms_TOLD = 0
LastKnownSymptoms = ""
last_response = ""


@app.route("/", methods=["POST", "GET"])
# def home():
#     userMessage = str(request.form["message"]).lower()
#     return(kernal.respond(userMessage))
def home():
    # enabling the use of global variables
    global Symptoms_TOLD
    global last_response
    global LastKnownSymptoms

    if (request.method == "POST"):
        # inputs from form
        userMessage = str(request.form["message"]).lower()
        print(userMessage)
        response = str(kernal.respond(userMessage)).upper()
        List_Of_Words_ = response.split(" ")
        # UNCOMMENT THIS LINE TO BYPASS ALL THE PYTHON CODE AND GET REPLY DIRECTLY FROM AIML
        # return responseApi(response, "userMessage", userMessage)

       # HARD CODED TO GET THE DATA USING WORD "SAY" IN API
        if (userMessage.upper() == "SAY"):
            responseMessage = "You are suffering from: "+str(Symptoms_TOLD)
            return responseApi(User_Symptoms, symtopms, responseMessage)

        # HARD CODED TO RUN THE MODEL USING WORD "MODEL" IN API
        if((userMessage).upper() == "MODEL" or (userMessage).upper() == 'NOW RUN MODEL' or (response).upper().__contains__("GREAT THAT WILL BE ALL")):
            modelResponse = MODEL.predict([User_Symptoms])[0][0]
            if(str(round(modelResponse)) == '1'):
                message = POSITIVE_DENGUE+", Confidence Level: " + \
                    str(MODEL.predict([User_Symptoms])[0][0]*100) + " % "
            else:
                message = NEGATIVE_DENGUE + " Chances of Dengue are: " + \
                    str(MODEL.predict([User_Symptoms])[0][0]*100) + " % "
            return responseApi(True, message, str(modelResponse))

        if((userMessage).isdigit() and last_response.__contains__("IN SCALE OF 1-10 HOW BAD IT IS")):
            print("disease sinority check worked")
            User_Symptoms[KNOWN_SYMPTOMS.index((LastKnownSymptoms+"_S").upper())] = int(userMessage)
            # LastKnownSymptoms = ""
            return responseApi(User_Symptoms, response+"h", "User_Symptoms")

        # THIS HERE KNOWS SYMPTOMS TOLD IF ARE MORE THAN 2 THAN IT WILL RUN THE MODEL AUTOMATICALLY
        # KEEPING IN MIND THAT SYMPTOMS ARE COUNTED WHICH ARE NOT AVAILABLE IN  KNOWN FUNCTIONS

        # if((Symptoms_TOLD) > 2):
        #     correct_symptoms = 0
        #     for i in range(len(User_Symptoms)):
        #         # print(User_Symptoms[i])
        #         if(int(User_Symptoms[i]) == 1):
        #             correct_symptoms += 1
        #     if(Symptoms_TOLD-correct_symptoms > 2):
        #         modelResponse = MODEL.predict([User_Symptoms])[0][0]
        #         if(str(round(modelResponse)) == '1'):
        #             message = POSITIVE_DENGUE+", Confidence Level: " + \
        #                 str(MODEL.predict([User_Symptoms])[0][0]*100) + " % "
        #         else:
        #             message = NEGATIVE_DENGUE + " Chances of Dengue are: " + \
        #                 str(MODEL.predict([User_Symptoms])[0][0]*100) + " % "
        #         return responseApi(True, message, str(modelResponse))

        if(len(List_Of_Words_) < 5):
            return responseApi(False, response, "D")
        # else:
        #     return str(len(List_Of_Words_))+response
        if((List_Of_Words_[3]) == "FEEL"):
            matched_sypmtoms = 0
            related_words = [""]

            # HERE WE ARE GOING TO TAKE RESPONSE OF OUR MATCHING SYMPTOMS
            # if(get == True):
            #     return responseApi("GREATE", "GREATE", "GREATE")

            # HERE WE WILL CHECK WHETHER USER TYPED SYMPTOMS ARE DEFINED OR HE HAVE MISTYPED
            if (List_Of_Words_[4]).upper() in KNOWN_SYMPTOMS:
                print("Great to proceed")
            else:
                # return responseApi(List_Of_Words_[5].upper(), KNOWN_SYMPTOMS, "")
                response = "Following   is not found in our known dictionary "
                # str(List_Of_Words_[5]) + \
                # " is not found in our known dictionary "
                # IF THERE IS  SUGGESTION IN THE KNOWN SYMPTOMS THEN USER IS REQUESTED TO ENTER THE NUMBER IN CHOICE OF IN TEXT AGAIN
                if(len(related_words) > 0):
                    response += "but we have following choices kindly choose: "
                    predicted_symptoms = difflib.get_close_matches(
                        List_Of_Words_[5].upper(), KNOWN_SYMPTOMS)
                    for i in range(len(predicted_symptoms)):
                        response = response + \
                            str(i+1) + ") " + str(predicted_symptoms[i]) + " "
                    return responseApi(response, predicted_symptoms, " vv")

                # SINCE THERE IS NO ELSE SO IF THERE IS NO SUGGESTION USERS SYMPTOMS WILL BE RECORDED

            # HAVING A GRAPH NOW HOW MUCH TOTAL SYMPTOMS ARE MATCHED IN OUR KNOWN
            for i in range(len(User_Symptoms)):
                if(User_Symptoms[i] == 1):
                    matched_sypmtoms += 1

            # IF  RESPONSE IS LESS THAN 3 WORDS THEN WILL RETURN AS FALSE BUT API WILL WORK FINE.
            if(len(List_Of_Words_) < 3):
                return responseApi(False, response, "FAILED")

            # CHECKING IF 4TH WORD IS SYMPTOMS SO WE CAN USE THIS CONCEPT TO EXCLUDE INFORMATION FROM THE AIML
            elif((List_Of_Words_[3]) == "FEEL"):

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
                if List_Of_Words_[4].upper() in symtopms:
                    print(symtopms.index(List_Of_Words_[4].upper()))

                # IF NOT ALREADY KNOWN
                else:

                    # THEN WE MATCH THAT SYMPTOMS IN DENGUE SYMPTOMS
                    if List_Of_Words_[4].upper() in KNOWN_SYMPTOMS:
                        # responseApi(List_Of_Words_[5], KNOWN_SYMPTOMS, "extra")
                        for i in range(len(KNOWN_SYMPTOMS)):
                            # IF SYMPTOMS IS IN DENGUE SYMPTOMSIT MAKES IT 1 IN USER_SYMPTOMS ELSE OTHERS ARE 0
                            if(List_Of_Words_[4].upper() == str(KNOWN_SYMPTOMS[i]).upper()):
                                User_Symptoms[i] = 1
                                LastKnownSymptoms = List_Of_Words_[4].upper()
                    # IF THEY ARE NOT IN KNOWN SYMPTOMS, WE SIMPLY ADD THEM IN USER KNOWN SYMPTOMS
                    else:
                        symtopms.append((List_Of_Words_[4]))

                related_words = difflib.get_close_matches(
                    List_Of_Words_[4].lower(), KNOWN_SYMPTOMS)
            last_response = response
            print("THIS WORKED")
            return responseApi(LastKnownSymptoms, response, "related_words")
        # else:
        return responseApi(False, response, "D")


if __name__ == "__main__":
    app.run(debug=True)
