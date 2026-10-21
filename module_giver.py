import vk_api
from vk_api.utils import get_random_id

# Отправка обычного сообщения
def send_message(vk, peer_id, message):
    vk.messages.send(
        peer_id = peer_id,
        message = message,
        random_id = get_random_id()
    )

# Отправка сообщения с пересылом сообщения:
    # Нахождение сообщения:
        # Получение имени/фамилии по id
def find_name(vk, user_id):
    return vk.users.get(user_ids=user_id)[0]
        # Получение последних сообщений поиском
def search_messages(vk, user_id, message, peer_id, count=20, offset=0):
    user = find_name(vk, user_id)
    first_name = user['first_name']
    last_name = user['last_name']
    name = f'{first_name} {last_name}'
    last_messages = vk.messages.search(
        q=f'{message} {name}',
        peer_id=peer_id,
        offset=offset,
        count=count
    )
    return last_messages
        # Получение сообщения для "ответа" (пересыла)
def analitic_messages(messages, user_id):
    message_id = 0
    for i in range(len(messages['items'])):
        if not message_id and messages['items'][i]['from_id'] == user_id:
            message_id = messages['items'][i]['id']
    return message_id
    # Полная подготовка к отправке
def get_message_id(vk, user_id, message, peer_id):
     return analitic_messages(search_messages(vk, user_id, message, peer_id), user_id)
    # Отправка сообщения
def send_message_person(vk, peer_id, message, user_id, find_message):
    message_id = get_message_id(vk, user_id, find_message, peer_id)
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