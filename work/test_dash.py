import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

# 가상의 데이터 프레임을 만들어서 사용하도록 합시다.
data = {
    "_id": ["65682ad51346d40b291815bc", "65682ad51346d40b291815bd"],
    "Noun": [
        ["아기", "토끼", "딸기", "아이스크림", "달라", "어필", "하나"],
        ["어린이", "마", "니", "터폰", "중독", "휴대폰", "이제", "매트", "폰", "프리", "죤", "사진"],
    ],
    "Verb": [
        ["하다", "끄다", "얻어먹다"],
        ["서다", "하다", "보다", "찍다", "나가다", "때리다", "먹다", "하다", "나가다", "돌보다", "하다"],
    ],
    "Adjective": [["끈질기다"], ["미치다", "그렇다", "아쉽다", "있다", "그렇다", "신나다"]],
    "user_name": ["krrang2_bebe", "esjxuniverse"],
    "like_count": [94, 0],
    "upload_date": ["2023-11-29", "2023-11-29"],
}

df = pd.DataFrame(data)

# Dash 앱 초기화
app = dash.Dash(__name__)

# 레이아웃 정의
app.layout = html.Div(
    [
        html.H1("텍스트 데이터 Dash 보드"),
        # Dropdown으로 사용자 선택
        dcc.Dropdown(
            id="user-dropdown",
            options=[{"label": user, "value": user} for user in df["user_name"]],
            value=df["user_name"][0],
            multi=False,
        ),
        # 선택된 사용자의 정보 출력
        html.Div(id="user-info"),
        # 선택된 사용자의 텍스트 정보 출력
        dcc.Markdown(id="user-text"),
    ]
)


# 콜백 함수 정의
@app.callback(
    [Output("user-info", "children"), Output("user-text", "children")],
    [Input("user-dropdown", "value")],
)
def update_output(selected_user):
    # 선택된 사용자의 정보
    user_info = df[df["user_name"] == selected_user][
        ["_id", "like_count", "upload_date"]
    ].to_dict("records")[0]

    # 선택된 사용자의 텍스트 정보
    user_text = df[df["user_name"] == selected_user][
        ["Noun", "Verb", "Adjective"]
    ].to_dict("records")[0]

    return (
        f"게시물 ID: {user_info['_id']}, 좋아요 수: {user_info['like_count']}, 업로드 날짜: {user_info['upload_date']}",
        f"Noun: {user_text['Noun']}\nVerb: {user_text['Verb']}\nAdjective: {user_text['Adjective']}",
    )


# 앱 실행
if __name__ == "__main__":
    app.run_server(debug=True)
