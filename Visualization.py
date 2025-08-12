import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.io as pio
import networkx as nx
import plotly.graph_objects as go
pio.templates.default = "simple_white"  # 其它可选 'plotly', 'ggplot2', 'seaborn', 'simple_white'


# 预设选项
field_to_csv = {
    "Information Retrieval": "./results/IR.csv",
    "Artificial Intelligence": "./results/AI.csv",
    "Machine Learning": "./results/ML.csv",
    "Natural Language Processing": "./results/NLP.csv",
    "Computer Vision": "./results/CV.csv",
}

st.logo("img/UoG_colour.png")
# 标志 + 标题

# 居中 logo + 标题
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("img/UoG_colour.png", width=300)
    st.title("Expert Search")

st.markdown("</div>", unsafe_allow_html=True)
st.caption("I want to find a PhD supervisor in...")

# 页面标题



# 搜索行（搜索框 + 搜索按钮）
col1, col2 = st.columns([ 4, 1])  # 搜索框占3份宽度，按钮占1份
with col1:
    
    selected_field = st.selectbox("I want to find a PhD supervisor in...", list(field_to_csv.keys()),label_visibility="collapsed")
with col2:
    
    search_clicked = st.button("Search")

# 搜索按钮
# 点击搜索后
db = pd.read_csv('./data/staff_paper_data.csv')
# 点击搜索后加载并展示专家卡片
if search_clicked:
    csv_file = field_to_csv[selected_field]

    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)

        if not df.empty:
            st.subheader(f"Experts in *{selected_field}*:")

            for i, row in df.head(5).iterrows():
                with st.container():
                    with st.expander(f"**#{i+1} {row['author_name']}**"):
                        tab1, tab2, tab3 = st.tabs([ "Publications", "Analytics","Network"])

                        with tab1:
                                author_pubs = db[db['author_name'] == row['author_name']][['year', 'title', 'type']]

                                
                                    # 按 type 排序（article 在前），再按 year 降序
                                type_order = {"article": 0, "conference_proceedings": 1}
                                author_pubs['type_order'] = author_pubs['type'].map(type_order).fillna(99)
                                author_pubs = author_pubs.sort_values(by=['type_order', 'year'], ascending=[True, False])

                                # 去掉排序辅助列 & 重置索引（隐藏原索引）
                                author_pubs = author_pubs.drop(columns=['type_order']).reset_index(drop=True)

                                # 显示表格
                                st.dataframe(author_pubs, use_container_width=True)

                        with tab2:
                            author_df = db[db['author_name'] == row['author_name']]

                            col1, col2 = st.columns(2)
                            col3, col4 = st.columns(2)

                            # 1. 论文年份趋势
                            yearly_counts = author_df.groupby('year').size().reset_index(name='count')
                            fig_year = px.line(yearly_counts, x='year', y='count', markers=True,
                                            title="Yearly Publication Trend")
                            col1.plotly_chart(fig_year, use_container_width=True)

                            # 2. 论文类型分布
                            if 'type' in author_df.columns:
                                fig_type = px.pie(author_df, names='type', hole=0.6,
                                                title="Publication Type Distribution")
                                col2.plotly_chart(fig_type, use_container_width=True)
                            else:
                                col2.write("No publication type data available")

                            # 3. 第几作者分布（水平条形图）
                            if 'author_position' in author_df.columns:
                                pos_counts = author_df['author_position'].value_counts().reset_index()
                                pos_counts.columns = ['author_position', 'count']

                                # 转成整数排序
                                pos_counts['author_position'] = pos_counts['author_position'].astype(int)
                                pos_counts = pos_counts.sort_values(by='author_position', ascending=False)

                                fig_pos = px.bar(pos_counts, x='count', y='author_position',
                                                orientation='h', title="Author Position Distribution")
                                col3.plotly_chart(fig_pos, use_container_width=True)
                            else:
                                col3.write("No author position data available")

                            # 4. CORE rank 分布（柱状图）
                            if 'core_rank' in author_df.columns and 'author_position' in author_df.columns:
                                core_order = ["A*", "A", "B", "C"]

                                # 转换成整数排序
                                author_df['author_position'] = author_df['author_position'].astype(int)

                                # 获取所有作者顺位并按数值排序
                                author_pos_order = sorted(author_df['author_position'].unique())

                                fig_core = px.histogram(
                                    author_df,
                                    x='core_rank',
                                    color='author_position',
                                    category_orders={
                                        "core_rank": core_order,
                                        "author_position": author_pos_order
                                    },
                                    barmode='group',
                                    title="CORE Rank by Author Position"
                                )

                                col4.plotly_chart(fig_core, use_container_width=True)
                            else:
                                col4.write("No CORE rank or author position data available")

                        with tab3:
                            
                            
                            # 筛选当前作者的所有合作数据
                            author_papers = db[db['author_name'] == row['author_name']]['paper_id'].unique()
                            coauthor_df = db[db['paper_id'].isin(author_papers)]

                            # 建立 NetworkX 图
                            G = nx.Graph()

                            # 添加节点和边
                            for paper_id in author_papers:
                                paper_authors = coauthor_df[coauthor_df['paper_id'] == paper_id]['author_name'].tolist()
                                for i in range(len(paper_authors)):
                                    for j in range(i + 1, len(paper_authors)):
                                        G.add_edge(paper_authors[i], paper_authors[j])

                            # 布局（spring_layout 会自动排布节点位置）
                            pos = nx.spring_layout(G, k=0.5, iterations=50,seed=42)  


                            # 节点坐标
                            node_x, node_y = [], []
                            for node in G.nodes():
                                x, y = pos[node]
                                node_x.append(x)
                                node_y.append(y)

                            # 节点颜色（当前作者红色，其余蓝色）
                            node_color = ["#FF6B6B" if node == row['author_name'] else "#AEC6CF" for node in G.nodes()]


                            # 边坐标
                            edge_x, edge_y = [], []
                            for edge in G.edges():
                                x0, y0 = pos[edge[0]]
                                x1, y1 = pos[edge[1]]
                                edge_x.extend([x0, x1, None])
                                edge_y.extend([y0, y1, None])

                            # 画边
                            edge_trace = go.Scatter(
                                x=edge_x, y=edge_y,
                                line=dict(width=1, color='gray'),
                                hoverinfo='none',
                                mode='lines'
                            )

                            # 画节点
                            node_trace = go.Scatter(
                                x=node_x, y=node_y,
                                mode='markers+text',
                                text=list(G.nodes()),
                                textposition="top center",
                                marker=dict(size=15, color=node_color, line_width=2)
                            )

                            # 生成图表
                            fig = go.Figure(data=[edge_trace, node_trace],
                                            layout=go.Layout(
                                                title="Co-author Network",
                                                title_x=0.5,
                                                showlegend=False,
                                                hovermode='closest',
                                                margin=dict(b=20, l=5, r=5, t=40)
                                            ))

                            # Streamlit 显示
                            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning(f"No data available in {csv_file}.")
    else:
        st.error(f"Data file '{csv_file}' not found.")
