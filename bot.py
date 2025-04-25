from menu import *

load_dotenv()
TOKEN = os.getenv('TOKEN')

dp = Dispatcher()

WEEKDAYS = {
    "mon": "Понеділок",
    "tue": "Вівторок",
    "wed": "Середа",
    "thu": "Четвер",
    "fri": "П'ятниця",
    "sat": "Субота",
    "sun": "Неділя"
}

dp.message.register(start_handler, CommandStart())
dp.message.register(today_schedule, F.text == "Сьогодні")
dp.message.register(my_schedule, F.text == "Мій розклад")
dp.message.register(view_schedule, F.text == "Переглянути розклад")
dp.message.register(create_pair, F.text == "Створити")
dp.message.register(cancel_creation, F.text == "⏹ Скасувати")
dp.message.register(return_to_main_menu, F.text.in_(["🏠 Головне меню", "Головне меню"]))

async def main():
    await register_additional_handlers(dp)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())