from flask import Flask, request, json
import requests

app=Flask(__name__)

@app.route("/saludar", methods=["GET"])
def saludar():
    return "Hola mundo"

@app.route("/", methods=["GET"])
def home():
    return "Hola desde python"

@app.route("/whatsapp", methods=["GET"])
def verifyToken():
    try:
        access_token = "myaccesstokensecreto"
        token = request.args.get("hub.verify_token")
        challenge=request.args.get("hub.challenge")

        if token==access_token:
            return challenge
        else:
            return "error",400
    except:
        return "error",400
    

@app.route("/whatsapp", methods=["POST"])
def ReceivedMessage():

    try:
        body=request.get_json()
        entry=body["entry"][0]
        changes=entry["changes"][0]
        value=changes["value"]
        message=value["messages"][0]
        text=message["text"]
        question_user=text["body"]
        number=message["from"]

        print("este es el texto recibido del usuario: ", question_user)

        body_answer=enviarMensaje(question_user,number)
        send_message=whatsappService(body_answer)

        if send_message:
            print("Mensaje enviado correctamenteo")
        else:
            print("Error al envío del mensaje")
        
        return "EVENT_RECEIVED"
    except Exception as e:
        print(e)
        return "EVENT_RECEIVED"



def whatsappService(body):
    try:
        token="EAAKSEHZBrwZAQBOzGWQVf9TFm0S94C2tldtFZCsxpbyeuwwszc0xH17KzZCNRLfIM8IzbkoPXAyqtkdZCaHCZApgnTjE9mDK2frpVC5hZCQaVW7W0hgZCwRd9Ali2A0XsevDWGxZAZAdBhIIlOl2gHz2tZB1dIw9E0IZCEmUrPWGlbHSEKKqWB4U1vttgCMUJkFWYZBcP"
        api_url="https://graph.facebook.com/v20.0/124967277376915/messages"
        headers={
            "Content-Type":"application/json",
            "Authorization": f"Bearer {token}"
        }

        response=requests.post(api_url,
                            data=json.dumps(body),
                            headers=headers)
        if response.status_code==200:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def enviarMensaje(text,numero):
    url="https://c3rra2vkpj.execute-api.us-east-1.amazonaws.com/prod/query"
    data = {
    "query": text
    }
    responseJson=requests.post(url,json=data)
    responseJson = responseJson.json()
    responseGPT = responseJson['answer']

    responseSinGPT="Hola esto es una respuesta automatica"
    
    body={
        "messaging_product": "whatsapp",    
        "recipient_type": "individual",
        "to": numero,
        "type": "text",
        "text": {
            "body": responseGPT
        }
    }
    return body


if __name__=="__main__":
    app.run(host="0.0.0.0",port="8501",debug=True)


# token permanente
# "EAAKSEHZBrwZAQBOzGWQVf9TFm0S94C2tldtFZCsxpbyeuwwszc0xH17KzZCNRLfIM8IzbkoPXAyqtkdZCaHCZApgnTjE9mDK2frpVC5hZCQaVW7W0hgZCwRd9Ali2A0XsevDWGxZAZAdBhIIlOl2gHz2tZB1dIw9E0IZCEmUrPWGlbHSEKKqWB4U1vttgCMUJkFWYZBcP"