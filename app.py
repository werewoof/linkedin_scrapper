from flask import Flask, jsonify
from linkedin_api import Linkedin
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route("/<name>")
def get_data(name):
    # Initialize your scraper

    # Example LinkedIn API usage
    linkedin_email = os.getenv("LINKEDIN_EMAIL")
    linkedin_password = os.getenv("LINKEDIN_PASSWORD")

    api = Linkedin(linkedin_email, linkedin_password)
    profile = api.get_profile(name)
    contact_info = api.get_profile_contact_info(name)
    connections = api.get_profile_connections('1234asc12304')

    return jsonify({
        "profile": profile,
        "contact_info": contact_info,
        "connections": connections
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
