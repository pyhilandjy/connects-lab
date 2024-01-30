from konlpy.tag import *
import re

def remove_emoji(text):
    """이모티콘 삭제"""
    # 이모티콘 패턴 정규 표현식
    emoji_pattern = re.compile("[^\w\s가-힣]+", flags=re.UNICODE)
    # 이모티콘 제거
    text = emoji_pattern.sub(r'', text)
    return text


def remove_hashtags(text):
    """해시태그를 삭제"""
    # 해시태그 패턴 정규 표현식
    hashtag_pattern = re.compile(r'#\w+\s?')
    # 해시태그 삭제
    text = hashtag_pattern.sub(r'', text)
    return text