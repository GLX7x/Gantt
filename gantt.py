import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import matplotlib.colors as mcolors

st.markdown('# Gráfico de Gantt')

df = pd.read_csv('Insurance_claims_event_log.csv')
df = df.rename(columns={'activity_name': 'activity'})
selected_cases = df['case_id'].unique()[:10]
df = df[df['case_id'].isin(selected_cases)]
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values(by=['case_id', 'timestamp'])

last_event_per_case = df.groupby('case_id')['timestamp'].transform('max')
df['time_remain'] = (last_event_per_case - df['timestamp']).dt.total_seconds()/3600 # em horas

for case in selected_cases:
    df_case = df[df['case_id'] == case].copy()
    df_case = df_case.reset_index(drop=True)
    print(df_case)
    fig, ax = plt.subplots(figsize=(10, 6))

    activities = df_case['activity'].tolist()
    activities_reversed = list(reversed(activities))

    for i in range(len(df_case)):
        y_pos = len(activities) - i - 1
        duration = df_case['time_remain'].iloc[i]

        ax.barh(y_pos, width=duration, left=0, alpha=0.7, edgecolor='black', label=df_case['activity'].iloc[i])
    ax.set_yticks(range(len(activities)))
    ax.set_yticklabels(activities_reversed)
    ax.set_xlabel('Tempo restante (h)')
    ax.set_title(f'Case {case} - Gráfico de Gantt (Tempo remanescente)')
    ax.grid(axis='x', alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)