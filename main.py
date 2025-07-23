from flask import Flask, request, jsonify
import requests
import vertexai
from vertexai.generative_models import GenerativeModel
from google import genai
 
app = Flask(__name__)
 
PROJECT_ID = "absolute-accord-465308-g0"
LOCATION = "us-central1"
 
# Initialize Vertex AI for Gemini use
vertexai.init(project=PROJECT_ID, location=LOCATION)
 
@app.route("/", methods=["POST"])
def webhook_handler():
    req = request.get_json()
    pan = req.get("sessionInfo", {}).get("parameters", {}).get("pan", "")
    user_query = req.get("text", {}).get("text", [""])[0]
 
    print("PAN:", pan)
    print("Query:", user_query)
 
    # 👉 If PAN exists, call the Cloud Function to fetch policy info
    if pan:
        try:
            print("pan is provided, calling policy API...")
            api_response = requests.post(
                "https://us-west1-absolute-accord-465308-g0.cloudfunctions.net/get_policy_by_pan1",
                headers={"Content-Type": "application/json"},
                json={"pan": pan}
            )
 
            if api_response.status_code != 200:
                raise Exception(f"API returned status {api_response.status_code}")
 
            api_data = api_response.json()
 
            if "error" in api_data:
                return jsonify({
                    "fulfillment_response": {
                        "messages": [
                            {"text": {"text": [f"❌ {api_data['error']}"]}}
                        ]
                    }
                })
 
            customer = api_data.get("customer_summary", {})
            policies = api_data.get("policies", [])
            display_message = api_data.get("display_message", "")
 
            if policies:
                policy_name = policies[0].get("policy_type", "Unknown Policy")
                status = policies[0].get("status", "N/A")
            else:
                policy_name = "No active policy"
                status = "N/A"
 
            return jsonify({
                "fulfillment_response": {
                    "messages": [
                        {"text": {"text": [f"✅ Policy Found for PAN {pan}"]}},
                        {"text": {"text": [f"{display_message}"]}}
                    ]
                },
                "session_info": {
                    "parameters": {
                        "policy_name": policy_name,
                        "policy_status": status
                    }
                }
            })
 
        except Exception as e:
            return jsonify({
                "fulfillment_response": {
                    "messages": [
                        {"text": {"text": [f"🚫 Error calling policy API: {str(e)}"]}}
                    ]
                }
            })
 
    # 👉 Else: Use Gemini 1.5 Pro for conversation
    try:
        print("No PAN provided, using Gemini for conversation...")
        client = genai.Client(vertexai=True, project="YOUR_PROJECT_ID", location="YOUR_LOCATION",)
        chat = client.chats.create(model="gemini-1.0-pro-002")
        response = chat.send_message(user_query)
 
        print("Gemini response:", response.text)
        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": [response.text]}}
                ]
            }
        })
 
    except Exception as e:
        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": [f"💥 Gemini error: {str(e)}"]}}
                ]
            }
        })
 
if __name__ == "__main__":
    app.run(debug=True)