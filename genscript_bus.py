import streamlit as st
import json
from streamlit.components.v1 import html

# 高德地图API密钥（需替换为实际密钥）
AMAP_KEY = "YOUR_AMAP_API_KEY"

# 线路数据（示例）
lines_data = {
    "线路1": {
        "stations": [
            {"name": "南京金斯瑞", "lng": 118.91721, "lat": 31.932633,
             "photo": "https://pic.ltywl.top/mn/api.php"},
            {"name": "南京南站", "lng": 118.798034, "lat": 31.968763,
             "photo": "https://pic.ltywl.top/mn/api.php"},
            {"name": "江苏金斯瑞", "lng": 119.518992, "lat": 32.153292,
             "photo": "https://pic.ltywl.top/mn/api.php"}
        ],
        "path": [
            [118.91721, 31.932633],
            [118.798034, 31.968763],
            [119.518992, 32.153292]
        ]
    },
    "线路2": {
        "stations": [
            {"name": "站点D", "lng": 116.387428, "lat": 39.89923,
             "photo": "https://pic.ltywl.top/mn/api.php"},
            {"name": "站点E", "lng": 116.427428, "lat": 39.93923,
             "photo": "https://pic.ltywl.top/mn/api.php"}
        ],
        "path": [
            [116.387428, 39.89923],
            [116.427428, 39.93923]
        ]
    }
}


# 生成高德地图HTML
def generate_amap_html(line_data):
    stations = line_data["stations"]
    path = line_data["path"]

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>金斯瑞班车线路图</title>
        <link rel="stylesheet" href="https://cache.amap.com/lbs/static/main1119.css"/>
        <script src="https://webapi.amap.com/maps?v=1.4.15&key={AMAP_KEY}"></script>
        <script type="text/javascript" src="https://cache.amap.com/lbs/static/addToolbar.js"></script>
        <style>
            #container {{
                width: 100%;
                height: 600px;
            }}
            .info-content {{
                min-width: 200px;
                max-width: 300px;
            }}
            .info-image {{
                width: 100%;
                height: auto;
                max-height: 200px;
                object-fit: contain;
                margin: 10px 0;
                border-radius: 4px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            }}
            .info-title {{
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 5px;
                color: #333;
            }}
            .info-wrapper {{
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            @media (max-width: 480px) {{
                .info-content {{
                    max-width: 200px;
                }}
                .info-image {{
                    max-height: 150px;
                }}
            }}
        </style>
    </head>
    <body>
        <div id="container"></div>
        <script>
            var map = new AMap.Map('container', {{
                resizeEnable: true,
                zoom: 13
            }});

            // 创建带箭头的线路
            var polyline = new AMap.Polyline({{
                path: {json.dumps(path)},
                isOutline: true,
                outlineColor: '#ffeeff',
                borderWeight: 1,
                strokeColor: "#3366FF", 
                strokeOpacity: 1,
                strokeWeight: 6,
                strokeStyle: "solid",
                showDir: true,
                dirColor: 'red',
                zIndex: 50,
            }});
            polyline.setMap(map);

            // 设置地图视野
            map.setFitView();

            // 添加站点标记
            var stations = {json.dumps(stations)};
            var infoWindow = new AMap.InfoWindow({{
                offset: new AMap.Pixel(0, -30),
                isCustom: true,  // 使用自定义信息窗口
                autoMove: true,  // 自动调整位置
                closeWhenClickMap: true  // 点击地图关闭窗口
            }});

            for (var i = 0; i < stations.length; i++) {{
                var station = stations[i];

                // 创建自定义标记图标
                var marker = new AMap.Marker({{
                    position: [station.lng, station.lat],
                    title: station.name,
                    content: '<div style="background-color: #3366FF; ' +
                             'width: 24px; height: 24px; ' +
                             'border-radius: 50%; ' +
                             'text-align: center; ' +
                             'line-height: 24px; ' +
                             'color: white;">' + (i+1) + '</div>',
                    offset: new AMap.Pixel(-12, -12)
                }});

                marker.on('click', function(e) {{
                    var stationData = e.target.getExtData();
                    var content = `
                    <div class="info-content">
                        <div class="info-wrapper">
                            <div class="info-title">${{stationData.name}}</div>
                            <img class="info-image" src="${{stationData.photo}}" 
                                 alt="${{stationData.name}}站点照片"
                                 onerror="this.src='https://placehold.co/200x150?text=图片加载失败'">
                        </div>
                    </div>`;
                    infoWindow.setContent(content);
                    infoWindow.open(map, e.target.getPosition());
                }});

                // 将站点数据附加到标记对象
                marker.setExtData(station);
                marker.setMap(map);
            }}
        </script>
    </body>
    </html>
    """
    return html_content


# Streamlit应用
st.title("🚗金斯瑞班车线路图")
st.subheader("请选择需要查看的线路，点击站点查看详细信息")

# 线路选择
selected_line = st.selectbox("选择线路", list(lines_data.keys()))

# 显示地图
if selected_line:
    st.write(f"当前选择: **{selected_line}**")
    line_data = lines_data[selected_line]
    amap_html = generate_amap_html(line_data)
    html(amap_html, height=600)

    # 显示站点列表
    st.subheader("站点列表")
    cols = st.columns(2)  # 创建两列布局

    for i, station in enumerate(line_data["stations"]):
        # 交替在左右列显示
        with cols[i % 2]:
            st.markdown(f"**{i + 1}. {station['name']}**")
            st.image(
                station["photo"],
                caption=f"{station['name']}站点照片",
                use_container_width=True,  # 关键修复：使用新参数替代use_column_width
                output_format="PNG"
            )
else:
    st.warning("请选择一条线路")