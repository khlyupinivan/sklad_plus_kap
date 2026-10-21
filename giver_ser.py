import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType

import seller
import time


def send_message(peer_id, message):
    vk.messages.send(
        peer_id = peer_id,
        message = message,
        random_id = get_random_id()
    )


def send_message_person(peer_id, message, message_id):
    vk.messages.send(
        peer_id = peer_id,
        message = message,
        random_id = get_random_id(),
        forward_messages = message_id
    )


def check_item(items, item):
    if item in items:
        return True
    else:
        return False

# def get_name(get_api, user_id):
#     print('x')
#     user_get = get_api.users.get(user_id = userid)
#     print(user_get)
#     user_get = user_get[0]
#     first_name = user_get['first_name']
#     # last_name = user_get['last_name']
#     # full_name = first_name + " " + last_name
#     return first_name


token = ""

vk_session = vk_api.VkApi(token = token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
         
peer_htonik = None
peer_sovet = None

id_vopl = -183040898

my_id = None
vip_id = {}

name_db = 'server.db'
base = seller.db_connection(name_db)

ban_list = []

word_give = 'шеф хочу'
word_guild_give = 'шеф дай'
word_put = 'шеф положи'
word_get = '👝[id6443587'
word_give_sto = "вы положили на склад"
id_message_person_who_get = 0
what_need_give = ''
word_activation = '!активация'
word_balance = '/души'
word_block1 = "золота"
word_block2 = "осколков"
word_block3 = " душ"
word_change = "/изменить"
word_message = "шеф"
word_price = "/цена"
word_prices = "/цены"
word_check = "/дай список"
word_change_price_books = "/изменить цены"
word_change_mode = "/активировать положить"

flag_give_mode = True

while True:
    try:
        for event in longpoll.listen():
            if id_message_person_who_get != 0:
                try:
                    print('Send.')
                    send_message_person(peer_htonik, f"Передать {what_need_give}", id_message_person_who_get)
                except Exception as _ex:
                    print(f'[Error] {_ex}')
                finally:
                    print("Delete...")
                    id_message_person_who_get = 0
                    print("Deleted")
            if event.type == VkEventType.MESSAGE_NEW:
                original_message = event.text
                message = original_message.lower()
                user_id = event.user_id
                peer = event.peer_id
                if not (user_id in ban_list):
                    if event.from_chat and event.peer_id == peer_htonik and message[0:len(word_give)] == word_give and word_block1 \
                            not in message and word_block2 not in message and word_block3 not in message:
                        if message.find('-') == -1:
                            item = message[len(word_give)+1:]
                            quant = 1
                        else:
                            item = message[len(word_give)+1: message.find('-')-1]
                            quant_str = message[message.find('-')+2:]
                            if quant_str[1] == ' ':
                                quant = int(quant_str[0])
                            else:
                                quant = int(quant_str[:2])

                        if not check_item(seller.get_book_list(base), item) and \
                                    not check_item(seller.get_item_list(base), item):
                            what_need_give = message[len(word_give)+1:]
                            send_message(peer_htonik, f"Взять {what_need_give}")
                            id_message_person_who_get = event.message_id
                            time.sleep(12)
                        
                        elif check_item(seller.get_item_list(base), item) and user_id in vip_id:
                            what_need_give = message[len(word_give)+1:]
                            send_message(peer_htonik, f"Взять {what_need_give}")
                            id_message_person_who_get = event.message_id
                            time.sleep(12)
                        elif check_item(seller.get_item_list(base), item):
                            send_message_person(peer_htonik, f"Требуя {item}, ты претендуешь на нечто большее, чем можешь себе позволить", event.message_id)
                        else:
                            if seller.check_cash(base, user_id, seller.get_price_book(base, item)*quant):
                                what_need_give = message[len(word_give)+1:]
                                print('update...')
                                send_message(peer_htonik, seller.update_users_cash(base, user_id, seller.get_price_book(base, item)*quant, False))
                                print('Excelent')
                                send_message(peer_htonik, f"Взять {what_need_give}")
                                id_message_person_who_get = event.message_id
                                time.sleep(12)
                            else:
                                send_message_person(peer_htonik, f"Ты слишком немощен, Смертный. Захвати ещё \
                                                                    {seller.get_price_book(base, item)*quant - seller.get_cash(base, user_id)} \
                                                                    душ врагов и возвращайся.", event.message_id)

                    elif event.from_chat and event.peer_id == peer_htonik and message[0:len(word_guild_give)] == word_guild_give and word_block1 \
                            not in message and word_block2 not in message and word_block3 not in message:
                        if message.find('-') == -1:
                            item = message[len(word_guild_give)+1:]
                            quant = 1
                        else:
                            item = message[len(word_guild_give)+1: message.find('-')-1]
                            quant_str = message[message.find('-')+2:]
                            if quant_str[1] == ' ':
                                quant = int(quant_str[0])
                            else:
                                quant = int(quant_str[:2])

                        if not check_item(seller.get_book_list(base), item) and \
                                    not check_item(seller.get_item_list(base), item):
                            what_need_give = message[len(word_guild_give)+1:]
                            id_message_person_who_get = event.message_id
                            send_message_person(peer_htonik, f"Выдать {what_need_give}", id_message_person_who_get)
                            id_message_person_who_get = 0
                            time.sleep(11)
                        
                        elif check_item(seller.get_item_list(base), item) and user_id in vip_id:
                            what_need_give = message[len(word_guild_give)+1:]
                            id_message_person_who_get = event.message_id
                            send_message_person(peer_htonik, f"Выдать {what_need_give}", id_message_person_who_get)
                            id_message_person_who_get = 0
                            time.sleep(11)
                        elif check_item(seller.get_item_list(base), item):
                            send_message_person(peer_htonik, f"Требуя {item}, ты претендуешь на нечто большее, чем можешь себе позволить", event.message_id)
                        else:
                            if seller.check_cash(base, user_id, seller.get_price_book(base, item)*quant):
                                what_need_give = message[len(word_guild_give)+1:]
                                print('update...')
                                send_message(peer_htonik, seller.update_users_cash(base, user_id, seller.get_price_book(base, item)*quant, False))
                                print('Excelent')
                                id_message_person_who_get = event.message_id
                                send_message_person(peer_htonik, f"Выдать {what_need_give}", id_message_person_who_get)
                                id_message_person_who_get = 0
                                time.sleep(11)
                            else:
                                send_message_person(peer_htonik, f"Ты слишком немощен, Смертный. Захвати ещё \
                                                                    {seller.get_price_book(base, item)*quant - seller.get_cash(base, user_id)} \
                                                                    душ врагов и возвращайся.", event.message_id)


                    elif event.from_chat and event.peer_id == peer_htonik and word_give_sto in message and user_id == id_vopl and flag_give_mode:
                        user_get = message[message.find('[')+3: message.find("|")]
                        quant = int(message[message.find(':')+3: message.find('*')])
                        what_need_get = message[message.find("*")+1:message.find("!")]
                        if check_item(seller.get_book_list(base), what_need_get):
                            print(seller.get_price_book(base, what_need_get)*quant)
                            text = seller.update_users_cash(base, user_get, seller.get_price_book(base, what_need_get)*quant, True)
                            send_message(peer_htonik, text)

                    elif event.from_chat and event.peer_id == peer_htonik and message == word_change_mode:
                        flag_give_mode = not flag_give_mode
                        if flag_give_mode:
                            message_to_send = f'Так уж и быть, теперь я буду выплачивать души в обход Шефа!'
                        else:
                            message_to_send = f'Ну а теперь идите за душами к Шефу.'
                        send_message(peer_htonik, message_to_send)




                    elif event.from_chat and event.peer_id == peer_htonik and message[:11] == word_get and user_id == id_vopl:
                        message = message[message.find(',')+2:]
                        if message[0:2] == 'по':
                            user_get = message[message.find('[')+3: message.find("|")]
                            if message.find('*') != -1:
                                quant = int(message[message.find(':')+3: message.find('*')])
                            else:
                                quant = 1
                            what_need_get = ''
                            if quant == 1 and message.find('*') == -1:
                                thing_start = message.find(':')+3
                                message = message[thing_start:]
                                while message[0:3] != 'от ':
                                    what_need_get = what_need_get + ' ' + message[: message.find(' ')]
                                    message = message[message.find(' ')+1:]
                                if check_item(seller.get_book_list(base), what_need_get[1:]):
                                    send_message(peer_htonik, seller.update_users_cash(base, user_get, seller.get_price_book(base, what_need_get[1:])*quant, True))
                                    if flag_give_mode:
                                        send_message(peer_htonik, seller.update_users_cash(base, my_id, seller.get_price_book(base, what_need_get[1:])*quant, False))
                            else:
                                thing_start = message.find('*')+1
                                message = message[thing_start:]
                                while message[:3] != 'от ':
                                    what_need_get = what_need_get + ' ' + message[: message.find(' ')]
                                    message = message[message.find(' ')+1:]
                                if check_item(seller.get_book_list(base), what_need_get[1:]):
                                    print(seller.get_price_book(base, what_need_get[1:])*quant)
                                    send_message(peer_htonik, seller.update_users_cash(base, user_get, seller.get_price_book(base, what_need_get[1:])*quant, True))
                                    if flag_give_mode:
                                        send_message(peer_htonik, seller.update_users_cash(base, my_id, seller.get_price_book(base, what_need_get[1:])*quant, False))
                                what_need_get = f"{what_need_get} - {quant} штук"
                            send_message(peer_htonik, f'Положить{what_need_get}')

                    elif event.from_chat and event.peer_id == peer_htonik and message == word_activation:
                        user_get = vk.users.get(user_ids = user_id)
                        user_get = user_get[0]
                        first_name = user_get['first_name']
                        send_message(peer_htonik, seller.add_user(base, user_id, first_name))

                    elif event.from_chat and event.peer_id == peer_htonik and message == word_balance:
                        send_message(peer_htonik, seller.print_user(base, user_id))

                    elif event.from_chat and event.peer_id == peer_htonik and message == word_message:
                        send_message(peer_htonik, ".")

                    elif event.from_chat and event.peer_id == peer_htonik and message[:5] == word_price:
                        send_message_person(peer_htonik, seller.get_price_book(base, message[6:]), event.message_id)

                    elif event.from_chat and event.peer_id == peer_htonik and message == word_prices:
                        send_message(peer_htonik, seller.print_table_books(base))

                    elif event.from_chat and event.peer_id == peer_htonik and message[:len(word_put)] == word_put and \
                        word_block1 not in message and word_block2 not in message and word_block3 not in message:
                        send_message(peer_htonik, f"Положить{message[10:]}")

                    elif event.from_chat and event.peer_id == peer_htonik and message[:14] == word_change_price_books and \
                        user_id in vip_id:
                        items = []
                        prices = []
                        books_price = message[15:] + '\n'
                        while books_price.find('\n') != -1:
                            string = books_price[:books_price.find('\n')]
                            books_price = books_price[books_price.find('\n') + 1:]
                            items.append(string[:string.find(':')])
                            prices.append(int(string[string.find(':') + 2:]))
                        count = 0
                        for i in range(len(items)):
                            ret = seller.update_price(base, items[i], prices[i])
                            if ret == "Цена обновлена":
                                count += 1
                        if count == len(items):
                            send_message(peer_htonik, "Цены обновлены")
                        else:
                            send_message((peer_htonik, "Что-то пошло не так"))

    except:
        Exception
