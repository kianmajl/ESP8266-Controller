import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

URL = 'http://YOUR_IP_ADDRESS/device/{}/'


async def send_req(msg_tot, update: Update):
    msg = msg_tot.split()[-1]

    if msg.isnumeric():
        if 'on' in msg_tot:
            on_time = msg
            try:
                with requests.Session() as s:
                    s.get(URL.format('time'), timeout=60)
                    response = s.post(URL.format('time'), data={'on_time': int(on_time)}, timeout=60,
                                      headers={'X-CSRFToken': s.cookies.get('csrftoken'),
                                               'Referer': URL.format('time')})
                    if response.status_code != 200:
                        await update.message.reply_text(
                            f'[{response.status_code}]: Server is not available right now! Please try again later.')
                    else:
                        await update.message.reply_text(f'Your request was successful.')
            except requests.exceptions.RequestException as e:
                await update.message.reply_text(str(e))

        elif 'off' in msg_tot:
            off_time = msg
            try:
                with requests.Session() as s:
                    s.get(URL.format('time'), timeout=60)
                    response = s.post(URL.format('time'), data={'off_time': int(off_time)}, timeout=60,
                                      headers={'X-CSRFToken': s.cookies.get('csrftoken'),
                                               'Referer': URL.format('time')})
                    if response.status_code != 200:
                        await update.message.reply_text(
                            f'[{response.status_code}]: Server is not available right now! Please try again later.')
                    else:
                        await update.message.reply_text(f'Your request was successful.')
            except requests.exceptions.RequestException as e:
                await update.message.reply_text(str(e))
    else:
        if 'on' in msg:
            on_time = 500
            off_time = 0
            try:
                with requests.Session() as s:
                    s.get(URL.format('time'), timeout=60)
                    response = s.post(URL.format('time'), data={'off_time': int(off_time), 'on_time': int(on_time)},
                                      timeout=60, headers={'X-CSRFToken': s.cookies.get('csrftoken'),
                                                           'Referer': URL.format('time')})
                    if response.status_code != 200:
                        await update.message.reply_text(
                            f'[{response.status_code}]: Server is not available right now! Please try again later.')
                    else:
                        await update.message.reply_text(f'Your request was successful.')

            except requests.exceptions.RequestException as e:
                await update.message.reply_text(str(e))

        elif 'off' in msg:
            off_time = 500
            on_time = 0
            try:
                with requests.Session() as s:
                    s.get(URL.format('time'), timeout=60)
                    response = s.post(URL.format('time'), data={'off_time': int(off_time), 'on_time': int(on_time)},
                                      timeout=60, headers={'X-CSRFToken': s.cookies.get('csrftoken'),
                                                           'Referer': URL.format('time')})
                    if response.status_code != 200:
                        await update.message.reply_text(
                            f'[{response.status_code}]: Server is not available right now! Please try again later.')
                    else:
                        await update.message.reply_text(f'Your request was successful.')

            except requests.exceptions.RequestException as e:
                await update.message.reply_text(str(e))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Welcome to the esp controller {update.effective_user.first_name}!')


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('start bot: /start\n'
                                    'set the off time: /set_off 200\n'
                                    'set the on time: /set_on 200\n'
                                    'check the current on and off times: /status\n'
                                    'help: /help'
                                    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(str(update))


async def set_off(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_req(update.message.text, update)


async def set_on(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_req(update.message.text, update)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = requests.get(URL.format('get'), timeout=60)

        if response.status_code == 200:
            await update.message.reply_text(f"On time: {response.text.split(';')[0]}\n"
                                            f"Off time: {response.text.split(';')[1]}")

        else:
            await update.message.reply_text(
                f'[{response.status_code}]: Server is not available right now! Please try again later.'
                f'\n\n{response.text}')
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(str(e))


async def sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_sticker(update.message.sticker)
    await update.message.reply_text("Am I a joke to you?")
    await update.message.reply_text("Please enter a valid command. See /help for more information.")


async def animation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_animation(update.message.animation)
    await update.message.reply_text("Am I a joke to you?")
    await update.message.reply_text("Please enter a valid command. See /help for more information.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Please enter a valid command. See /help for more information.")


if __name__ == '__main__':
    app = ApplicationBuilder().token("YOUR_TOKEN").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("message", message))
    app.add_handler(CommandHandler("set_on", set_on))
    app.add_handler(CommandHandler("set_off", set_off))
    app.add_handler(CommandHandler("status", status))

    app.add_handler(MessageHandler(filters.Sticker.ALL, sticker))
    app.add_handler(MessageHandler(filters.ANIMATION, animation))
    app.add_handler(MessageHandler(filters.ALL, echo))

    app.run_polling()
