import io
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(page_title="Monitoramento Fotovoltaico", page_icon="☀️", layout="wide")

def aplicar_estilo_interface(tema_visual: str):
    """Aplica uma identidade visual solar em tons suaves, sem depender do tema do navegador."""
    if tema_visual == "Claro suave":
        paleta = {
            "app_bg": "#E8EFE8",
            "sidebar_bg": "linear-gradient(180deg, #DDE9DF 0%, #E9F0E8 100%)",
            "panel": "#F5F8F2",
            "panel_alt": "#EDF3EB",
            "panel_hover": "#E4EEE5",
            "text": "#263B30",
            "muted": "#66786C",
            "border": "#D2DFD3",
            "accent": "#94B82F",
            "accent_2": "#23966B",
            "blue": "#4B9FC0",
            "shadow": "rgba(43, 75, 54, 0.10)",
            "grid": "#DCE6DC",
            "chart_paper": "#F5F8F2",
            "chart_plot": "#F0F5EE",
            "chart_text": "#30483A",
            "chart_hover": "#FFFFFF",
            "hero_bg": "linear-gradient(120deg, #DCEBDD 0%, #D6EAE3 54%, #F1EBCF 100%)",
            "hero_text": "#243B30",
            "hero_sub": "rgba(36, 59, 48, 0.82)",
            "hero_kicker_text": "#3D702F",
            "hero_kicker_bg": "rgba(255, 255, 255, 0.48)",
            "hero_orb": "rgba(80, 145, 70, 0.34)",
            "hero_sun": "#88A92B",
            "color_scheme": "light",
        }
    else:
        paleta = {
            "app_bg": "#182820",
            "sidebar_bg": "linear-gradient(180deg, #1B3027 0%, #20352B 100%)",
            "panel": "#22372D",
            "panel_alt": "#293F34",
            "panel_hover": "#304B3D",
            "text": "#ECF4EC",
            "muted": "#B0C2B4",
            "border": "#3C5948",
            "accent": "#D7EC55",
            "accent_2": "#39C58A",
            "blue": "#78C7E8",
            "shadow": "rgba(0, 0, 0, 0.22)",
            "grid": "#3A5144",
            "chart_paper": "#22372D",
            "chart_plot": "#1D3027",
            "chart_text": "#EAF3EB",
            "chart_hover": "#30473A",
            "hero_bg": "radial-gradient(circle at 86% 18%, rgba(215, 236, 85, 0.22), transparent 23%), radial-gradient(circle at 72% 110%, rgba(57, 197, 138, 0.22), transparent 34%), linear-gradient(115deg, #173D30 0%, #1D5642 48%, #264B3A 100%)",
            "hero_text": "#FFFFFF",
            "hero_sub": "rgba(244, 250, 242, 0.82)",
            "hero_kicker_text": "#E4F58C",
            "hero_kicker_bg": "rgba(8, 25, 18, 0.22)",
            "hero_orb": "rgba(229, 247, 124, 0.42)",
            "hero_sun": "#E9F77B",
            "color_scheme": "dark",
        }

    st.markdown(f"""
    <style>
    :root {{
        color-scheme: {paleta['color_scheme']};
        --fv-app-bg: {paleta['app_bg']};
        --fv-sidebar-bg: {paleta['sidebar_bg']};
        --fv-panel: {paleta['panel']};
        --fv-panel-alt: {paleta['panel_alt']};
        --fv-panel-hover: {paleta['panel_hover']};
        --fv-text: {paleta['text']};
        --fv-muted: {paleta['muted']};
        --fv-border: {paleta['border']};
        --fv-accent: {paleta['accent']};
        --fv-accent-2: {paleta['accent_2']};
        --fv-blue: {paleta['blue']};
        --fv-shadow: {paleta['shadow']};
        --fv-hero-bg: {paleta['hero_bg']};
        --fv-hero-text: {paleta['hero_text']};
        --fv-hero-sub: {paleta['hero_sub']};
        --fv-hero-kicker-text: {paleta['hero_kicker_text']};
        --fv-hero-kicker-bg: {paleta['hero_kicker_bg']};
        --fv-hero-orb: {paleta['hero_orb']};
        --fv-hero-sun: {paleta['hero_sun']};
    }}

    html, body, .stApp, [data-testid="stApp"],
    [data-testid="stAppViewContainer"], [data-testid="stMain"],
    [data-testid="stMainBlockContainer"], section.main {{
        background: var(--fv-app-bg) !important;
        color: var(--fv-text) !important;
    }}
    [data-testid="stHeader"] {{ background: transparent !important; }}
    [data-testid="stToolbar"] {{ background: transparent !important; }}
    .block-container {{
        max-width: 1660px;
        padding-top: 1.35rem;
        padding-bottom: 3rem;
    }}
    [data-testid="stSidebar"] {{
        background: {paleta['sidebar_bg']} !important;
        border-right: 1px solid var(--fv-border);
    }}
    [data-testid="stSidebar"] > div:first-child {{ background: transparent !important; }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {{ color: var(--fv-text) !important; }}

    h1, h2, h3, h4, p {{
        text-wrap: pretty;
    }}
    /* Keep compact controls and numeric badges on one line. */
    label, span, div {{
        overflow-wrap: normal;
        word-break: normal;
    }}
    h1, h2, h3, h4 {{ color: var(--fv-text) !important; }}
    h2 {{
        padding: 0.35rem 0 0.45rem 0.75rem;
        border-left: 4px solid var(--fv-accent-2);
        margin-top: 1rem;
    }}
    h3 {{ color: var(--fv-accent-2) !important; }}
    [data-testid="stCaptionContainer"], [data-testid="stWidgetLabel"] p {{ color: var(--fv-muted) !important; }}
    [data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {{ color: var(--fv-text); }}
    hr {{ border-color: var(--fv-border) !important; }}

    /* Cartões e indicadores */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: var(--fv-panel) !important;
        border: 1px solid var(--fv-border) !important;
        border-radius: 18px !important;
        box-shadow: 0 8px 24px var(--fv-shadow);
        overflow: hidden;
    }}
    [data-testid="stMetric"] {{
        min-height: 112px;
        padding: 15px 16px;
        border: 1px solid var(--fv-border);
        border-radius: 16px;
        background: linear-gradient(135deg, var(--fv-panel-alt), var(--fv-panel));
        box-shadow: 0 6px 18px var(--fv-shadow);
    }}
    [data-testid="stMetricLabel"] {{
        color: var(--fv-muted) !important;
        font-weight: 650 !important;
    }}
    [data-testid="stMetricValue"] {{
        color: var(--fv-accent-2) !important;
        font-size: 1.85rem !important;
        font-weight: 780 !important;
    }}
    [data-testid="stMetricDelta"] {{ font-weight: 600 !important; }}

    /* Campos de seleção, filtros e botões */
    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div,
    [data-baseweb="textarea"] > div,
    [data-testid="stDateInput"] input,
    [data-testid="stTextInput"] input,
    input, textarea {{
        background: var(--fv-panel) !important;
        color: var(--fv-text) !important;
        border-color: var(--fv-border) !important;
        border-radius: 10px !important;
    }}
    [data-baseweb="select"] span, [data-baseweb="select"] input,
    [data-baseweb="select"] svg {{ color: var(--fv-text) !important; fill: var(--fv-text) !important; }}
    [data-baseweb="popover"], [data-baseweb="menu"],
    [data-baseweb="popover"] ul {{
        background: var(--fv-panel) !important;
        color: var(--fv-text) !important;
        border-color: var(--fv-border) !important;
    }}
    [role="option"] {{ background: var(--fv-panel) !important; color: var(--fv-text) !important; }}
    [role="option"]:hover {{ background: var(--fv-panel-hover) !important; }}
    [data-baseweb="tag"] {{
        background: var(--fv-accent-2) !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
    }}
    button[kind="secondary"], button[kind="primary"] {{
        border-radius: 10px !important;
        border: 1px solid var(--fv-border) !important;
        transition: all 0.18s ease-in-out;
    }}
    button[kind="primary"] {{
        background: var(--fv-accent-2) !important;
        color: #FFFFFF !important;
    }}
    button[kind="secondary"] {{
        background: var(--fv-panel-alt) !important;
        color: var(--fv-text) !important;
    }}
    button:hover {{ filter: brightness(1.06); border-color: var(--fv-accent-2) !important; }}

    /* Abas, tabelas, alertas e gráficos */
    [data-baseweb="tab-list"] {{ gap: 8px; }}
    button[data-baseweb="tab"] {{
        background: var(--fv-panel-alt) !important;
        border-radius: 10px 10px 0 0 !important;
        color: var(--fv-muted) !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: var(--fv-accent-2) !important;
        border-bottom: 3px solid var(--fv-accent-2) !important;
    }}
    [data-testid="stDataFrame"], [data-testid="stTable"] {{
        border: 1px solid var(--fv-border);
        border-radius: 12px;
        overflow: hidden;
    }}
    [data-testid="stExpander"] {{
        background: var(--fv-panel);
        border: 1px solid var(--fv-border);
        border-radius: 14px;
    }}
    .stAlert {{ border-radius: 12px !important; }}
    [data-testid="stPlotlyChart"] {{
        background: var(--fv-panel);
        border: 1px solid var(--fv-border);
        border-radius: 16px;
        padding: 9px 10px 4px 10px;
        box-shadow: 0 7px 20px var(--fv-shadow);
    }}
    /* Plotly toolbar remains visible even when the pointer is away from the chart. */
    [data-testid="stPlotlyChart"] .modebar-container {{
        display: block !important;
        opacity: 1 !important;
        visibility: visible !important;
        top: 7px !important;
        right: 9px !important;
        z-index: 20 !important;
    }}
    [data-testid="stPlotlyChart"] .modebar {{
        opacity: 1 !important;
        visibility: visible !important;
        background: var(--fv-panel-alt) !important;
        border: 1px solid var(--fv-border) !important;
        border-radius: 10px !important;
        padding: 4px 6px !important;
        box-shadow: 0 3px 10px var(--fv-shadow) !important;
    }}
    [data-testid="stPlotlyChart"] .modebar-btn {{ opacity: 1 !important; color: var(--fv-text) !important; }}
    [data-testid="stPlotlyChart"] .modebar-btn svg,
    [data-testid="stPlotlyChart"] .modebar-btn path {{ fill: var(--fv-text) !important; }}
    [data-testid="stPlotlyChart"] .modebar-btn:hover {{ background: var(--fv-panel-hover) !important; }}

    /* Cabeçalho principal */
    .fv-hero {{
        position: relative;
        overflow: hidden;
        padding: 25px 30px 24px 30px;
        margin: 0 0 22px 0;
        border: 1px solid var(--fv-border);
        border-radius: 22px;
        background: var(--fv-hero-bg);
        box-shadow: 0 12px 30px var(--fv-shadow);
        color: #F4FAF2;
    }}
    .fv-hero-kicker {{
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 6px 11px;
        margin-bottom: 9px;
        border: 1px solid rgba(231, 248, 187, 0.32);
        border-radius: 30px;
        background: var(--fv-hero-kicker-bg);
        color: var(--fv-hero-kicker-text);
        font-size: 0.76rem;
        font-weight: 750;
        letter-spacing: 0.08em;
    }}
    .fv-hero h1 {{
        margin: 0 !important;
        color: var(--fv-hero-text) !important;
        font-size: clamp(1.7rem, 3vw, 2.45rem) !important;
        line-height: 1.12;
        letter-spacing: -0.035em;
    }}
    .fv-hero p {{
        max-width: 780px;
        margin: 9px 0 0 0;
        color: var(--fv-hero-sub) !important;
        font-size: 1rem;
    }}
    .fv-hero-orb {{
        position: absolute;
        right: 5%;
        top: 13%;
        width: 118px;
        height: 118px;
        border: 1px solid var(--fv-hero-orb);
        border-radius: 50%;
        box-shadow: 0 0 0 13px rgba(229, 247, 124, 0.055), 0 0 0 27px rgba(229, 247, 124, 0.035);
    }}
    .fv-hero-orb:after {{
        content: "☀";
        position: absolute;
        inset: 0;
        display: grid;
        place-items: center;
        color: var(--fv-hero-sun);
        font-size: 3.8rem;
        opacity: 0.9;
    }}
    .section-intro {{
        padding: 14px 17px;
        border-radius: 13px;
        background: linear-gradient(100deg, rgba(57, 197, 138, 0.13), rgba(120, 199, 232, 0.10));
        border: 1px solid var(--fv-border);
        border-left: 4px solid var(--fv-accent-2);
        color: var(--fv-text);
        margin: 5px 0 14px 0;
    }}
    .explanation-box {{
        background: linear-gradient(135deg, var(--fv-panel-alt), var(--fv-panel));
        border: 1px solid var(--fv-border);
        border-left: 4px solid var(--fv-blue);
        color: var(--fv-text);
        padding: 14px 17px;
        border-radius: 12px;
        margin-bottom: 15px;
        font-size: 0.95rem;
    }}
    .explanation-box h4 {{ color: var(--fv-accent-2) !important; }}
    .temperature-panel {{
        min-height: 172px;
        padding: 18px 19px;
        border-radius: 17px;
        background:
            radial-gradient(circle at 90% 15%, rgba(255, 211, 92, 0.22), transparent 28%),
            linear-gradient(120deg, rgba(50, 151, 185, 0.22), rgba(44, 170, 119, 0.17), rgba(231, 178, 64, 0.12)),
            var(--fv-panel);
        border: 1px solid var(--fv-border);
        box-shadow: 0 8px 21px var(--fv-shadow);
        margin: 8px 0 15px 0;
        color: var(--fv-text);
    }}
    .temperature-icon {{ font-size: 2.05rem; line-height: 1.2; }}
    .temperature-main {{ color: var(--fv-text); font-size: 1.28rem; font-weight: 780; margin-top: 3px; line-height: 1.35; }}
    .temperature-sub {{ color: var(--fv-muted); font-size: 0.86rem; }}
    .thermal-context {{
        padding: 13px 15px;
        margin-top: 9px;
        border-radius: 15px;
        background: linear-gradient(105deg, rgba(72, 157, 191, 0.15), rgba(61, 177, 126, 0.12), rgba(228, 183, 75, 0.14));
        border: 1px solid var(--fv-border);
    }}
    .sensitivity-badge {{
        margin-top: 26px;
        padding: 10px 12px;
        border-radius: 12px;
        background: linear-gradient(120deg, var(--fv-panel-alt), var(--fv-panel-hover));
        border: 1px solid var(--fv-border);
        color: var(--fv-accent-2);
        text-align: center;
        font-size: 1.05rem;
        font-weight: 800;
        white-space: nowrap;
        box-shadow: 0 4px 12px var(--fv-shadow);
    }}
    [data-testid="stSlider"] [role="slider"] {{
        border-color: var(--fv-accent-2) !important;
    }}

    @media (max-width: 760px) {{
        .block-container {{ padding-left: 1rem; padding-right: 1rem; }}
        .fv-hero {{ padding: 21px 19px; }}
        .fv-hero-orb {{ right: -28px; opacity: 0.45; }}
    }}
    </style>
    """, unsafe_allow_html=True)


def exibir_grafico(fig):
    """Padroniza somente a aparência dos gráficos; não altera dados ou séries."""
    tema_visual = st.session_state.get("tema_dashboard", "Escuro suave")
    if tema_visual == "Claro suave":
        papel, area, texto = "#F5F8F2", "#F0F5EE", "#30483A"
        grade, hover, template = "#DCE6DC", "#FFFFFF", "plotly_white"
    else:
        papel, area, texto = "#22372D", "#1D3027", "#EAF3EB"
        grade, hover, template = "#3A5144", "#30473A", "plotly_dark"

    fig.update_layout(
        template=template,
        paper_bgcolor=papel,
        plot_bgcolor=area,
        font=dict(family="Inter, Arial, sans-serif", color=texto, size=12),
        title_font=dict(color=texto, size=16),
        legend=dict(font=dict(color=texto), bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor=hover, font=dict(color=texto)),
        margin=dict(l=18, r=18, t=72, b=24),
    )
    fig.update_xaxes(
        gridcolor=grade,
        linecolor=grade,
        zerolinecolor=grade,
        tickfont=dict(color=texto),
        title_font=dict(color=texto),
    )
    fig.update_yaxes(
        gridcolor=grade,
        linecolor=grade,
        zerolinecolor=grade,
        tickfont=dict(color=texto),
        title_font=dict(color=texto),
    )
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "responsive": True,
            "modeBarButtonsToRemove": ["select2d", "lasso2d"],
        },
    )

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
        df['Hora_Tempo'] = df[data_col].dt.time
        df['Dia_Do_Mes'] = df[data_col].dt.day
        df['Ano_Mes_Sort'] = df[data_col].dt.to_period('M').dt.to_timestamp()

        df['Semestre_Num'] = df['Mes_Num'].apply(lambda mes: 1 if mes <= 6 else 2)
        df['Semestre_Nome'] = df['Semestre_Num'].astype(str) + 'º Semestre'

        meses_pt = {
            1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
            7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
        }
        df['Nome_Mes_Formatado'] = df['Mes_Num'].map(meses_pt).fillna('Indefinido')
        df['Ano_Mes_Texto'] = df['Nome_Mes_Formatado'] + '/' + df['Ano_Num'].astype(str)

        cols_reservadas = {
            data_col, 'Ano_Num', 'Mes_Num', 'Dia_Data', 'Hora_Tempo',
            'Dia_Do_Mes', 'Nome_Mes_Formatado', 'Semestre_Num',
            'Semestre_Nome', 'Ano_Mes_Sort', 'Ano_Mes_Texto'
        }

        # Converte as grandezas para números sem trocar espaços por pontos.
        for col in df.columns:
            if col in cols_reservadas or pd.api.types.is_numeric_dtype(df[col]):
                continue

            valores = df[col].astype('string').str.strip()
            valores = valores.str.replace('\u00a0', '', regex=False)
            valores = valores.str.replace(' ', '', regex=False)

            # Trata números no padrão brasileiro, por exemplo: 1.234,56.
            tem_virgula = valores.str.contains(',', na=False)
            valores.loc[tem_virgula] = (
                valores.loc[tem_virgula]
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
            )
            df[col] = pd.to_numeric(valores, errors='coerce')

        var_cols = [col for col in df.columns if col not in cols_reservadas]
        if not var_cols:
            st.error("Não encontrei colunas numéricas para gerar os indicadores e gráficos.")
            return None, None

        return df, data_col

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
        return None, None

def criar_grafico_base(df, x_col, y_col, titulo, tipo_grafico, cor='#2980B9'):
    if tipo_grafico == "Linhas":
        fig = px.line(df, x=x_col, y=y_col, title=titulo, color_discrete_sequence=[cor])
    elif tipo_grafico == "Colunas":
        fig = px.bar(df, x=x_col, y=y_col, title=titulo, color_discrete_sequence=[cor])
    elif tipo_grafico == "Pontos":
        fig = px.scatter(df, x=x_col, y=y_col, title=titulo, color_discrete_sequence=[cor])
    else:
        fig = px.line(df, x=x_col, y=y_col, markers=True, title=titulo, color_discrete_sequence=[cor])
    
    fig.update_layout(hovermode="x unified", margin=dict(l=15, r=15, t=35, b=15))
    return fig


def exibir_condicoes_termicas(df, variavel_y, irrad_col):
    """Mostra o contexto térmico ao lado dos indicadores gerais quando a variável é temperatura."""
    st.markdown(f"### 🌡️ Condições térmicas — {variavel_y}")
    st.caption(
        "Os símbolos de sol e nuvens representam as condições de irradiância medidas pela própria planta; "
        "não são uma previsão meteorológica."
    )

    dias_temperatura = sorted(df['Dia_Data'].dropna().unique())
    if not dias_temperatura:
        st.info("Não há datas disponíveis para contextualizar a temperatura.")
        return

    with st.container(border=True):
        dia_temperatura = st.selectbox(
            "Dia para contextualizar a temperatura:",
            options=dias_temperatura,
            index=len(dias_temperatura) - 1,
            format_func=lambda d: d.strftime('%d/%m/%Y'),
            key="dia_contexto_temperatura_topo"
        )

        df_temp_contexto = df[df['Dia_Data'] == dia_temperatura]
        serie_temp = df_temp_contexto[variavel_y].dropna()
        media_temp = serie_temp.mean() if not serie_temp.empty else None
        maxima_temp = serie_temp.max() if not serie_temp.empty else None

        irradiancia_media_dia = None
        if irrad_col:
            serie_irrad_luz = df_temp_contexto.loc[df_temp_contexto[irrad_col] >= 100, irrad_col].dropna()
            if not serie_irrad_luz.empty:
                irradiancia_media_dia = serie_irrad_luz.mean()

        if irradiancia_media_dia is not None:
            if irradiancia_media_dia >= 600:
                icone_ceu = "☀️"
                texto_ceu = "Irradiância elevada durante os períodos de luz"
            elif irradiancia_media_dia >= 250:
                icone_ceu = "⛅"
                texto_ceu = "Irradiância intermediária durante os períodos de luz"
            else:
                icone_ceu = "☁️"
                texto_ceu = "Irradiância reduzida durante os períodos de luz"
            texto_irrad = f"Irradiância média com luz: {irradiancia_media_dia:.1f} W/m²"
        else:
            icone_ceu = "🌤️"
            texto_ceu = "Sem irradiância suficiente para caracterizar visualmente o céu"
            texto_irrad = "Irradiância não disponível neste dia"

        t1, t2 = st.columns(2)
        with t1:
            valor_media = f"{media_temp:.1f} °C" if media_temp is not None else "N/D"
            st.markdown(
                f'<div class="temperature-panel"><div class="temperature-icon">🌡️</div>'
                f'<div class="temperature-sub">Temperatura média</div>'
                f'<div class="temperature-main">{valor_media}</div>'
                f'<div class="temperature-sub">{variavel_y}</div></div>',
                unsafe_allow_html=True
            )
        with t2:
            valor_max = f"{maxima_temp:.1f} °C" if maxima_temp is not None else "N/D"
            st.markdown(
                f'<div class="temperature-panel"><div class="temperature-icon">🔥</div>'
                f'<div class="temperature-sub">Temperatura máxima</div>'
                f'<div class="temperature-main">{valor_max}</div>'
                f'<div class="temperature-sub">{dia_temperatura.strftime("%d/%m/%Y")}</div></div>',
                unsafe_allow_html=True
            )

        st.markdown(
            f'<div class="thermal-context"><div class="temperature-icon">{icone_ceu}</div>'
            f'<div class="temperature-sub">Contexto de irradiância</div>'
            f'<div class="temperature-main">{texto_ceu}</div>'
            f'<div class="temperature-sub">{texto_irrad}</div></div>',
            unsafe_allow_html=True
        )


def main():
    # --- BARRA LATERAL ---
    st.sidebar.header("☀️ Central Solar")
    st.sidebar.caption(f"Aplicação: Streamlit {st.__version__}")
    tema_visual = st.sidebar.selectbox(
        "Aparência da interface",
        ["Escuro suave", "Claro suave"],
        index=0,
        key="tema_dashboard",
        help="Escolha uma paleta equilibrada. O tema altera também o fundo dos gráficos."
    )
    aplicar_estilo_interface(tema_visual)

    st.markdown(
        """
        <div class="fv-hero">
            <div class="fv-hero-orb"></div>
            <div class="fv-hero-kicker">☀ MONITORAMENTO • ENERGIA FOTOVOLTAICA</div>
            <h1>Painel de Análise da Planta Fotovoltaica</h1>
            <p>Acompanhe geração, condições ambientais e desempenho da planta com análises históricas e comparativas.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.divider()
    st.sidebar.header("📁 Importação de Dados")
    uploaded_file = st.sidebar.file_uploader("Carregue sua planilha (.csv, .xls, .xlsx)", type=['csv', 'xlsx', 'xls'])

    if uploaded_file is not None:
        with st.spinner("Carregando dados..."):
            df, col_data = load_and_clean_data(uploaded_file.getvalue(), uploaded_file.name)
            
        if df is not None:
            cols_reservadas = [col_data, 'Ano_Num', 'Mes_Num', 'Dia_Data', 'Hora_Tempo', 'Dia_Do_Mes', 
                               'Nome_Mes_Formatado', 'Semestre_Num', 'Semestre_Nome', 'Ano_Mes_Sort', 'Ano_Mes_Texto']
            var_cols = [c for c in df.columns if c not in cols_reservadas]

            st.sidebar.divider()
            st.sidebar.header("⚙️ Configurações Visuais")
            variavel_y = st.sidebar.selectbox("Variável Principal (Eixo Y):", var_cols)
            modo_exibicao = st.sidebar.radio("Layout dos Gráficos:", ["📊 Modo Grid (3 Simultâneos)", "🔍 Modo Foco (Ampliado)"])
            tipo_grafico = st.sidebar.selectbox("Estilo do Gráfico:", ["Pontos e Linhas", "Linhas", "Colunas", "Pontos"])

            # --- SAÚDE DOS DADOS ---
            total_celulas = df[var_cols].size
            celulas_vazias = df[var_cols].isnull().sum().sum()
            pct_saude = ((total_celulas - celulas_vazias) / total_celulas) * 100 if total_celulas > 0 else 100

            if celulas_vazias > 0:
                st.warning(f"⚠️ **Aviso de Integridade:** Foram identificadas **{celulas_vazias} células em branco/nulas** na planilha ({pct_saude:.1f}% de preenchimento). Os cálculos e gráficos tratam automaticamente essas lacunas sem travar o painel.")
            else:
                st.success("✅ **Qualidade dos Dados:** Planilha 100% preenchida (sem células em branco).")

            # --- INDICADORES GERAIS + PAINEL TÉRMICO LATERAL ---
            potencia_col = next((c for c in var_cols if 'power' in c.lower() or 'potência' in c.lower() or 'potencia' in c.lower()), None)
            temp_mod_col = next((c for c in var_cols if 'temp' in c.lower() and ('mod' in c.lower() or 'fv' in c.lower())), None)
            irrad_col = next((c for c in var_cols if 'piranometro' in c.lower() or 'irradiância' in c.lower() or 'g' == c.lower() or 'irrad' in c.lower()), None)
            variavel_temperatura = ('temp' in str(variavel_y).lower() or 'temperatura' in str(variavel_y).lower())

            # Busca a data exata em que ocorreu o valor máximo.
            def obter_data_maxima(col_nome):
                if col_nome and not df[col_nome].dropna().empty:
                    idx_max = df[col_nome].idxmax()
                    return df.loc[idx_max, col_data].strftime('%d/%m/%Y')
                return "N/A"

            data_pot_max = obter_data_maxima(potencia_col)
            data_temp_max = obter_data_maxima(temp_mod_col)
            data_irrad_max = obter_data_maxima(irrad_col)

            if variavel_temperatura:
                indicadores_col, termico_col = st.columns([1.05, 0.95], gap="large")
                with indicadores_col:
                    st.markdown("### 📊 Indicadores gerais da planta")
                    k1, k2 = st.columns(2)
                    with k1:
                        with st.container(border=True):
                            val_p = f"{df[potencia_col].max():.2f} W" if potencia_col else "N/A"
                            st.metric("Potência Máxima", val_p, delta=f"📅 {data_pot_max}", delta_color="off")
                    with k2:
                        with st.container(border=True):
                            val_e = f"{(df[potencia_col].sum() * 0.25) / 1000:.2f} kWh" if potencia_col else "N/A"
                            st.metric("Energia Estimada Total", val_e)
                    k3, k4 = st.columns(2)
                    with k3:
                        with st.container(border=True):
                            val_t = f"{df[temp_mod_col].max():.1f} °C" if temp_mod_col else "N/A"
                            st.metric("Temp. Máxima Módulo", val_t, delta=f"📅 {data_temp_max}", delta_color="off")
                    with k4:
                        with st.container(border=True):
                            val_i = f"{df[irrad_col].max():.1f} W/m²" if irrad_col else "N/A"
                            st.metric("Irradiância Máxima", val_i, delta=f"📅 {data_irrad_max}", delta_color="off")
                with termico_col:
                    exibir_condicoes_termicas(df, variavel_y, irrad_col)
            else:
                st.markdown("### 📊 Indicadores gerais do período")
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    with st.container(border=True):
                        val_p = f"{df[potencia_col].max():.2f} W" if potencia_col else "N/A"
                        st.metric("Potência Máxima", val_p, delta=f"📅 {data_pot_max}", delta_color="off")
                with c2:
                    with st.container(border=True):
                        val_e = f"{(df[potencia_col].sum() * 0.25) / 1000:.2f} kWh" if potencia_col else "N/A"
                        st.metric("Energia Estimada Total", val_e)
                with c3:
                    with st.container(border=True):
                        val_t = f"{df[temp_mod_col].max():.1f} °C" if temp_mod_col else "N/A"
                        st.metric("Temp. Máxima Módulo", val_t, delta=f"📅 {data_temp_max}", delta_color="off")
                with c4:
                    with st.container(border=True):
                        val_i = f"{df[irrad_col].max():.1f} W/m²" if irrad_col else "N/A"
                        st.metric("Irradiância Máxima", val_i, delta=f"📅 {data_irrad_max}", delta_color="off")

            # --- DESTAQUES DE PERFORMANCE ---
            st.markdown(f"### 🏆 Destaques de Maior Valor para: `{variavel_y}`")
            
            df_dia_grp = df.groupby('Dia_Data')[variavel_y].mean().reset_index()
            top_dia_row = (df_dia_grp.loc[df_dia_grp[variavel_y].idxmax()]
                           if not df_dia_grp.empty and df_dia_grp[variavel_y].notna().any()
                           else None)

            df_mes_grp_total = df.groupby(['Ano_Num', 'Mes_Num', 'Nome_Mes_Formatado'])[variavel_y].mean().reset_index()
            top_mes_row = (df_mes_grp_total.loc[df_mes_grp_total[variavel_y].idxmax()]
                           if not df_mes_grp_total.empty and df_mes_grp_total[variavel_y].notna().any()
                           else None)

            ct1, ct2 = st.columns(2)
            with ct1:
                with st.container(border=True):
                    if top_dia_row is not None:
                        st.metric("🥇 Dia de Maior Média", f"{top_dia_row['Dia_Data'].strftime('%d/%m/%Y')}", f"Média: {top_dia_row[variavel_y]:.2f}")
                    else:
                        st.metric("🥇 Dia de Maior Média", "N/A")
            with ct2:
                with st.container(border=True):
                    if top_mes_row is not None:
                        label_mes = f"{top_mes_row['Nome_Mes_Formatado']}/{int(top_mes_row['Ano_Num'])}"
                        st.metric("🏆 Mês de Maior Média", label_mes, f"Média: {top_mes_row[variavel_y]:.2f}")
                    else:
                        st.metric("🏆 Mês de Maior Média", "N/A")

            st.divider()

            # --- GRÁFICO HISTÓRICO COMPLETO (TODOS OS MESES DO ARQUIVO) ---
            st.markdown(f"### 🌐 Visão Histórica Completa do Arquivo (`{variavel_y}`)")
            st.caption("Visão contínua de todos os meses contidos na planilha importada, organizados cronologicamente.")

            df_hist_grp = df.groupby(['Ano_Mes_Sort', 'Ano_Mes_Texto'])[variavel_y].mean().reset_index().sort_values('Ano_Mes_Sort')
            
            fig_hist = criar_grafico_base(
                df_hist_grp, 
                x_col='Ano_Mes_Texto', 
                y_col=variavel_y, 
                titulo=f"Evolução Média Mensal de {variavel_y} (Todos os Meses do Arquivo)", 
                tipo_grafico=tipo_grafico, 
                cor='#8E44AD'
            )
            fig_hist.update_layout(xaxis=dict(title="Mês/Ano"), yaxis=dict(title=variavel_y))
            exibir_grafico(fig_hist)

            st.divider()

            # --- GRÁFICOS INTEGRADOS (SEMESTRAL, MENSAL, DIÁRIO) ---
            st.markdown("## 📈 Painel Integrado de Gráficos")
            anos_disponiveis = sorted(df['Ano_Num'].dropna().unique())

            if modo_exibicao == "📊 Modo Grid (3 Simultâneos)":
                g1, g2, g3 = st.columns(3)
                
                # CARD 1: SEMESTRAL
                with g1:
                    with st.container(border=True):
                        st.markdown("#### 🗓️ Visão Semestral")
                        cs1, cs2 = st.columns(2)
                        with cs1:
                            ano_semestral = st.selectbox("Ano:", anos_disponiveis, key='k_ano_semestral')
                        semestres_disp = sorted(df[df['Ano_Num'] == ano_semestral]['Semestre_Nome'].dropna().unique())
                        with cs2:
                            semestre_sel = st.selectbox("Semestre:", semestres_disp, key='k_semestre_semestral')
                        
                        df_sem = df[(df['Ano_Num'] == ano_semestral) & (df['Semestre_Nome'] == semestre_sel)]
                        df_sem_grp = df_sem.groupby(['Mes_Num', 'Nome_Mes_Formatado'])[variavel_y].mean().reset_index().sort_values('Mes_Num')
                        fig_sem = criar_grafico_base(df_sem_grp, 'Nome_Mes_Formatado', variavel_y, f"Média Mensal ({semestre_sel}/{ano_semestral})", tipo_grafico, '#E67E22')
                        exibir_grafico(fig_sem)

                # CARD 2: MENSAL
                with g2:
                    with st.container(border=True):
                        st.markdown("#### 📆 Visão Mensal")
                        cm1, cm2 = st.columns(2)
                        with cm1:
                            ano_mensal = st.selectbox("Ano:", anos_disponiveis, key='k_ano_mensal')
                        meses_disp = sorted(df[df['Ano_Num'] == ano_mensal]['Mes_Num'].dropna().unique())
                        with cm2:
                            mes_mensal = st.selectbox("Mês:", meses_disp, key='k_mes_mensal')
                        
                        df_mes = df[(df['Ano_Num'] == ano_mensal) & (df['Mes_Num'] == mes_mensal)]
                        df_mes_grp = df_mes.groupby('Dia_Do_Mes')[variavel_y].mean().reset_index()
                        fig_mes = criar_grafico_base(df_mes_grp, 'Dia_Do_Mes', variavel_y, f"Média Diária ({mes_mensal}/{ano_mensal})", tipo_grafico, '#2980B9')
                        fig_mes.update_layout(xaxis=dict(tickmode='linear', dtick=1))
                        exibir_grafico(fig_mes)

                # CARD 3: DIÁRIO
                with g3:
                    with st.container(border=True):
                        st.markdown("#### 🕐 Visão Diária")
                        dias_disp = sorted(df['Dia_Data'].dropna().unique())
                        dia_diario = st.selectbox("Data:", dias_disp, key='k_dia_diario')
                        
                        df_dia = df[df['Dia_Data'] == dia_diario].sort_values(by=col_data)
                        fig_dia = criar_grafico_base(df_dia, col_data, variavel_y, f"Intradiário ({dia_diario.strftime('%d/%m/%Y')})", tipo_grafico, '#27AE60')
                        exibir_grafico(fig_dia)

            else:
                # MODO FOCO (AMPLIADO)
                with st.container(border=True):
                    st.markdown("#### 🔍 Selecione o Gráfico para Ampliar")
                    opcao_foco = st.radio("Gráfico em Destaque:", ["🗓️ Semestral", "📆 Mensal", "🕐 Diário"], horizontal=True)
                    
                    if "Semestral" in opcao_foco:
                        cf1, cf2 = st.columns(2)
                        with cf1:
                            ano_semestral = st.selectbox("Ano:", anos_disponiveis, key='foco_ano_s')
                        semestres_disp = sorted(df[df['Ano_Num'] == ano_semestral]['Semestre_Nome'].dropna().unique())
                        with cf2:
                            semestre_sel = st.selectbox("Semestre:", semestres_disp, key='foco_semestre')
                        df_sem = df[(df['Ano_Num'] == ano_semestral) & (df['Semestre_Nome'] == semestre_sel)]
                        df_sem_grp = df_sem.groupby(['Mes_Num', 'Nome_Mes_Formatado'])[variavel_y].mean().reset_index().sort_values('Mes_Num')
                        fig_sem = criar_grafico_base(df_sem_grp, 'Nome_Mes_Formatado', variavel_y, f"Evolução Semestral ({semestre_sel}/{ano_semestral})", tipo_grafico, '#E67E22')
                        exibir_grafico(fig_sem)
                    elif "Mensal" in opcao_foco:
                        cf1, cf2 = st.columns(2)
                        with cf1:
                            ano_mensal = st.selectbox("Ano:", anos_disponiveis, key='foco_ano_m')
                        meses_disp = sorted(df[df['Ano_Num'] == ano_mensal]['Mes_Num'].dropna().unique())
                        with cf2:
                            mes_mensal = st.selectbox("Mês:", meses_disp, key='foco_mes')
                        df_mes = df[(df['Ano_Num'] == ano_mensal) & (df['Mes_Num'] == mes_mensal)]
                        df_mes_grp = df_mes.groupby('Dia_Do_Mes')[variavel_y].mean().reset_index()
                        fig_mes = criar_grafico_base(df_mes_grp, 'Dia_Do_Mes', variavel_y, f"Evolução Mensal ({mes_mensal}/{ano_mensal})", tipo_grafico, '#2980B9')
                        exibir_grafico(fig_mes)
                    else:
                        dias_disp = sorted(df['Dia_Data'].dropna().unique())
                        dia_diario = st.selectbox("Data:", dias_disp, key='foco_dia')
                        df_dia = df[df['Dia_Data'] == dia_diario].sort_values(by=col_data)
                        fig_dia = criar_grafico_base(df_dia, col_data, variavel_y, f"Evolução Diária ({dia_diario.strftime('%d/%m/%Y')})", tipo_grafico, '#27AE60')
                        exibir_grafico(fig_dia)

            st.divider()

            # --- SEÇÃO DO GRÁFICO DE PIZZA / ROSCA E EXPLICAÇÃO ---
            st.markdown(f"### 🍕 Distribuição Média Mensal de `{variavel_y}`")
            
            exp_col, pie_col = st.columns([1, 1.2])
            
            with exp_col:
                st.markdown("""
                <div class="explanation-box">
                    <h4>💡 Como interpretar este gráfico?</h4>
                    <p>Este gráfico de rosca representa a <b>proporção percentual</b> que cada mês representa no valor médio acumulado da variável selecionada.</p>
                    <ul>
                        <li><b>Fatias Maiores:</b> Indicam os meses em que a variável analisada (ex: geração, irradiância ou tensão) operou com médias mais elevadas.</li>
                        <li><b>Fatias Menores:</b> Apontam meses de baixa produção ou períodos com maior incidência de nebulosidade e manutenções.</li>
                        <li><b>Interatividade:</b> Passe o ponteiro do mouse sobre qualquer fatia para consultar o nome do mês e o valor médio exato.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with pie_col:
                with st.container(border=True):
                    df_pie_grp = df.groupby('Nome_Mes_Formatado')[variavel_y].mean().reset_index()
                    df_pie_grp = df_pie_grp.dropna(subset=[variavel_y])
                    fig_pie = px.pie(
                        df_pie_grp, 
                        values=variavel_y, 
                        names='Nome_Mes_Formatado', 
                        hole=0.4,
                        title=f"Participação Percentual por Mês (`{variavel_y}`)",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_pie.update_traces(textinfo='percent+label')
                    fig_pie.update_layout(margin=dict(l=10, r=10, t=35, b=10))
                    exibir_grafico(fig_pie)

            st.divider()

            # --- COMPARAÇÃO MULTI-MESES NO MESMO GRÁFICO ---
            st.markdown("### ⚔️ Comparação entre Diferentes Meses")
            st.caption("Selecione dois ou mais meses para sobrepor as curvas de média diária no mesmo gráfico.")
            
            df['Ano_Mes_Label'] = df['Nome_Mes_Formatado'] + '/' + df['Ano_Num'].astype(str)
            meses_opcoes = sorted(df['Ano_Mes_Label'].unique())
            
            default_meses = meses_opcoes[:2] if len(meses_opcoes) >= 2 else meses_opcoes
            meses_selecionados = st.multiselect(
                "Escolha os meses para comparar:", 
                options=meses_opcoes, 
                default=default_meses
            )
            
            if meses_selecionados:
                df_comp_meses = df[df['Ano_Mes_Label'].isin(meses_selecionados)]
                df_comp_grp = df_comp_meses.groupby(['Ano_Mes_Label', 'Dia_Do_Mes'])[variavel_y].mean().reset_index()
                
                fig_multi_mes = px.line(
                    df_comp_grp, x='Dia_Do_Mes', y=variavel_y, color='Ano_Mes_Label',
                    title=f"Curvas Comparativas de `{variavel_y}` entre Meses (Dia 1 ao 31)",
                    markers=True
                )
                fig_multi_mes.update_layout(xaxis=dict(title="Dia do Mês", tickmode='linear', dtick=1), hovermode="x unified")
                exibir_grafico(fig_multi_mes)

            st.divider()

            # --- COMPARAÇÃO MULTI-GRANDEZAS / VARIÁVEIS (ATÉ 3) ---
            st.markdown("### 🔄 Comparação entre Diferentes Grandezas Físicas")
            st.caption("Compare a grandeza principal com até 3 outras variáveis no mesmo dia.")
            
            dias_disp = sorted(df['Dia_Data'].dropna().unique())
            dia_comp_var = st.selectbox("Data para Análise das Grandezas:", dias_disp, key='dia_comp_var')
            df_dia_comp = df[df['Dia_Data'] == dia_comp_var].sort_values(by=col_data)
            
            var_opcoes = [c for c in var_cols if c != variavel_y]
            vars_comparacao = st.multiselect(
                "Selecione até 3 grandezas secundárias para comparar:", 
                options=var_opcoes, 
                max_selections=3
            )

            if vars_comparacao:
                fig_comp = make_subplots(specs=[[{"secondary_y": True}]])
                fig_comp.add_trace(go.Scatter(x=df_dia_comp[col_data], y=df_dia_comp[variavel_y], name=f"Principal: {variavel_y}", line=dict(color='#27AE60', width=3)), secondary_y=False)
                
                cores_sec = ['#E74C3C', '#8E44AD', '#F39C12']
                for idx, v_sec in enumerate(vars_comparacao):
                    fig_comp.add_trace(go.Scatter(x=df_dia_comp[col_data], y=df_dia_comp[v_sec], name=v_sec, line=dict(color=cores_sec[idx % len(cores_sec)], width=2, dash='dot')), secondary_y=True)
                
                fig_comp.update_layout(title=f"Comparação de Grandezas em {dia_comp_var.strftime('%d/%m/%Y')}", hovermode='x unified')
                fig_comp.update_yaxes(title_text=f"<b>{variavel_y}</b>", secondary_y=False)
                fig_comp.update_yaxes(title_text="<b>Grandezas Secundárias</b>", secondary_y=True)
                exibir_grafico(fig_comp)

            # --- NOVAS ANÁLISES: COMPARAÇÃO ENTRE DIAS E ANOS ---
            # Esta seção é adicional. Os gráficos de sobreposição já existentes
            # (comparação entre meses e comparação entre grandezas) foram mantidos.
            st.divider()
            st.markdown("## 📅 Comparações adicionais de períodos")
            st.markdown(
                '<div class="section-intro">Compare dias específicos pela curva ao longo do dia '
                'e compare anos pela evolução mensal. Estas análises são independentes dos gráficos '
                'de sobreposição que já existiam no painel.</div>',
                unsafe_allow_html=True
            )

            tab_dias, tab_anos = st.tabs(["🗓️ Comparar dias", "📆 Comparar anos"])

            with tab_dias:
                st.caption(
                    "Selecione dois ou mais dias para comparar o comportamento intradiário "
                    "da variável escolhida na barra lateral."
                )
                dias_comparacao = sorted(df['Dia_Data'].dropna().unique())
                padrao_dias = dias_comparacao[-2:] if len(dias_comparacao) >= 2 else dias_comparacao
                dias_selecionados = st.multiselect(
                    "Dias para comparar:",
                    options=dias_comparacao,
                    default=padrao_dias,
                    format_func=lambda d: d.strftime('%d/%m/%Y'),
                    key="novos_dias_comparacao"
                )

                if len(dias_selecionados) >= 2:
                    df_dias_novo = df[df['Dia_Data'].isin(dias_selecionados)].copy()
                    df_dias_novo['Horario_Comparacao'] = df_dias_novo[col_data].dt.strftime('%H:%M')
                    df_dias_novo['Dia_Comparacao'] = df_dias_novo['Dia_Data'].apply(
                        lambda d: d.strftime('%d/%m/%Y')
                    )
                    df_dias_novo_grp = (
                        df_dias_novo.groupby(['Dia_Comparacao', 'Horario_Comparacao'], as_index=False)[variavel_y]
                        .mean()
                    )
                    fig_dias_novo = px.line(
                        df_dias_novo_grp,
                        x='Horario_Comparacao',
                        y=variavel_y,
                        color='Dia_Comparacao',
                        markers=True,
                        title=f"Comparação intradiária de {variavel_y}"
                    )
                    fig_dias_novo.update_layout(
                        xaxis_title="Horário",
                        yaxis_title=variavel_y,
                        hovermode="x unified",
                        legend_title="Dia",
                        margin=dict(l=15, r=15, t=45, b=15)
                    )
                    exibir_grafico(fig_dias_novo)
                elif len(dias_selecionados) == 1:
                    st.info("Selecione pelo menos dois dias para realizar a comparação.")
                else:
                    st.info("Selecione os dias que deseja comparar.")

            with tab_anos:
                st.caption(
                    "Compare a evolução dos meses entre anos diferentes. Quando existe uma coluna "
                    "de potência, o gráfico utiliza energia mensal estimada em kWh, considerando "
                    "o intervalo de amostragem de 15 minutos já adotado no cálculo original."
                )
                anos_para_comparar = sorted(df['Ano_Num'].dropna().unique())
                padrao_anos = anos_para_comparar[-2:] if len(anos_para_comparar) >= 2 else anos_para_comparar
                anos_selecionados = st.multiselect(
                    "Anos para comparar:",
                    options=anos_para_comparar,
                    default=padrao_anos,
                    key="novos_anos_comparacao"
                )

                if len(anos_selecionados) >= 2:
                    df_anos_novo = df[df['Ano_Num'].isin(anos_selecionados)].copy()
                    if potencia_col:
                        df_anos_novo['_Energia_Intervalo_kWh'] = df_anos_novo[potencia_col] * 0.25 / 1000
                        df_anos_grp = (
                            df_anos_novo.groupby(['Ano_Num', 'Mes_Num'], as_index=False)['_Energia_Intervalo_kWh']
                            .sum(min_count=1)
                        )
                        df_anos_grp = df_anos_grp.rename(columns={'_Energia_Intervalo_kWh': 'Energia mensal estimada (kWh)'})
                        coluna_ano_y = 'Energia mensal estimada (kWh)'
                        titulo_ano = "Energia mensal estimada por ano"
                        eixo_y_ano = "Energia (kWh)"
                    else:
                        df_anos_grp = (
                            df_anos_novo.groupby(['Ano_Num', 'Mes_Num'], as_index=False)[variavel_y]
                            .mean()
                        )
                        coluna_ano_y = variavel_y
                        titulo_ano = f"Média mensal de {variavel_y} por ano"
                        eixo_y_ano = variavel_y

                    meses_nomes = {
                        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
                        7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
                    }
                    df_anos_grp['Mês'] = df_anos_grp['Mes_Num'].map(meses_nomes)
                    df_anos_grp['Ano'] = df_anos_grp['Ano_Num'].astype(int).astype(str)
                    fig_anos_novo = px.line(
                        df_anos_grp,
                        x='Mes_Num',
                        y=coluna_ano_y,
                        color='Ano',
                        markers=True,
                        title=titulo_ano
                    )
                    fig_anos_novo.update_layout(
                        xaxis=dict(
                            title="Mês",
                            tickmode="array",
                            tickvals=list(range(1, 13)),
                            ticktext=[meses_nomes[m] for m in range(1, 13)]
                        ),
                        yaxis_title=eixo_y_ano,
                        hovermode="x unified",
                        legend_title="Ano",
                        margin=dict(l=15, r=15, t=45, b=15)
                    )
                    exibir_grafico(fig_anos_novo)
                elif len(anos_selecionados) == 1:
                    st.info("Selecione pelo menos dois anos para realizar a comparação.")
                else:
                    st.info("Selecione os anos que deseja comparar.")

            # --- DETECÇÃO DE DIAS COM BAIXA GERAÇÃO / POSSÍVEIS ANOMALIAS ---
            st.divider()
            st.markdown("## 🚨 Análise de geração e possíveis anomalias")
            st.caption(
                "A análise usa a potência registrada e estima a energia diária. Quando há irradiância, "
                "também compara a energia com a radiação recebida para evitar classificar automaticamente "
                "um dia nublado como falha da planta."
            )

            if potencia_col:
                slider_col, valor_col = st.columns([5, 1])
                with slider_col:
                    limite_amostras = st.slider(
                        "Sensibilidade para sinalizar desempenho abaixo da referência:",
                        min_value=10,
                        max_value=50,
                        value=20,
                        step=5,
                        format="%d",
                        help="É um critério indicativo: sinaliza dias cujo indicador energia/irradiação ficou abaixo da mediana de referência por esta porcentagem."
                    )
                with valor_col:
                    st.markdown(
                        f'<div class="sensitivity-badge">{limite_amostras}%</div>',
                        unsafe_allow_html=True
                    )

                df_anomalia_base = df.dropna(subset=[potencia_col]).copy()
                df_anomalia_base['_Energia_Intervalo_kWh'] = df_anomalia_base[potencia_col] * 0.25 / 1000
                agregacoes_diarias = {
                    'Energia_kWh': ('_Energia_Intervalo_kWh', lambda s: s.sum(min_count=1)),
                    'Amostras': (potencia_col, 'count'),
                    'Potencia_Media': (potencia_col, 'mean'),
                    'Potencia_Maxima': (potencia_col, 'max')
                }
                df_diario_energia = (
                    df_anomalia_base.groupby('Dia_Data')
                    .agg(**agregacoes_diarias)
                    .reset_index()
                )

                if irrad_col:
                    df_irrad_diaria = df.dropna(subset=[irrad_col]).copy()
                    # Irradiância (W/m²) integrada em intervalos de 15 min -> kWh/m².
                    df_irrad_diaria['_Irradiacao_Intervalo_kWh_m2'] = df_irrad_diaria[irrad_col] * 0.25 / 1000
                    df_irrad_diaria = (
                        df_irrad_diaria.groupby('Dia_Data')['_Irradiacao_Intervalo_kWh_m2']
                        .sum(min_count=1)
                        .reset_index(name='Irradiacao_kWh_m2')
                    )
                    df_diario_energia = df_diario_energia.merge(df_irrad_diaria, on='Dia_Data', how='left')
                    denominador_irrad = df_diario_energia['Irradiacao_kWh_m2'].where(
                        df_diario_energia['Irradiacao_kWh_m2'] > 0
                    )
                    df_diario_energia['Energia_por_Irradiacao'] = (
                        df_diario_energia['Energia_kWh'] / denominador_irrad
                    )
                else:
                    df_diario_energia['Classificacao'] = 'Menor geração (sem ajuste por irradiância)'

                # Dias com menos de 75% da quantidade típica de amostras não entram
                # na referência nem na classificação de anomalia, pois podem estar incompletos.
                amostras_tipicas = df_diario_energia['Amostras'].median()
                if pd.notna(amostras_tipicas) and amostras_tipicas > 0:
                    df_diario_energia['Dados_Completos'] = df_diario_energia['Amostras'] >= (0.75 * amostras_tipicas)
                else:
                    df_diario_energia['Dados_Completos'] = False

                if irrad_col:
                    condicao_referencia = (
                        df_diario_energia['Irradiacao_kWh_m2'].notna()
                        & (df_diario_energia['Irradiacao_kWh_m2'] >= 0.5)
                        & df_diario_energia['Dados_Completos']
                    )
                    dias_com_irradiacao = df_diario_energia.loc[condicao_referencia]
                    referencia_indice = dias_com_irradiacao['Energia_por_Irradiacao'].median()
                    df_diario_energia['Classificacao'] = 'Sem irradiância suficiente'
                    if pd.notna(referencia_indice) and referencia_indice > 0:
                        limite_indice = referencia_indice * (1 - limite_amostras / 100)
                        df_diario_energia.loc[condicao_referencia, 'Classificacao'] = 'Dentro da referência'
                        condicao_anomalia = (
                            condicao_referencia
                            & (df_diario_energia['Energia_por_Irradiacao'] < limite_indice)
                        )
                        df_diario_energia.loc[condicao_anomalia, 'Classificacao'] = 'Possível anomalia'
                    else:
                        df_diario_energia.loc[condicao_referencia, 'Classificacao'] = 'Sem referência suficiente'
                df_diario_energia.loc[~df_diario_energia['Dados_Completos'], 'Classificacao'] = 'Dados incompletos'

                menor_dia = df_diario_energia.loc[df_diario_energia['Energia_kWh'].idxmin()] if not df_diario_energia.empty else None
                maior_dia = df_diario_energia.loc[df_diario_energia['Energia_kWh'].idxmax()] if not df_diario_energia.empty else None

                if menor_dia is not None:
                    ka, kb, kc = st.columns(3)
                    with ka:
                        st.metric("Menor geração diária", f"{menor_dia['Energia_kWh']:.2f} kWh", delta=menor_dia['Dia_Data'].strftime('%d/%m/%Y'), delta_color="off")
                    with kb:
                        st.metric("Maior geração diária", f"{maior_dia['Energia_kWh']:.2f} kWh", delta=maior_dia['Dia_Data'].strftime('%d/%m/%Y'), delta_color="off")
                    with kc:
                        qtd_anomalias = int((df_diario_energia['Classificacao'] == 'Possível anomalia').sum())
                        st.metric("Possíveis anomalias", str(qtd_anomalias))

                    df_energia_plot = df_diario_energia.sort_values('Dia_Data')
                    fig_energia_dias = px.bar(
                        df_energia_plot,
                        x='Dia_Data',
                        y='Energia_kWh',
                        color='Classificacao',
                        title="Energia estimada por dia e classificação",
                        color_discrete_map={
                            'Dentro da referência': '#25A56A',
                            'Possível anomalia': '#E74C3C',
                            'Menor geração (sem ajuste por irradiância)': '#E67E22',
                            'Sem referência suficiente': '#7F8C8D',
                            'Sem irradiância suficiente': '#3498DB',
                            'Dados incompletos': '#8E44AD'
                        }
                    )
                    fig_energia_dias.update_layout(
                        xaxis_title="Dia",
                        yaxis_title="Energia estimada (kWh)",
                        hovermode="x unified",
                        margin=dict(l=15, r=15, t=45, b=15)
                    )
                    exibir_grafico(fig_energia_dias)

                    if irrad_col:
                        st.markdown("#### Dias com possível desempenho abaixo da referência")
                        df_suspeitos = df_diario_energia[
                            df_diario_energia['Classificacao'].isin(['Possível anomalia', 'Dados incompletos'])
                        ].copy()
                        if not df_suspeitos.empty:
                            colunas_tabela = ['Dia_Data', 'Energia_kWh', 'Irradiacao_kWh_m2', 'Energia_por_Irradiacao', 'Amostras', 'Classificacao']
                            st.dataframe(
                                df_suspeitos[colunas_tabela].sort_values('Energia_por_Irradiacao', na_position='last'),
                                use_container_width=True,
                                hide_index=True
                            )
                        else:
                            st.success("Nenhum dia foi sinalizado pelo critério selecionado.")
                        st.info(
                            "A classificação é um alerta estatístico, não um diagnóstico de falha. "
                            "Sombreamento, sujeira, indisponibilidade, diferenças de amostragem e falhas "
                            "de sensores também podem influenciar o resultado."
                        )
                    else:
                        st.warning(
                            "Não foi identificada uma coluna de irradiância. O painel mostra os dias de "
                            "menor geração, mas não classifica esses dias como anomalias de desempenho, "
                            "pois não é possível separar baixa radiação de possível falha usando apenas potência."
                        )
                        st.dataframe(
                            df_diario_energia.nsmallest(10, 'Energia_kWh')[['Dia_Data', 'Energia_kWh', 'Amostras', 'Classificacao']],
                            use_container_width=True,
                            hide_index=True
                        )
                else:
                    st.info("Não há registros suficientes de potência para calcular a geração diária.")
            else:
                st.info(
                    "Não encontrei uma coluna identificável como potência. Para calcular energia diária "
                    "e procurar dias com baixa geração, inclua uma coluna cujo nome contenha 'Power' ou 'Potência'."
                )

            # --- EXPANDER PARA INSPEÇÃO DA PLANILHA ---
            with st.expander("🔍 Inspecionar Tabela Completa e Dados Brutos"):
                st.dataframe(df, use_container_width=True)

    else:
        st.info("Por favor, carregue a planilha de dados no menu lateral para iniciar o sistema.")

if __name__ == "__main__":
    main()
