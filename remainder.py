import logging
import time
from functools import wraps

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
def time_table(update:Update,context:CallbackContext):
	print(update)
	message = ''
	day = time.localtime().tm_wday
	classes=['probability - http://meet.google.com/xoc-vbtf-fbs ',
				'M&I - https://teams.microsoft.com/l/meetup-join/19%3a147121e710ba484f9ba5ede2ea51c000%40thread.tacv2/1609153145963?context=%7b%22Tid%22%3a%22858dc6a1-05e7-48c7-8a2b-4172a00a524a%22%2c%22Oid%22%3a%225fdaf900-6f9c-464b-b695-f1fa040f99e5%22%7d' ,
				'Digital electronics - https://meet.google.com/btv-jzsw-sfn ',
				'ISM - https://meet.google.com/fam-mmjr-ign?hs=224 ',
				'Control System - http://meet.google.com/rdp-pfgx-zff',
				'EPGS - https://meet.google.com/aux-byuh-ves ',
				'Indian consitution - https://meet.google.com/fyz-xvup-jpg?hs=224 ']
	map_classes = {0:[5,3,0,4],1:[2,1,6,0],2:[4,1,2,5],3:[5,3,4,2],4:[0,6,1,3],5:[]}
	session = ["9 :30 - 10:30","11:00 - 12:00","2 :00 - 3 :00","3 :30 - 4 :00"]
	for i,j in enumerate(map_classes[day]):
		message = message+session[i]+' '+classes[j]+'\n'

	context.bot.send_message(update.message.chat_id,message)



def main():
    updater = Updater("1572002778:AAG3_uigizXjMUC6AV2gDoQXY2LBHLEWXIs", use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("job",job))
    dispatcher.add_handler(CommandHandler("stop",stop))
    dispatcher.add_handler(CommandHandler("timetable",time_table))
    dispatcher.add_handler(MessageHandler(Filters.all,msg))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
	main()