from flask import Flask, request, jsonify
import openai
import os

# Initialize the Flask application
app = Flask(__name__)

# Set your OpenAI API key here (ensure the key is set as an environment variable)
openai.api_key = os.getenv('OPENAI_API_KEY')  # Ensure this is properly set in Render's environment variables

@app.route('/')
def home():
    return "Welcome to the Legal Chatbot!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the message from the incoming JSON request
        data = request.get_json()
        message = data.get('message')

        # If message is empty or not provided, return an error
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        # Call OpenAI API to get a response
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can change this to another model if needed
            prompt=message,
            max_tokens=150
        )
        
        # Extract the assistant's reply from the API response
        reply = response.choices[0].text.strip()

        # Return the reply as a JSON response
        return jsonify({"reply": reply})
    
    except Exception as e:
        # If there's an error, return the error message
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the app with the Flask development server (only for local testing)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
