import telebot
from config import TOKEN
from database.rooms import RoomAggregator
from game.abstract.abstract_maze import BaseCell
from game.effect_type import WinEffectType, \
    IncreasesEffectTypeCellCompletionTime, ReduceTimeRemainingEffectType
from message import (WELCOME_NEXT_1_TEXT, WELCOME_MESSAGE,
                     WELCOME_NEXT_RULE_TEXT, WELCOME_NEXT_RULE_2_TEXT,
                     WELCOME_START_GAME_TEXT, WELCOME_NEXT_RULE_3_TEXT,
                     CREATE_ROOM_TEXT, JOIN_TO_ROOM_TEXT, CHOOSE_ACTION_TEXT,
                     ROOM_SUCCESS_CREATE_TEXT, ROOM_ERROR_CREATE_TEXT,
                     LEAVE_ROOM_TEXT, PARTICIPANT_ALREADY_IN_ROOM,
                     PARTICIPANT_NOT_IN_ROOM, ROOM_SUCCESS_LEAVE_TEXT,
                     ROOM_ERROR_LEAVE_TEXT, ENTER_ROOM_NUMBER_TEXT,
                     LOGIN_SUCCESS_IN_ROOM_NUMBER_TEXT,
                     LOGIN_ERROR_IN_ROOM_NUMBER_TEXT, BUTTON_BACK_TEXT,
                     IN_MENU_TEXT, BUTTON_START_GAME_TEXT, START_GAME_TEXT,
                     BUTTON_FORWARD, BUTTON_RIGHT, BUTTON_BACK, BUTTON_LEFT,
                     CANT_MOVE_TEXT, ALREADY_EXISTED_TEXT, NEW_WAY_TEXT)

bot = telebot.TeleBot(TOKEN)

ROOM_AGGREGATOR = RoomAggregator()
messages = {}


def get_keyboard_back():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_back = telebot.types.KeyboardButton(text=BUTTON_BACK_TEXT)
    keyboard.add(button_back)
    return keyboard


@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_welcome_next_1 = telebot.types.InlineKeyboardButton(
        text="Что это?",
        callback_data=
        'welcome_next_1'
    )
    keyboard.add(button_welcome_next_1)
    bot.send_message(chat_id,
                     WELCOME_MESSAGE,
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'welcome_next_1')
def welcome_next_1(call):
    message = call.message
    chat_id = message.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_welcome_next_rules = telebot.types.InlineKeyboardButton(
        text="Как это?",
        callback_data=
        'welcome_next_rule'
    )
    keyboard.add(button_welcome_next_rules)
    bot.edit_message_text(WELCOME_NEXT_1_TEXT, chat_id=chat_id,
                          message_id=message.message_id, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'welcome_next_rule')
def welcome_next_rules(call):
    message = call.message
    chat_id = message.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_welcome_next_rules = telebot.types.InlineKeyboardButton(
        text="Какие опасности?",
        callback_data=
        'welcome_next_rule_2'
    )
    keyboard.add(button_welcome_next_rules)
    bot.edit_message_text(WELCOME_NEXT_RULE_TEXT, chat_id=chat_id,
                          message_id=message.message_id, reply_markup=keyboard)


@bot.callback_query_handler(
    func=lambda call: call.data == 'welcome_next_rule_2')
def welcome_next_rules(call):
    message = call.message
    chat_id = message.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_welcome_next_rules = telebot.types.InlineKeyboardButton(
        text="А что делать с этими препятствиями?",
        callback_data=
        'welcome_next_rule_3'
    )
    keyboard.add(button_welcome_next_rules)
    bot.edit_message_text(WELCOME_NEXT_RULE_2_TEXT, chat_id=chat_id,
                          message_id=message.message_id, reply_markup=keyboard)


@bot.callback_query_handler(
    func=lambda call: call.data == 'welcome_next_rule_3')
def welcome_next_rules(call):
    message = call.message
    chat_id = message.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_welcome_next_rules = telebot.types.InlineKeyboardButton(
        text="Понял, начнём?",
        callback_data='welcome_start_game'
    )
    keyboard.add(button_welcome_next_rules)
    bot.edit_message_text(WELCOME_NEXT_RULE_3_TEXT, chat_id=chat_id,
                          message_id=message.message_id, reply_markup=keyboard)


@bot.callback_query_handler(
    func=lambda call: call.data == 'welcome_start_game')
def welcome_start_game(call):
    message = call.message
    chat_id = message.chat.id
    bot.edit_message_text(WELCOME_START_GAME_TEXT, chat_id=chat_id,
                          message_id=message.message_id)
    menu(message)


def menu(message):
    keyboard = get_keyboard_in_menu()
    bot.send_message(message.chat.id, CHOOSE_ACTION_TEXT,
                     reply_markup=keyboard)


def get_keyboard_in_menu():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_create_room = telebot.types.KeyboardButton(text=CREATE_ROOM_TEXT)
    button_join_room = telebot.types.KeyboardButton(
        text=JOIN_TO_ROOM_TEXT)
    keyboard.add(button_create_room, button_join_room)
    return keyboard


@bot.message_handler(
    func=lambda message: message.text == CREATE_ROOM_TEXT)
def create_room(message):
    chat_id = message.chat.id
    if ROOM_AGGREGATOR.get_room_by_participant(chat_id):
        bot.send_message(message.chat.id, PARTICIPANT_ALREADY_IN_ROOM)
        return
    room_number = ROOM_AGGREGATOR.create_room()

    keyboard = get_keyboard_in_room()

    name = message.chat.first_name
    surname = message.chat.first_name

    if ROOM_AGGREGATOR.join_room_participant(room_number,
                                             chat_id,
                                             name,
                                             surname):
        bot.send_message(chat_id,
                         ROOM_SUCCESS_CREATE_TEXT.format(room_number),
                         reply_markup=keyboard)
    else:
        bot.send_message(chat_id, ROOM_ERROR_CREATE_TEXT)


def get_keyboard_in_room():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = telebot.types.KeyboardButton(text=BUTTON_START_GAME_TEXT)
    button_leave_room = telebot.types.KeyboardButton(text=LEAVE_ROOM_TEXT)
    keyboard.add(button_start)
    keyboard.add(button_leave_room)
    return keyboard


@bot.message_handler(
    func=lambda message: message.text == LEAVE_ROOM_TEXT)
def leave_room(message):
    chat_id = message.chat.id
    room_number = ROOM_AGGREGATOR.get_room_by_participant(chat_id)
    keyboard = get_keyboard_in_menu()
    if not room_number:
        bot.send_message(message.chat.id,
                         PARTICIPANT_NOT_IN_ROOM,
                         reply_markup=keyboard)
        return
    if ROOM_AGGREGATOR.leave_room_participant(room_number, chat_id):
        bot.send_message(message.chat.id,
                         ROOM_SUCCESS_LEAVE_TEXT,
                         reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, ROOM_ERROR_LEAVE_TEXT)


@bot.message_handler(
    func=lambda message: message.text == JOIN_TO_ROOM_TEXT)
def join_to_room_text(message):
    chat_id = message.chat.id
    if ROOM_AGGREGATOR.get_room_by_participant(chat_id):
        bot.send_message(message.chat.id, PARTICIPANT_ALREADY_IN_ROOM)
        return
    keyboard = get_keyboard_back()
    bot.send_message(chat_id, ENTER_ROOM_NUMBER_TEXT, reply_markup=keyboard)
    bot.register_next_step_handler_by_chat_id(chat_id, join_to_room)


def join_to_room(message):
    chat_id = message.chat.id
    if message.text == BUTTON_BACK_TEXT:
        keyboard = get_keyboard_in_menu()
        bot.send_message(message.chat.id,
                         IN_MENU_TEXT,
                         reply_markup=keyboard)
        return
    room_number = message.text
    name = message.chat.first_name
    surname = message.chat.first_name
    if ROOM_AGGREGATOR.join_room_participant(room_number,
                                             chat_id,
                                             name,
                                             surname):
        keyboard = get_keyboard_in_room()
        bot.send_message(message.chat.id,
                         LOGIN_SUCCESS_IN_ROOM_NUMBER_TEXT,
                         reply_markup=keyboard)
        participants = ROOM_AGGREGATOR.get_participants(room_number)
        for participant in participants:
            if participant != chat_id:
                if name != surname:
                    bot.send_message(participant,
                                     f'Новый участник комнаты: '
                                     f'{name} '
                                     f'{surname}')
                else:
                    bot.send_message(participant,
                                     f'Новый участник комнаты: '
                                     f'{name}')
        return
    keyboard = get_keyboard_back()
    bot.send_message(message.chat.id,
                     LOGIN_ERROR_IN_ROOM_NUMBER_TEXT,
                     reply_markup=keyboard)
    bot.register_next_step_handler_by_chat_id(chat_id, join_to_room)


@bot.message_handler(
    func=lambda message: message.text == BUTTON_START_GAME_TEXT)
def start_game(message):
    chat_id = message.chat.id
    messages[chat_id] = []
    maze = ROOM_AGGREGATOR.get_maze_by_participant_id(chat_id)
    maze.generate_maze()
    maze.arrange_effects(15)
    bot.send_message(chat_id, START_GAME_TEXT)
    game(message)


def game(message):
    chat_id = message.chat.id
    messages[chat_id].append(message)
    maze = ROOM_AGGREGATOR.get_maze_by_participant_id(chat_id)
    maze = maze.get_maze()
    text = message.text

    for i in range(len(messages[chat_id])):
        msg = messages[chat_id][0]
        bot.delete_message(msg.chat.id, msg.message_id)
        messages[chat_id].remove(msg)

    if text in (BUTTON_FORWARD, BUTTON_RIGHT, BUTTON_BACK,
                BUTTON_LEFT):
        cell = _make_move(message)
        if not cell:
            send_message(chat_id, CANT_MOVE_TEXT.format(text.lower()))
        else:
            _cell_effect(chat_id, cell)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    if not maze.current_cell.walls['top']:
        button_forward = telebot.types.KeyboardButton(text=BUTTON_FORWARD)
        keyboard.add(button_forward)

    buttons_left_right = []
    if not maze.current_cell.walls['left']:
        buttons_left_right.append(
            telebot.types.KeyboardButton(text=BUTTON_LEFT))

    if not maze.current_cell.walls['right']:
        buttons_left_right.append(
            telebot.types.KeyboardButton(text=BUTTON_RIGHT))

    if buttons_left_right:
        keyboard.add(*buttons_left_right)

    if not maze.current_cell.walls['bottom']:
        button_back = telebot.types.KeyboardButton(text=BUTTON_BACK)
        keyboard.add(button_back)

    if maze.current_cell.user_visited:
        send_message(chat_id, ALREADY_EXISTED_TEXT, reply_markup=keyboard)
    else:
        send_message(chat_id, NEW_WAY_TEXT, reply_markup=keyboard)
    bot.register_next_step_handler_by_chat_id(chat_id, game)


def _make_move(message):
    chat_id = message.chat.id
    way = message.text
    maze = ROOM_AGGREGATOR.get_maze_by_participant_id(chat_id)
    if way not in (BUTTON_FORWARD, BUTTON_RIGHT, BUTTON_BACK, BUTTON_LEFT):
        return False
    if way == BUTTON_FORWARD:
        return maze.move_forward()
    if way == BUTTON_RIGHT:
        return maze.move_right()
    if way == BUTTON_BACK:
        return maze.move_bottom()
    if way == BUTTON_LEFT:
        return maze.move_left()


def _cell_effect(chat_id: int, cell: BaseCell):
    for effect in cell.effects:
        if effect.effect_type == WinEffectType:
            send_message(chat_id, 'Лабиринт закончен, вы победили!')
        elif effect.effect_type == IncreasesEffectTypeCellCompletionTime:
            send_message(chat_id, 'Время прохождения клетки увеличено!')
        elif effect.effect_type == ReduceTimeRemainingEffectType:
            send_message(chat_id, 'Оставшееся время уменьшено!')


def send_message(chat_id, text, reply_markup=None):
    if reply_markup:
        message = bot.send_message(chat_id, text, reply_markup=reply_markup)
    else:
        message = bot.send_message(chat_id, text)
    messages[chat_id].append(message)


if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling()
