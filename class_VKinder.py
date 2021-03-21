from module_dotenv import login, password
import vk_api


# login = str(input('введите логин:'))
# password = str(input('введите пароль:'))



class Vkinder(vk_api.vk_api.VkApi):

    pass



vk_session = Vkinder(login, password)
vk_session.auth(token_only=True)