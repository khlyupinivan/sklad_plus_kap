import time
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType

import math

import seller


def send_message(peer_id, message, keyboard=None, forward=None):
    post = {
        "peer_id": peer_id,
        "message": message,
        "random_id": get_random_id()

    }
    if keyboard != None:
        if message_id is None:
            post = {
                "peer_id": peer_id,
                "message": message,
                "random_id": get_random_id(),
                "keyboard": keyboard.get_keyboard()
            }
        else:
            post = {
                "peer_id": peer_id,
                "message": message,
                "random_id": get_random_id(),
                "keyboard": keyboard.get_keyboard(),
                "forward_messages": forward
            }
    elif forward != None:
        post ={
            "peer_id": peer_id,
            "message": message,
            "random_id": get_random_id(),
            "forward_messages": forward
        }
        print(post)
    vk_session.method("messages.send", post)

token = ""
id_group = None

vk_session = vk_api.VkApi(token = token)
vk = vk_session.get_api()


longpoll = VkBotLongPoll(vk_session, id_group)

keyboard = VkKeyboard()
keyboard.add_button('🕍Замок')
keyboard.add_button('Cсылки')
keyboard.add_line()
keyboard.add_button("Хранилище")
keyboard.add_line()
keyboard.add_openlink_button('Профиль','https://vk.com/app6987489')
message_keyboard = VkKeyboard(False, True)
message_keyboard.add_openlink_button('экспедиции', 'https://vk.com/@order_ofliberty-ekspedicii-kolodca')
message_keyboard.add_openlink_button('события', 'https://vk.com/@shaden87-sobytiya')
message_keyboard.add_line()
message_keyboard.add_openlink_button('достижения', 'https://vk.com/@hornyapostol-dostizheniya')
message_keyboard.add_openlink_button('расы', 'https://vk.com/app7055214_-182985865#page=pages&id=621')
message_keyboard.add_line()
message_keyboard.add_openlink_button('лес', 'https://vk.com/@welldungeon-spravochnik-temnolesya')
message_keyboard.add_openlink_button('справочник', 'https://vk.com/@welldungeon-help')
message_keyboard.add_line()
message_keyboard.add_openlink_button('еда', 'https://docs.google.com/spreadsheets/d/1afdiHFoCdAO9ssp0bdDkipO2uJNR6uR5svQWEmJ_h0I/edit?usp=sharing')

id_dima = 0#223365008

vip_id = {}
peer_htonik = None
peer_sovet = None
name_db = 'server.db'
base = seller.db_connection(name_db)

word_check = "/дай список"
word_check_one_user = "/покажи"
word_link = "cсылки"
word_button = "верни кнопки"
word_tax = "налог"
word_change = "/изменить"

while True:
    try:

        for event in longpoll.listen():

            if event.type == VkBotEventType.MESSAGE_NEW:
                if not ('reactions' in event.object.message.keys()):
                    if event.message.peer_id in [peer_htonik, peer_sovet]:
                        message = event.message.text.lower()
                        peer_id = event.message.peer_id
                        user_id = event.message.from_id
                        message_id = event.message.conversation_message_id
                        print(event.message)
                        forward = event.object.message['fwd_messages']
                        if (word_link in message) and event.object.user_id != id_dima:
                            send_message(peer_htonik, 'ссылки', message_keyboard)
                        elif message == word_button and event.object.user_id != id_dima:
                            send_message(peer_htonik, 'Возвращаю кнопки', keyboard)
                        elif message[:5] == word_tax:
                            a = str(math.ceil(int(message[5:])*150/9*10))
                            send_message(peer_htonik, f"Налог для уровня{message[5:]}: {a}")
                        elif len(forward) != 0:
                            new_id = forward[0]['from_id']
                            if message[:9] == word_change and user_id in vip_id and new_id != 0:
                                send_message(peer_htonik, seller.update_users_cash(base, new_id, int(message[10:]), True))
                            elif message[:9] == 'передать ' and ' душ' in message and new_id != 0:
                                new_message = message[9:]
                                quant = int(new_message[:new_message.find(' ')])
                                if seller.check_cash(base, user_id, abs(quant)):
                                    if quant < 0:
                                        send_message(peer_htonik, seller.update_users_cash(base, user_id, quant, True))
                                        send_message(peer_htonik, seller.update_users_cash(base, new_id, quant, False))
                                        send_message(peer_htonik, 'Следующая попытка обмануть меня, Смертный, будет последней...')
                                    elif seller.check_cash(base, user_id, quant):
                                        send_message(peer_htonik, seller.update_users_cash(base, user_id, quant, False))
                                        send_message(peer_htonik, seller.update_users_cash(base, new_id, quant, True))
                                    else:
                                        send_message(peer_htonik, f"Ты пытаешься меня обмануть, Смертный? \
                                                                            Тебе не хватает ещё \
                                                                            {quant - seller.get_cash(base, user_id)} \
                                                                            душ врагов.")
                                else:
                                    send_message(peer_htonik,
                                                 'Следующая попытка обмануть меня, Смертный, будет последней...')
                                    # send_message(peer_id=peer_sovet, message="", forward=message_id)
                            elif message == word_check_one_user and user_id in vip_id:
                               send_message(peer_id, seller.get_cash(base, new_id))
                            new_id = 0
                        elif peer_id == peer_sovet and message == word_check:
                            message_to_send = f'{seller.print_table_users(base)}\n\n\
                                                    Суммарное количество душ участников: {seller.get_sum_cash(base)}'
                            send_message(peer_sovet, message_to_send)
    except:
        Exception