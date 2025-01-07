from aiogram import Bot, Dispatcher, executor, types
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot,storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    msg = State()

@dp.message_handler(commands = ['start'])
async def start_message(message):
    await message.answer("Привет! Введите слово Calories, чтобы начать расчёт калорий")

@dp.message_handler(text = ['Calories', 'Калории', 'calories', 'калории'])
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler()
async def start_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.")

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age_info = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth_info = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight_info = message.text)
    data = await state.get_data()
    try:
        result = 10*int(data['weight_info']) + 6.25*int(data['growth_info']) - 5*int(data['age_info']) - 161
        await message.answer(f'Ваша норма калорий {result}')
    except:
        await message.answer(f'Пожалуйста, попробуйте заново. Для корректного расчета необходимо вводить только '
                             f'целые числа (без точек, запятых или пробелов)')
    finally:
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



