import logging

from functools import wraps
import time_table

from telegram import Update, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def send_typing_action(func):
	@wraps(func)
	def command_func(update,context):
		context.bot.send_chat_action(chat_id = update.effective_message.chat_id, action = ChatAction.TYPING)
		return func(update,context)
	return command_func

@send_typing_action
def msg(update: Update, context = CallbackContext)-> None:
	print(update)
	print(hex(ord(update.message.text)))
	if update.message.text.lower() == "hii":		
		message = "Hii "+update.message.chat.first_name
	elif update.message.text.lower() == "thank you":
		message = "you are welcome"
	else:
		message = "please enter Hii or enter /job to start job, /stop to end the job \n /timetable to ..."

	update.message.reply_text(message)

def job_message(context,text = "job running"):
	job = context.job
	chat_id = job.context
	#print(chat_id)
	#text = time_table()
	context.bot.send_message(chat_id ,text )

def stop(update:Update,context:CallbackContext) -> None:
	current_jobs = context.job_queue.get_jobs_by_name(str(update.message.chat_id))
	for job in current_jobs:
		job.schedule_removal()
	print("job stopped")
	context.bot.send_message(update.message.chat_id,text="job stopped")

def job(update: Update, context: CallbackContext) -> None:
	context.job_queue.run_repeating(job_message,5,context= update.message.chat_id,name=str(update.message.chat_id))
	print("job set successfully")
	update.message.reply_text("job started")



@send_typing_action
def send_timetable(update:Update,context:CallbackContext):
	print(update)

	context.bot.send_message(update.message.chat_id,time_table.time_table())



def main():
    updater = Updater("1572002778:AAG3_uigizXjMUC6AV2gDoQXY2LBHLEWXIs", use_context=True)
    dispatcher = updater.dispatcher
    print(dispatcher.bot)
    #dispatcher.bot.send_message(1242866255,temp.time_table())
    dispatcher.add_handler(CommandHandler("job",job))
    dispatcher.add_handler(CommandHandler("stop",stop))
    dispatcher.add_handler(CommandHandler("timetable",send_timetable))
    dispatcher.add_handler(MessageHandler(Filters.all,msg))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
	main()