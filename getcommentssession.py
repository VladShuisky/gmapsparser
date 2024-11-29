
from typing import List, Optional

import pandas
from gmapscomments import GoogleMapsComments
from originprotobufgetterbase import OriginProtobufGetterBase


class GoogleCommentsPriority:
    RELEVANT = '1' #max 360 comments
    # NEW = '2' #NOT WORKS CORRECTLY
    RAITING_DECREASE = '3' 
    # RATING_INCREASE = '4' #NOT WORKS CORRECTLY


class GoogleCommentsLanguages:
    ENG = 'en'
    RUS = 'ru'


class NoProtobufError(Exception):
    pass

class GetCommentsSession:
    def __init__(
            self,
            comments_parser: GoogleMapsComments,
            link_to_place_object: str,
            comments_priority: int, 
            origin_protobuf_getter: OriginProtobufGetterBase,
            language: str,
            number: int,
            file: str = None,
        ) -> None:
        self.link_to_place_object = link_to_place_object
        self.comments_parser = comments_parser
        self.comments_priority = comments_priority
        self.origin_protobuf_getter = origin_protobuf_getter
        self.language = language
        self.number = number
        self.filename_with_ext = file

    def get(self) -> Optional[List]:
        origin_protobuf = self.origin_protobuf_getter.get_origin_protobuf()
        if not origin_protobuf:
            raise NoProtobufError()
        comments: list = self.comments_parser.get_all_comments(self.language, origin_protobuf, self.number, self.comments_priority)

        if self.filename_with_ext:
            df = pandas.DataFrame(comments, columns=['comments'])
            df.to_csv(f'{self.filename_with_ext}', index=True)

        return comments