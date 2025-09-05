# Import libraries
import streamlit as st
import pandas as pd 
import plotly.graph_objects as go

df = pd.DataFrame({
    'case_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'time_remain': [500, 600, 450, 700, 550, 800, 650, 900, 750, 600]
})

st.markdown('# Gráfico de Gantt')

current_time = st.slider('Posição atual do tempo (horas)', 0, max(df['time_remain']), 0)

df_selected = df.copy()

fig = go.Figure()

for i, row in df_selected.iterrows():
    completed = min(current_time, row['time_remain'])
    if completed > 0:
        fig.add_trace(go.Bar(
            y = [f'Case {row["case_id"]}'],
            x = [completed],
            orientation='h',
            marker_color='#2ECC71',
            hoverinfo='text',
            hovertext=(
                f'<b>Case {row["case_id"]}</b><br>'
                f'Concluído: {completed} horas<br>'
                f'Restante: {max(0, row["time_remain"] - current_time)} horas<br>'
                f'Total: {row["time_remain"]} horas'
            ),
            showlegend=False,
            name=f'Completed {row["case_id"]}'
        ))

for i, row in df_selected.iterrows():
    fig.add_trace(go.Bar(
        y = [f'Case {row["case_id"]}'],
        x = [row['time_remain']],
        orientation='h',
        marker_color='lightgray',
        opacity=0.3,
        hoverinfo='skip',
        showlegend=False,
        name=f'Total {row["case_id"]}'
    ))

for i, row in df_selected.iterrows():
    fig.add_shape(
        type='line',
        x0 = current_time, y0=i-0.4,
        x1 = current_time, y1=i+0.4,
        line = dict(color='red', width=3),
        name='Current Time'
    )

fig.update_layout(
    title=f'Progresso no tempo: {current_time} horas',
    xaxis_title='Horas',
    yaxis_title='Casos',
    height=500,
    width=800,
    bargap=0.3,
    hovermode='closest',
    barmode='overlay'
)

fig.add_annotation(
    x = 0.5,
    y = 1.05,
    xref='paper',
    yref='paper',
    text='🟩 Concluído | 🔴 Tempo Atual | ⬜ Restante',
    showarrow=False,
    font=dict(size=12)
)

st.plotly_chart(fig)

st.write('**Progresso individual:**')
for _, row in df_selected.iterrows():
    completed = min(current_time, row['time_remain'])
    remaining = max(0, row['time_remain'] - current_time)
    percentage = (completed / row['time_remain'] * 100) if row['time_remain'] > 0 else 0
    
    progress_bar = st.progress(percentage/100)
    st.caption(f"Case {row['case_id']} - Concluído:{completed}h | Restante:{remaining}h ({percentage:.1f}% completo)")