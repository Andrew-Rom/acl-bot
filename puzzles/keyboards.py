from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import keyboard_button, reply_keyboard_markup, InlineKeyboardButton


def keyboard_difficulty_level():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='легко')
    keyboard.button(text='нормально')
    keyboard.button(text='сложно')
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)


def keyboard_operations():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text='сложение')
    keyboard.button(text='вычитание')
    keyboard.button(text='деление')
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)

def keyboard_difficulty_level_callback():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='легко', callback_data='легко'),
        InlineKeyboardButton(text='нормально', callback_data='нормально'),
        InlineKeyboardButton(text='сложно', callback_data='сложно')
    )
    return builder.as_markup()

def keyboard_operations_callback():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='сложение', callback_data='сложение'),
        InlineKeyboardButton(text='вычитание', callback_data='вычитание'),
        InlineKeyboardButton(text='деление', callback_data='деление')
    )
    return builder.as_markup()
