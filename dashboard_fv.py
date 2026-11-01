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

@st.cache_data
def load_and_clean_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, sep=';', decimal=',') 
            if len(df.columns) == 1:
                df = pd.read_csv(uploaded_file, sep=',', decimal='.')
        else:
            df = pd.read_excel(uploaded_file)
        
        col_data = [col for col in df.columns if 'data' in col.lower() or 'hora' in col.lower() or 'date' in col.lower() or 'time' in col.lower()]
        if not col_data:
            st.error("Não foi possível identificar a coluna de Data e Hora.")
            return None, None
        
        data_col = col_data[0]
        df[data_col] = pd.to_datetime(df[data_col], dayfirst=True, errors='coerce')
        df = df.dropna(subset=[data_col]).sort_values(by=data_col).reset_index(drop=True)
        
        # Componentes de data
        df['Ano_Num'] = df[data_col].dt.year
        df['Mes_Num'] = df[data_col].dt.month
        df['Dia_Data'] = df[data_col].dt.date
        df['Hora_Tempo'] = df[data_col].dt.time
        df['Dia_Do_Mes'] = df[data_col].dt.day
        
        # Colunas auxiliares para ordenação cronológica de meses
        df['Ano_Mes_Sort'] = df[data_col].dt.to_period('M').dt.to_timestamp()
        
        # Cálculo do Semestre (1º ou 2º)
        df['Semestre_Num'] = df['Mes_Num'].apply(lambda m: 1 if m <= 6 else 2)
        df['Semestre_Nome'] = df['Semestre_Num'].astype(str) + 'º Semestre'
        
        meses_pt = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 
                    7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
        df['Nome_Mes_Formatado'] = df['Mes_Num'].map(meses_pt).fillna('Indefinido')
        df['Ano_Mes_Texto'] = df['Nome_Mes_Formatado'] + '/' + df['Ano_Num'].astype(str)
        
        cols_reservadas = [data_col, 'Ano_Num', 'Mes_Num', 'Dia_Data', 'Hora_Tempo', 'Dia_Do_Mes', 
                           'Nome_Mes_Formatado', 'Semestre_Num', 'Semestre_Nome', 'Ano_Mes_Sort', 'Ano_Mes_Texto']
        for col in df.columns:
            if col not in cols_reservadas:
                if df[col].dtype == object:
                    df[col] = df[col].astype(str).str.replace(' ', '.', regex=False)
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
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

def main():
    st.title("☀️ Painel de Análise de Planta Fotovoltaica")

    # --- BARRA LATERAL ---
    st.sidebar.header("📁 Importação de Dados")
    uploaded_file = st.sidebar.file_uploader("Carregue sua planilha (.csv, .xls, .xlsx)", type=['csv', 'xlsx', 'xls'])

    if uploaded_file is not None:
        with st.spinner("Carregando dados..."):
            df, col_data = load_and_clean_data(uploaded_file)
            
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

            # --- INDICADORES GERAIS COM DATAS DOS PICOS ---
            st.markdown("### 📊 Indicadores Gerais do Período")
            potencia_col = next((c for c in var_cols if 'power' in c.lower() or 'potência' in c.lower() or 'potencia' in c.lower()), None)
            temp_mod_col = next((c for c in var_cols if 'temp' in c.lower() and ('mod' in c.lower() or 'fv' in c.lower())), None)
            irrad_col = next((c for c in var_cols if 'piranometro' in c.lower() or 'irradiância' in c.lower() or 'g' == c.lower() or 'irrad' in c.lower()), None)
            
            # Busca da data exata em que ocorreu o valor máximo
            def obter_data_maxima(col_nome):
                if col_nome and not df[col_nome].dropna().empty:
                    idx_max = df[col_nome].idxmax()
                    return df.loc[idx_max, col_data].strftime('%d/%m/%Y')
                return "N/A"

            data_pot_max = obter_data_maxima(potencia_col)
            data_temp_max = obter_data_maxima(temp_mod_col)
            data_irrad_max = obter_data_maxima(irrad_col)

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
            top_dia_row = df_dia_grp.loc[df_dia_grp[variavel_y].idxmax()] if not df_dia_grp.empty else None

            df_mes_grp_total = df.groupby(['Ano_Num', 'Mes_Num', 'Nome_Mes_Formatado'])[variavel_y].mean().reset_index()
            top_mes_row = df_mes_grp_total.loc[df_mes_grp_total[variavel_y].idxmax()] if not df_mes_grp_total.empty else None

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
            st.plotly_chart(fig_hist, use_container_width=True)

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
                        st.plotly_chart(fig_sem, use_container_width=True)

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
                        st.plotly_chart(fig_mes, use_container_width=True)

                # CARD 3: DIÁRIO
                with g3:
                    with st.container(border=True):
                        st.markdown("#### 🕐 Visão Diária")
                        dias_disp = sorted(df['Dia_Data'].dropna().unique())
                        dia_diario = st.selectbox("Data:", dias_disp, key='k_dia_diario')
                        
                        df_dia = df[df['Dia_Data'] == dia_diario].sort_values(by=col_data)
                        fig_dia = criar_grafico_base(df_dia, col_data, variavel_y, f"Intradiário ({dia_diario.strftime('%d/%m/%Y')})", tipo_grafico, '#27AE60')
                        st.plotly_chart(fig_dia, use_container_width=True)

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
                        st.plotly_chart(fig_sem, use_container_width=True)
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
                        st.plotly_chart(fig_mes, use_container_width=True)
                    else:
                        dias_disp = sorted(df['Dia_Data'].dropna().unique())
                        dia_diario = st.selectbox("Data:", dias_disp, key='foco_dia')
                        df_dia = df[df['Dia_Data'] == dia_diario].sort_values(by=col_data)
                        fig_dia = criar_grafico_base(df_dia, col_data, variavel_y, f"Evolução Diária ({dia_diario.strftime('%d/%m/%Y')})", tipo_grafico, '#27AE60')
                        st.plotly_chart(fig_dia, use_container_width=True)

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
                    st.plotly_chart(fig_pie, use_container_width=True)

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
                st.plotly_chart(fig_multi_mes, use_container_width=True)

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
                st.plotly_chart(fig_comp, use_container_width=True)

            # --- EXPANDER PARA INSPEÇÃO DA PLANILHA ---
            with st.expander("🔍 Inspecionar Tabela Completa e Dados Brutos"):
                st.dataframe(df, use_container_width=True)

    else:
        st.info("Por favor, carregue a planilha de dados no menu lateral para iniciar o sistema.")

if __name__ == "__main__":
    main()