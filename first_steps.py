from pprint import pprint
from class_VKinder import vk_session
import json
import vk_api
from database import VK_user, session
from time import sleep



# city = str(input('введите город:'))
city = 'Санкт-Петербург'



def users():
    candidates = list()
    # users_list = vk_session.method('users.search',
    #                                    {'count': 1000,'age_from': 18, 'age_to': 25, 'sex': 1,
    #                                     'status': 1,
    #                                     'fields': 'bdate, sex, city, relation, domain'})['items']
    users_list = vk_session.method('users.search', {'count': 100, 'fields': 'bdate, sex, city, relation, domain'})[
        'items']
    for person in users_list:
                # if person in candidates:
                    # continue
                # else:
                    if 'city' in person.keys():
                        if person['city']['title'] == city:
                            try:
                                user_photos = vk_session.method('photos.get',
                                                                {'user_id': person['id'], 'owner_id': person['id'],
                                                                 'album_id': 'profile',
                                                                 'extended': 1, 'photo_sizes': 0})['items']
                                candidates.append(person)
                            except vk_api.exceptions.ApiError:
                                pass
    return candidates


# pprint(users())


def get_user_photos(person):
    user_photos = vk_session.method('photos.get', {'user_id': person['id'], 'owner_id': person['id'], 'album_id': 'profile',
                                                 'extended': 1, 'photo_sizes': 0})['items']
    # sleep(1)
    return user_photos


def top_three_photo(person):
    photos_dict = dict()
    photos = get_user_photos(person)
    top_three_id = list()
    for pic in photos:
        photos_dict[pic['id']] = pic['likes']['count'] + pic['comments']['count']
    rating = sorted(photos_dict.values(), reverse=True)[0:3]
    for item in rating:
        for k, v in photos_dict.items():
            if item == v:
                top_three_id.append(k)
    return top_three_id


def get_photos_url(candidates):
    # candidates = users()
    candidates_list = dict()
    for person in candidates:
        top_three_best = dict()
        photos = get_user_photos(person)
        best_photos = top_three_photo(person)
        for i in best_photos:
            for pic in photos:
                if pic['id'] in best_photos:
                    for size in pic['sizes']:
                        if size['type'] == 'x':
                            top_three_best[pic['id']] = size['url']
                        elif size['type'] == 'y':
                            top_three_best[pic['id']] = size['url']
                        elif size['type'] == 'z':
                            top_three_best[pic['id']] = size['url']
                        elif size['type'] == 'w':
                            top_three_best[pic['id']] = size['url']
        candidates_list['https://vk.com/' + person['domain']] = list(top_three_best.values())
        person['id'] = VK_user(user_domain='https://vk.com/' + person['domain'])
        session.add(person['id'])
    session.commit()
    with open('file.json', 'w', encoding='utf-8') as f:
        json.dump(candidates_list, f, ensure_ascii=False, indent=2)

    return candidates_list



pprint(get_photos_url(users()))


