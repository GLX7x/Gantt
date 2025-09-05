# Project Management App

Este é um aplicativo desenvolvido em **Python** utilizando Streamlit.  
O app faz uso de logs de eventos, gráficos de Gantt e templates visuais para auxiliar na análise de processos.

---

## Estrutura de Arquivos

Todos os arquivos devem estar na **mesma pasta** para que o aplicativo funcione corretamente
- project_management_app.py # Código principal do aplicativo (Streamlit)
- Insurance_claims_event_log.csv # Dataset de exemplo (event log)
- template.png # Imagem usada como template
- gantt.png # Imagem do gráfico de Gantt como logo

## Requisitos

- Bibliotecas necessárias:
```bash
pip install streamlit streamlit-aggrid pandas plotly pillow

```

## Como executar
1. Baixe os arquivos.
2. Certifique-se de que os 4 arquivos estão na mesma pasta.
3. No terminal, navegue até a pasta e execute:
```bash
streamlit run project_management_app.py

```
