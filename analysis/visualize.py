import folium
import json

def visualize_gu(df):
    # 서울 중심 좌표
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=12, tiles=None)

    # geojson 파일 불러오기
    with open('./서울특별시_행정구별.geojson', encoding='utf-8') as f:
        seoul_geo = json.load(f)

    # Choropleth Map
    folium.Choropleth(
        geo_data=seoul_geo,
        data=df,
        columns=['구','적발건수' if '적발건수' in df.columns else '사고건수'],
        key_on='feature.properties.sggnm',  # GeoJSON에서 구 이름 필드
        fill_color='OrRd',
        fill_opacity=0.7,
        line_opacity=0.5,
        legend_name=f'{df['발생년월'].iloc[0] if '발생년월' in df.columns else None} 서울 사고 건수'
    ).add_to(m)
        # 시군구 이름 표시 (툴팁)
    folium.GeoJson(
        seoul_geo,
        name='구',
        tooltip=folium.GeoJsonTooltip(fields=['sggnm'], aliases=['행정구:']),
        style_function=lambda feature: {
        'fillOpacity': 0,
        'color': 'black',
        'weight': 0.5
    },
    ).add_to(m)

    return m


def visualize_dong(df):
    # 서울 중심 좌표
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=12, tiles=None)

    # geojson 파일 불러오기
    with open('./서울특별시_행정동별.geojson', encoding='utf-8') as f:
        seoul_geo = json.load(f)

    # Choropleth Map
    folium.Choropleth(
        geo_data=seoul_geo,
        data=df,
        columns=['시군구','적발건수' if '적발건수' in df.columns else '사고건수'],
        key_on='feature.properties.adm_nm',  # GeoJSON에서 구 이름 필드
        fill_color='OrRd',
        fill_opacity=0.7,
        line_opacity=0.5,
        legend_name=f'{df['발생년월'].iloc[0] if '발생년월' in df.columns else None} 서울 사고 건수'
    ).add_to(m)
        # 시군구 이름 표시 (툴팁)
    folium.GeoJson(
        seoul_geo,
        name='시군구',
        tooltip=folium.GeoJsonTooltip(fields=['adm_nm'], aliases=['행정동:']),
        style_function=lambda feature: {
        'fillOpacity': 0,
        'color': 'black',
        'weight': 0.5
    },
    ).add_to(m)

    return m