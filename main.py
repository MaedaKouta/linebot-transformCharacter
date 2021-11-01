from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)
# 環境変数
# YOUR_CHANNEL_ACCESS_TOKENとYOUR_CHANNEL_SECRETはダミー
YOUR_CHANNEL_ACCESS_TOKEN = "0d32c9b54f089a06a5b43cad81b3923b"
YOUR_CHANNEL_SECRET = "1656585230"
line_bot_api=LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler=WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=["POST"])
def callback():
    signature=request.headers["X-Line-Signature"]

    body=request.get_data(as_text=True)
    app.logger.info("Request body"+body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

if __name__=="__main__":
    port=int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
