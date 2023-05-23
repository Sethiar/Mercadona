from googleapiclient.errors import HttpError

def send_email(sender, to, subject, message_text):
    message = {
        'from': sender,
        'to': to,
        'subject': subject,
        'text': message_text
    }

    try:
        message = (service.users().messages().send(userId='me', body=message)
                   .execute())
        print(f"Message sent. Message ID: {message['id']}")
    except HttpError as error:
        print(f"An error occurred: {error}")