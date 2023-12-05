from services.morphs_tools import remove_emoji, remove_hashtags
from services.database import morphs_to_mongo, pull_daily_mongo
from konlpy.tag import *
import re

def morphs():
    okt = Okt()
    data = pull_daily_mongo()

    contents = data['caption'].astype(str)
    morphs_list = []


    for content in contents:
        #형태소 분석
        content = remove_hashtags(content)
        content = remove_emoji(content)
        morphs = okt.pos(content,norm=True, stem=True)
        morphs_list.append(morphs)

    data.drop('caption',axis=1,inplace=True)

    kind = ['Noun','Verb','Adjective','Determiner','Adverb','Conjunction','Exclamation','Josa','PreEomi',
            'Punctuation','Foreign','Alpha','Number','KoreanParticle','Modifier']

    for i in kind:
            globals()[f"{i}_list"] = []

    for mor in morphs_list:
        for i in kind:
            try:
                a = [item[0] for item in mor if item[1] == str(i)]
                globals()[f"{i}_list"].append(a)
            except:
                globals()[f"{i}_list"].append('')


    for index,value in enumerate(kind):
        data.insert(index+1,f'{value}',globals()[f"{value}_list"])
    data = data.to_dict('records')
    morphs_to_mongo(data=data)