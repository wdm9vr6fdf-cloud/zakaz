import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

TOKEN = "YOUR_TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher()

class OrderForm(StatesGroup):
    waiting_for_time = State()
    waiting_for_place = State()
    waiting_for_product = State()

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Укажите желаемое время доставки:")
    await state.set_state(OrderForm.waiting_for_time)

@dp.message(OrderForm.waiting_for_time)
async def process_time(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer("Укажите место доставки:")
    await state.set_state(OrderForm.waiting_for_place)

@dp.message(OrderForm.waiting_for_place)
async def process_place(message: types.Message, state: FSMContext):
    await state.update_data(place=message.text)
    await message.answer("Укажите товар:")
    await state.set_state(OrderForm.waiting_for_product)

@dp.message(OrderForm.waiting_for_product)
async def process_product(message: types.Message, state: FSMContext):
    data = await state.get_data()
    time = data["time"]
    place = data["place"]
    product = message.text
    
    response = (
        f"Заказ подтвержден:\n"
        f"Товар: {product}\n"
        f"Время: {time}\n"
        f"Место: {place}"
    )
    await message.answer(response)
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
