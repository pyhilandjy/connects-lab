from datetime import datetime
import pandas as pd
from pymongo import MongoClient

url = "mongodb+srv://startup_proj_de_08:Team08!!@team08.mi7hgs1.mongodb.net/?retryWrites=true&w=majority"

def crawl_to_mongo(data: list[dict]):
    """ crawl_data mongodb 적재"""

    # mongodb 접속정보 host 는 docker 컨테이너 이름으로 지정해야함.
    client = MongoClient(url)

    # db 이름
    db = client["ConnectsLab"]

    # 연결할 컬랙션 이름
    collection = db["insta_crawling_test"]

    # 적재
    collection.insert_many(data)

    # MongoDB 연결 종료
    client.close()

def morphs_to_mongo(data: list[dict]):
    """ morphs_data mongodb 적재"""

    # mongodb 접속정보 host 는 docker 컨테이너 이름으로 지정해야함.
    client = MongoClient(url)

    # db 이름
    db = client["ConnectsLab"]

    # 연결할 컬랙션 이름
    collection = db["ts"]

    # 적재
    collection.insert_many(data)

    # MongoDB 연결 종료
    client.close()

def crawl_to_mongo_daily(data: list[dict]):
    """ daily_data mongodb 적재"""

    # mongodb 접속정보 host 는 docker 컨테이너 이름으로 지정해야함.
    client = MongoClient(url)

    # db 이름
    db = client["ConnectsLab"]

    # 연결할 컬랙션 이름
    collection = db["insta_daily_data_test"]

    collection.delete_many({})

    # 적재
    collection.insert_many(data)

    # MongoDB 연결 종료
    client.close()

def pull_daily_mongo():
    """daily로 크롤링한 데이터 불러오기 (return:Dataframe)"""

    # mongodb 접속정보 host 는 docker 컨테이너 이름으로 지정해야함.
    client = MongoClient(url)

    # db 이름
    db = client["ConnectsLab"]

    # 연결할 컬랙션 이름
    collection = db["insta_daily_data_test"]

    # 쿼리
    query = {}
    daily_data = collection.find(query)
    daily_data = pd.DataFrame(daily_data)
    return daily_data

def search_id():
    """user collection 접속 및 id 조회"""

    client = MongoClient(url)
    db = client.ConnectsLab  # 데이터베이스 이름으로 변경
    collection = db.user  # 컬렉션 이름으로 변경

    # 조회할 컬럼 이름
    desired_column = 'id'  # 조회하려는 컬럼 이름으로 변경

    # 특정 컬렉션에서 특정 컬럼 조회
    result = collection.find({}, {desired_column: 1, '_id': 0})

    id_list = []
    # 결과 출력
    for document in result:
        id_list.append(document['id'])

    return id_list