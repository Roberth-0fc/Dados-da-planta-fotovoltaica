import io
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(page_title="Monitoramento Fotovoltaico", page_icon="☀️", layout="wide")

# Estilização CSS Flexível (Modo Claro/Escuro)
st.markdown("""
    <style>
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    .stAlert {
        border-radius: 8px;
    }
    .explanation-box {
        background-color: rgba(41, 128, 185, 0.08);
        border-left: 4px solid #2980B9;
        padding: 12px 15px;
        border-radius: 6px;
        margin-bottom: 15px;
        font-size: 0.95rem;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_and_clean_data(file_bytes: bytes, file_name: str):
    """Lê, normaliza e prepara os dados da planilha enviada."""
    try:
        buffer = io.BytesIO(file_bytes)
        nome = file_name.lower()

        if nome.endswith('.csv'):
            # Primeiro tenta o padrão mais comum em planilhas brasileiras.
            df = pd.read_csv(
                buffer,
                sep=';',
                decimal=',',
                encoding='utf-8-sig'
            )

            # Se tudo veio em uma coluna, tenta CSV separado por vírgula.
            if len(df.columns) == 1:
                buffer.seek(0)
                df = pd.read_csv(
                    buffer,
                    sep=',',
                    decimal='.',
                    encoding='utf-8-sig'
                )
        else:
            df = pd.read_excel(buffer)

        if df.empty:
            st.error("A planilha foi lida, mas não contém linhas de dados.")
            return None, None

        # Localiza a primeira coluna que aparenta conter data/hora.
        col_data = [
            col for col in df.columns
            if any(termo in str(col).lower() for termo in ('data', 'hora', 'date', 'time'))
        ]
        if not col_data:
            st.error("Não foi possível identificar a coluna de Data e Hora.")
            return None, None

        data_col = col_data[0]
        try:
            df[data_col] = pd.to_datetime(
                df[data_col], dayfirst=True, format='mixed', errors='coerce'
            )
        except (TypeError, ValueError):
            # Compatibilidade com versões de pandas que não aceitam format='mixed'.
            df[data_col] = pd.to_datetime(
                df[data_col], dayfirst=True, errors='coerce'
            )

        df = (
            df.dropna(subset=[data_col])
              .sort_values(by=data_col)
              .reset_index(drop=True)
        )
        if df.empty:
            st.error("Nenhuma data/hora válida foi encontrada na planilha.")
            return None, None

        # Componentes de data usados nos filtros e agrupamentos.
        df['Ano_Num'] = df[data_col].dt.year
        df['Mes_Num'] = df[data_col].dt.month
        df['Dia_Data'] = df[data_col].dt.date
