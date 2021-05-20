import aiml


kernal = aiml.Kernel()
kernal.learn("./std-startup.xml")
kernal.respond("load aiml b")


while True:
    input_text = input("Human> ")
    response = kernal.respond(input_text)
    print("Bot> "+response)
