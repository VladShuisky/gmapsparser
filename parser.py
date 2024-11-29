import traceback
import argparse

from customchrome import ChromeWithDebugMode, UndetectedChromeWithDebugMode
from getcommentssession import GetCommentsSession, GoogleCommentsLanguages, GoogleCommentsPriority
from gmapscomments import GoogleMapsComments
from originprotobuffselenium import OriginProtobufSelenium

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    '--place_link',
    type=str,
    required=True,
    help='Ссылка на достопримечательность'
    )

arg_parser.add_argument(
    '--priority',
    type=str,
    required=True,
    help='Способ сортировки: самые релевантные(до 360 комментариев), или по убыванию рейтинга(более 1000)'
)

arg_parser.add_argument(
    '--lang',
    type=str,
    required=True,
    help='Язык комментариев'
)

arg_parser.add_argument(
    '--number',
    type=int,
    required=True,
    help='Необходимое количество комментариев'
)

arg_parser.add_argument(
    '--file',
    type=str,
    required=True,
    help='Файл, в который необходимо сохранить результаты'
)

args = arg_parser.parse_args()

comments_priority = None
if args.priority == 'relevant':
    comments_priority = GoogleCommentsPriority.RELEVANT
elif args.priority == 'rating_decrease':
    comments_priority = GoogleCommentsPriority.RAITING_DECREASE
if not comments_priority:
    raise Exception('Назначьте параметр --priority (relevant или rating_decrease)')

language = None
if args.lang == 'en':
    language = GoogleCommentsLanguages.ENG
elif args.lang == 'ru':
    language = GoogleCommentsLanguages.RUS
if not language:
    raise Exception('Назначьте параметр --priority (en или ru)')

# #entry to program
if __name__ == '__main__':
    link = args.place_link
    chrome = UndetectedChromeWithDebugMode() #тут должен быть хром с подключенным дебаг режимом
    get_comments_ses = GetCommentsSession(
        comments_parser=GoogleMapsComments,
        link_to_place_object=link,
        comments_priority=comments_priority,
        origin_protobuf_getter=OriginProtobufSelenium(chrome.driver, chrome.action_chains, link),
        language=language,
        number=args.number,
        file=args.file
    )

    try:
        get_comments_ses.get()
    except Exception as e:
        print('Глобальная ошибка')
        traceback.print_exc()