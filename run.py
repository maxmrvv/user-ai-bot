import logging

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction  

from decouple import config
from deepseek import ai_generate


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


app = Client(
    name="first",
    api_id=config('API_ID'),
    api_hash=config('API_HASH'),
    phone_number=config('PHONE')
)

@app.on_message(filters.text & ~filters.me)
async def handle_message(client: Client, message: Message):
    text = message.text
    if "@aimaxmrvv" in text.lower():

        query = text.split("@aimaxmrvv", 1)[1].strip()
        
        if not query:
            await message.reply("ℹ️ Пожалуйста, укажите вопрос после @aimaxmrvv")
            return
            
        try:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            result = await ai_generate(query)
            
            if result and result['response']:
                response = f"{result['response']}\n\n(🪙 Использовано токенов: {result['usage']})"
                await message.reply(response)
            else:
                await message.reply("⚠️ Не удалось получить ответ от DeepSeek")
                
        except Exception as e:
            logger.error(f"Error: {e}")
            await message.reply("⚠️ Произошла ошибка при обработке запроса")

if __name__ == "__main__":
    logger.info("Бот запускается...")
    app.run()