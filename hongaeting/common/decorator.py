import shutil

from django.conf import settings


def delete_media_root(func):
    # 테스트 도중 생성된 MEDIA root directory를 삭제하는 decorator
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        finally:
            media_root = settings.MEDIA_ROOT.split('/')[0]
            shutil.rmtree(media_root)
        return result

    return wrapper
