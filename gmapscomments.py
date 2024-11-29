import json
import time
import traceback
import urllib.parse

import requests
import tqdm


class GoogleMapsComments:
    BASE_URL = 'https://www.google.com/maps/rpc/listugcposts'

    @classmethod
    def _request_to_gmaps_api(cls, type: str, **params):
        payload = urllib.parse.urlencode(params, safe='!%')
        if type == 'get':
            r = requests.get(
                url=cls.BASE_URL,
                params=payload
            )
        else:
            pass ### TODO дописать логику для пост запросов
        return r

    @classmethod
    def get_ten(cls, language: str, pb: str):
        '''
        Возвращает словарь из 2 ключей: 
        comments -10 последних комментариев(по релевантности - то как отдаёт гугл апи изначально)
        pagination_token - токен для внедрения в payload для следующего запроса следующих комментариев
        '''
        r = cls._request_to_gmaps_api(type='get', authuser='0', hl=language, gl=language, pb=pb)

        data = json.loads(r.text[5:])
        return {
            'comments': [el[0][2][-1][0][0] for el in data[2]],
            'pagination_token': data[1]
            }
    
    @classmethod
    def _format_pb(cls, origin_pb: str, pb_elem_index: int, value: str):
        try:
            splitted = origin_pb.split('!')
            if not splitted:
                raise Exception
            splitted[pb_elem_index] = value
            return '!'.join(splitted)
        except Exception as e:
            print(
                f'Ошибка в функции format_pb, '
                f'не удалось разделить строку по восклицательному знаку!'
                f'исходная строка >>> {origin_pb}'
                )

    @classmethod
    def get_all_comments(cls, language: str, pb: str, number: int, priority: int = None):
        comments = []

        origin_cell_for_paginator = pb.split('!')[10]

        origin_cell_for_ordering_type = pb.split('!')[-1]

        pbar = tqdm.tqdm(total=number, desc='Получено комментариев >>>')

        pb = cls._format_pb(pb, -1, origin_cell_for_ordering_type[:2]+priority)

        first_ten_comments_data: dict = cls.get_ten(language=language, pb=pb)

        token = first_ten_comments_data.get('pagination_token')

        if first_ten_comments_data.get('comments'):
            comments.extend(first_ten_comments_data.get('comments'))
            pbar.update(10)
        try:
            while True:
                token_with_prefix = origin_cell_for_paginator + token
                pb_with_pagination_token: str = cls._format_pb(pb, 10, token_with_prefix)
                res = cls.get_ten(language=language, pb=pb_with_pagination_token) #сюда нужно передать уже обработанный параметр pb с вставленным в него токеном пагинации
                new_pagination_token = res.get('pagination_token')
                token = new_pagination_token
                comments_slice = res.get('comments')
                if comments_slice:
                    comments.extend(comments_slice)
                    pbar.update(10)

                else:
                    print('Нету нихуя!!!')
                if len(comments) >= number:
                    break
                time.sleep(1)
        except Exception:
            print('ОШИБКА В БЛОКЕ!!!')
            traceback.print_exc()

        finally:
            pbar.close()
            return comments