from flask import Flask, jsonify
from linkedin_api import Linkedin
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

#initialize data - THIS ONLY NEEDS TO RUN ONCE
linkedin_email = os.getenv("LINKEDIN_EMAIL")
linkedin_password = os.getenv("LINKEDIN_PASSWORD")
api = Linkedin(linkedin_email, linkedin_password)


def normalize_profile(profile):
    profile.pop("$anti_abuse_metadata")
    profile.pop("elt")
    profile.pop("entityUrn")
    for experience in profile["experience"]:
        experience.pop("$anti_abuse_metadata")
        experience.pop("entityUrn")
    profile.pop("profile_id")
    profile.pop("profile_urn")

def normalize_connections(connections):
    for connection in connections:
        connection.pop("distance")

@app.route("/<name>")
def get_data(name):
    
    result = None
    try:
        profile = normalize_profile(api.get_profile(name))
        contact_info = api.get_profile_contact_info(name)
        connections = normalize_connections(api.get_profile_connections('1234asc12304'))
        result = jsonify({
        "status" : "success",
        "body" : {
        "profile": profile,
        "contact_info": contact_info,
        "connections": connections
        }
        })
    # TODO: Exception handler for specific exception
    except Exception as e:
        result = jsonify({
            "status" : "error",
            "body" : {
                "error" : e
            }
        })
    return result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
