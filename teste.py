# Import libraries
from st_aggrid import AgGrid
import streamlit as st
import pandas as pd 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
import io 

# Create de sidebar
st.set_page_config(layout='wide')

logo = Image.open(r'gantt.png')
st.sidebar.image(logo, width=120)

# Create the main interface — Section 1
with st.sidebar.expander('Sobre o app'):
    st.write('''
             Este é um app que mostra o gráfico de Gantt para o tempo remanescente das atividades de cada caso
             ''')
    
st.markdown('''<style> .font {
            font-size:30px ; font-family: 'Cooper Black'; color: #FF9633;}
            </style> ''', unsafe_allow_html=True)
st.markdown('<p class="font">Gráfico de Gantt - Tempo Remanescente por Caso</p>', unsafe_allow_html=True)

# Create the main interface — Section 2
st.subheader('Passo 2: Carregue seus dados e selecione os casos')

uploaded_file = st.file_uploader('Faça o upload do arquivo CSV com os dados dos casos', type=['csv'])
if uploaded_file is not None:
    tasks = pd.read_csv(uploaded_file)

    grid_response = AgGrid(
        tasks,
        editable=True,
        height=300,
        width='100%',
    )
    
    updated = grid_response['data']
    df = pd.DataFrame(updated)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Calcular tempo remanescente
    max_time_per_case = df.groupby('case_id')['timestamp'].transform('max')
    df['time_remain'] = (max_time_per_case - df['timestamp']).dt.total_seconds()/3600  # em horas
    
    # Selecionar casos para mostrar
    all_cases = df['case_id'].unique()
    selected_cases = st.multiselect(
        'Selecione os casos para visualizar:', 
        options=all_cases,
        default=all_cases[:3] if len(all_cases) > 3 else all_cases,
        help='Selecione os casos que deseja analisar'
    )
    
    if not selected_cases:
        st.warning('Por favor, selecione pelo menos um caso.')
    else:
        df_selected = df[df['case_id'].isin(selected_cases)]
        
        # Create the main interface — Section 3
        st.subheader('Passo 3: Gerar gráficos de Gantt por caso')
        
        if st.button('Gerar gráficos de Gantt'):
            for case in selected_cases:
                df_case = df_selected[df_selected['case_id'] == case].copy()
                df_case = df_case.sort_values('timestamp')
                
                st.markdown(f"---")
                st.markdown(f"### 📋 Caso: `{case}`")
                
                # Criar gráfico com Plotly
                fig = go.Figure()
                
                # Adicionar uma barra para cada atividade
                for i, row in df_case.iterrows():
                    fig.add_trace(go.Bar(
                        y=[row['activity_name']],
                        x=[row['time_remain']],
                        orientation='h',
                        name=row['activity_name'],
                        hovertemplate=(
                            f"<b>Atividade:</b> {row['activity_name']}<br>" +
                            f"<b>Tempo restante:</b> {row['time_remain']:.2f} horas<br>" +
                            f"<b>Timestamp:</b> {row['timestamp']}<br>" +
                            "<extra></extra>"
                        ),
                        showlegend=True
                    ))
                
                # Personalizar layout
                fig.update_layout(
                    title=f'Caso {case} - Tempo remanescente por atividade',
                    xaxis_title='Tempo remanescente (horas)',
                    yaxis_title='Atividades',
                    barmode='overlay',
                    height=400,
                    showlegend=True,
                    hovermode='closest'
                )
                
                # Ordenar atividades por timestamp (mais antiga no topo)
                fig.update_yaxes(autorange="reversed")
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Mostrar tabela com dados do caso
                with st.expander(f"📊 Ver dados detalhados do caso {case}"):
                    st.dataframe(
                        df_case[['activity_name', 'timestamp', 'time_remain']]
                        .sort_values('timestamp')
                        .style.format({
                            'time_remain': '{:.2f} horas',
                            'timestamp': lambda x: x.strftime('%Y-%m-%d %H:%M:%S')
                        })
                    )

else:
    st.warning('Você precisa carregar um arquivo do tipo CSV')