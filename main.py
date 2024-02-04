import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
from google.oauth2 import service_account
import base64
from flask import Flask, jsonify, request 
from flask_restful import Resource, Api 
from flask_cors import CORS

def encode_image_to_base64(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            base64_encoded = base64.b64encode(image_file.read()).decode('utf-8')
        return base64_encoded
    except Exception as e:
        print(f"Error encoding image to Base64: {e}")
        return None

def generate(imageData):
  credentials = service_account.Credentials.from_service_account_file('tia-ai.json')
  vertexai.init(project='tia-ai',credentials=credentials),
  model = GenerativeModel("gemini-pro-vision")
#   base64_encoded_image = encode_image_to_base64('lonely_bhavesh.jpg')
#   print(base64_encoded_image == imageData) 
  image = Part.from_data(data=base64.b64decode(imageData), mime_type="image/jpeg")
  responses = model.generate_content(
    ["""What is this""", image],
    generation_config={
        "max_output_tokens": 2048,
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32
    },
    safety_settings=[],
  stream=True,
  )
  for response in responses:
    print(response.text, end="")
    return response.text


def flaskinit():
    app = Flask(__name__) 
    api = Api(app)  
    CORS(app, origins="http://localhost:4200", allow_headers="Content-Type")
    class GetResponse(Resource): 
        def post(self): 
            data = request.get_json()     
            response = generate(data['imageData']) 
            return jsonify({"response": response})
            
    api.add_resource(GetResponse, '/getImage') 
    app.run(debug = True) 
  

if __name__ == '__main__': 
    flaskinit()
  
