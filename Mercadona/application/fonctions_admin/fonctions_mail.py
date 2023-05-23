# Créez une fonction pour créer le message d'e-mail
def create_message(sender, recipient, subject, body):
    message = {
        'from': sender,
        'to': recipient,
        'subject': subject,
        'body': {
            'text': body
        }
    }
    return message


def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message sent successfully.')
        return message
    except Exception as e:
        print('An error occurred while sending the message:', str(e))
        return None
