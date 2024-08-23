from flask import Blueprint, request
from flask_cors import CORS
from flask_mail import Message

from app.utils.validators import check_if_form_is_not_empty, validate_email, validate_phone_number

message_api_v1 = Blueprint(
    'message_api_v1', 'message_api_v1', url_prefix='/api/v1/messages')

CORS(message_api_v1)


@message_api_v1.route("/send-message", methods=["POST"])
def send_message():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide message details",
                "data": None,
                "error": "Bad request"
            }, 400

        is_form_not_empty, empty_fields = check_if_form_is_not_empty(data)

        if not is_form_not_empty:
            return {
                "message": f"Not all fields are fulfilled. Empty fields: {', '.join(map(str, empty_fields))}",
                "data": None,
                "error": "Bad request"
            }, 400

        is_email_correct = validate_email(data["email"])
        is_phone_number_correct = validate_phone_number(data["phone"])

        if not is_phone_number_correct and not is_email_correct:
            return {
                "message": "Email or phone number is not correct.",
                "data": None,
                "error": "Bad request"
            }, 400

        if not data["agreement"]:
            return {
                "message": "Please read Private Policy",
                "data": None,
                "error": "Bad request"
            }, 400

        is_organization_email = validate_email(data["organizationEmail"])
        if not is_organization_email:
            return {
                "message": "Organization email not exist or is not correct.",
                "data": None,
                "error": "Bad request"
            }, 400

        # try:
        #     message = Message(subject=data["subject"], sender=data["email"], recipients=data["organization_email"])
        #     message.body = data["message"]
        #     message.send(message)
        #     return {
        #             "message": "Message was send successfully.",
        #             "data": None
        #         }
        # except Exception as e:
        #     return {
        #         "message": "Something went wrong! Message can not be send",
        #         "error": str(e),
        #         "data": None
        #     }, 500
        return {
            "message": "Message was send successfully.",
            "data": None
        }

    except Exception as e:
        return {
            "message": "Something went wrong!",
            "error": str(e),
            "data": None
        }, 500
