import requests
import uuid
import datetime
from flask import jsonify
from config import Config
from models.transaction_model import DataTransaction


def generate_request_id():
    return str(uuid.uuid4())

def buy_data_service(phone_number, plan, network):
    request_id = generate_request_id()
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "username": Config.VTU_API_USERNAME,
        "password": Config.VTU_API_PASSWORD,
        "secret_key": Config.VTU_API_SECRET_KEY,
        "public_key": Config.VTU_API_PUBLIC_KEY,
        "serviceID": network,  # e.g., mtn, glo, airtel, etisalat
        "phone_number": phone_number,
        "variation_code": plan,  # This represents the data bundle code
        "request_id": request_id,
    }

    try:
        response = requests.post(Config.VTU_API_BASE_URL, json=payload, headers=headers)

        try:
            result = response.json()
        except ValueError:
            result = response.text  # fallback if not JSON

        # Handle both dict and string response safely
        if isinstance(result, dict):
            status = result.get("response_description") or result.get("message") or "Success"
        else:
            status = f"Error: Unexpected response - {result}"

        # Save transaction
        transaction = DataTransaction(
            phone_number=phone_number,
            plan=plan,
            network=network,
            amount=payload.get("amount", "N/A"),  # You can fetch amount if returned
            request_id=request_id,
            status=status,
            timestamp=datetime.datetime.now()
        )
        transaction.save()

        return result if isinstance(result, dict) else {"error": result}

    except Exception as e:
        # Save failed transaction
        transaction = DataTransaction(
            phone_number=phone_number,
            plan=plan,
            network=network,
            amount="0",
            request_id=request_id,
            status=f"Error: {str(e)}",
            timestamp=datetime.datetime.now()
        )
        transaction.save()

        return {"error": str(e)}
