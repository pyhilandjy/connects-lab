from datetime import datetime

from pymongo import MongoClient


def insert_to_mongo(data: list[dict]):
    """mongodb 적재"""

    # mongodb 접속정보 host 는 docker 컨테이너 이름으로 지정해야함.
    client = MongoClient(host="ig-airflow-mongodb-1", port=27017)

    # db 이름
    db = client["instagram_data"]

    # 적재할 컬랙션 이름
    collection = db["posts"]

    # 데이터 삽입
    try:
        collection.insert_many(data)
    except Exception as e:
        print(f"{e}")
    else:
        print(f"Inserted: {data}")
        return True
    finally:
        # MongoDB 연결 종료
        client.close()
