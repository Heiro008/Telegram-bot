import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def msg(update: Update, context = CallbackContext)-> None:
	print(update)
	if update.message.text == "Hii":		
		name = "Hii "+update.message.chat.first_name
	else:
		name = "please enter Hii or enter /job to start job, /stop to end the job"

	update.message.reply_text(name)

def hii(context):
	job = context.job
	chat_id = job.context
	#print(chat_id)
	context.bot.send_message(chat_id ,text = "Happy birthday Kavin")

def stop(update:Update,context:CallbackContext) -> None:
	current_jobs = context.job_queue.get_jobs_by_name("hii")
	for job in current_jobs:
		job.schedule_removal()
	print("job stopped")
	context.bot.send_message(update.message.chat_id,text="job stopped")




def job(update: Update, context: CallbackContext) -> None:
	context.job_queue.run_repeating(hii,5,context= update.message.chat_id)
	print("job set successfully")
	update.message.reply_text("job started")


def main():
    updater = Updater("1572002778:AAG3_uigizXjMUC6AV2gDoQXY2LBHLEWXIs", use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("job",job))
    dispatcher.add_handler(CommandHandler("stop",stop))
    dispatcher.add_handler(MessageHandler(Filters.text,msg))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
	main()