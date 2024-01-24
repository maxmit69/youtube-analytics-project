import os
from googleapiclient.discovery import build


class Video:
    """ Класс для ютуб-видео.
    """

    def __init__(self, video_id) -> None:
        """ Экземпляр инициализируется id видео.
        """
        try:
            self.__video_id = video_id
            """ Дальше все данные будут подтягиваться по API.
            """
            video_response = self.get_service.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                            id=video_id
                                                            ).execute()

            self.title = video_response['items'][0]['snippet']['title']              # Название видео
            self.description = video_response['items'][0]['snippet']['description']  # Описание видео
            self.url = f'https://www.youtube.com/watch?v={video_id}'                 # Ссылка на видео
            self.like_count = video_response['items'][0]['statistics']['likeCount']  # Количество лайков
            self.view_count = video_response['items'][0]['statistics']['viewCount']  # Количество просмотров

        except Exception:
            """ Если пользователь передал не корректное id.
            """
            self.title = None
            self.description = None
            self.url = None
            self.like_count = None
            self.view_count = None

    def __str__(self) -> str:
        """ Выводит информацию о видео в строке.
        """
        return f"{self.title}"

    def __repr__(self):
        """ Выводит информацию о видео в строке для разработчика
        """
        return f"{self.__class__.__name__}{self.title}, {self.url}, {self.like_count}, {self.view_count}"

    @property
    def get_service(self) -> build:
        """ Возвращает экземпляр API.
        """
        return build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))


class PLVideo(Video):
    """ Класс для ютуб-видео из плейлиста.
    """

    def __init__(self, video_id, playlist_id):
        """ Экземпляр инициализируется id видео и id плейлиста.
        """
        super().__init__(video_id)
        self.playlist_id = playlist_id
