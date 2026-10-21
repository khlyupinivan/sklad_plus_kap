import time
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from vk_api.longpoll import VkLongPoll, VkEventType

def write_msg(user_id, message, random_id):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})


def send_message(peer_id, message, message_id):
    vk.messages.send(
        peer_id = peer_id,
        message = message,
        random_id = get_random_id(),
        reply_to = message_id
    )


token = ""

vk_session = vk_api.VkApi(token = token)
vk = vk_session.get_api()


longpoll = VkLongPoll(vk_session)

vip_id = {}

while True:
    try:


        for event in longpoll.listen():



            if event.type == VkEventType.MESSAGE_NEW:


                message = event.text.lower()
                peer = event.peer_id
                message_id = event.message_id
                if event.from_chat and event.peer_id == 2000000280  and message == 'босс, стройку!' and event.user_id in vip_id:
                    send_message(peer, "@club183040898 Строительство", message_id)
                
        time.sleep(2)
    except:
        Exception