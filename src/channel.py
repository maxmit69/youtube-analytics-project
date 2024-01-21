import os
import json
from googleapiclient.discovery import build


class Channel:
    """ Класс для ютуб-канала.
    """
    API_KEY: str = os.getenv('YT_API_KEY')

    def __init__(self, channel_id) -> None:
        """ Экземпляр инициализируется id канала.
        """
        self.__channel_id = channel_id
        """ Дальше все данные будут подтягиваться по API.
        """
        channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']                          # Название канала
        self.description = channel['items'][0]['snippet']['description']              # Описание канала
        self.video_count = channel['items'][0]['statistics']['videoCount']            # Количество видео в канале
        self.url = f'https://www.youtube.com/channel/{channel_id}'                    # Ссылка на канал
        self.view_count = channel['items'][0]['statistics']['viewCount']              # Количество просмотров в канале
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']  # Количество подписчиков в канале

    def __str__(self) -> str:
        """ Выводит информацию о канале в строке.
        """
        return f"{self.title} ({self.url})"

    def __repr__(self):
        return (f"{self.__class__.__name__}{self.title}, {self.url}, {self.video_count}, {self.view_count}, "
                f"{self.subscriber_count}, {self.description}")

    def __add__(self, other: str) -> int:
        """ Сложение подписчиков каналов.
        """
        if isinstance(other, self.__class__):
            return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other: str) -> int:
        """ Вычитание подписчиков из второго канала.
        """
        if isinstance(other, self.__class__):
            return int(other.subscriber_count) - int(self.subscriber_count)

    def __sub__(self, other: str) -> int:
        """ Вычитание подписчиков каналов из первого канала.
        """
        if isinstance(other, self.__class__):
            return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other: str) -> int:
        """ Сравнение подписчиков каналов на больше.
        """
        if isinstance(other, self.__class__):
            return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other: str) -> int:
        """ Сравнение подписчиков каналов на больше или равно.
        """
        if isinstance(other, self.__class__):
            return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other: str) -> int:
        """ Сравнение подписчиков каналов на меньше.
        """
        if isinstance(other, self.__class__):
            return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other: str) -> int:
        """ Сравнение подписчиков каналов на меньше или равно.
        """
        if isinstance(other, self.__class__):
            return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other: str) -> int:
        """ Сравнение подписчиков каналов на равенство.
        """
        if isinstance(other, self.__class__):
            return int(self.subscriber_count) == int(other.subscriber_count)

    def print_info(self) -> None:
        """ Выводит в консоль информацию о канале.
        """
        channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls) -> object:
        """ Возвращает объект для работы с API вне класса.
        """
        return build('youtube', 'v3', developerKey=cls.API_KEY)

    def to_dict(self) -> dict:
        """ Возвращает словарь данных канала.
        """
        return {
            'title': self.title,
            'description': self.description,
            'video_count': self.video_count,
            'url': self.url,
            'view_count': self.view_count,
            'subscriber_count': self.subscriber_count
        }

    def to_json(self, file_name: str) -> json:
        """ Сохраняет канал в файл.
        """
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
