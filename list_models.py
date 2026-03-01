from google import genai
KEY = "AIzaSyBzIdZAcztMjzCUIggJQPLU4NRKdo3jO2o"
client = genai.Client(api_key=KEY)

for model in client.models.list():
    print(model.name)