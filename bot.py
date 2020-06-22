

import vk_api
import random

class vkBot:

    listMessage = []

    def __init__(self, key):
        self.vk_session = vk_api.VkApi(token=key)
        self.vk = self.vk_session.get_api()
        print("Vk bot is Started")

    def readMessage(self):
        from vk_api.longpoll import VkLongPoll, VkEventType

        longpoll = VkLongPoll(self.vk_session)


        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                if event.from_user:
                    # Проверка сообщения
                    for m in self.listMessage:

                        #Функция
                        if m['func'] != None:
                            m['func']( event.user_id, event.text)

                        #Проверка текста
                        if event.text == m['check']:
                            if len(m['img']) != 0:
                                self.vk.messages.send(
                                    user_id=event.user_id,  # Пользователь получатель
                                    message=m['message'],  # Текст сообщения
                                    random_id=random.randint(1, 2147483647),
                                    attachment=','.join(m['img'])
                                )
                            elif m['message'] != "":
                                self.vk.messages.send(
                                    user_id=event.user_id,  # Пользователь получатель
                                    message=m['message'],  # Текст сообщения
                                    random_id=random.randint(1, 2147483647)
                                )

                            # Отправка сообщения

    def addMessage(self, check="!", message="", img=[], func=None):
        from vk_api import VkUpload
        upload = VkUpload(self.vk_session)
        for i in range(len(img)):
            print(img[i])
            photo = upload.photo_messages(photos=img[i])[0]
            print(photo)
            img[i] = 'photo{}_{}'.format(photo['owner_id'], photo['id'])
        self.listMessage.append({"check": check, "message": message, "img": img, "func": func})

    def sendMessage(self, user, message):
        self.vk.messages.send(
            user_id=user,  # Пользователь получатель
            message=message,  # Текст сообщения
            random_id=random.randint(1, 2147483647),
        )