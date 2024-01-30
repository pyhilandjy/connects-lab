from PIL import Image
from io import BytesIO
from dash import dcc, html
from pymongo import MongoClient
from wordcloud import WordCloud
from collections import Counter
from dash.dependencies import Input, Output
from datetime import datetime
import dash
import json
import base64
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#Json 데이터 로드 함수 정의
def load_data():
    with open('/home/ubuntu/airflow-docker/dags/services/insta_crawling_morphs.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def filter_data_by_date(data, start_date, end_date):

    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

    filtered_data = [entry for entry in data if
                     start_datetime <= datetime.strptime(entry.get('upload_date'), '%Y-%m-%d') <= end_datetime]
    return filtered_data

def generate_empty_wordcloud():
    empty_wordcloud = WordCloud(
        width=300,
        height=300,
        background_color='black',
        contour_color='black',
        font_path=font_path,
        repeat=False
    )

    # Generate an empty WordCloud
    empty_wordcloud.generate("없음")
    empty_image = empty_wordcloud.to_image()
    empty_resized_image = empty_image.resize((600, 600))  # 사이즈 조절 (필요에 따라 조절)

    # Convert the resized image to base64 for display
    buffered = BytesIO()
    empty_resized_image.save(buffered, format="PNG")
    encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return f"data:image/png;base64,{encoded_image}"

# Dash 애플리케이션 초기화
app = dash.Dash(__name__)

# 인스타그램 로고 이미지 경로
instagram_logo_path = "/home/ubuntu/airflow-docker/dags/services/instagram.webp"
instagram_logo = np.array(Image.open(instagram_logo_path))

# 한글 폰트 경로 설정 (설치된 폰트 경로로 수정 필요)
font_path = "/home/ubuntu/airflow-docker/dags/services/NanumGothic-Regular.ttf"

#유저아이디 & 형태소 종류
user_id = ['ALL', 'to.gangnang','baby._.tobitori','skwhaqkqk','lovely._.yuminimi','anvely._.22',
            '_rubi.21','harin_kong','choi._.maeum','hitobok_ahin','__sol.2020__v','bring_luck_b','40_ellie',
            'yeony_m0m','chandolmom','l___br','_torimom96','princesa_hana20','avelymami','si__a_a_','syws1473',
            '9._.kan','___j.nsa','kokoamy2011','yooyoo_log','2ddu_inside','wonian_love','dh_ruri','lua_onew',
            '20210101_jelly','p_g_y__','arin_jy','nayeon.wk','joyjoy_3_','evain425','chenvely_yun','rohee_days',
            'ji_a_2023','2dodo_solsol','ye.dami__','_choco.seol_a','do0_6astagram','lonny_mom','podo_sana',
            'eunn_vely','tory_zhi','mybaby_du','adorable_gaeul','thankwon_','j_chaewoo','kkomi_unni',
            's_.yulls','wooju_likeee','jihoon230713','ttaappongg','mozzileedohoo','shiny__day23','r_a_n_g22',
            'kim.nosan','y_youngji','pepero_love23','seon.yul_bebe','esjxuniverse','krrang2_bebe']

morphs_type = {'ALL': 'ALL', 'NNG': '일반명사', 'NNP': '고유명사', 'NP': '대명사', 'Verb': '동사', 'Adjective': '형용사','Adverb': '부사', 'Conjunction': '접속사', 'Josa': '조사', 'Number': '숫자'}
keys_list = ['NNG', 'NNP', 'NP', 'Verb', 'Adjective', 'Adverb', 'Conjunction', 'Josa', 'Number']

# 레이아웃 정의
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H2("유저별 발화 형태소 비율", style={'textAlign': 'center', 'padding': '15px', 'background-color': '#ccc', 'color': 'black', 'border-radius': '10px 10px 0 0', 'margin-top': '0','font-size': '24px','font-family': 'Open Sans', 'fontWeight': 'semi bold'}),
                html.Div([
                    html.H1("원하시는 ID를 선택하세요.", style={'font-size': '22px', 'font-family': 'Open Sans','fontWeight': 'normal' , 'margin-left': '50px','margin-top': '40px'}),
                    dcc.Dropdown(
                        id='dropdown1',
                        options=[{'label': user, 'value': user} for user in user_id],
                        value='ALL',
                        style={'width': '50%', 'margin-left': 'auto'}
                    ),
                    dcc.DatePickerRange(
                        id='date-picker-range1',
                        start_date='2023-01-01',  # 기본 시작 날짜
                        end_date='2023-12-31',  # 기본 종료 날짜
                        display_format='YYYY-MM-DD',  # 표시 형식 설정
                        style={'width': '50%', 'margin-left': '75%'}
                    ),
                ]),
                dcc.Graph(id='graph1', style={'margin': 'auto', 'display': 'block', 'height': '60vh'}),
            ],
            style={'width': '70%', 'margin': 'auto', 'border': '1px solid #ccc', 'border-radius': '10px'}
        ),
        html.Div(
            children=[
                html.H2("모든 유저 사용 단어 순위", style={'textAlign': 'center', 'padding': '15px', 'background-color': '#ccc', 'color': 'black', 'border-radius': '10px 10px 0 0', 'margin-top': '0','font-size': '24px','font-family': 'Open Sans', 'fontWeight': 'semi bold'}),
                html.Div([
                    html.H1("원하시는 형태소를 선택해주세요.", style={'font-size': '22px', 'font-family': 'Open Sans','fontWeight': 'normal' , 'margin-left': '50px','margin-top': '40px'}),
                    dcc.Dropdown(
                        id='dropdown2',
                        options=[
                            {'label': morphs_type[field], 'value': field} for field in morphs_type
                        ],
                        value='ALL',
                        style={'width': '50%', 'margin-left': 'auto'}
                    ),
                    dcc.DatePickerRange(
                        id='date-picker-range2',
                        start_date='2023-01-01',  # 기본 시작 날짜
                        end_date='2023-12-31',  # 기본 종료 날짜
                        display_format='YYYY-MM-DD',  # 표시 형식 설정
                        style={'width': '50%', 'margin-left': '75%'}
                    ),
                ]),
                dcc.Graph(id='graph2', style={'margin': 'auto', 'display': 'block', 'height': '60vh'}),
            ],
            style={'width': '70%', 'margin': 'auto', 'border': '1px solid #ccc', 'border-radius': '10px'}
        ),
        html.Div(
            children=[
                html.H2("유저별 사용 단어 순위", style={'textAlign': 'center', 'padding': '15px', 'background-color': '#ccc', 'color': 'black', 'border-radius': '10px 10px 0 0', 'margin-top': '0','font-size': '24px','font-family': 'Open Sans', 'fontWeight': 'semi bold'}),
                html.Div([
                    html.H1("원하시는 ID와 형태소를 선택해주세요.", style={'font-size': '22px', 'font-family': 'Open Sans','fontWeight': 'normal' , 'margin-left': '50px', 'margin-top': '40px' }),
                    dcc.Dropdown(
                        id='dropdown3-1',
                        options=[
                            {'label': field, 'value': field} for field in user_id[1:]
                        ],
                        value='to.gangnang',
                        style={'width': '50%', 'margin-left': 'auto'}
                    ),
                    dcc.Dropdown(
                        id='dropdown3-2',
                        options=[
                            {'label': morphs_type[field], 'value': field} for field in morphs_type
                        ],
                        value='ALL',
                        style={'width': '50%', 'margin-left': 'auto'}
                    ),
                    dcc.DatePickerRange(
                        id='date-picker-range3',
                        start_date='2023-01-01',  # 기본 시작 날짜
                        end_date='2023-12-31',  # 기본 종료 날짜
                        display_format='YYYY-MM-DD',  # 표시 형식 설정
                        style={'width': '50%', 'margin-left': '75%'}
                    ),
                ]),
                dcc.Graph(id='graph3', style={'margin': 'auto', 'display': 'block', 'height': '60vh'}),
            ],
            style={'width': '70%', 'margin': 'auto', 'border': '1px solid #ccc', 'border-radius': '10px', 'margin-top': '100px'}
        ),
        html.Div(
    children=[
        html.Div(
            children=[
                html.H2("워드클라우드 & 상위(%)차트", style={'textAlign': 'center', 'padding': '15px', 'background-color': '#ccc', 'color': 'black', 'border-radius': '10px 10px 0 0', 'margin-top': '0','font-size': '24px','font-family': 'Open Sans', 'fontWeight': 'semi bold'}),
                html.Div(
                    children=[
                        dcc.Dropdown(
                        id='dropdown4-1',
                        options=[
                            {'label': morphs_type[field], 'value': field} for field in morphs_type
                        ],
                        value='ALL',
                        style={'width': '70%', 'margin-left': 'auto'}
                    ),
                        dcc.DatePickerRange(
                        id='date-picker-range4',
                        start_date='2023-01-01',  # 기본 시작 날짜
                        end_date='2023-12-31',  # 기본 종료 날짜
                        display_format='YYYY-MM-DD',  # 표시 형식 설정
                        style={'width': '50%', 'margin-left': '51%'}
                    ),

                        # html.H2("Vertical Bar Chart", style={'textAlign': 'center'}),
                        dcc.Graph(id='graph4', style={'height': '600px'}),
                    ],
                    style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}
                ),
                html.Div(
                    children=[
                        dcc.Dropdown(
                        id='dropdown4-2',
                        options= [
                            '50', '30', '10'
                        ],
                        value='50',
                        style={'width': '50%', 'margin-left': 'auto'}
                    ),
                        # html.H2("Word Cloud", style={'textAlign': 'center'}),
                        html.Img(id='wordcloud', style={'width': '100%', 'height': '100%'})
                    ],
                    style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}
                ),
            ],
            style={'width': '70%', 'margin': 'auto', 'border': '1px solid #ccc', 'border-radius': '10px','margin-top': '100px'}
        ),
    ]
)
    ]
)

#1.형태소별 비율 콜백 함수 정의

@app.callback(
    Output('graph1', 'figure'),
    [Input('dropdown1', 'value'),
     Input('date-picker-range1', 'start_date'),
     Input('date-picker-range1', 'end_date')]
)
def update_graph(selected_user, start_date, end_date):
    data = load_data()

    data = filter_data_by_date(data, start_date, end_date)

    if not data:
        # Handle empty data or invalid date range
        return px.bar()  # Or return an empty figure or an error message

    if selected_user == "ALL":
        data = data
    else:
        data = [item for item in data if item.get('user_name') == selected_user]

    # 품사별 단어 수 계산
    word_counts = {}
    total_count = 0
    for entry in data:
        for pos, words in entry.items():
            if pos in morphs_type:
                for word in words:
                    word_counts[pos] = word_counts.get(pos, 0) + 1
                    total_count += 1

    # 각 품사별 비율 계산
    pos_ratios = {}
    for pos, count in word_counts.items():
        ratio = count / total_count
        pos_ratios[pos] = ratio

    # 원형 그래프 생성
    labels = [f"{morphs_type[key]}: {round(value*100, 2)}% ({word_counts[key]}개)" for key, value in pos_ratios.items()]
    values = list(pos_ratios.values())
    text = [f"{round(value*100, 2)}%, {word_counts[key]}개" for key, value in pos_ratios.items()]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, text=text, textinfo='text')])

    fig.update_layout(
        title=f'{selected_user} 발화 형태소 비율',
        showlegend=True,
    )

    return fig


#2.전체 형태소 콜백 함수 정의
@app.callback(
    Output('graph2', 'figure'),
    [Input('dropdown2', 'value'),
     Input('date-picker-range2', 'start_date'),
     Input('date-picker-range2', 'end_date')]
)
def update_graph(selected_pos, start_date, end_date):
    data = load_data()

    data = filter_data_by_date(data, start_date, end_date)

    if not data:
        return px.bar()

    # 품사별 단어 수 계산
    word_counts = {}
    for entry in data:
        if "ALL" == selected_pos:
            for pos in keys_list:
                for word in entry.get(pos, []):
                    word_counts[word] = word_counts.get(word, 0) + 1
        else:
            for word in entry.get(selected_pos, []):
                word_counts[word] = word_counts.get(word, 0) + 1

    # 내림차순으로 정렬
    sorted_word_counts = dict(sorted(word_counts.items(), key=lambda item: item[1], reverse=True))

    # Plotly Express를 사용하여 막대 차트 생성
    fig = px.bar(
        x=list(sorted_word_counts.keys()),
        y=list(sorted_word_counts.values()),
        labels={'x': 'Word', 'y': 'Count'},
        title=f'{morphs_type[selected_pos]} 단어 사용 순위',
    )

    fig.update_xaxes(range=[0, 20])
    fig.update_yaxes(range=[0, max(list(sorted_word_counts.values())[:20])])

    return fig

#3.유저별 형태소 콜백 함수 정의
@app.callback(
    Output('graph3', 'figure'),
    [Input('dropdown3-1', 'value'),
     Input('dropdown3-2', 'value'),
     Input('date-picker-range3', 'start_date'),
     Input('date-picker-range3', 'end_date')]
)
def update_graph(selected_user, selected_pos, start_date, end_date):
    data = load_data()

    data = [item for item in data if item.get('user_name') == selected_user]

    data = filter_data_by_date(data, start_date, end_date)

    if not data:
        return px.bar()

    # 품사별 단어 수 계산
    word_counts = {}
    for entry in data:
        if "ALL" == selected_pos:
            for pos in keys_list:
                for word in entry.get(pos, []):
                    word_counts[word] = word_counts.get(word, 0) + 1
        else:
            for word in entry.get(selected_pos, []):
                word_counts[word] = word_counts.get(word, 0) + 1

    # 내림차순으로 정렬
    sorted_word_counts = dict(sorted(word_counts.items(), key=lambda item: item[1], reverse=True))


    # Plotly Express를 사용하여 막대 차트 생성
    fig = px.bar(
        x=list(sorted_word_counts.keys()),
        y=list(sorted_word_counts.values()),
        labels={'x': 'Word', 'y': 'Count'},
        title=f'{selected_user} : {morphs_type[selected_pos]} 단어 사용 순위',
    )

    fig.update_xaxes(range=[0, 20])
    fig.update_yaxes(range=[0, max(list(sorted_word_counts.values())[:20])])

    return fig

#4.워드클라우드 콜백 함수 정의
@app.callback(
    [Output('graph4', 'figure'),
     Output('wordcloud', 'src')],
    [Input('date-picker-range4', 'start_date'),
     Input('date-picker-range4', 'end_date'),
     Input('dropdown4-1', 'value'),
     Input('dropdown4-2', 'value')]
)
def update_graph(start_date, end_date, selected_pos, selected_percent):
    data = load_data()

    data = filter_data_by_date(data, start_date, end_date)

    if not data:
        empty_fig = px.bar()  # 빈 막대 차트 생성
        empty_wordcloud = generate_empty_wordcloud()  # 빈 워드클라우드 생성
        return empty_fig, empty_wordcloud

    # 품사별 단어 수 계산
    word_counts = {}
    for entry in data:
        if "ALL" == selected_pos:
            for pos in keys_list:
                for word in entry.get(pos, []):
                    word_counts[word] = word_counts.get(word, 0) + 1
        else:
            for word in entry.get(selected_pos, []):
                word_counts[word] = word_counts.get(word, 0) + 1

    # 내림차순으로 정렬
    sorted_word_counts = dict(sorted(word_counts.items(), key=lambda item: item[1], reverse=True))

    # 퍼센트를 값으로 변환
    percent_value = int(selected_percent)
    total_entries = len(word_counts)
    selected_entries = int((percent_value / 100) * total_entries)

    top_keys = list(sorted(word_counts.items(), key=lambda item: item[1], reverse=True))[:selected_entries]
    # 상위 퍼센트의 데이터만 선택
    top_entries = {k: word_counts[k] for k, v in top_keys}

    # Plotly Express를 사용하여 막대 차트 생성
    fig = px.bar(
        x=list(top_entries.values()),
        y=list(top_entries.keys()),
        labels={},
        orientation='h',  # 수평 막대 차트로 설정
    )

    # WordCloud 생성
    wordcloud = WordCloud(
        width=300,
        height=300,
        background_color='black',
        contour_color='black',
        font_path=font_path,
        mask=instagram_logo,
        repeat=False
    )

    fig.update_layout(xaxis_title=None, yaxis_title=None, yaxis_categoryorder='total ascending')

    # 중복 제거한 리스트를 그대로 사용하여 WordCloud에 텍스트 데이터 추가
    text_data_list = [f"{word} " * count for word, count in top_keys]

    # 빈도수를 반영하여 중복 제거한 리스트 생성
    unique_text_data_list = []
    for word, count in top_keys:
        unique_text_data_list.extend([word])

    all_word = Counter(unique_text_data_list)

    # WordCloud에 텍스트 데이터 추가
    wordcloud.generate_from_frequencies(dict(all_word))



    # 워드 클라우드 이미지 생성
    image = wordcloud.to_image()

    # Resize the image using PIL
    resized_image = image.resize((600, 600))  # Adjust the size as needed

    # Convert the resized image to base64 for display
    buffered = BytesIO()
    resized_image.save(buffered, format="PNG")
    encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return fig, f"data:image/png;base64,{encoded_image}"

# 애플리케이션 실행
if __name__ == '__main__':
    app.run_server(debug=True, host= '0.0.0.0', port=8061)