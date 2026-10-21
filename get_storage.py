import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from copy import deepcopy
import time
import threading

import seller

# from config.config_manager import (
#     start_config_watcher,
#     get_group_token,
#     get_admin_ids,
# )

# start_config_watcher()

GROUP_TOKEN = ""

def is_admin(user_id: int) -> bool:
    return user_id in get_admin_ids()


def send_message(peer_id, message):
    result = vk.messages.send(
        peer_id = peer_id,
        message = message,
        random_id = get_random_id()
    )
    return result

def find_admin(peer_id):
    result = vk.messages.getConversationMembers(
        peer_id = peer_id
    )
    return result['items']

def delete_message(group_id, peer_id, cmids):
    try:
        result = vk.messages.delete(
            peer_id = peer_id,
            # message_ids = message_ids,
            group_id = group_id,
            delete_for_all = 1,
            cmids = cmids
        )
        return result
    except Exception as _ex:
        print(_ex)
    
def get_original_dict():
    item_dict_original = {
        "🌕Валюта:": {
            "Золото": [0],
            "Осколки Сердца": [0],
            "Свободное место": [0]
        },
        "🍃Ресурсы:": {
            "Бревно": [0],
            "Железная руда": [0],
            "Камень": [0],
            "Лен": [0],
            "Доска": [0],
            "Железный слиток": [0],
            "Каменный блок": [0],
            "Ткань": [0]
        },
        "💍Кольца": {
            "Кольцо великана": [0],
            "Кольцо гоблина": [0],
            "Кольцо зелий": [0],
            "Кольцо злого глаза": [0],
            "Кольцо редкостей": [0],
            "Кольцо характеристик": [0],
            "Кольцо экипировки": [0],
            "Малое кольцо выносливости": [0],
            "Малое кольцо ловкости": [0],
            "Малое кольцо силы": [0]
        },
        "🎩Шлема": {
            "Шлем охотника": [0],
            "Деревянная каска": [0],
            "Деревенский капюшон": [0],
            "Шлем огра": [0],
            "Шлем Валькирии": [0],
            "Маска демона": [0],
            "Шлем мимика": [0],
            "Шлем Сакалава": [0],
            "Диадема Розы": [0]

        },
        "🔔Экипировка": {
            "Амулет с жемчугом": [0],
            "Башенный щит": [0],
            "Вечный факел": [0],
            "Доспехи стража стихий": [0],
            "Королевский пояс": [0],
            "Меч повелителя стихий": [0],
            "Посох молний": [0],
            "Рыцарские перчатки": [0],
            "Рыцарские сапоги": [0]
        },
        "🗺Карты": {
            "Карта испытания": [0],
            "Карта источника": [0],
            "Карта озера": [0],
            "Карта окрестностей": [0],
            "Карта руин": [0],
            "Карта сокровищ": [0],
            "Карта угодий": [0]
        },
        "💡Ингредиенты": {
            "Пещерный корень": [0],
            "Адский гриб": [0],
            "Адский корень": [0],
            "Болотник": [0],
            "Первозданная вода": [0],
            "Камнецвет": [0],
            "Необычная ракушка": [0],
            "Необычный цветок": [0],
            "Рыбий глаз": [0],
            "Рыбий жир": [0],
            "Сверкающая чешуя": [0],
            "Сквернолист": [0],
            "Чистая первозданная вода": [0]
        },
        "⛔Запретная зона": {
            "Амулет Адмов (ИНИ)": [0],
            "Амулет Адмов (СОБ)": [0],
            "Амулет Адмов (УПО)": [0],
            "Доспех Адмов (ВЛ)": [0],
            "Доспех Адмов (ВС)": [0],
            "Доспех Адмов (ЛВ)": [0],
            "Доспех Адмов (ЛС)": [0],
            "Доспех Адмов (СВ)": [0],
            "Доспех Адмов (СЛ)": [0],
            "Кинжал Адмов (ЛВ)": [0],
            "Кинжал Адмов (ЛС)": [0],
            "Меч Адмов (СВ)": [0],
            "Меч Адмов (СЛ)": [0],
            "Молот Адмов (ВЛ)": [0],
            "Молот Адмов (ВС)": [0],
            "Посох Адмов (РАС)": [0],
            "Посох Адмов (РЕГ)": [0],
            "Посох Адмов (УЧЕ)": [0],
            "Пояс Адмов (ВЕД)": [0],
            "Пояс Адмов (ВНИ)": [0],
            "Пояс Адмов (ФЕН)": [0],
            "Факел Адмов (МБ)": [0],
            "Факел Адмов (НЕП)": [0],
            "Факел Адмов (ОШЕ)": [0],
            "Щит Адмов (НЕУ)": [0],
            "Щит Адмов (ПРО)": [0],
            "Щит Адмов (УСТ)": [0],
            "Эссенция Адмов": [0],
            "Жемчужина Адмов": [0],
            "Цветок Адмов": [0],
            "Кровь Адмов": [0],
            "Обломок Сердца": [0],
            "Чернильник": [0],
            "Корень знаний": [0],
            "Рунное кольцо": [0],
            "Кольцо древних": [0],
            "Кольцо S ранга": [0],
            "Кольцо ордена": [0],
            "Малое кольцо точности": [0],
            "Малое кольцо концентрации": [0],
            "Свиток заточки предмета": [0],
            "Бездонный мешок адмов": [0],
            "Кровавый гриб": [0],
            "презрение к боли": [0],
            "Мешок элитных трофеев": [0]
        },
        "📕Книги Активных умений": {
            "берсеркер": [],
            "грязный удар": [],
            "заражение": [],
            "кровотечение": [],
            "мощный удар": [],
            "огонек надежды": [],
            "проклятие тьмы": [],
            "раскол": [],
            "расправа": [],
            "рассечение": [],
            "сила теней": [],
            "слабое исцеление": [],
            "слепота": [],
            "таран": [],
            "удар вампира": [],
            "целебный огонь": [],
        },
        "📘Книги Пассивных умений": {
            "дробящий удар": [],
            "защитная стойка": [],
            "колющий удар": [],
            "режущий удар": [],
            "стойка сосредоточения": [],
            "атлетика": [],
            "барьер": [],
            "бесстрашие": [],
            "браконьер": [],
            "быстрое восстановление": [],
            "ведьмак": [],
            "внимательность": [],
            "водохлеб": [],
            "воздаяние": [],
            "гладиатор": [],
            "еретик": [],
            "запасливость": [],
            "знания древних": [],
            "инициативность": [],
            "исследователь": [],
            "картограф": [],
            "контратака": [],
            "ловкость рук": [],
            "мародер": [],
            "незаметность": [],
            "непоколебимый": [],
            "неуязвимый": [],
            "охотник за головами": [],
            "ошеломление": [],
            "парирование": [],
            "подвижность": [],
            "прочность": [],
            "расторопность": [],
            "расчетливость": [],
            "регенерация": [],
            "рыбак": [],
            "собиратель": [],
            "суеверность": [],
            "угроза": [],
            "упорность": [],
            "устойчивость": [],
            "устрашение": [],
            "ученик": [],
            "феникс": [],
        }
    }
    return item_dict_original

def get_dict(base):
    item_dict_original = deepcopy(get_original_dict())

    books = seller.print_table_books(base)
    case_book = item_dict_original["📕Книги Активных умений"].keys()
    while books.find('\n') != -1:
        string = books[:books.find('\n')]
        books = books[books.find('\n')+1:]
        if string.find(':') != -1:
            item = string[:string.find(':')].lower()
            count = string[string.find(':')+2:]
            if item in case_book:
                item_dict_original["📕Книги Активных умений"][item].append(count)
    books = seller.print_table_books(base)
    case_book = item_dict_original["📘Книги Пассивных умений"].keys()
    while books.find('\n') != -1:
        string = books[:books.find('\n')]
        books = books[books.find('\n')+1:]
        if string.find(':') != -1:
            item = string[:string.find(':')]
            count = string[string.find(':')+2:]
            if item in case_book:
                item_dict_original["📘Книги Пассивных умений"][item].append(count)
    print(item_dict_original)
    return item_dict_original

def delete_loop(vk, group_id, peer_id, cmids):
    while True:
        if len(conversation_message_ids)>0:
            try:
                delete_message(group_id, peer_id, cmids)
                cmids.clear()
            finally:
                cmids.clear()
        time.sleep(1)

def admin_loop(vk, peer_id, admin_list):
    # admin_list_duplicate = []
    while True:
        admin_list.clear()
        list_chat = find_admin(peer_id)
        for people in list_chat:
            if 'is_admin' in people.keys():
                admin_list.append(people['member_id'])
        # admin_list.clear()
        # admin_list = admin_list_duplicate[:]
        # admin_list_duplicate.clear()
        print(admin_list)
        time.sleep(600)

name_db = 'server.db'
base = seller.db_connection(name_db)

id_vopla = -183040898
id_group = None

peer_htoniks = None
peer_sovets = None

vk_session = vk_api.VkApi(token = GROUP_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, id_group)

conversation_message_ids = []
admin_list = []


flag_book = 0
flag_item = 0
flag_delete = 1
storage_word = "Хранилище"
delete_word = "/удаление"


threading.Thread(target=admin_loop, args=[vk, peer_htoniks, admin_list], daemon=True).start()
threading.Thread(target=delete_loop, args=[vk, id_group, peer_htoniks, conversation_message_ids], daemon=True).start()

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if not ('reactions' in event.object.message.keys()):
                    peer_id = event.message.peer_id
                    original_message = event.message.text
                    user_id = event.message.from_id
                    if event.from_chat and peer_id == peer_htoniks:
                        if original_message == delete_word:
                            flag_delete = not flag_delete
                            if flag_delete:
                                message_to_send = f'Удаление активировано'
                            else:
                                message_to_send = f'Удаление отключено'
                            send_message(peer_htoniks, message_to_send)

                        if original_message[:10] == "📘Книгохран" and user_id == id_vopla:
                            if not (user_id in admin_list) and flag_delete:
                                
                                message_id = event.message.conversation_message_id
                                conversation_message_ids.append(message_id)
                                print('Not skip')
                            else:
                                print('Skip')
                            book_storage = original_message[original_message.find("Книга"):] + "\n"
                            flag_book = 1
                            
                            # res = delete_message(id_group, peer_htoniks, conversation_message_ids)
                            # print(res)

                        elif original_message[:7] == "👝Склад:" and user_id == id_vopla:
                            if not (user_id in admin_list) and flag_delete:
                                message_id = event.message.conversation_message_id
                                conversation_message_ids.append(message_id)
                                print('Not skip')
                            else:
                                print('Skip')
                            item_storage = original_message[original_message.find("Золото"):] + "\n"
                            flag_item = 1
                            # delete_message(id_group, peer_htoniks, message_ids)

                        elif storage_word in original_message:
                            if not (int(user_id) in admin_list) and flag_delete:
                                message_id = event.message.conversation_message_id
                                conversation_message_ids.append(message_id)
                                print('Not skip')
                            else:
                                print('Skip')
                        if flag_book and flag_item:
                            s = []
                            s.append(book_storage)
                            s.append(item_storage)
                            item_dict = get_dict(base)
                            for index_message in s:
                                while index_message.find('\n') != -1:
                                    string = index_message[:index_message.find('\n')]
                                    index_message = index_message[index_message.find('\n')+1:]
                                    if string.find(':') != -1:
                                        item = string[:string.find(':')]
                                        if item[:5] == "Книга":
                                            item = item[8:].lower()
                                        count = string[string.find(':')+2:]
                                        for i in item_dict.keys():
                                            if item in item_dict[i].keys():
                                                item_dict[i][item].append(count)
                                                break
                            for section_name, section in item_dict.items():
                                if section_name in ("📕Книги Активных умений", "📘Книги Пассивных умений"):
                                    for book_name, values in section.items():
                                        # варианты:
                                        # [price]               -> нет количества, ставим 0
                                        # [price, qty]          -> уже всё ок
                                        # [] (на всякий случай) -> нет цены и количества, считаем [0, 0]
                                        if len(values) == 1:
                                            values.append(0)
                                        elif len(values) == 0:
                                            values.extend([0, 0])
                            message_to_send = ''
                            # print(item_dict)
                            for i in item_dict.keys():
                                message_to_send += f"{i}\n"
                                for j in item_dict[i].keys():
                                    if len(item_dict[i][j]) == 2:
                                        if item_dict[i][j][0] == 0:
                                            message_to_send += f"{j} - {item_dict[i][j][1]}\n"
                                        else:
                                            message_to_send += f"{j} - {item_dict[i][j][1]} ({item_dict[i][j][0]})\n"
                                message_to_send += "\n"
                            send_message(peer_htoniks, message_to_send)
                            flag_book, flag_item = 0, 0
                            
                    elif event.from_chat and peer_id == peer_sovets and original_message.lower() == "покажи запасы":
                        if item_dict != {}:
                            count = 0
                            sum_prise = 0
                            for j in item_dict["📕Книги Активных умений"].keys():
                                if len(item_dict["📕Книги Активных умений"][j]) == 2:
                                    sum_prise += int(item_dict["📕Книги Активных умений"][j][0])*int(item_dict["📕Книги Активных умений"][j][1])
                                    count += int(item_dict["📕Книги Активных умений"][j][1])
                            for j in item_dict["📘Книги Пассивных умений"].keys():
                                if len(item_dict["📘Книги Пассивных умений"][j]) == 2:
                                    sum_prise += int(item_dict["📘Книги Пассивных умений"][j][0])*int(item_dict["📘Книги Пассивных умений"][j][1])
                                    count += int(item_dict["📘Книги Пассивных умений"][j][1])
                            message_to_send = f"📘Книг на складе: {count}\n🌕Суммарная стоимость книг на складе: {sum_prise}"
                            send_message(peer_sovets, message_to_send)
                        else:
                            message_to_send = f"Стоимость книг не определена, запросите содержимое хранилища."
                            send_message(peer_sovets, message_to_send)



    except():
        Exception()

