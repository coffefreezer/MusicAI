from google import genai
KEY = "API key here"
client = genai.Client(api_key=KEY)

for model in client.models.list():
    print(model.name)
