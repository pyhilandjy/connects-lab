from datetime import datetime
import pandas as pd
from pymongo import MongoClient
import json

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
    return data

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

def pull_morphs():
    """daily로 크롤링한 데이터 불러오기 (return:Dataframe)"""

    # mongodb 접속정보 host 는 docker 컨테이너 이름으로 지정해야함.
    client = MongoClient(url)

    # db 이름
    db = client["ConnectsLab"]

    # 연결할 컬랙션 이름
    collection = db["insta_crawling_mongo"]

    # 쿼리
    query = {}
    daily_data = collection.find(query)
    daily_data = pd.DataFrame(daily_data)
    return daily_data

def mongo_to_json(all_data):
    url = "mongodb+srv://startup_proj_de_08:Team08!!@team08.mi7hgs1.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(url)

    # 데이터베이스 및 컬렉션 선택
    db = client["ConnectsLab"]
    collection = db["insta_crawling_mongo"]

    # MongoDB에서 데이터 가져오기
    cursor = collection.find()

    # 결과를 리스트로 변환
    all_data = list(cursor)

    file_path = '/opt/airflow/dags/services/insta_crawling_morphs.json'

    # 중복을 방지하기 위해 기존 데이터에서 _id 필드 제거
    for item in all_data:
        if '_id' in item:
            del item['_id']

    # 새로운 데이터 삽입
    collection.insert_many(all_data)

    # 기존 데이터와 새로운 데이터를 다시 가져오기
    cursor = collection.find()
    data = list(cursor)

    # JSON 파일로 저장
    with open(file_path, 'w', encoding='utf-8') as insta_json:
        json.dump(data, insta_json, ensure_ascii=False, indent=4)

    # MongoDB 연결 닫기
    client.close()

def delete_id(user_id):
    """비활성화 ID 삭제"""

    client = MongoClient(url)
    db = client.ConnectsLab
    collection = db.user

    # 삭제할 문서의 조건 설정
    delete_condition = {'id': user_id}

    #collection.delete_one(delete_condition) # 조정 완료

    db = client["ConnectsLab"]

    # 연결할 컬랙션 이름
    collection = db["delete_user"]

    # 적재
    collection.insert_one({'id' : user_id})