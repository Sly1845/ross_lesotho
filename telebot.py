from flask import Flask, request, Response, redirect, render_template
import telegram

global bot
global TOKEN
global state
Url = "https://cf090f5a97fe.ngrok.io"
bot_user_name = "Ross_Lesotho_bot"
TOKEN = "1592081568:AAFkuf-eurEzQEvCLqoR3fuBu9rPDNNuVoY"
bot = telegram.Bot(token=TOKEN)


app = Flask(__name__)

global state
state = 0


@app.route("/bot", methods=["POST"])
def main():

    print("first state")
    global state
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    print(update.message)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    if update.message.text:
        text = update.message.text.encode("utf-8").decode()

    else:
        text = "2"

    # Telegram understands UTF-8, so encode text for unicode compatibility
    #

    # for debugging purposes only
    print("got text message :", text)
    # the first time you chat with the bot AKA the welcoming message
    if text == "/start":
        # print the welcoming message
        bot_welcome = """
       \n\n Select one of the options below to continue \n\n 1. To visit Ross fashion  \n 2. To visit Ross interior    """
        # send the welcoming message
        bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

    elif text == "1" and state == 1:
        # print("in here")
        # print(request.values)
        state = 3
        bot.sendMessage(
            chat_id=chat_id,
            text="\n 1.card \n 2.Eco-cash \n 3.M-pesa",
        )
    elif text == "1" and state == 3:
        state = 0
        bot.sendMessage(
            chat_id=chat_id,
            text="Thank you! You've decided to pay with card",
        )
    elif text == "2" and state == 3:
        state = 0
        bot.sendMessage(
            chat_id=chat_id,
            text="Thank you! You've decided to pay with Eco-cash",
        )
    elif text == "3" and state == 3:
        state = 0
        bot.sendMessage(
            chat_id=chat_id,
            text="Thank you! You've decided to pay with M-pesa",
        )

    elif text == "1" and state == 0:

        bot.sendMessage(
            chat_id=chat_id,
            text="Welcome to Ross fashion, please click on the link to begin shopping https://cf090f5a97fe.ngrok.io/checkout?Melvin="
            + str(chat_id),
            reply_to_message_id=msg_id,
        )
    elif text == "2" and state == 1:
        # print("in here")
        # print(request.values)
        bot.sendMessage(
            chat_id=chat_id,
            text="please click on the link to add or substitute order http://cf090f5a97fe.ngrok.io/checkout?Melvin="
            + str(chat_id),
        )
    elif text == "2":

        # print(update.message)
        if update.message.contact:
            print("test")
            bot.sendMessage(
                chat_id=1460462298,
                text=update.message.chat.first_name
                + " Wants to hear more about ross interiors, contact them on "
                + update.message.contact.phone_number,
            )
            bot.sendMessage(
                chat_id=chat_id,
                text="Thanks for contacting us, chat to you soon...",
                reply_to_message_id=msg_id,
            )

        else:

            interior_menu = [
                [telegram.KeyboardButton("Send contact", True)],
                [telegram.KeyboardButton("Cancel")],
            ]
            bot.sendMessage(
                chat_id=1679766741,
                reply_markup=telegram.ReplyKeyboardMarkup(interior_menu),
                text="This feature is underway...",
                reply_to_message_id=msg_id,
            )

    # try:
    #     # clear the message we got from any non alphabets
    #     text = re.sub(r"\W", "_", text)
    #     # create the api link for the avatar based on http://avatars.adorable.io/
    #     url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
    #     # reply with a photo to the name the user sent,
    #     # note that you can send photos by url and telegram will fetch it for you
    #     bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
    # except Exception:
    #     # if things went wrong
    #     bot.sendMessage(
    #         chat_id=chat_id,
    #         text="There was a problem in the name you used, please enter different name",
    #         reply_to_message_id=msg_id,
    #     )

    return "ok"


@app.route("/finiliseorder", methods=["POST"])
def finilise():
    print(request.values)
    print(request.values.get("vehicle[]", ""))
    global state
    # print(state)
    # print("indeed")
    # print the welcoming message
    # Dispaly checked items on telegram
    # Options to select from to finilise payment

    bot.sendMessage(
        chat_id=request.values.get("chat", ""),
        # reply_markup=telegram.ReplyKeyboardMarkup(interior_menu),
        text="Complete your order, "
        + "\n"
        + request.values.get("vehicle1", "")
        + "\n"
        + request.values.get("vehicle2", "")
        + "\n"
        + request.values.get("vehicle3", "")
        + "\n"
        + "Select \n1 To choose payment method \n2 To add or remove item",
        # reply_to_message_id=msg_id,
    )
    state = 1
    # print(state)
    # print("Last state")

    # bot_welcome = """
    #       """
    # send the welcoming message
    # bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

    return redirect(
        "https://T.me/ross_lesotho_bot",
        code=302,
    )


@app.route("/checkout", methods=["GET"])
def checkout():

    return render_template("index.html")


if __name__ == "__main__":
    app.run()
