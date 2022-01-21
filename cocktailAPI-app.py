import pandas as pd
import numpy as np
import requests
import json
import streamlit as st

st.title('カクテルサーチ')
st.write('265種類のカクテル情報を検索できます')
st.text('カクテルレシピ検索サイト「カクテルエフ・リカー」様のAPIを用いて情報を取得しています')
url = "https://cocktail-f.com/api/v1/cocktails";

bases = ['ジン','ウォッカ','テキーラ','ラム','ウイスキー','ブランデー','リキュール','ワイン','ビール','日本酒','ノンアルコール']
base_id = {'ジン':1, 'ウォッカ':2, 'テキーラ':3, 'ラム':4, 'ウイスキー':5, 'ブランデー':6, 'リキュール':7, 'ワイン':8, 'ビール':9, '日本酒':10, 'ノンアルコール':0}
select_base = base_id[st.sidebar.selectbox("ベースを選んでください", bases)]

techniques = ['ビルド','ステア','シェイク']
technique_id = {'ビルド':1, 'ステア':2, 'シェイク':3}
select_technique = technique_id[st.sidebar.selectbox("技法を選んでください", techniques)]


tastes = ['甘口','中甘口','中口','中辛口','辛口']
taste_id = {'甘口':1, '中甘口':2, '中口':3, '中辛口':4,'辛口':5}
select_taste = taste_id[st.sidebar.selectbox("テイストを選んでください",tastes)]

styles = ['ロング','ショート']
style_id = {'ショート':1, 'ロング':2}

if select_base != 0:
    select_style = style_id[st.sidebar.radio("スタイルを選んでください",styles)]
    alcohol_from, alcohol_to = st.sidebar.slider(
        label='アルコール度数',
        min_value=0,
        max_value=50,
        value=(5, 30),
        )
    st.sidebar.text(f'Selected: {alcohol_from}% ~ {alcohol_to}%')
else:
    alcohol_from=0
    alcohol_to=0
    select_style=2

param = {
    'base':select_base,
    'technique':select_technique,
    'taste':select_taste,
    'style':select_style,
    'alcohol_from':alcohol_from,
    'alcohol_to':alcohol_to
} 
res = requests.get(url, params=param).json()

cocktails = res["cocktails"]
# st.write(cocktails)
if not cocktails:
    st.info('条件に当てはまるカクテルが見つかりません!')

for cocktail in cocktails:
    cocktail_name = cocktail["cocktail_name"]
    cocktail_name_english = cocktail["cocktail_name_english"]
    cocktail_digest = cocktail["cocktail_digest"]
    cocktail_desc = cocktail["cocktail_desc"]
    recipe_desc = cocktail["recipe_desc"]
    recipes = cocktail["recipes"]
    alcohol = cocktail["alcohol"]
    top_name = cocktail["top_name"]
    with st.expander(cocktail_name):
        st.title(cocktail_name_english)
        st.subheader(cocktail_digest)
        st.write(cocktail_desc)
        col2, col3 = st.columns(2)
        col2.metric("ALCHOL", f"{alcohol}度")
        col3.metric("TOP", top_name)
        st.write("レシピ")
        for recipe in recipes:
            ingredient_name = recipe["ingredient_name"]
            amount = recipe["amount"]
            unit = recipe["unit"]
            col4, col5, = st.columns(2)
            col4.text(ingredient_name)
            if unit is None:
                col5.text(amount)
            else:
                col5.text(amount + unit)
        st.write(recipe_desc)
        st.text('カクテルレシピ検索サイト「カクテルエフ・リカー」(https://cocktail-f.com/api)より')

