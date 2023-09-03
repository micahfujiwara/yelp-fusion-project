from flask import Flask, render_template, request
from yelpapi import YelpAPI
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
api_key = os.getenv("API_KEY")

# Check for valid Yelp API credentials
if not client_id or not api_key:
    raise ValueError("Please set the CLIENT_ID and API_KEY environment variables.")

# Initialize Yelp API
yelp_api = YelpAPI(api_key)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        search_term = request.form.get("search_term")
        location = request.form.get("location")
        limit = request.form.get("limit", 10)

        try:
            search_results = yelp_api.search_query(
                term=search_term, location=location, limit=limit
            )
            businesses = search_results.get("businesses", [])
        except Exception as e:
            businesses = []
            error_message = f"An error occurred: {str(e)}"
            return render_template("index.html", businesses=businesses, error_message=error_message)

        return render_template("index.html", businesses=businesses)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
