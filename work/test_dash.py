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