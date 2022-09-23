import re
import shlex
from subprocess import Popen, PIPE
from telegram.ext import CommandHandler

from bot import LOGGER, dispatcher
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage

def index_scraper(update, context):
    message = update.effective_message
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) == 1:
        return message.reply_text('Send an Index Folder Link with command to Get All Links Inside...', parse_mode='HTML')
    if len(args) > 1:
        link = args[1]
        msg = sendMessage("Extracting Links.! Please Wait...", context.bot, update.message)
        cmd = f"python3 web/index_scraper.py {shlex.quote(link)}"
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stdout = stdout.decode()
    deleteMessage(context.bot, msg)
    if len(stdout) != 0:
        reply += f"{stdout}\n"
    if len(reply) > 3000:
        with open('index_scraper.txt', 'w') as file:
            file.write(reply)
        with open('index_scraper.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    elif len(reply) != 0:
        sendMessage(reply, context.bot, update.message)
    else:
        message.reply_text('Not a valid Index Folder Link. Check Again..', parse_mode='Markdown')

def up(update, context):
    message = update.effective_message
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) == 1:
        return message.reply_text('Send a FileName with command to Upload on GDrive...', parse_mode='HTML')
    if len(args) > 1:
        link = args[1]
        msg = sendMessage("Uploading! Please Wait...", context.bot, update.message)
        cmd = f"python3 web/cwup.py -f {shlex.quote(link)}"
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stdout = stdout.decode()
    deleteMessage(context.bot, msg)
    if len(stdout) != 0:
        reply += f"*Your File Uploaded Successfully...*\n\n*Link*: `{stdout}`\n"
    if len(reply) != 0:
        message.reply_text(reply, parse_mode='Markdown')
    else:
        message.reply_text('This file is not available on server. Check Again..', parse_mode='Markdown')

def dl(update, context):
    message = update.effective_message
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) == 1:
        return message.reply_text('Download an Index, GDrive or any valid Direct Link to Server...', parse_mode='HTML')
    if len(args) > 1:
        link = args[1]
        msg = sendMessage("Downloading!! Please Wait...", context.bot, update.message)
    if "drive.google.com" in link:
        cmd = f"bash web/gdrive_dl {shlex.quote(link)}"
    else:
        cmd = f"bash web/aria_dl {shlex.quote(link)}"
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stdout = stdout.decode()
    deleteMessage(context.bot, msg)
    if len(stdout) != 0:
        reply += f"*Your File Downloaded Successfully...*\n\n*Name*: `{stdout}`\n"
    if len(reply) != 0:
        message.reply_text(reply, parse_mode='Markdown')
    else:
        message.reply_text('Not a valid Direct Link. Check Again..', parse_mode='Markdown')

def g_lh(update, context):
    message = update.effective_message
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) == 1:
       return message.reply_text('Send a FileName with command to get Localhost Link...', parse_mode='HTML')
    if len(args) > 1:
        link = args[1]
        cmd = f"bash web/lh_g {shlex.quote(link)}"
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stdout = stdout.decode()
    if len(stdout) != 0:
        reply += f"{stdout}"
    if len(reply) != 0:
      message.reply_text(reply, parse_mode='Markdown')

def shell(update, context):
    message = update.effective_message
    cmd = message.text.split(' ', 1)
    if len(cmd) == 1:
        return message.reply_text('No command to execute was given.', parse_mode='HTML')
    cmd = cmd[1]
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if len(stdout) != 0:
        reply += f"*Stdout*\n`{stdout}`\n"
        LOGGER.info(f"Shell - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"*Stderr*\n`{stderr}`\n"
        LOGGER.error(f"Shell - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('shell_output.txt', 'w') as file:
            file.write(reply)
        with open('shell_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    elif len(reply) != 0:
        message.reply_text(reply, parse_mode='Markdown')
    else:
        message.reply_text('No Reply', parse_mode='Markdown')

SHELL_HANDLER = CommandHandler(BotCommands.ShellCommand, shell,
                                                  filters=CustomFilters.owner_filter, run_async=True)
R_HANDLER = CommandHandler(BotCommands.RCommand, shell,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
JK_HANDLER = CommandHandler(BotCommands.JkCommand, shell,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
DL_HANDLER = CommandHandler(BotCommands.DlCommand, dl,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
UP_HANDLER = CommandHandler(BotCommands.UpCommand, up,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
INS_HANDLER = CommandHandler(BotCommands.InScrCommand, index_scraper,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
G_HANDLER = CommandHandler(BotCommands.GCommand, g_lh,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)    
dispatcher.add_handler(SHELL_HANDLER)
dispatcher.add_handler(R_HANDLER)
dispatcher.add_handler(JK_HANDLER)
dispatcher.add_handler(DL_HANDLER)
dispatcher.add_handler(UP_HANDLER)
dispatcher.add_handler(INS_HANDLER)
dispatcher.add_handler(G_HANDLER)
