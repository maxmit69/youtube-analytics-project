import os
from datetime import timedelta
import isodate
from googleapiclient.discovery import build


class PlayList:
    """ Класс для ютуб-плейлиста.
    """

    def __init__(self, playlist_id) -> None:
        """ Экземпляр инициализируется id плейлиста.
        """
        self.__playlist_id = playlist_id
        """ Дальше все данные будут подтягиваться по API.
        """
        playlist_videos = self.get_service.playlistItems().list(playlistId=self.__playlist_id,
                                                                part='contentDetails',
                                                                ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        playlist_response = self.get_service.playlists().list(id=self.__playlist_id, part='snippet').execute()
        self.video_response = self.get_service.videos().list(part='contentDetails, statistics',
                                                             id=','.join(video_ids)
                                                             ).execute()
        self.title = playlist_response['items'][0]['snippet']['title']     # Название плейлиста
        self.url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'  # Ссылка на плейлист

    def __str__(self) -> str:
        """ Выводит информацию о плейлисте в строке для пользователя
        """
        return f"{self.title}"

    def __repr__(self):
        """ Выводит информацию о плейлисте в строке для разработчиков
        """
        return f"{self.__class__.__name__}{self.title}, {self.url}"

    @property
    def get_service(self) -> build:
        """ Возвращает экземпляр API.
        """
        return build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))

    @property
    def total_duration(self) -> timedelta:
        """ Возвращает общую длительность плейлиста.
        """
        duration = 0
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration += int(isodate.parse_duration(iso_8601_duration).total_seconds())
        return timedelta(seconds=duration)

    def show_best_video(self) -> str:
        """ Возвращает ссылку на лучшее видео плейлиста.
        """
        list_video = []
        for video in self.video_response['items']:
            list_video.append(video['statistics']['likeCount'])
        return f'https://youtu.be/{self.video_response["items"][list_video.index(max(list_video))]["id"]}'
