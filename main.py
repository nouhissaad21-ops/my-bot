import os
import requests
from fastapi import FastAPI, Request
import google.generativeai as genai

app = FastAPI()

GEMINI_KEY = "AQ.Ab8RN6Ky29R2b3kfFkiRDSdkRl0uUc1UO-JgVlcY9MikaDnY4g"
ID_INSTANCE = "710701674368"
API_TOKEN_INSTANCE = "306c0a731cd644d48f6c4136a1731645e00b5109e4eb48c3bb"

genai.configure(api_key=GEMINI_KEY)
store_instructions = "أنت مساعد مبيعات لمتجر Décopatch. تبيع ورق جدران بـ 2500 دج وملصقات بـ 1800 دج. تحدث بالدارجة الجزائرية."
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=store_instructions)

@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    if "body" in data:
        body = data["body"]
        if body.get("typeWebhook") == "incomingMessageReceived":
            sender_number = body["senderData"]["sender"]
            message_data = body.get("messageData", {})
            
            if "textMessageData" in message_data:
                message_text = message_data["textMessageData"]["textMessage"]
                ai_reply = model.generate_content(message_text).text
                
                send_url = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN_INSTANCE}"
                payload = {"chatId": sender_number, "message": ai_reply}
                requests.post(send_url, json=payload)
                
            elif "audioMessageData" in message_data:
                send_url = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN_INSTANCE}"
                payload = {"chatId": sender_number, "message": "سمعت الفوكال تيعك، لحظة برك نرجعلك!"}
                requests.post(send_url, json=payload)
                
    return {"status": "success"}

@app.get("/")
def read_root():
    return {"status": "Server is alive"}
