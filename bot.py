import os

import config
import telebot
from telebot import types
import random
import sqlite3
import datetime
from time import sleep
import keep_alive

bot = telebot.TeleBot(config.TOKEN)
conn = sqlite3.connect('databased.db',check_same_thread = False)
cursor = conn.cursor()


def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("В чем смысл каждой игры")  # добавить табличку
    item2 = types.KeyboardButton("Выбрать игру")
    item3 = types.KeyboardButton("Баланс")
    item4 = types.KeyboardButton("Связь с администрацией")
    markup.add(item1, item2)  # эта и строчка ниже выводит таблички
    markup.add(item3, item4)
    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)
@bot.message_handler(commands=['start'])
#/start
def start_message(message):
    bot.send_message(message.chat.id,'Привет, этот бот предназначен для игры в казино. Для корректной работы соблюдайте все условия, которые будут написаны.')#отправить сообщение
    def main_menu(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("В чем смысл каждой игры")  # добавить табличку
        item2 = types.KeyboardButton("Выбрать игру")
        item3 = types.KeyboardButton("Баланс")
        item4 = types.KeyboardButton("Связь с администрацией")
        markup.add(item1, item2)  # эта и строчка ниже выводит таблички
        markup.add(item3, item4)
        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)
    main_menu(message)
    cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (message.chat.id,))
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO users (`user_id`,'username','join_date','balance') VALUES (?,?,?,?)", (message.chat.id, message.from_user.username,datetime.datetime.utcnow()+datetime.timedelta(hours=3),0))
        conn.commit()
    else:
        for value in cursor.execute("SELECT * FROM users"):
            print(value)
@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="В чем смысл каждой игры":
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemroulette = types.KeyboardButton("Рулетка")
        itemdice = types.KeyboardButton("Кости")
        itempocker = types.KeyboardButton("Покер")
        itemblack_jack = types.KeyboardButton("Блэк-Джек")
        itemcoin = types.KeyboardButton("Монетка")
        itemguess_the_number = types.KeyboardButton("Больше-меньше")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemroulette,itemdice,itempocker,itemblack_jack,itemcoin,itemguess_the_number)
        markup_meaning_games.add(item_main_menu)
        mesgmainmenu=bot.send_message(message.chat.id, 'О какой игре вы хотите узнать?', reply_markup=markup_meaning_games)
        bot.register_next_step_handler(mesgmainmenu,message_reply_meaning_games) #при после нажатия на кнопку позволяет приступить к выполнению следующей функции
    elif message.text=="Выбрать игру":
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemroulette = types.KeyboardButton("Рулетка")
        itemdice = types.KeyboardButton("Кости")
        itemblack_jack = types.KeyboardButton("Блэк-Джек")
        itemcoin = types.KeyboardButton("Монетка")
        itemguess_the_number = types.KeyboardButton("Больше-меньше")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemroulette, itemdice, itemblack_jack, itemcoin, itemguess_the_number)
        markup_meaning_games.add(item_main_menu)
        mesgmainmenu = bot.send_message(message.chat.id, 'Во что хотите поиграть?',reply_markup=markup_meaning_games)
        bot.register_next_step_handler(mesgmainmenu, message_reply_selection_game)
    elif message.text=="Баланс":
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"\n\nВаш баланс: {value[0]}",
                             parse_mode='html')
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_POPOLNENIE = types.KeyboardButton("Пополнить баланс")
        item_VYVOD= types.KeyboardButton("Вывеcти денги")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(item_POPOLNENIE,item_VYVOD,item_main_menu,row_width=2)
        mesgmainmenu = bot.send_message(message.chat.id, 'Для продолжения нажмите нужную кнопку', reply_markup=markup_meaning_games)
        bot.register_next_step_handler(mesgmainmenu, balance_knopka)
    elif message.text=="Связь с администрацией":
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(item_main_menu)
        mesgmainmenu = bot.send_message(message.chat.id, 'Напишите ваш запрос и администация с вами свяжится',
                                        reply_markup=markup_meaning_games)
        bot.register_next_step_handler(mesgmainmenu, svyaz_s_adminami)

    else:
        bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
#В ЧЁМ СМЫСЛ ИГР
@bot.message_handler(content_types='text')
def message_reply_meaning_games(message):
    if message.text == "Рулетка":
        mesgRULETKA= bot.send_message(message.chat.id,'*Рулетка* - игра, представляющая собой вращающееся колесо с 36 секторами красного и чёрного цветов и 37-м зелёным сектором «зеро» с обозначением нуля. Игроки, играющие в рулетку, могут сделать ставку на выпадение шарика на цвет (красное или чёрное), чётное или нечётное число, диапазон (1—18 или 19—36) или конкретное число. Крупье запускает шарик над колесом рулетки, который движется в сторону, противоположную вращению колеса рулетки, и в конце концов выпадает на один из секторов. Выигрыши получают все, чья ставка сыграла (ставка на цвет, диапазон, чётное-нечётное или номера).',
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgRULETKA, message_reply_meaning_games)
    elif message.text == "Кости":
        mesgKOSTI = bot.send_message(message.chat.id,'*Кости* - игра, заключающаяся в выбрасывании кубиков и дальнейшем подсчёте очков, количество которых и определяет победителя.(В нашем случае между игроком и казино)',
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgKOSTI, message_reply_meaning_games)
    elif message.text == "Блэк-Джек":
        mesgBLACKDJACK = bot.send_message(message.chat.id,'*Блэк-Джек* - карточная игра, цель которой заключается в том, чтобы набрать как можно больше очков, чем у диллера но не более 21. Раздаётся дилеру и игроку изначально 2 карты, в дальнейшем вы и диллер принимаете решение остановиться и вскрыть карты или взять еще. Значения очков каждой карты: от двойки до десятки — от 2 до 10 соответственно, у туза — 1 или 11 (11 пока общая сумма не больше 21, далее 1), у так называемых картинок (король, дама, валет) — 10.',
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBLACKDJACK, message_reply_meaning_games)
    elif message.text == "Монетка":
        mesgMONETKA = bot.send_message(message.chat.id,'*Монетка* - или же орёл-решка, суть игры заключается в угадывании того что выпадет: орёл или решка.',
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgMONETKA, message_reply_meaning_games)
    elif message.text == "Больше-меньше":
        mesgBOLSHEMENSHE = bot.send_message(message.chat.id,'*Больше-меньше* - суть игры заключается в угадывании исхода. Игроку предлагается выбор из чисел от 1 до 1000000, после выбора он загадывает исход: больше заданного числа или меньше.',
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBOLSHEMENSHE, message_reply_meaning_games)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, message_reply_meaning_games)
#ВЫБРАТЬ ИГРУ
@bot.message_handler(content_types='text')
def message_reply_selection_game(message):
    if message.text == "Рулетка":
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemSTAVKA_NA_CVET = types.KeyboardButton("Поставить на цвет")
        itemSTAVKA_NA_CHISLO = types.KeyboardButton("Поставить на число")
        itemSTAVKA_NA_CHETNOE = types.KeyboardButton("Поставить на чётное или нечётное")
        itemSTAVKA_NA_DIAPAZON = types.KeyboardButton("Поставить на диапазон")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemSTAVKA_NA_CVET, itemSTAVKA_NA_CHISLO, itemSTAVKA_NA_CHETNOE,
                                 itemSTAVKA_NA_DIAPAZON, item_main_menu, row_width=2)
        mesgVYBOR = bot.send_message(message.chat.id, 'Вы выбрали игру - *Рулетка*. Выберите на что хотите поставить',
                                     reply_markup=markup_meaning_games,
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgVYBOR, game_VYBOR_NA_CHTO_POSTAVIT)
    elif message.text == "Кости":
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(item_main_menu)
        bot.send_message(message.chat.id, 'Вы выбрали игру - *Кости*. При выйгрыше ваша ставка умножается на 2, при поражении сгорает. Один кубик',reply_markup=markup_meaning_games,
                             parse_mode= 'Markdown')
        mesgKOSTI = bot.send_message(message.chat.id,'Введите целочисленную сумму ставки(без пробелов) пример: 15')
        bot.register_next_step_handler(mesgKOSTI, message_game_kosti_stavka)
    elif message.text == "Блэк-Джек":
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(item_main_menu)
        mesgDJACK = bot.send_message(message.chat.id,
                         'Вы выбрали игру - *Блэк-Джек*. При выйгрыше ваша ставка умножается на 2, при поражении сгорает. Введите целочисленную сумму ставки',
                         reply_markup=markup_meaning_games,
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgDJACK, prinyat_stavku_DJACK)
    elif message.text == "Монетка":
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(item_main_menu)
        bot.send_message(message.chat.id, 'Вы выбрали игру - *Монетка*. При выйгрыше ваша ставка умножается на 2, при поражении сгорает. Орёл или решка.',reply_markup=markup_meaning_games,
                             parse_mode= 'Markdown')
        mesgMONETKA = bot.send_message(message.chat.id,'Введите целочисленную сумму ставки(без пробелов) пример: 15')
        bot.register_next_step_handler(mesgMONETKA, message_game_monetka_stavka)
    elif message.text == "Больше-меньше":
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemstavka = types.KeyboardButton("Выбрать больше или меньше какого числа")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemstavka, item_main_menu)
        bot.send_message(message.chat.id,'Вы выбрали игру - *Больше-меньше*. При выйгрыше ваша ставка умножается в зависимости от выбранного коэффициента, при поражении сгорает, числа могут выпадать. Числа от 1 до 1000000',reply_markup=markup_meaning_games,
                             parse_mode= 'Markdown')
        mesgBOLSHEMENSHE = bot.send_message(message.chat.id, 'Для продолжения нажмите нужную вам кнопку.')
        bot.register_next_step_handler(mesgBOLSHEMENSHE, game_VYBOR_BOLSHE_ILI_MENSHE_KAKOGO_CHISLA)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, message_reply_selection_game)
#ПОСЛЕ ВЫБОРА ИГРЫ КОСТИ!!!!!!!!!!!!!!!!!!!!!
@bot.message_handler(content_types='text')
def results_dice(message):
    x = {1:'dice/1.gif', 2:'dice/2.gif', 3:'dice/3.gif', 4:'dice/4.gif', 5:'dice/5.gif', 6:'dice/6.gif'}
    y = {1:'dice/1.gif', 2:'dice/2.gif', 3:'dice/3.gif', 4:'dice/4.gif', 5:'dice/5.gif', 6:'dice/6.gif'}
    dice_diller = random.randint(0, 5)
    dice_gamer = random.randint(0, 5)
    print(dice_diller)
    if dice_diller > dice_gamer:
        bot.send_animation(message.chat.id, open(x[dice_diller], 'rb'))
        sleep(5)
        bot.send_message(message.chat.id, f'*Диллер*: {dice_diller} 🎲',
                             parse_mode= 'Markdown')
        bot.send_animation(message.chat.id, open(x[dice_gamer], 'rb'))
        sleep(5)
        bot.send_message(message.chat.id, f'Игрок: {dice_gamer} 🎲')
        bot.send_message(message.chat.id, 'Вы проиграли, ваша ставка сгорает')
        conn.execute(f"UPDATE users SET balance = balance - {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
    elif dice_diller == dice_gamer:
        bot.send_animation(message.chat.id, open(x[dice_diller], 'rb'))
        sleep(5)
        bot.send_message(message.chat.id, f'*Диллер*: {dice_diller} 🎲',
                             parse_mode= 'Markdown')
        bot.send_animation(message.chat.id, open(x[dice_gamer], 'rb'))
        sleep(5)
        bot.send_message(message.chat.id, f'Игрок: {dice_gamer} 🎲')
        bot.send_message(message.chat.id, 'Ничья, ваша ставка остаётся')
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}" ,
                             parse_mode= 'Markdown')
    else:
        bot.send_animation(message.chat.id, open(x[dice_diller], 'rb'))
        sleep(5)
        bot.send_message(message.chat.id, f'*Диллер*: {dice_diller} 🎲',
                             parse_mode= 'Markdown')
        bot.send_animation(message.chat.id, open(x[dice_gamer], 'rb'))
        sleep(5)
        bot.send_message(message.chat.id, f'Игрок: {dice_gamer} 🎲')
        bot.send_message(message.chat.id, 'Вы выйграли, поздравляем!')
        conn.execute(f"UPDATE users SET balance = balance + {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
@bot.message_handler(content_types='text')
def message_game_kosti_stavka(message):
    if message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) <= balance_na_oshibke(message):
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemdice = types.KeyboardButton("Подбросить кости")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemdice, item_main_menu)
        conn.execute(f"UPDATE users SET stavka = {int(message.text)} WHERE user_id = {message.chat.id}")
        conn.commit()
        mesgSTAVKA= bot.send_message(message.chat.id,f'Сумма вашей ставки: *{int(message.text)}* при победе вы получите: *{2*int(message.text)}*, Играем?',reply_markup=markup_meaning_games,
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgSTAVKA, game_kosti_knopki)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    elif message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) >= balance_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем счёте недостаточно средств')
        bot.register_next_step_handler(mesgBAG, message_game_kosti_stavka)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю такой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, message_game_kosti_stavka)
@bot.message_handler(content_types='text')
def game_kosti_knopki(message):
    if message.text == "Подбросить кости" and balance_na_oshibke(message)>=stavka_na_oshibke(message):
        results_dice(message)
        mesgdice=bot.send_message(message.chat.id, f'Играем дальше?',
                       )
        bot.register_next_step_handler(mesgdice, game_kosti_knopki)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    elif message.text == "Подбросить кости" and balance_na_oshibke(message)<=stavka_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем счёте недостаточно средств')
        bot.register_next_step_handler(mesgBAG, game_kosti_knopki)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, game_kosti_knopki)
#ПОСЛЕ ВЫБОРА ИГРЫ МОНЕТКА
@bot.message_handler(content_types='text')
def results_monetka(message):
    x = ['Решка','Орёл']
    monetka_diller = x[random.randint(0, 1)]
    if message.text == monetka_diller and balance_na_oshibke(message)>=stavka_na_oshibke(message):
        bot.send_message(message.chat.id,f'Вы подкинули монету и выпала сторона: *{monetka_diller}* 🪙',
                             parse_mode= 'Markdown')
        mesgBAG = bot.send_message(message.chat.id, 'Вы угадали, поздравляем!')
        conn.execute(
            f"UPDATE users SET balance = balance + {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBAG, results_monetka)
    elif message.text != monetka_diller and (message.text == 'Решка' or message.text == 'Орёл') and balance_na_oshibke(message)>=stavka_na_oshibke(message):
        bot.send_message(message.chat.id, f'Вы подкинули монету и выпала сторона: *{monetka_diller}* 🪙')
        mesgBAG = bot.send_message(message.chat.id, 'Вы не угадали, в следующий раз повезёт!')
        conn.execute(
            f"UPDATE users SET balance = balance - {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBAG, results_monetka)
    elif (message.text == 'Решка' or message.text == 'Орёл') and balance_na_oshibke(message)<=stavka_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем счёте недостаточно средств')
        bot.register_next_step_handler(mesgBAG, results_monetka)
    elif message.text == 'Вернуться в главное меню':
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, results_monetka)
@bot.message_handler(content_types='text')
def message_game_monetka_stavka(message):
    if message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) <= balance_na_oshibke(message):
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemdice = types.KeyboardButton("Подбросить монетку")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemdice, item_main_menu)
        conn.execute(f"UPDATE users SET stavka = {int(message.text)} WHERE user_id = {message.chat.id}")
        conn.commit()
        mesgSTAVKA= bot.send_message(message.chat.id,f'Сумма вашей ставки: *{int(message.text)}* при победе вы получите: *{2*int(message.text)}*, Играем?',reply_markup=markup_meaning_games,
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgSTAVKA, game_monetka_knopki)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    elif message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) >= balance_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем счёте недостаточно средств')
        bot.register_next_step_handler(mesgBAG, message_game_monetka_stavka)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, message_game_monetka_stavka)
@bot.message_handler(content_types='text')
def game_monetka_knopki(message):
    if message.text == "Подбросить монетку" and balance_na_oshibke(message)>=stavka_na_oshibke(message):
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemOREL = types.KeyboardButton("Орёл")
        itemRESHKA = types.KeyboardButton("Решка")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemOREL,itemRESHKA, item_main_menu,row_width=2)
        mesgMONETKA=bot.send_message(message.chat.id, f'Выберете сторону', reply_markup=markup_meaning_games)
        bot.register_next_step_handler(mesgMONETKA, results_monetka)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, game_monetka_knopki)
#ПОСЛЕ ВЫБОРА ИГРЫ БОЛЬШЕ-МЕНЬШЕ
@bot.message_handler(content_types='text')
def game_VYBOR_BOLSHE_ILI_MENSHE_KAKOGO_CHISLA(message):
    if message.text == "Выбрать больше или меньше какого числа":
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemBOLSHE = types.KeyboardButton("Больше")
        itemMENSHE = types.KeyboardButton("Меньше")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemBOLSHE, itemMENSHE, item_main_menu, row_width=2)
        mesgVYBOR = bot.send_message(message.chat.id, 'Выберите больше или меньше',reply_markup=markup_meaning_games)
        bot.register_next_step_handler(mesgVYBOR, game_VYBOR_BOLSHE_ILI_MENSHE)

    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, game_VYBOR_BOLSHE_ILI_MENSHE_KAKOGO_CHISLA)
@bot.message_handler(content_types='text')
def game_VYBOR_BOLSHE_ILI_MENSHE(message):
    if message.text == "Больше":
        mesgSTAVKA = bot.send_message(message.chat.id, 'Введите *ЦЕЛОЧИСЛЕННОЕ* значение больше которого вы считаете выпадет число(от 2 до 999999). Пример: 15673',
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgSTAVKA, game_VYBOR_BOLSHE_MESSAGE)

    elif message.text == "Меньше":
        mesgSTAVKA = bot.send_message(message.chat.id, 'Введите *ЦЕЛОЧИСЛЕННОЕ* значение меньше которого вы считаете выпадет число(от 2 до 999999). Пример: 15673',
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgSTAVKA, game_VYBOR_MENSHE_MESSAGE)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, game_VYBOR_BOLSHE_ILI_MENSHE)
@bot.message_handler(content_types='text')
def game_VYBOR_BOLSHE_MESSAGE(message):
    if message.text.isnumeric() == True and int(message.text) > 1 and int(message.text) < 1000000:
        c = message.text
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(item_main_menu)
        conn.execute(f"UPDATE users SET chislo_bolshe_menshe = {int(c)} WHERE user_id = {message.chat.id}")
        conn.commit()
        conn.execute(f"UPDATE users SET koef = {koef_game_bolshe(int(c))} WHERE user_id = {message.chat.id}")
        conn.commit()
        bot.send_message(message.chat.id,f'Выбрано число: *{int(c)}*, ваш коэффициент: *{koef_game_bolshe(int(c))}*',reply_markup=markup_meaning_games,
                             parse_mode= 'Markdown')
        mesgSTAVKA = bot.send_message(message.chat.id, 'Введите *ЦЕЛОЧИСЛННУЮ* сумму ставки(без пробелов) пример: 15',
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgSTAVKA, message_game_stavka_bolshe)
        return c
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Введите только число от 2 до 999999')
        bot.register_next_step_handler(mesgBAG, game_VYBOR_BOLSHE_MESSAGE)
@bot.message_handler(content_types='text')
def game_VYBOR_MENSHE_MESSAGE(message):
    if message.text.isnumeric() == True and int(message.text) > 1 and int(message.text) < 1000000:
        c = message.text
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(item_main_menu)
        conn.execute(f"UPDATE users SET chislo_bolshe_menshe = {int(c)} WHERE user_id = {message.chat.id}")
        conn.commit()
        conn.execute(f"UPDATE users SET koef = {koef_game_menshe(int(c))} WHERE user_id = {message.chat.id}")
        conn.commit()
        bot.send_message(message.chat.id,f'Выбрано число: *{int(c)}*, ваш коэффициент: *{koef_game_menshe(int(c))}*',reply_markup=markup_meaning_games,
                             parse_mode= 'Markdown')
        mesgSTAVKA = bot.send_message(message.chat.id, 'Введите *ЦЕЛОЧИСЛЕННУЮ* сумму ставки(без пробелов) пример: 15',
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgSTAVKA, message_game_stavka_menshe)
        return c
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Введите только число от 2 до 999999')
        bot.register_next_step_handler(mesgBAG, game_VYBOR_MENSHE_MESSAGE)
@bot.message_handler(content_types='text')
def message_game_stavka_bolshe(message):
    if message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) <= balance_na_oshibke(message):
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemdice = types.KeyboardButton("Подобрать число")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemdice, item_main_menu)
        conn.execute(f"UPDATE users SET stavka = {int(message.text)} WHERE user_id = {message.chat.id}")
        conn.commit()
        mesgSTAVKA= bot.send_message(message.chat.id,f'Сумма вашей ставки: *{int(message.text)}*, Играем?',reply_markup=markup_meaning_games,
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgSTAVKA, message_game_bolshe_podbor_chisla)#выбрать переход к какой
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    elif message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) >= balance_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем балансе недостаточно средств')
        bot.register_next_step_handler(mesgBAG, message_game_stavka_bolshe)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю такой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, message_game_stavka_bolshe)
@bot.message_handler(content_types='text')
def message_game_stavka_menshe(message):
    if message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) <= balance_na_oshibke(message):
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemCHISLA = types.KeyboardButton("Подобрать число")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemCHISLA, item_main_menu)
        conn.execute(f"UPDATE users SET stavka = {int(message.text)} WHERE user_id = {message.chat.id}")
        conn.commit()
        mesgSTAVKA= bot.send_message(message.chat.id,f'Сумма вашей ставки: *{int((message.text))}*, Играем?',reply_markup=markup_meaning_games,
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgSTAVKA, message_game_menshe_podbor_chisla)#выбрать переход к какой
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    elif message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) >= balance_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем балансе недостаточно средств')
        bot.register_next_step_handler(mesgBAG, message_game_stavka_menshe)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю такой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, message_game_stavka_menshe)
@bot.message_handler(content_types='text')
def message_game_bolshe_podbor_chisla(message):
    if message.text == "Подобрать число" and balance_na_oshibke(message)>=stavka_na_oshibke(message):
        mesgPODBOR = bot.send_message(message.chat.id, 'Генерируем число...')
        game_bolshe_podbor_chisla(message)
        bot.register_next_step_handler(mesgPODBOR, message_game_bolshe_podbor_chisla)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    elif message.text == "Подобрать число" and balance_na_oshibke(message)<=stavka_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем счёте недостаточно средств')
        bot.register_next_step_handler(mesgBAG, message_game_bolshe_podbor_chisla)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, message_game_bolshe_podbor_chisla)
@bot.message_handler(content_types='text')
def message_game_menshe_podbor_chisla(message):
    if message.text == "Подобрать число" and balance_na_oshibke(message)>=stavka_na_oshibke(message):
        mesgPODBOR = bot.send_message(message.chat.id, 'Генерируем число...')
        game_menshe_podbor_chisla(message)
        bot.register_next_step_handler(mesgPODBOR, message_game_menshe_podbor_chisla)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    elif message.text == "Подобрать число" and balance_na_oshibke(message)<=stavka_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем счете недостаточно средств.')
        bot.register_next_step_handler(mesgBAG, message_game_menshe_podbor_chisla)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, message_game_menshe_podbor_chisla)
@bot.message_handler(content_types='text')
def game_bolshe_podbor_chisla(message):
    x = list(range(2, 1000000))
    bolshe_menshe_diller = x[random.randint(0, 999998)]
    if chislo_na_oshibke(message) < bolshe_menshe_diller:
        bot.send_message(message.chat.id, f'*Подобранное число*: {bolshe_menshe_diller}',
                             parse_mode= 'Markdown')
        bot.send_message(message.chat.id, f'Ваше загаданное число: {chislo_na_oshibke(message)} оказалось меньше, поздравляем!')
        conn.execute(
            f"UPDATE users SET balance = balance + {stavka_na_oshibke(message)*koef_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
    else:
        bot.send_message(message.chat.id, f'*Подобранное число*: {bolshe_menshe_diller}',
                             parse_mode= 'Markdown')
        bot.send_message(message.chat.id,
                                      f'Ваше загаданное число: {chislo_na_oshibke(message)} оказалось больше, соболезнуем..')
        conn.execute(
            f"UPDATE users SET balance = balance - {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
@bot.message_handler(content_types='text')
def game_menshe_podbor_chisla(message):
    x = list(range(2, 1000000))
    bolshe_menshe_diller = x[random.randint(0, 999998)]
    if chislo_na_oshibke(message) > bolshe_menshe_diller:
        bot.send_message(message.chat.id, f'*Подобранное число*: {bolshe_menshe_diller}')
        bot.send_message(message.chat.id, f'Ваше загаданное число: {chislo_na_oshibke(message)} оказалось больше, поздравляем!')
        conn.execute(
            f"UPDATE users SET balance = balance + {stavka_na_oshibke(message) * koef_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
    else:
        bot.send_message(message.chat.id, f'*Подобранное число*: {bolshe_menshe_diller}',
                             parse_mode= 'Markdown')
        bot.send_message(message.chat.id,
                                      f'Ваше загаданное число: {chislo_na_oshibke(message)} оказалось меньше, соболезнуем..')
        conn.execute(
            f"UPDATE users SET balance = balance - {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
def koef_game_menshe(message):
    x = 1000000/(int(message)-1)
    return round(x,3)
def koef_game_bolshe(message):
    x = 1000000 / (1000000 - int(message))
    return round(x,3)
#ПОСЛЕ ВЫБОРА ИГРЫ РУЛЕТКА
#выбор на что поставить(рулетка)
@bot.message_handler(content_types='text')
def game_VYBOR_NA_CHTO_POSTAVIT(message):
    if message.text == "Поставить на цвет":
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemKRASNIY = types.KeyboardButton("КРАСНЫЙ")
        itemCHERNIY = types.KeyboardButton("ЧЁРНЫЙ")
        itemZELENIY = types.KeyboardButton("ЗЕЛЁНЫЙ")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemKRASNIY, itemCHERNIY, itemZELENIY, item_main_menu, row_width=3)
        mesgSTAVKA = bot.send_message(message.chat.id, 'Выберите цвет на который хотите поставить',reply_markup=markup_meaning_games)
        bot.register_next_step_handler(mesgSTAVKA, game_POSLE_VYBOR_CVETA)
    elif message.text == "Поставить на число":
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(item_main_menu)
        mesgSTAVKA = bot.send_message(message.chat.id, 'Введите число на которое хотите поставить',reply_markup=markup_meaning_games)
        bot.register_next_step_handler(mesgSTAVKA, game_POSLE_VYBOR_CHISLA)
    elif message.text == "Поставить на чётное или нечётное":
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemCHETNIY = types.KeyboardButton("ЧЁТНОЕ")
        itemNECHETNIY = types.KeyboardButton("НЕЧЁТНОЕ")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemCHETNIY, itemNECHETNIY, item_main_menu, row_width=2)
        mesgSTAVKA = bot.send_message(message.chat.id, 'Выберите на что вы хотите поставить: чётное или нечётное',
                                      reply_markup=markup_meaning_games)
        bot.register_next_step_handler(mesgSTAVKA, game_POSLE_VYBOR_CHETNOSTI)
    elif message.text == "Поставить на диапазон":
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemDO18 = types.KeyboardButton("1-18")
        itemPOSLE18 = types.KeyboardButton("19-36")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemDO18, itemPOSLE18, item_main_menu, row_width=2)
        mesgSTAVKA = bot.send_message(message.chat.id, 'Выберите на какой диапазон вы хотите поставить: 1-18 или 19-36',
                                      reply_markup=markup_meaning_games)
        bot.register_next_step_handler(mesgSTAVKA, game_POSLE_VYBOR_DIAPAZONA)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, game_VYBOR_NA_CHTO_POSTAVIT)
#Поставить на цвет(рулетка)
@bot.message_handler(content_types='text')
def game_POSLE_VYBOR_CVETA(message):
    if message.text == "ЧЁРНЫЙ" or message.text == "КРАСНЫЙ":
        conn.execute(f"UPDATE users SET na_chto_stavim_ruletka = '{message.text}' WHERE user_id = {message.chat.id}")
        conn.commit()
        bot.send_message(message.chat.id, 'В случае выйгрыша вы получаете удвоенную сумму вашей ставки')
        mesgVYBOR = bot.send_message(message.chat.id, 'Введите *ЦЕЛОЧИСЛЕННУЮ* сумму ставки(без пробелов) пример: 15',
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgVYBOR, prinyat_stavku)
    elif message.text == "ЗЕЛЁНЫЙ":
        conn.execute(f"UPDATE users SET na_chto_stavim_ruletka = '{message.text}' WHERE user_id = {message.chat.id}")
        conn.commit()
        bot.send_message(message.chat.id, 'В случае выйгрыша вы получаете сумму вашей ставки увеличенную в 35 раз')
        mesgVYBOR = bot.send_message(message.chat.id, 'Введите *ЦЕЛОЧИСЛЕННУЮ* сумму ставки(без пробелов) пример: 15',
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgVYBOR, prinyat_stavku)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, game_POSLE_VYBOR_CVETA)
#зарегать ставку(рулетка)
def prinyat_stavku(message):
    if message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) <= balance_na_oshibke(message):
        conn.execute(f"UPDATE users SET stavka = {int(message.text)} WHERE user_id = {message.chat.id}")
        conn.commit()
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemVRASHAEM = types.KeyboardButton("Вращать рулетку")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemVRASHAEM, item_main_menu, row_width=1)
        mesgSTAVKA= bot.send_message(message.chat.id,f'Сумма вашей ставки: *{int(message.text)}*, для продолжения нажмите "Вращать рулетку"',reply_markup=markup_meaning_games,
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgSTAVKA, game_VRASHAEM_RULETKU)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    elif message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) >= balance_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем счёте недостаточно средств')
        bot.register_next_step_handler(mesgBAG, prinyat_stavku)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю такой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, prinyat_stavku)
#вращать рулетку со ставкой на цвет(рулетка)
@bot.message_handler(content_types='text')
def game_VRASHAEM_RULETKU(message):
    if message.text == "Вращать рулетку" and balance_na_oshibke(message)>=stavka_na_oshibke(message):
      RULETKA_STAVKA_NA_CVET(message)
    elif message.text == "Вращать рулетку" and balance_na_oshibke(message)<=stavka_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем счёте недостаточно средств')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU)
#алгоритм игры в рулетку со ставкой на цвет(рулетка)
def RULETKA_STAVKA_NA_CVET(message):
    znacheniya = {0:'ЗЕЛЁНЫЙ',
                  1:'КРАСНЫЙ',
                  2:'ЧЁРНЫЙ',
                  3:'КРАСНЫЙ',
                  4:'ЧЁРНЫЙ',
                  5:'КРАСНЫЙ',
                  6:'ЧЁРНЫЙ',
                  7:'КРАСНЫЙ',
                  8:'ЧЁРНЫЙ',
                  9:'КРАСНЫЙ',
                  10:'ЧЁРНЫЙ',
                  11:'ЧЁРНЫЙ',
                  12:'КРАСНЫЙ',
                  13:'ЧЁРНЫЙ',
                  14:'КРАСНЫЙ',
                  15:'ЧЁРНЫЙ',
                  16:'КРАСНЫЙ',
                  17:'ЧЁРНЫЙ',
                  18:'КРАСНЫЙ',
                  19:'КРАСНЫЙ',
                  20:'ЧЁРНЫЙ',
                  21:'КРАСНЫЙ',
                  22:'ЧЁРНЫЙ',
                  23:'КРАСНЫЙ',
                  24:'ЧЁРНЫЙ',
                  25:'КРАСНЫЙ',
                  26:'ЧЁРНЫЙ',
                  27:'КРАСНЫЙ',
                  28:'ЧЁРНЫЙ',
                  29:'ЧЁРНЫЙ',
                  30:'КРАСНЫЙ',
                  31:'ЧЁРНЫЙ',
                  32:'КРАСНЫЙ',
                  33:'ЧЁРНЫЙ',
                  34:'КРАСНЫЙ',
                  35:'ЧЁРНЫЙ',
                  36:'КРАСНЫЙ'}
    chislo = random.randint(0,36)
    if na_chto_stavim_ruletka(message)==znacheniya[chislo] and (na_chto_stavim_ruletka(message)=='КРАСНЫЙ' or na_chto_stavim_ruletka(message)=='ЧЁРНЫЙ'):
        bot.send_message(message.chat.id, f'В результате вращения выпало число: *{chislo}* у которого *{znacheniya[chislo]}* цвет',
                             parse_mode= 'Markdown')
        mesgBAG = bot.send_message(message.chat.id, 'Вы угадали, поздравляем!')
        conn.execute(
            f"UPDATE users SET balance = balance + {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU)
    elif na_chto_stavim_ruletka(message) == 'ЗЕЛЁНЫЙ' and na_chto_stavim_ruletka(message)==znacheniya[chislo]:
        bot.send_message(message.chat.id,
                         f'В результате вращения выпало число: *{chislo}* у которого *{znacheniya[chislo]}* цвет',
                             parse_mode= 'Markdown')
        mesgBAG = bot.send_message(message.chat.id, 'Вы угадали, поздравляем!')
        conn.execute(
            f"UPDATE users SET balance = balance + 35*{stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU)
    else:
        bot.send_message(message.chat.id,
                         f'В результате вращения выпало число: *{chislo}* у которого *{znacheniya[chislo]}* цвет',
                             parse_mode= 'Markdown')
        mesgBAG = bot.send_message(message.chat.id, 'Вы не угадали, соболезнуем!')
        conn.execute(
            f"UPDATE users SET balance = balance - {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU)
#Поставить на число(рулетка)
@bot.message_handler(content_types='text')
def game_POSLE_VYBOR_CHISLA(message):
    if message.text.isnumeric() == True and int(message.text) >= 0 and int(message.text) <= 36:
        conn.execute(f"UPDATE users SET na_chto_stavim_ruletka = {int(message.text)} WHERE user_id = {message.chat.id}")
        conn.commit()
        bot.send_message(message.chat.id, 'В случае выйгрыша вы получаете сумму вашей ставки увеличенную в 35 раз')
        mesgVYBOR = bot.send_message(message.chat.id, 'Введите *ЦЕЛОЧИСЛЕННУЮ* сумму ставки(без пробелов) пример: 15',
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgVYBOR, prinyat_stavku_na_chislo)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, game_POSLE_VYBOR_CHISLA)
#зарегать ставку на число(рулетка)
def prinyat_stavku_na_chislo(message):
    if message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) <= balance_na_oshibke(message):
        conn.execute(f"UPDATE users SET stavka = {int(message.text)} WHERE user_id = {message.chat.id}")
        conn.commit()
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemVRASHAEM = types.KeyboardButton("Вращать рулетку")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemVRASHAEM, item_main_menu, row_width=1)
        mesgSTAVKA= bot.send_message(message.chat.id,f'Сумма вашей ставки: *{int(message.text)}*, для продолжения нажмите "Вращать рулетку"',reply_markup=markup_meaning_games,
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgSTAVKA, game_VRASHAEM_RULETKU_STAVKA_NA_CHISLO)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    elif message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) >= balance_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем счёте недостаточно средств')
        bot.register_next_step_handler(mesgBAG, prinyat_stavku_na_chislo)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю такой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, prinyat_stavku_na_chislo)
#вращать рулетку со ставкой на число(рулетка)
@bot.message_handler(content_types='text')
def game_VRASHAEM_RULETKU_STAVKA_NA_CHISLO(message):
    if message.text == "Вращать рулетку" and balance_na_oshibke(message)>=stavka_na_oshibke(message):
      RULETKA_STAVKA_NA_CHISLO(message)
    elif message.text == "Вращать рулетку" and balance_na_oshibke(message)<=stavka_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем счёте недостаточно средств')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_STAVKA_NA_CHISLO)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_STAVKA_NA_CHISLO)
#алгоритм игры в рулетку со ставкой на число(рулетка)
def RULETKA_STAVKA_NA_CHISLO(message):
    znacheniya = {0:'ЗЕЛЁНЫЙ',
                  1:'КРАСНЫЙ',
                  2:'ЧЁРНЫЙ',
                  3:'КРАСНЫЙ',
                  4:'ЧЁРНЫЙ',
                  5:'КРАСНЫЙ',
                  6:'ЧЁРНЫЙ',
                  7:'КРАСНЫЙ',
                  8:'ЧЁРНЫЙ',
                  9:'КРАСНЫЙ',
                  10:'ЧЁРНЫЙ',
                  11:'ЧЁРНЫЙ',
                  12:'КРАСНЫЙ',
                  13:'ЧЁРНЫЙ',
                  14:'КРАСНЫЙ',
                  15:'ЧЁРНЫЙ',
                  16:'КРАСНЫЙ',
                  17:'ЧЁРНЫЙ',
                  18:'КРАСНЫЙ',
                  19:'КРАСНЫЙ',
                  20:'ЧЁРНЫЙ',
                  21:'КРАСНЫЙ',
                  22:'ЧЁРНЫЙ',
                  23:'КРАСНЫЙ',
                  24:'ЧЁРНЫЙ',
                  25:'КРАСНЫЙ',
                  26:'ЧЁРНЫЙ',
                  27:'КРАСНЫЙ',
                  28:'ЧЁРНЫЙ',
                  29:'ЧЁРНЫЙ',
                  30:'КРАСНЫЙ',
                  31:'ЧЁРНЫЙ',
                  32:'КРАСНЫЙ',
                  33:'ЧЁРНЫЙ',
                  34:'КРАСНЫЙ',
                  35:'ЧЁРНЫЙ',
                  36:'КРАСНЫЙ'}
    chislo = random.randint(0,36)
    if int(na_chto_stavim_ruletka(message))==chislo:
        bot.send_message(message.chat.id,
                         f'В результате вращения выпало число: *{chislo}* у которого *{znacheniya[chislo]}* цвет',
                             parse_mode= 'Markdown')
        mesgBAG = bot.send_message(message.chat.id, 'Вы угадали, поздравляем!')
        conn.execute(
            f"UPDATE users SET balance = balance + 35*{stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_STAVKA_NA_CHISLO)
    else:
        bot.send_message(message.chat.id,
                         f'В результате вращения выпало число: *{chislo}* у которого *{znacheniya[chislo]}* цвет',
                             parse_mode= 'Markdown')
        mesgBAG = bot.send_message(message.chat.id, 'Вы не угадали, соболезнуем!')
        conn.execute(
            f"UPDATE users SET balance = balance - {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_STAVKA_NA_CHISLO)
#Поставить на чётное или нечётное(рулетка)
@bot.message_handler(content_types='text')
def game_POSLE_VYBOR_CHETNOSTI(message):
    if message.text == "ЧЁТНОЕ" or message.text == "НЕЧЁТНОЕ":
        conn.execute(f"UPDATE users SET na_chto_stavim_ruletka = '{message.text}' WHERE user_id = {message.chat.id}")
        conn.commit()
        bot.send_message(message.chat.id, 'В случае выйгрыша вы получаете удвоенную сумму вашей ставки')
        mesgVYBOR = bot.send_message(message.chat.id, 'Введите *ЦЕЛОЧИСЛЕННУЮ* сумму ставки(без пробелов) пример: 15',
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgVYBOR, prinyat_stavku_chetnost)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, game_POSLE_VYBOR_CHETNOSTI)
#зарегать ставку(рулетка)
def prinyat_stavku_chetnost(message):
    if message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) <= balance_na_oshibke(message):
        conn.execute(f"UPDATE users SET stavka = {int(message.text)} WHERE user_id = {message.chat.id}")
        conn.commit()
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemVRASHAEM = types.KeyboardButton("Вращать рулетку")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemVRASHAEM, item_main_menu, row_width=1)
        mesgSTAVKA= bot.send_message(message.chat.id,f'Сумма вашей ставки: *{int(message.text)}*, для продолжения нажмите "Вращать рулетку"',reply_markup=markup_meaning_games,
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgSTAVKA, game_VRASHAEM_RULETKU_CHETNOST)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    elif message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) >= balance_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем счёте недостаточно средств')
        bot.register_next_step_handler(mesgBAG, prinyat_stavku_chetnost)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю такой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, prinyat_stavku_chetnost)
#вращать рулетку со ставкой на чётность(рулетка)
@bot.message_handler(content_types='text')
def game_VRASHAEM_RULETKU_CHETNOST(message):
    if message.text == "Вращать рулетку" and balance_na_oshibke(message)>=stavka_na_oshibke(message):
      RULETKA_STAVKA_NA_CHETNOST(message)
    elif message.text == "Вращать рулетку" and balance_na_oshibke(message)<=stavka_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем счёте недостаточно средств')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_CHETNOST)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_CHETNOST)
#алгоритм игры в рулетку со ставкой на чётность(рулетка)
def RULETKA_STAVKA_NA_CHETNOST(message):
    znacheniya = {0:'ЗЕЛЁНЫЙ',
                  1:'КРАСНЫЙ',
                  2:'ЧЁРНЫЙ',
                  3:'КРАСНЫЙ',
                  4:'ЧЁРНЫЙ',
                  5:'КРАСНЫЙ',
                  6:'ЧЁРНЫЙ',
                  7:'КРАСНЫЙ',
                  8:'ЧЁРНЫЙ',
                  9:'КРАСНЫЙ',
                  10:'ЧЁРНЫЙ',
                  11:'ЧЁРНЫЙ',
                  12:'КРАСНЫЙ',
                  13:'ЧЁРНЫЙ',
                  14:'КРАСНЫЙ',
                  15:'ЧЁРНЫЙ',
                  16:'КРАСНЫЙ',
                  17:'ЧЁРНЫЙ',
                  18:'КРАСНЫЙ',
                  19:'КРАСНЫЙ',
                  20:'ЧЁРНЫЙ',
                  21:'КРАСНЫЙ',
                  22:'ЧЁРНЫЙ',
                  23:'КРАСНЫЙ',
                  24:'ЧЁРНЫЙ',
                  25:'КРАСНЫЙ',
                  26:'ЧЁРНЫЙ',
                  27:'КРАСНЫЙ',
                  28:'ЧЁРНЫЙ',
                  29:'ЧЁРНЫЙ',
                  30:'КРАСНЫЙ',
                  31:'ЧЁРНЫЙ',
                  32:'КРАСНЫЙ',
                  33:'ЧЁРНЫЙ',
                  34:'КРАСНЫЙ',
                  35:'ЧЁРНЫЙ',
                  36:'КРАСНЫЙ'}
    chislo = random.randint(0,36)
    chetnoe = list(range(2,37))[0::2]
    nechetnoe = list(range(1,37))[0::2]
    if na_chto_stavim_ruletka(message)=='ЧЁТНОЕ' and (chislo in chetnoe) == True:
        bot.send_message(message.chat.id, f'В результате вращения выпало *ЧЁТНОЕ* число: *{chislo}* у которого *{znacheniya[chislo]}* цвет',
                             parse_mode= 'Markdown')
        mesgBAG = bot.send_message(message.chat.id, 'Вы угадали, поздравляем!')
        conn.execute(
            f"UPDATE users SET balance = balance + {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_CHETNOST)
    elif na_chto_stavim_ruletka(message) == 'НЕЧЁТНОЕ' and (chislo in nechetnoe) == True:
        bot.send_message(message.chat.id,
                         f'В результате вращения выпало *НЕЧЁТНОЕ* число: *{chislo}* у которого *{znacheniya[chislo]}* цвет',
                             parse_mode= 'Markdown')
        mesgBAG = bot.send_message(message.chat.id, 'Вы угадали, поздравляем!')
        conn.execute(
            f"UPDATE users SET balance = balance + {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_CHETNOST)
    elif na_chto_stavim_ruletka(message) == 'ЧЁТНОЕ' and (chislo in chetnoe) == False and chislo != 0:
        bot.send_message(message.chat.id,
                         f'В результате вращения выпало *НЕЧЁТНОЕ* число: *{chislo}* у которого *{znacheniya[chislo]}* цвет',
                             parse_mode= 'Markdown')
        mesgBAG = bot.send_message(message.chat.id, 'Вы не угадали, соболезнуем!')
        conn.execute(
            f"UPDATE users SET balance = balance - {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_CHETNOST)
    elif na_chto_stavim_ruletka(message) == 'НЕЧЁТНОЕ' and (chislo in nechetnoe) == False and chislo != 0:
        bot.send_message(message.chat.id,
                         f'В результате вращения выпало *ЧЁТНОЕ* число: *{chislo}* у которого *{znacheniya[chislo]}* цвет',
                             parse_mode= 'Markdown')
        mesgBAG = bot.send_message(message.chat.id, 'Вы не угадали, соболезнуем!')
        conn.execute(
            f"UPDATE users SET balance = balance - {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_CHETNOST)
    else:
        bot.send_message(message.chat.id,
                         f'В результате вращения выпало число: *{chislo}* у которого *{znacheniya[chislo]}* цвет',
                             parse_mode= 'Markdown')
        mesgBAG = bot.send_message(message.chat.id, 'Вы не угадали, соболезнуем!')
        conn.execute(
            f"UPDATE users SET balance = balance - {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_CHETNOST)
#Поставить на диапазон(рулетка)
@bot.message_handler(content_types='text')
def game_POSLE_VYBOR_DIAPAZONA(message):
    if message.text == "1-18" or message.text == "19-36":
        conn.execute(f"UPDATE users SET na_chto_stavim_ruletka = '{message.text}' WHERE user_id = {message.chat.id}")
        conn.commit()
        bot.send_message(message.chat.id, 'В случае выйгрыша вы получаете удвоенную сумму вашей ставки')
        mesgVYBOR = bot.send_message(message.chat.id, 'Введите *ЦЕЛОЧИСЛЕННУЮ* сумму ставки(без пробелов) пример: 15',
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgVYBOR, prinyat_stavku_DIAPAZON)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, game_POSLE_VYBOR_DIAPAZONA)
#зарегать ставку(рулетка)
def prinyat_stavku_DIAPAZON(message):
    if message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) <= balance_na_oshibke(message):
        conn.execute(f"UPDATE users SET stavka = {int(message.text)} WHERE user_id = {message.chat.id}")
        conn.commit()
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemVRASHAEM = types.KeyboardButton("Вращать рулетку")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemVRASHAEM, item_main_menu, row_width=1)
        mesgSTAVKA= bot.send_message(message.chat.id,f'Сумма вашей ставки: *{int(message.text)}*, для продолжения нажмите "Вращать рулетку"',reply_markup=markup_meaning_games,
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgSTAVKA, game_VRASHAEM_RULETKU_DIAPAZON)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    elif message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) >= balance_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем счёте недостаточно средств')
        bot.register_next_step_handler(mesgBAG, prinyat_stavku_DIAPAZON)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю такой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, prinyat_stavku_DIAPAZON)
#вращать рулетку со ставкой на диапазон(рулетка)
@bot.message_handler(content_types='text')
def game_VRASHAEM_RULETKU_DIAPAZON(message):
    if message.text == "Вращать рулетку" and balance_na_oshibke(message)>=stavka_na_oshibke(message):
      RULETKA_STAVKA_NA_DIAPAZON(message)
    elif message.text == "Вращать рулетку" and balance_na_oshibke(message)<=stavka_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем счёте недостаточно средств')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_DIAPAZON)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_DIAPAZON)
#алгоритм игры в рулетку со ставкой на диапазон(рулетка)
def RULETKA_STAVKA_NA_DIAPAZON(message):
    znacheniya = {0:'ЗЕЛЁНЫЙ',
                  1:'КРАСНЫЙ',
                  2:'ЧЁРНЫЙ',
                  3:'КРАСНЫЙ',
                  4:'ЧЁРНЫЙ',
                  5:'КРАСНЫЙ',
                  6:'ЧЁРНЫЙ',
                  7:'КРАСНЫЙ',
                  8:'ЧЁРНЫЙ',
                  9:'КРАСНЫЙ',
                  10:'ЧЁРНЫЙ',
                  11:'ЧЁРНЫЙ',
                  12:'КРАСНЫЙ',
                  13:'ЧЁРНЫЙ',
                  14:'КРАСНЫЙ',
                  15:'ЧЁРНЫЙ',
                  16:'КРАСНЫЙ',
                  17:'ЧЁРНЫЙ',
                  18:'КРАСНЫЙ',
                  19:'КРАСНЫЙ',
                  20:'ЧЁРНЫЙ',
                  21:'КРАСНЫЙ',
                  22:'ЧЁРНЫЙ',
                  23:'КРАСНЫЙ',
                  24:'ЧЁРНЫЙ',
                  25:'КРАСНЫЙ',
                  26:'ЧЁРНЫЙ',
                  27:'КРАСНЫЙ',
                  28:'ЧЁРНЫЙ',
                  29:'ЧЁРНЫЙ',
                  30:'КРАСНЫЙ',
                  31:'ЧЁРНЫЙ',
                  32:'КРАСНЫЙ',
                  33:'ЧЁРНЫЙ',
                  34:'КРАСНЫЙ',
                  35:'ЧЁРНЫЙ',
                  36:'КРАСНЫЙ'}
    chislo = random.randint(0,36)
    do18 = list(range(1,19))
    posle18 = list(range(19,37))
    if na_chto_stavim_ruletka(message)=='1-18' and (chislo in do18) == True:
        bot.send_message(message.chat.id, f'В результате вращения выпало число: *{chislo}* из диапазона *1-18* у которого *{znacheniya[chislo]}* цвет',
                             parse_mode= 'Markdown')
        mesgBAG = bot.send_message(message.chat.id, 'Вы угадали, поздравляем!')
        conn.execute(
            f"UPDATE users SET balance = balance + {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_DIAPAZON)
    elif na_chto_stavim_ruletka(message) == '19-36' and (chislo in posle18) == True:
        bot.send_message(message.chat.id,
                         f'В результате вращения выпало число: *{chislo}* из диапазона *19-36* у которого *{znacheniya[chislo]}* цвет',
                             parse_mode= 'Markdown')
        mesgBAG = bot.send_message(message.chat.id, 'Вы угадали, поздравляем!')
        conn.execute(
            f"UPDATE users SET balance = balance + {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_DIAPAZON)
    elif na_chto_stavim_ruletka(message) == '1-18' and (chislo in do18) == False and chislo != 0:
        bot.send_message(message.chat.id,
                         f'В результате вращения выпало число: *{chislo}* из диапазона *19-36* у которого *{znacheniya[chislo]}* цвет',
                             parse_mode= 'Markdown')
        mesgBAG = bot.send_message(message.chat.id, 'Вы не угадали, соболезнуем!')
        conn.execute(
            f"UPDATE users SET balance = balance - {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_DIAPAZON)
    elif na_chto_stavim_ruletka(message) == '19-36' and (chislo in posle18) == False and chislo != 0:
        bot.send_message(message.chat.id,
                         f'В результате вращения выпало число: *{chislo}* из диапазона *1-18* у которого *{znacheniya[chislo]}* цвет',
                             parse_mode= 'Markdown')
        mesgBAG = bot.send_message(message.chat.id, 'Вы не угадали, соболезнуем!')
        conn.execute(
            f"UPDATE users SET balance = balance - {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_DIAPAZON)
    else:
        bot.send_message(message.chat.id,
                         f'В результате вращения выпало число: *{chislo}* у которого *{znacheniya[chislo]}* цвет',
                             parse_mode= 'Markdown')
        mesgBAG = bot.send_message(message.chat.id, 'Вы не угадали, соболезнуем!')
        conn.execute(
            f"UPDATE users SET balance = balance - {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgBAG, game_VRASHAEM_RULETKU_DIAPAZON)

#ПОСЛЕ ВЫБОРА ИГРЫ БЛЭК-ДЖЭК

#зарегать ставку(БЛЭК-ДЖЭК)
@bot.message_handler(content_types='text')
def prinyat_stavku_DJACK(message):
    if message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) <= balance_na_oshibke(message):
        conn.execute(f"UPDATE users SET stavka = {int(message.text)} WHERE user_id = {message.chat.id}")
        conn.commit()
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemVRASHAEM = types.KeyboardButton("Раздать карты")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemVRASHAEM, item_main_menu, row_width=1)
        mesgSTAVKA= bot.send_message(message.chat.id,f'Сумма вашей ставки: *{int(message.text)}*, для продолжения нажмите "Раздать карты"',reply_markup=markup_meaning_games,
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgSTAVKA, game_RAZDAT_KARTY)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    elif message.text.isnumeric() == True and int(message.text) > 0 and int(message.text) >= balance_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем счёте недостаточно средств')
        bot.register_next_step_handler(mesgBAG, prinyat_stavku_DJACK)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю такой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, prinyat_stavku_DJACK)
#раздать карты(блэк-джэк)
@bot.message_handler(content_types='text')
def game_RAZDAT_KARTY(message):
    if message.text == "Раздать карты" and balance_na_oshibke(message)>=stavka_na_oshibke(message):
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item2KARTY = types.KeyboardButton("Получить 2 карты")
        item_main_menu = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(item2KARTY, item_main_menu)
        mesg2KARTY = bot.send_message(message.chat.id, 'Диллер уже получил свои карты, теперь ваша очередь.',reply_markup=markup_meaning_games)
        bot.register_next_step_handler(mesg2KARTY, game_PROCESS_RAZDACHI)
    elif message.text == "Раздать карты" and balance_na_oshibke(message)<=stavka_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем счёте недостаточно средств')
        bot.register_next_step_handler(mesgBAG, game_RAZDAT_KARTY)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, game_RAZDAT_KARTY)
#процесс раздачи карт игроку
@bot.message_handler(content_types='text')
def game_PROCESS_RAZDACHI(message):
    if message.text == "Получить 2 карты":
        colloda = {'2♦': 2, '2♣': 2, '2♥': 2, '2♠': 2,
                   '3♦': 3, '3♣': 3, '3♥': 3, '3♠': 3,
                   '4♦': 4, '4♣': 4, '4♥': 4, '4♠': 4,
                   '5♦': 5, '5♣': 5, '5♥': 5, '5♠': 5,
                   '6♦': 6, '6♣': 6, '6♥': 6, '6♠': 6,
                   '7♦': 7, '7♣': 7, '7♥': 7, '7♠': 7,
                   '8♦': 8, '8♣': 8, '8♥': 8, '8♠': 8,
                   '9♦': 9, '9♣': 9, '9♥': 9, '9♠': 9,
                   '10♦': 10, '10♣': 10, '10♥': 10, '10♠': 10,
                   'В♦': 10, 'В♣': 10, 'В♥': 10, 'В♠': 10,
                   'Д♦': 10, 'Д♣': 10, 'Д♥': 10, 'Д♠': 10,
                   'К♦': 10, 'К♣': 10, 'К♥': 10, 'К♠': 10,
                   'А♦': 11, 'А♣': 11, 'А♥': 11, 'А♠': 11,
                   }
        karta1 = POLUCHENIE_PERVOY_KARTY(message,colloda)
        karta2 = POLUCHENIE_VTOROY_KARTY(message,karta1)
        for value in conn.execute(f"SELECT kakie_karty_black_djack FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"Ваши карты: {value[0]}",
                             parse_mode='html')
        for value in conn.execute(f"SELECT ochki_black_djack FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"Ваши очки: {value[0]}",
                             parse_mode='html')
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemKARTY = types.KeyboardButton("Получить ещё карту")
        itemOSTANOVKA = types.KeyboardButton("Остановиться")
        markup_meaning_games.add(itemKARTY,itemOSTANOVKA, row_width=2)
        mesg2KARTY = bot.send_message(message.chat.id, 'Ещё карту или останавливаемся?',
                                      reply_markup=markup_meaning_games)
        bot.register_next_step_handler(mesg2KARTY, game_PROCESS_RAZDACHI_ESHE)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, game_PROCESS_RAZDACHI)
#Взять еще карту
@bot.message_handler(content_types='text')
def game_PROCESS_RAZDACHI_ESHE(message):
    if message.text == "Получить ещё карту" and ochki_djack(message) >= 11 and ochki_djack(message) <=21:
        colloda = {'2♦': 2, '2♣': 2, '2♥': 2, '2♠': 2,
                   '3♦': 3, '3♣': 3, '3♥': 3, '3♠': 3,
                   '4♦': 4, '4♣': 4, '4♥': 4, '4♠': 4,
                   '5♦': 5, '5♣': 5, '5♥': 5, '5♠': 5,
                   '6♦': 6, '6♣': 6, '6♥': 6, '6♠': 6,
                   '7♦': 7, '7♣': 7, '7♥': 7, '7♠': 7,
                   '8♦': 8, '8♣': 8, '8♥': 8, '8♠': 8,
                   '9♦': 9, '9♣': 9, '9♥': 9, '9♠': 9,
                   '10♦': 10, '10♣': 10, '10♥': 10, '10♠': 10,
                   'В♦': 10, 'В♣': 10, 'В♥': 10, 'В♠': 10,
                   'Д♦': 10, 'Д♣': 10, 'Д♥': 10, 'Д♠': 10,
                   'К♦': 10, 'К♣': 10, 'К♥': 10, 'К♠': 10,
                   'А♦': 1, 'А♣': 1, 'А♥': 1, 'А♠': 1,
                   }
        for value in conn.execute(f"SELECT kakie_karty_black_djack FROM users WHERE user_id = {message.chat.id}"):
            spisok_kart_ispolzuemyh = value[0].split(' ')
            kartaESHE = POLUCHENIE_KART(message, spisok_kart(spisok_kart_ispolzuemyh,colloda))
        for value in conn.execute(f"SELECT kakie_karty_black_djack FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"Ваши карты: {value[0]}",
                             parse_mode='html')
        for value in conn.execute(f"SELECT ochki_black_djack FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"Ваши очки: {value[0]}",
                             parse_mode='html')
        proverka_ochkov(message)
    elif message.text == "Получить ещё карту" and ochki_djack(message) < 11:
        colloda = {'2♦': 2, '2♣': 2, '2♥': 2, '2♠': 2,
                   '3♦': 3, '3♣': 3, '3♥': 3, '3♠': 3,
                   '4♦': 4, '4♣': 4, '4♥': 4, '4♠': 4,
                   '5♦': 5, '5♣': 5, '5♥': 5, '5♠': 5,
                   '6♦': 6, '6♣': 6, '6♥': 6, '6♠': 6,
                   '7♦': 7, '7♣': 7, '7♥': 7, '7♠': 7,
                   '8♦': 8, '8♣': 8, '8♥': 8, '8♠': 8,
                   '9♦': 9, '9♣': 9, '9♥': 9, '9♠': 9,
                   '10♦': 10, '10♣': 10, '10♥': 10, '10♠': 10,
                   'В♦': 10, 'В♣': 10, 'В♥': 10, 'В♠': 10,
                   'Д♦': 10, 'Д♣': 10, 'Д♥': 10, 'Д♠': 10,
                   'К♦': 10, 'К♣': 10, 'К♥': 10, 'К♠': 10,
                   'А♦': 11, 'А♣': 11, 'А♥': 11, 'А♠': 11,
                   }
        for value in conn.execute(f"SELECT kakie_karty_black_djack FROM users WHERE user_id = {message.chat.id}"):
            spisok_kart_ispolzuemyh = value[0].split(' ')
            kartaESHE = POLUCHENIE_KART(message, spisok_kart(spisok_kart_ispolzuemyh,colloda))
        for value in conn.execute(f"SELECT kakie_karty_black_djack FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"Ваши карты: {value[0]}",
                             parse_mode='html')
        for value in conn.execute(f"SELECT ochki_black_djack FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"Ваши очки: {value[0]}",
                             parse_mode='html')
        proverka_ochkov(message)
    elif message.text == "Остановиться" and ochki_djack(message) <= 21:
        colloda = {'2♦': 2, '2♣': 2, '2♥': 2, '2♠': 2,
                   '3♦': 3, '3♣': 3, '3♥': 3, '3♠': 3,
                   '4♦': 4, '4♣': 4, '4♥': 4, '4♠': 4,
                   '5♦': 5, '5♣': 5, '5♥': 5, '5♠': 5,
                   '6♦': 6, '6♣': 6, '6♥': 6, '6♠': 6,
                   '7♦': 7, '7♣': 7, '7♥': 7, '7♠': 7,
                   '8♦': 8, '8♣': 8, '8♥': 8, '8♠': 8,
                   '9♦': 9, '9♣': 9, '9♥': 9, '9♠': 9,
                   '10♦': 10, '10♣': 10, '10♥': 10, '10♠': 10,
                   'В♦': 10, 'В♣': 10, 'В♥': 10, 'В♠': 10,
                   'Д♦': 10, 'Д♣': 10, 'Д♥': 10, 'Д♠': 10,
                   'К♦': 10, 'К♣': 10, 'К♥': 10, 'К♠': 10,
                   'А♦': 11, 'А♣': 11, 'А♥': 11, 'А♠': 11,
                   }
        DILLER_POLUCHAET_KARTY(message, colloda)
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemRAZDAT = types.KeyboardButton("Раздать карты")
        itemMENU = types.KeyboardButton("Вернуться в главное меню")
        markup_meaning_games.add(itemRAZDAT,itemMENU, row_width=1)
        mesg2KARTY = bot.send_message(message.chat.id, 'Сравниваем очки..',reply_markup=markup_meaning_games)
        sravnenie_ochkov_s_dillerom(message)
        bot.register_next_step_handler(mesg2KARTY, game_RAZDAT_KARTY)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, game_PROCESS_RAZDACHI_ESHE)
# сравнение с диллером
def sravnenie_ochkov_s_dillerom(message):
    if ochki_djack(message) <= 21 and ochki_djack_diller(message)<ochki_djack(message):
        for value in conn.execute(f"SELECT kakie_karty_black_djack_diller FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Карты диллера*: {value[0]}",
                             parse_mode= 'Markdown')
        for value in conn.execute(f"SELECT ochki_black_djack_diller FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Очки диллера*: {value[0]}",
                             parse_mode= 'Markdown')
        for value in conn.execute(f"SELECT kakie_karty_black_djack FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"Ваши карты: {value[0]}",
                             parse_mode= 'Markdown')
        for value in conn.execute(f"SELECT ochki_black_djack FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"Ваши очки: {value[0]}",
                             parse_mode='html')
        mesg2KARTY = bot.send_message(message.chat.id, 'Вы победили!'
                                      )
        conn.execute(
            f"UPDATE users SET balance = balance + {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
    elif ochki_djack(message) <= 21 and ochki_djack_diller(message)>21:
        for value in conn.execute(f"SELECT kakie_karty_black_djack_diller FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Карты диллера*: {value[0]}",
                             parse_mode= 'Markdown')
        for value in conn.execute(f"SELECT ochki_black_djack_diller FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Очки диллера*: {value[0]}",
                             parse_mode= 'Markdown')
        for value in conn.execute(f"SELECT kakie_karty_black_djack FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"Ваши карты: {value[0]}",
                             parse_mode='html')
        for value in conn.execute(f"SELECT ochki_black_djack FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"Ваши очки: {value[0]}",
                             parse_mode='html')
        mesg2KARTY = bot.send_message(message.chat.id, 'Вы победили!'
                                      )
        conn.execute(
            f"UPDATE users SET balance = balance + {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
    elif ochki_djack(message) <= 21 and ochki_djack_diller(message)==ochki_djack(message):
        for value in conn.execute(f"SELECT kakie_karty_black_djack_diller FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Карты диллера*: {value[0]}",
                             parse_mode= 'Markdown')
        for value in conn.execute(f"SELECT ochki_black_djack_diller FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Очки диллера*: {value[0]}",
                             parse_mode= 'Markdown')
        for value in conn.execute(f"SELECT kakie_karty_black_djack FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"Ваши карты: {value[0]}",
                             parse_mode='html')
        for value in conn.execute(f"SELECT ochki_black_djack FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"Ваши очки: {value[0]}",
                             parse_mode='html')
        mesg2KARTY = bot.send_message(message.chat.id, 'Ничья!'
                                      )
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
    else:
        for value in conn.execute(f"SELECT kakie_karty_black_djack_diller FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Карты диллера*: {value[0]}",
                             parse_mode= 'Markdown')
        for value in conn.execute(f"SELECT ochki_black_djack_diller FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Очки диллера*: {value[0]}",
                             parse_mode= 'Markdown')
        for value in conn.execute(f"SELECT kakie_karty_black_djack FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"Ваши карты: {value[0]}",
                             parse_mode='html')
        for value in conn.execute(f"SELECT ochki_black_djack FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"Ваши очки: {value[0]}",
                             parse_mode='html')
        mesg2KARTY = bot.send_message(message.chat.id, 'Вы проиграли!'
                                      )
        conn.execute(
            f"UPDATE users SET balance = balance - {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode= 'Markdown')
#БАЛАНС
@bot.message_handler(content_types='text')
def balance_knopka(message):
    if message.text == 'Пополнить баланс':
        mesgPOPOLNENIE = bot.send_message(message.chat.id, 'Введите сумму *ЦЕЛОЧИСЛЕННУЮ* сумму на которую хотите пополнить баланс',
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgPOPOLNENIE, popolnenie_knopka)
    elif message.text == 'Вывеcти денги':
        mesgPOPOLNENIE = bot.send_message(message.chat.id,'Введите сумму *ЦЕЛОЧИСЛЕННУЮ* сумму которую хотите вывести',
                             parse_mode= 'Markdown')
        bot.register_next_step_handler(mesgPOPOLNENIE, vyvod_knopka)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, balance_knopka)
#Пополнить баланс
@bot.message_handler(content_types='text')
def popolnenie_knopka(message):
    if message.text.isnumeric() == True and int(message.text)>0:
        c = message.text
        conn.execute(f"UPDATE users SET balance = balance + {int(c)} WHERE user_id = {message.chat.id}")
        conn.commit()
        bot.send_message(message.chat.id, f"Вы пополнили баланс на *{int(c)}*.",
                         parse_mode='Markdown')
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode='Markdown')
        mesgCHISLO= bot.send_message(message.chat.id,'Для продолжения нажмите интересующую вас кнопку')
        bot.register_next_step_handler(mesgCHISLO, balance_knopka)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, popolnenie_knopka)
#Вывести с баланса
@bot.message_handler(content_types='text')
def vyvod_knopka(message):
    if (message.text.isnumeric() == True) and (int(message.text)>0) and int(message.text)<=balance_na_oshibke(message):
        c = message.text
        conn.execute(f"UPDATE users SET balance = balance - {int(c)} WHERE user_id = {message.chat.id}")
        conn.commit()
        bot.send_message(message.chat.id, f"Вы вывели *{int(c)}* с баланса.",
                         parse_mode='Markdown')
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode='Markdown')
        mesgCHISLO= bot.send_message(message.chat.id,'Для продолжения нажмите интересующую вас кнопку')
        bot.register_next_step_handler(mesgCHISLO, balance_knopka)
    elif message.text == "Вернуться в главное меню":
        main_menu(message)
    elif (message.text.isnumeric() == True) and (int(message.text)>0) and int(message.text)>=balance_na_oshibke(message):
        mesgBAG = bot.send_message(message.chat.id, 'На вашем балансе недостаточно средств')
        bot.register_next_step_handler(mesgBAG, vyvod_knopka)
    else:
        mesgBAG = bot.send_message(message.chat.id, 'Я пока не знаю этой команды, но в будущем возможно узнаю!')
        bot.register_next_step_handler(mesgBAG, vyvod_knopka)
#функция для проверки баланса для игр!!!
def balance_na_oshibke(message):
    for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
        return value[0]
#функция для того чтобы вытащить ставку
def stavka_na_oshibke(message):
    for value in conn.execute(f"SELECT stavka FROM users WHERE user_id = {message.chat.id}"):
        return value[0]
#функция для того чтобы вытащить число
def chislo_na_oshibke(message):
    for value in conn.execute(f"SELECT chislo_bolshe_menshe FROM users WHERE user_id = {message.chat.id}"):
        return value[0]
#функция для того чтобы вытащить на что ставим в рулетке
def na_chto_stavim_ruletka(message):
    for value in conn.execute(f"SELECT na_chto_stavim_ruletka FROM users WHERE user_id = {message.chat.id}"):
        return value[0]
#функция для вывода коэффициента
def koef_na_oshibke(message):
    for value in conn.execute(f"SELECT koef FROM users WHERE user_id = {message.chat.id}"):
        return value[0]
#функция для вывода очков блэк джэк
def ochki_djack(message):
    for value in conn.execute(f"SELECT ochki_black_djack FROM users WHERE user_id = {message.chat.id}"):
        return value[0]
# функция для вывода очков диллера блэк джэк
def ochki_djack_diller(message):
    for value in conn.execute(f"SELECT ochki_black_djack_diller FROM users WHERE user_id = {message.chat.id}"):
        return value[0]
#ПОЛУЧЕНИЕ ПЕРВОЙ КАРТЫ И ВЫВОД ИСПОЛЬЗУЕМОЙ
def POLUCHENIE_PERVOY_KARTY(message,colloda):
    karta1 = random.choice(list(colloda.keys()))
    print(karta1)
    conn.execute(
        f"UPDATE users SET kakie_karty_black_djack = '{str(karta1)}' WHERE user_id = {message.chat.id}")
    conn.commit()
    conn.execute(
        f"UPDATE users SET ochki_black_djack = {int(colloda[karta1])} WHERE user_id = {message.chat.id}")
    conn.commit()
    del colloda[karta1]
    return colloda
#ПОЛУЧЕНИЕ ВТОРОЙ КАРТЫ И ВЫВОД ИСПОЛЬЗУЕМОЙ
def POLUCHENIE_VTOROY_KARTY(message,colloda):
    karta1 = random.choice(list(colloda.keys()))
    print(karta1)
    if ochki_djack(message) >=11:
        colloda['А♦'] = 1
        colloda['А♣'] = 1
        colloda['А♥'] = 1
        colloda['А♠'] = 1
        for value in conn.execute(f"SELECT kakie_karty_black_djack FROM users WHERE user_id = {message.chat.id}"):
            spisok_kart_ispolzuemyh = value[0]
            del colloda[spisok_kart_ispolzuemyh]
        conn.execute(
            f"UPDATE users SET kakie_karty_black_djack = kakie_karty_black_djack ||' '||'{str(karta1)}' WHERE user_id = {message.chat.id}")
        conn.commit()
        conn.execute(
            f"UPDATE users SET ochki_black_djack = ochki_black_djack + {int(colloda[karta1])} WHERE user_id = {message.chat.id}")
        conn.commit()
        del colloda[karta1]
        return colloda
    else:
        conn.execute(
            f"UPDATE users SET kakie_karty_black_djack = kakie_karty_black_djack ||' '||'{str(karta1)}' WHERE user_id = {message.chat.id}")
        conn.commit()
        conn.execute(
            f"UPDATE users SET ochki_black_djack = ochki_black_djack + {int(colloda[karta1])} WHERE user_id = {message.chat.id}")
        conn.commit()
        del colloda[karta1]
        return colloda
#ПОЛУЧЕНИЕ КАРТ ИГРОКОМ И ВЫВОД ИСПОЛЬЗУЕМЫХ
def POLUCHENIE_KART(message,colloda):
    karta1 = random.choice(list(colloda.keys()))
    print(karta1)
    conn.execute(
        f"UPDATE users SET kakie_karty_black_djack = kakie_karty_black_djack ||' '||'{str(karta1)}' WHERE user_id = {message.chat.id}")
    conn.commit()
    conn.execute(
        f"UPDATE users SET ochki_black_djack = ochki_black_djack + {int(colloda[karta1])} WHERE user_id = {message.chat.id}")
    conn.commit()
    del colloda[karta1]
    return colloda
#СВЯЗЬ С АДМИНИСТРАТОРАМИ
def svyaz_s_adminami(message):
    if message.text == 'Вернуться в главное меню':
        main_menu(message)
    else:
        bot.forward_message(config.chatID, message.chat.id, message.message_id)
        mesgmainmenu = bot.send_message(message.chat.id, 'Ваш запрос принят, администратор скоро с вами свяжется')
        bot.register_next_step_handler(mesgmainmenu, svyaz_s_adminami)
#удаление карт добавленных
def spisok_kart(spisok_kart_ispolzuemyh,colloda):
    for karta in spisok_kart_ispolzuemyh:
        del colloda[karta]
    return colloda
#проверка очков больше 21 или нет(блэк-джэк)
def proverka_ochkov(message):
    if ochki_djack(message) > 21:
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemRAZDAT = types.KeyboardButton("Раздать карты")
        markup_meaning_games.add(itemRAZDAT, row_width=1)
        mesg2KARTY = bot.send_message(message.chat.id,
                                      'Сумма ваших очков превысила 21, вы проиграли',
                                      reply_markup=markup_meaning_games
                                      )
        conn.execute(
            f"UPDATE users SET balance = balance - {stavka_na_oshibke(message)} WHERE user_id = {message.chat.id}")
        conn.commit()
        for value in conn.execute(f"SELECT balance FROM users WHERE user_id = {message.chat.id}"):
            bot.send_message(message.chat.id, f"*Ваш баланс*: {value[0]}",
                             parse_mode='Markdown')
        bot.register_next_step_handler(mesg2KARTY, game_RAZDAT_KARTY)
    else:
        markup_meaning_games = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itemKARTY = types.KeyboardButton("Получить ещё карту")
        itemOSTANOVKA = types.KeyboardButton("Остановиться")
        markup_meaning_games.add(itemKARTY, itemOSTANOVKA, row_width=2)
        mesg2KARTY = bot.send_message(message.chat.id, 'Ещё карту или останавливаемся?',
                                      reply_markup=markup_meaning_games)
        bot.register_next_step_handler(mesg2KARTY, game_PROCESS_RAZDACHI_ESHE)

#игра диллера в блэк джэк
def DILLER_POLUCHAET_KARTY(message, colloda):
    for value in conn.execute(f"SELECT kakie_karty_black_djack FROM users WHERE user_id = {message.chat.id}"):
        spisok_kart_ispolzuemyh = value[0].split(' ')
        print(colloda)
        karta1 = POLUCHENIE_PERVOY_KARTY_DILLEROM(message, spisok_kart(spisok_kart_ispolzuemyh, colloda))
        print(karta1)
        karta2 = POLUCHENIE_VTOROY_KARTY_DILLEROM(message, karta1)
        print(karta2)
        if ochki_djack_diller(message)>=11:
            colloda['А♦'] = 1
            colloda['А♣'] = 1
            colloda['А♥'] = 1
            colloda['А♠'] = 1
            while ochki_djack_diller(message) <=16:
                karta3 = POLUCHENIE_KART_ESHE_DILLEROM(message, karta2)
                print(karta3)
        else:
            while ochki_djack_diller(message) <11:
                karta3 = POLUCHENIE_KART_ESHE_DILLEROM(message, karta2)
                print(karta3)
            colloda['А♦'] = 1
            colloda['А♣'] = 1
            colloda['А♥'] = 1
            colloda['А♠'] = 1
            while ochki_djack_diller(message) <= 16:
                karta3 = POLUCHENIE_KART_ESHE_DILLEROM(message, karta2)
                print(karta3)
# ПОЛУЧЕНИЕ ПЕРВОЙ КАРТЫ И ВЫВОД ИСПОЛЬЗУЕМОЙ ДИЛЛЕРА
def POLUCHENIE_PERVOY_KARTY_DILLEROM(message, colloda):
    karta1 = random.choice(list(colloda.keys()))
    print(karta1)
    conn.execute(
        f"UPDATE users SET kakie_karty_black_djack_diller = '{str(karta1)}' WHERE user_id = {message.chat.id}")
    conn.commit()
    conn.execute(
        f"UPDATE users SET ochki_black_djack_diller = {int(colloda[karta1])} WHERE user_id = {message.chat.id}")
    conn.commit()
    del colloda[karta1]
    return colloda

# ПОЛУЧЕНИЕ ВТОРОЙ КАРТЫ И ВЫВОД ИСПОЛЬЗУЕМОЙ ДИЛЛЕРА
def POLUCHENIE_VTOROY_KARTY_DILLEROM(message, colloda):
    karta1 = random.choice(list(colloda.keys()))
    print(karta1)
    if ochki_djack_diller(message) >= 11:
        colloda['А♦'] = 1
        colloda['А♣'] = 1
        colloda['А♥'] = 1
        colloda['А♠'] = 1
        for value in conn.execute(f"SELECT kakie_karty_black_djack_diller FROM users WHERE user_id = {message.chat.id}"):
            spisok_kart_ispolzuemyh = value[0]
            del colloda[spisok_kart_ispolzuemyh]
        conn.execute(
            f"UPDATE users SET kakie_karty_black_djack_diller = kakie_karty_black_djack_diller ||' '||'{str(karta1)}' WHERE user_id = {message.chat.id}")
        conn.commit()
        conn.execute(
            f"UPDATE users SET ochki_black_djack_diller = ochki_black_djack_diller + {int(colloda[karta1])} WHERE user_id = {message.chat.id}")
        conn.commit()
        del colloda[karta1]
        return colloda
    else:
        conn.execute(
            f"UPDATE users SET kakie_karty_black_djack_diller = kakie_karty_black_djack_diller ||' '||'{str(karta1)}' WHERE user_id = {message.chat.id}")
        conn.commit()
        conn.execute(
            f"UPDATE users SET ochki_black_djack_diller = ochki_black_djack_diller + {int(colloda[karta1])} WHERE user_id = {message.chat.id}")
        conn.commit()
        del colloda[karta1]
        return colloda

# ПОЛУЧЕНИЕ КАРТ ИГРОКОМ И ВЫВОД ИСПОЛЬЗУЕМЫХ ДИЛЛЕРА
def POLUCHENIE_KART_ESHE_DILLEROM(message, colloda):
    karta1 = random.choice(list(colloda.keys()))
    print(karta1)
    conn.execute(
        f"UPDATE users SET kakie_karty_black_djack_diller = kakie_karty_black_djack_diller ||' '||'{str(karta1)}' WHERE user_id = {message.chat.id}")
    conn.commit()
    conn.execute(
        f"UPDATE users SET ochki_black_djack_diller = ochki_black_djack_diller + {int(colloda[karta1])} WHERE user_id = {message.chat.id}")
    conn.commit()
    del colloda[karta1]
    return colloda



bot.polling(none_stop=True)
keep_alive.keep_alive()
bot.run(os.environ.get('TOKEN'),bot=True,reconnect=True)

