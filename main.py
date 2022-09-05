import types

import telebot;
def read_players():
    f = open("Players.txt")
    sep = f.read().split("\n")
    rating = {}
    for i in range(len(sep)):
        rating[sep[i][:sep[i].index("-")]] = sep[i][sep[i].index("-") + 1:]
    f.close()
    return rating
def write_players(rating):
    f = open("players.txt", "w")
    temp = ''
    for i in rating.keys:
        temp += i + ' - ' + rating[i] + '\n'
    f.write(temp)
    f.close()

def new_game(name1, name2, result):
    rating = read_players()
    if int(result.split()[0]) > int(result.split()[2]):
        winner = name1
        looser = name2
    else:
        winner = name2
        looser = name1
    if abs(int(result.split()[0]) - int(result.split()[2])) <=3:
        kf_score = 0.8
    elif abs(int(result.split()[0]) - int(result.split()[2])) <=6:
        kf_score = 1
    else:
        kf_score = 1.2
    delta = ((100 -(int(rating[winner]) - int(rating[looser])))/10) * kf_score
    rating[winner] = str(float(rating[winner]) + delta)
    rating[looser] = str(float(rating[looser]) - delta)
    write_players(rating)
    return [rating[winner], rating[looser], delta, winner, looser]
bot = telebot.TeleBot('2070733952:AAFZLpADmvZzLPtssdlYHbi92dFFhIN0cto');
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

name = ''
surname = ''
age = 0
@bot.message_handler(content_types=['text'])
def start(message):
    try:
        first_player = message.text[:message.text.index(" ")]
        score = message.text[message.text.index(" ")+1:message.text.rindex(" ")]
        second_player = message.text[message.text.rindex(" ")+1:]
        result = new_game(first_player, second_player, score)
        bot.send_message(message.from_uer.id, 'Изменение рейтинга: '+ result[3] + " " + result[0]+ " (+" + result[2] + "); "+ result[4] + " " + result[1]+ " (-" + result[2] + "); ")
    except:
        bot.send_message(message.from_uer.id, "Не зачтено. Попробуйте еще раз")
        bot.register_next_step_handler(message, start)










'''
     message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?");
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg');

def get_name(message): #получаем фамилию
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
    bot.register_next_step_handler(message, get_surname);

def get_surname(message):
    global surname;
    surname = message.text;
    bot.send_message(message.from_user.id,'Сколько тебе лет?');
    bot.register_next_step_handler(message, get_age);

def get_age(message):
    global age;
    while age == 0: #проверяем что возраст изменился
        try:
             age = int(message.text) #проверяем, что возраст введен корректно
        except Exception:
             bot.send_message(message.from_user.id, 'Цифрами, пожалуйста');
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
'''
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, 'Запомню : )');
bot.polling(none_stop=True, interval=0)