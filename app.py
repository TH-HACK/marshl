import logging
import openai
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# إعداد API Token الخاص بالبوت
API_TOKEN = '7375947460:AAE6E29xYN0F4jZ7dS-ath7E_v1Zun8CrTY'

# إعداد OpenAI API Key
openai.api_key = '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'

# إعدادات التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# دالة للتعامل مع الرسائل
def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text  # الكود المفكوك من المستخدم
    update.message.reply_text("قمت بإرسال الكود. جاري التحويل...")

    # إرسال الكود إلى ChatGPT مع الرسالة لتنسيق الكود
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # أو "gpt-3.5-turbo" حسب التوافر
            messages=[
                {"role": "system", "content": "You are an assistant that helps organize code."},
                {"role": "user", "content": f"قم بترتيب هذا الكود:\n{user_input}"}
            ]
        )

        # استخراج الكود المحسن من الاستجابة
        python_code = response['choices'][0]['message']['content']
        update.message.reply_text(f"إليك الكود المحول:\n\n{python_code}")

    except Exception as e:
        update.message.reply_text(f"حدث خطأ: {str(e)}")

# دالة لتشغيل البوت
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("مرحبًا! أرسل لي الكود المفكوك وسأقوم بترتيبه لك.")

# دالة لتسجيل الأخطاء
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    # إنشاء البوت
    updater = Updater(API_TOKEN)
    dispatcher = updater.dispatcher

    # تسجيل معالجات الأوامر والرسائل
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # تسجيل الأخطاء
    dispatcher.add_error_handler(error)

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
