                        }
                    )
                    fig_energia_dias.update_layout(
                        xaxis_title="Dia",
                        yaxis_title="Energia estimada (kWh)",
                        hovermode="x unified",
                        margin=dict(l=15, r=15, t=45, b=15)
                    )
                    st.plotly_chart(fig_energia_dias, use_container_width=True)

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

            # --- CONTEXTO VISUAL PARA VARIÁVEIS DE TEMPERATURA ---
            if 'temp' in str(variavel_y).lower() or 'temperatura' in str(variavel_y).lower():
                st.divider()
                st.markdown(f"## 🌡️ Condições térmicas — {variavel_y}")
                st.caption(
                    "Os símbolos de sol e nuvens são uma representação visual baseada na irradiância "
                    "medida pela própria planta; não são uma previsão meteorológica."
                )
                dias_temperatura = sorted(df['Dia_Data'].dropna().unique())
                dia_temperatura = st.selectbox(
                    "Dia para contextualizar a temperatura:",
                    options=dias_temperatura,
                    index=len(dias_temperatura) - 1 if dias_temperatura else 0,
                    format_func=lambda d: d.strftime('%d/%m/%Y'),
                    key="dia_contexto_temperatura"
                )
                df_temp_contexto = df[df['Dia_Data'] == dia_temperatura]
                serie_temp = df_temp_contexto[variavel_y].dropna()
                media_temp = serie_temp.mean() if not serie_temp.empty else None
                maxima_temp = serie_temp.max() if not serie_temp.empty else None

                irradiancia_media_dia = None
                if irrad_col:
                    # Calcula a média apenas nos intervalos em que há irradiância relevante,
                    # evitando que o período noturno reduza artificialmente a média do dia.
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

                tc1, tc2, tc3 = st.columns(3)
                with tc1:
                    valor_media_temp = f"{media_temp:.1f} °C" if media_temp is not None else "N/D"
                    st.markdown(
                        f'<div class="temperature-panel"><div class="temperature-icon">🌡️</div>'
                        f'<div class="temperature-sub">Temperatura média</div>'
                        f'<div class="temperature-main">{valor_media_temp}</div>'
                        f'<div class="temperature-sub">{variavel_y}</div></div>',
                        unsafe_allow_html=True
                    )
                with tc2:
                    valor_max_temp = f"{maxima_temp:.1f} °C" if maxima_temp is not None else "N/D"
                    st.markdown(
                        f'<div class="temperature-panel"><div class="temperature-icon">🔥</div>'
                        f'<div class="temperature-sub">Temperatura máxima</div>'
                        f'<div class="temperature-main">{valor_max_temp}</div>'
                        f'<div class="temperature-sub">{dia_temperatura.strftime("%d/%m/%Y")}</div></div>',
                        unsafe_allow_html=True
                    )
                with tc3:
                    st.markdown(
                        f'<div class="temperature-panel"><div class="temperature-icon">{icone_ceu}</div>'
                        f'<div class="temperature-sub">Contexto de irradiância</div>'
                        f'<div class="temperature-main">{texto_ceu}</div>'
                        f'<div class="temperature-sub">{texto_irrad}</div></div>',
                        unsafe_allow_html=True
                    )

            # --- EXPANDER PARA INSPEÇÃO DA PLANILHA ---
            with st.expander("🔍 Inspecionar Tabela Completa e Dados Brutos"):
                st.dataframe(df, use_container_width=True)

    else:
        st.info("Por favor, carregue a planilha de dados no menu lateral para iniciar o sistema.")
