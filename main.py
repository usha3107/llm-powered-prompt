from classifier import classify_intent
from router import route_and_respond

while True:
    message = input("User: ")
    intent_data = classify_intent(message)
    response = route_and_respond(message, intent_data)
    print("\nAI:", response)