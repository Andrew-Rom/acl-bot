from random import randint, randrange
from aiogram import Router, F, html
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery


from main import bot
from puzzles.keyboards import keyboard_difficulty_level_callback, keyboard_operations_callback

puzzle_router = Router()

GAMES = ['сложение', 'вычитание', 'деление']
LEVELS = ['легко', 'нормально', 'сложно']

difficulty_level = ''
game_type = ''
result_number = 0


class MathGameGenerator(StatesGroup):
    difficulty_level = State()
    game_type = State()


def generate_puzzle():
    global result_number, difficulty_level, game_type
    bot_ask = ''
    match difficulty_level:
        case 'легко':
            result_number = randint(10, 100)
        case 'нормально':
            result_number = randint(100, 1000)
        case 'сложно':
            result_number = randint(500, 3000)
        case _:
            result_number = 1000
    first_number = result_number - randint(1, (result_number // randint(2, 4)))
    match game_type:
        case 'сложение':
            second_number = result_number - first_number
            bot_ask = f'{first_number} + {second_number} = ?'
        case 'вычитание':
            second_number = result_number + first_number
            bot_ask = f'{second_number} - {first_number} = ?'
        case 'деление':
            second_number = result_number * first_number
            bot_ask = f'{second_number} : {first_number} = ?'
    return bot_ask


@puzzle_router.message(StateFilter(None), Command('math'))
async def select_level(message: Message, state: FSMContext):
    bot_text = f'{message.from_user.first_name}, хорошо, давай проверим твои знания по математике. ' \
               f'Выбери уровень сложности.'
    await message.answer(bot_text, reply_markup=keyboard_difficulty_level_callback())
    await state.set_state(MathGameGenerator.difficulty_level)


@puzzle_router.callback_query(
    MathGameGenerator.difficulty_level,
    F.data.in_(LEVELS))
async def select_game(callback: CallbackQuery, state: FSMContext):
    # global difficulty_level
    await state.update_data(select_level=callback.data)
    # difficulty_level = callback.data
    bot_text = f'Выбери математическое действие'
    await callback.message.edit_text(bot_text, reply_markup=keyboard_operations_callback())
    await callback.answer()
    await state.set_state(MathGameGenerator.game_type)
    # await callback.message.answer(bot_text, reply_markup=keyboard_operations())

# @puzzle_router.message(F.text.in_({'легко', 'нормально', 'сложно'}))
# async def select_game(message: Message):
#     global difficulty_level
#     difficulty_level = message.text
#     bot_text = f'Выбери математическое действие'
#     await bot.send_message(message.from_user.id,
#                            text=bot_text,
#                            reply_markup=keyboard_operations())


@puzzle_router.callback_query(
    MathGameGenerator.game_type,
    F.data.in_(GAMES))
async def bot_ask_question(callback: CallbackQuery):
    global game_type
    game_type = callback.data
    print(game_type)
    await callback.message.edit_text(generate_puzzle())
    await callback.answer()

# @puzzle_router.message(F.text.in_({'сложение', 'вычитание', 'деление'}))
# async def bot_ask_question(message: Message):
#     global game_type
#     game_type = message.text
#     await bot.send_message(message.from_user.id, text=generate_puzzle())

@puzzle_router.message()
async def check_answer(message: Message):
    try:
        if (int(message.text) == result_number):
            bot_text = html.bold('Right')
        else:
            bot_text = html.bold('Wrong')
        await bot.send_message(message.from_user.id, text=bot_text)
    except ValueError as e:
        print(e)
    finally:
        await bot.send_message(message.from_user.id, text=html.bold('Game over'))




if __name__ == '__main__':
    difficulty_level = 'нормально'
    game_type = 'сложение'
    print(generate_puzzle())
    print(result_number)