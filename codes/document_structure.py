# coding:utf-8
# time: 2023/11/12 10:59 下午
import abc
from abc import ABC


class Serializer(object):

    @abc.abstractmethod
    def serialization(self, resource):
        pass

    @classmethod
    @abc.abstractmethod
    def deserialization(cls, resource):
        pass


class Range(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Document(object):

    def __init__(self, page_list):
        self.page_list = page_list


class Page(Range):

    def __init__(self, width, height, page_num, element_list):
        Range.__init__(self, 0, 0, width, height)
        self.page_num = page_num
        self.element_list = element_list or []


class Element(Range):

    def __init__(self, text_range_list, element_type):
        x, y, width, height = self.get_element_region(text_range_list)
        Range.__init__(self, x, y, width, height)
        self.text_range_list = text_range_list or []
        self.element_type = element_type

    @staticmethod
    def get_element_region(text_range_list):
        x, y, width, height = 0, 0, 0, 0
        if text_range_list:
            start_char = text_range_list[0].character_list[0]
            x1, y1 = start_char.x, start_char.y
            x2, y2 = start_char.x + start_char.width, start_char.y
            for text_range in text_range_list:
                for character in text_range.character_list:
                    x1 = min(character.x, x1)
                    y1 = min(start_char.y - character.height, y1)
                    x2 = max(character.x + character.width, x2)
                    y2 = max(start_char.y, y2)
            x, y, width, height = x1, y1, x2 - x1, y2 - y1
        return x, y, width, height


class TextRange(Range):

    def __init__(self, character_list):
        if character_list:
            start_char, end_char = character_list[0], character_list[-1]
            x = start_char.x
            y = start_char.y
            width = end_char.x + end_char.width - x
            height = max([char.height for char in character_list])
        else:
            x, y, width, height = 0, 0, 0, 0
        Range.__init__(self, x, y, width, height)
        self.character_list = character_list


class Character(Range):

    def __init__(self, x, y, width, height, page_num, char, font_name=''):
        Range.__init__(self, x, y, width, height)
        self.page_num = page_num
        self.char = char
        self.font_name = font_name


if __name__ == '__main__':
    page_list = []
    for page_num in range(1, 3):
        character_list = []
        for index in range(1, 11):
            character_list.append(Character(index, index, 1, 1, page_num, str(index)))
        text_range = TextRange(character_list)
        paragraph = Element([text_range], element_type='paragraph')
        page_list.append(Page(1123, 794, page_num, [paragraph]))    # A4-96dpi
    document = Document(page_list)
    print()

