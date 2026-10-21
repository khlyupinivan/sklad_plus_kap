import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import datetime
import progress_module


def send_message(peer_id, message, attachment=None):
    vk.messages.send(
        peer_id=peer_id,
        message=message,
        random_id=get_random_id(),
        attachment=attachment
    )


def get_stats(message):
    if message[0] == '👑':
        message = message[1:]
    upgrade_id = message[1:message.find('|')]
    upgrade_name = message[message.find("|")+1: message.find("]")]
    upgrade_lvl = message[message.find("💀")+10: message.find("🎉")-1]
    start_stats = message.find('👊')
    end_stats = message.find('🍀')
    new_message = message[start_stats: end_stats]
    strang = new_message[1:new_message.find('🖐')-1]
    new_message = new_message[new_message.find('🖐'):]
    agil = new_message[1:new_message.find('❤')-1]
    new_message = new_message[new_message.find('❤')+1:]
    stam = new_message[:-1]
    return [upgrade_id, upgrade_name.title(), upgrade_lvl, strang, agil, stam]

# Сюда копируется токен
token = ""
id_group = None
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, id_group)
# Сюда вводится номер чата (сначала 2, потом 9 чисел, если в номере чата меньше чисел перед номером ставятся нули таким образом, чтобы в итоге вышло 9 чисел)
peer_chat = None
name_db = 'kaps_database.db'
base = progress_module.db_connection(name_db)
id_dima = 0
id_vopla = -183040898 
id_vip = {}

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if not ('reactions' in event.object.message.keys()):
                    message = event.message.text.lower()
                    peer = event.message.peer_id
                    user_id = event.message.from_id
                    message_id = event.message.message_id
                    print(message)
                    if event.message.peer_id == peer_chat and message.find('ваш профиль:') != -1:
                        now = datetime.datetime.now()
                        stats = get_stats(message)
                        print(progress_module.update_user_stats(base, stats[0], stats[2], stats[3], stats[4], stats[5], now))
                        print(progress_module.update_user_progress(base, stats[0], stats[2], stats[3], stats[4], stats[5], now))
                    elif event.message.peer_id == peer_chat and message == "мой профиль":
                        user = vk.users.get(user_ids=user_id, fields=[])
                        name_user = user[0]['first_name'] + ' ' + user[0]['last_name']
                        print(progress_module.add_user(base, f'id{user_id}', name_user))
                    elif event.message.peer_id == peer_chat and message == "/кап" and event.message.user_id != id_dima:
                        kap = progress_module.create_stats_message(base, f'id{user_id}')
                        send_message(peer_chat, kap)
                    elif event.message.peer_id == peer_chat and message == "/прогресс" and event.message.user_id != id_dima:
                        progress = progress_module.create_progress_message(base, f'id{user_id}')
                        send_message(peer_chat, progress)
                    elif event.message.peer_id == peer_chat and message == "/сброс":
                        print(progress_module.delete_progress(base, f'id{user_id}'))
                    elif event.message.peer_id == peer_chat and message == "/отсчёт" and (user_id in id_vip):
                        send_message(peer_chat, progress_module.update_user_progress_last_week(base))
                    elif event.message.peer_id == peer_chat and message == "/дай стату" and (user_id in id_vip):
                        print(progress_module.create_all_progress(base))
                        upload = vk_api.VkUpload(vk)
                        file = upload.document_message(doc="statistics.xlsx", title="statistics", peer_id=peer_chat)
                        owner_id = file['doc']['owner_id']
                        my_id = file['doc']['id']
                        send_message(peer_chat, "", f"doc{owner_id}_{my_id}")
                        vk.docs.delete(owner_id=owner_id, doc_id=my_id)
                    elif  event.message.peer_id == peer_chat and message == "/изгнать" and (user_id in id_vip):
                        delete_id = event.object.message['fwd_messages'][0]['from_id']
                        print(delete_id)
                        send_message(peer_chat, progress_module.delete_user(base, f'id{delete_id}'))

    except:
        pass
