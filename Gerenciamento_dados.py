from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

class GerenciamentoDados():

    @staticmethod
    def filtrar_ods(cidades_rs, numero_ods):
        municipio = 'MUNICIPIO'
        coluna_score = f'Goal {numero_ods} Score'
        colunas_ods = cidades_rs.filter(like=f'SDG{numero_ods}_').columns
        
        if coluna_score not in cidades_rs.columns:
            print(f"Aviso: Coluna '{coluna_score}' não encontrada.")
            return pd.DataFrame()
        
        return cidades_rs[[municipio, coluna_score] + list(colunas_ods)]    

    @staticmethod
    def main():
        nome_arquivo = 'Base_de_Dados_IDSC-BR_2024.xlsx'
        
        df = pd.read_excel(nome_arquivo, sheet_name='IDSC-BR 2024')
        livro_df = pd.read_excel(nome_arquivo, sheet_name='Livro de Códigos')

        cidades_rs = df.loc[df['SIGLA_UF'] == 'RS'].copy()
        cidades_rs.reset_index(drop=True, inplace=True)

        for i in range(1, 18):
            coluna_para_remover = f'ODS{i}_reg'
            if coluna_para_remover in cidades_rs.columns:
                cidades_rs.drop(columns=coluna_para_remover, inplace=True)

        cidades_rs['MUNICIPIO'] = cidades_rs['MUNICIPIO'].str.strip()

        try:
            numero_ods = int(input('Digite o número da ODS (1-17): '))
            if not 1 <= numero_ods <= 17:
                print("Número da ODS deve estar entre 1 e 17")
                return
        except ValueError:
            print("Por favor, digite um número válido.")
            return

        ods_escolhida = GerenciamentoDados.filtrar_ods(cidades_rs, numero_ods)
        
        ods_escolhida = GerenciamentoDados.limpeza_dados(ods_escolhida)

        ods_escolhida = ods_escolhida.sort_values(by=f'Goal {numero_ods} Score', ascending=False).reset_index(drop=True)

        if not ods_escolhida.empty:
            print(f"\nDados da ODS {numero_ods}:")
            print(ods_escolhida.head(20))
            print(ods_escolhida.tail(20))
            
            santa_cruz = ods_escolhida[ods_escolhida['MUNICIPIO'] == 'Santa Cruz do Sul']
            if not santa_cruz.empty:
                print(f"\nDados da ODS {numero_ods} para Santa Cruz do Sul:")
                print(santa_cruz)
        else:
            print(f"Não foram encontrados dados para a ODS {numero_ods}") 

        ods_grafico = ods_escolhida.head(20)
        tail_grafico = ods_escolhida.tail(20)
        ods_grafico = pd.concat([ods_grafico, tail_grafico], ignore_index=True)

        existe = 'Santa Cruz do Sul' in ods_grafico.values

        if existe is False:    
            ods_grafico = pd.concat([ods_grafico, santa_cruz], ignore_index=True)
        
        ods_grafico = ods_grafico.sort_values(by=f'Goal {numero_ods} Score', ascending=False)
        
        ods_grafico.plot(x='MUNICIPIO', y=[f'Goal {numero_ods} Score'], kind='bar', figsize=(10, 6), color=['#1f77b4', '#ff7f0e'])

        plt.title('Pontuação da ODS')
        plt.ylabel('Puntuação')
        plt.xlabel('Cidade')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.show()
        #time.sleep(5)
        #plt.close()

        municipios = ods_escolhida['MUNICIPIO']
        colunas = ods_escolhida.filter(like='Índice:')
        normalizados = pd.concat([municipios, colunas], axis=1)

        coluna_normalizados = normalizados.columns.tolist()
        tamanho_normalizados = len(normalizados)
        i=1

        while i < tamanho_normalizados:
            titulo = coluna_normalizados[i]
            normalizados = normalizados.sort_values(by=titulo, ascending=False)  
            head_normalizados = normalizados.head(20)
            tail_normalizados = normalizados.tail(20)
            normalizados_grafico = pd.concat([head_normalizados, tail_normalizados], ignore_index=True)

            santa_cruz_normalizados = normalizados[normalizados['MUNICIPIO'] == 'Santa Cruz do Sul']

            if 'Santa Cruz do Sul' not in normalizados_grafico['MUNICIPIO'].values:    
                normalizados_grafico = pd.concat([normalizados_grafico, santa_cruz_normalizados], ignore_index=False)

            normalizados_grafico = normalizados_grafico.sort_values(by=titulo, ascending=False) 

            normalizados_grafico.plot(x='MUNICIPIO', y=titulo, kind='bar', figsize=(10, 6), color=['#1f77b4', '#ff7f0e'])

            plt.title('Pontuação do índice')
            plt.ylabel('Puntuação')
            plt.xlabel('Cidade')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.legend(loc='upper right')
            plt.tight_layout()
            plt.show()
            i+=1
            
        livro_codigos = livro_df[livro_df['ODS'] == numero_ods]

        #with pd.ExcelWriter("DataFrame da ODS.xlsx") as writer:
            #livro_codigos.to_excel(writer, sheet_name= "Livro Códigos.xlsx", index=False)
            #ods_escolhida.to_excel(writer, sheet_name=f"ODS_{numero_ods}_IDSC-BR_2024.xlsx", index=False)

    @staticmethod
    def limpeza_dados(cidades_rs):
        cidades_rs.rename(columns={'Normalizado (0-100): SDG1_1_P_F_CU': 'Índice: Famílias inscritas no Cadastro Único para programas sociais (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG1_3_COBBF': 'Índice: Percentual de pessoas inscritas no Cadastro Único que recebem Bolsa Família'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG1_4_PBF': 'Índice: Percentual de pessoas abaixo da linha da pobreza no Cadastro Único pós Bolsa Família'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG1_4_R_1_4_SM': 'Pessoas com renda de até 1/4 do salário mínimo (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG2_1_OBS_INF': 'Índice: Obesidade infantil (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG2_2_P_NV_BPN': 'Índice: Baixo peso ao nascer (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG2_3_DSNT_INF': 'Índice: Desnutrição infantil (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG2_8_AGR_FAM': 'Índice: Produtores de agricultura familiar com apoio do PRONAF (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG2_9_AGR_ORG': 'Índice: Estabelecimentos que praticam agricultura orgânica (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG3_1_C_VCN': 'Índice: Cobertura vacinal (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG3_13_SCD': 'Índice: Mortalidade por suicídio (100 mil habitantes)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG3_15_T_M_INF': 'Índice: Mortalidade infantil (crianças menores de 1 ano) (mil nascidas vivas)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG3_16_M_MAT': 'Índice: Mortalidade materna (mil nascidos vivos)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG3_17_T_M_5A': 'Índice: Mortalidade na infância (número de óbitos infantis com 0 a 4 anos de idade, por mil nascidos vivos)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG3_18_T_M_NT': 'Índice: Mortalidade neonatal (crianças de 0 a 27 dias) (mil nascidas vivas)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG3_19_T_M_AIDS': 'Índice: Mortalidade por Aids (100 mil habitantes)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG3_2_INC_DNG': 'Índice: Incidência de dengue (100 mil habitantes)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG3_22_T_M_DC': 'Índice: Mortalidade prematura por doenças crônicas não-transmissíveis (100 mil habitantes de 30 a 69 anos)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG3_27_DSP_SAU': 'Índice: Orçamento municipal para a saúde (em reais, per capita)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG3_29_SF': 'Índice: População atendida por equipes de saúde da família (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG3_3_HPT': 'Índice: Detecção de hepatite (100 mil habitantes)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG3_3_P_NV_7PN': 'Índice: Pré-natal insuficiente (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG3_32_UBS': 'Índice: Unidades Básicas de Saúde (mil habitantes)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG3_6_ID_MD_M': 'Índice: Idade média ao morrer'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG3_8_GRV': 'Índice: Gravidez na adolescência (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG3_9_INC_TRB': 'Índice: Incidência de tuberculose (100 mil habitantes)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG4_1_P_EF_INT': 'Índice: Acesso à internet nas escolas do ensino fundamental e médio, na rede pública (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG4_4_PCT_CRECHE': 'Índice: Percentual de crianças de 0 a 3 anos matrículadas em creches'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG4_13_P_E_ACS': 'Índice: Escolas com dependências adequadas a pessoas com deficiência (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG4_14B_P_E_AEE': 'Índice: Escolas com recursos para Atendimento Educacional Especializado (taxa)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG4_15_IDEB_AF': 'Índice: Índice de Desenvolvimento da Educação Básica (IDEB) - anos finais (IN)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG4_16_IDEB_AI': 'Índice: Índice de Desenvolvimento da Educação Básica (IDEB) - anos iniciais (IN)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG4_17_JV_EM': 'Índice: Jovens com ensino médio concluído até os 19 anos de idade (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG4_18_D_SUP_EI': 'Índice: Professores com formação em nível superior - Educação Infantil - rede pública (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG4_19_D_SUP_EF': 'Índice: Professores com formação em nível superior - Ensino Fundamental - rede pública (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG4_26_R_M_D_PE': 'Índice: Razão entre o número de matrículas e professores na pré-escola (taxa)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG4_27_R_M_D_EF': 'Índice: Razão entre o número de matrículas e professores no ensino fundamental (taxa)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG4_3_TDI_EF_RP': 'Índice: Taxa de distorção idade-série no Ensino Fundamental - rede pública'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG4_5_T_AN_15A': 'Índice: Analfabetismo na população com 15 anos ou mais (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG4_6_EQP_CUL': 'Índice: '}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG': 'Índice: Centros culturais, casas e espaços de cultura (100 mil habitantes)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG4_7_FR_E_4A17_AJ': 'Índice: Crianças e jovens de 4 a 17 anos na escola (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG5_3_M_JV_NENT': 'Índice: Mulheres jovens de 15 a 24 anos de idade que não estudam nem trabalham (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG5_4_P_VRDR': 'Índice: Presença de vereadoras na Câmara Municipal (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG5_6_RND_GEN': 'Índice: Desigualdade de salário por sexo (salário de mulheres salário de homens)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG5_7_JV_NENT': 'Índice: Diferença percentual entre jovens mulheres e homens que não estudam e nem trabalham (p.p.)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG5_8_TX_FMNC': 'Índice: Taxa de feminicídio (100 mil mulheres)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG6_1_IN_DRSAI': 'Índice: Doenças relacionadas ao saneamento ambiental inadequado (100 mil habitantes)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG6_4_PRD_AG': 'Índice: Perda de água tratada na distribuição (IN049-SNIS)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG6_7_ESG_SAN': 'Índice: População atendida com esgotamento sanitário (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG6_8_CLT_DML': 'Índice: Índice de tratamento de esgoto (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG6_6_SERV_AG': 'Índice: População total atendida com abastecimento de água (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG7_2_ENRG': 'Índice: Domicílios com acesso à energia elétrica (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG7_3_VNLENER': 'Índice: Vulnerabilidade Energética'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG8_2_OCP_INF': 'Índice: '}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG': 'Índice: População ocupada entre 10 e 17 anos (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG8_2_PIB_CPT': 'Índice: PIB per capita (R$ per capita)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG8_3_T_DSC': 'Índice: Desemprego (taxa)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG8_4_T_DSC_JV': 'Índice: Desemprego de jovens (taxa)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG8_7_P_JV_NENT': 'Índice: Jovens de 15 a 24 anos de idade que não estudam nem trabalham (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG8_9_T_OCUP_FORM': 'Índice: Ocupação formal das pessoas com 16 anos ou mais de idade (taxa)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG9_1_INFRA': 'Índice: Investimento público em infraestrutura urbana por habitante (R$ per capita)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG9_2_EMP_INT': 'Índice: Participação dos empregos formais em atividades intensivas em conhecimento e tecnologia (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG10_1_PREN20': 'Índice: Renda municipal apropriada pelos 20% mais pobres (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG10_2_GINI': 'Índice: Coeficiente de Gini (IN)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG10_20_MINF': 'Índice: Diferença na taxa de mortalidade infantil entre crianças de mães PPI e BA'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG10_21_GRV': 'Índice: Diferença na taxa de gravidez na adolescência entre mães PP e BA'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG10_22_ADER': 'Índice: Diferença na taxa de distorção idade-série nos anos iniciais do Ensino Fundamental entre PP e BA'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG10_23_ADER': 'Índice: Diferença na taxa de distorção idade-série nos anos finais do Ensino Fundamental entre PP e BA'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG10_3_RZHOM': 'Índice: Diferença na taxa de homicídios entre PPI e BA'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG10_DIF_FEM_NNN': 'Índice: Diferença na taxa de feminicídio de mulheres PPI e BA'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG10_HM_JUV_NNN': 'Índice: Diferença na taxa de homicídio juvenil masculino entre jovens PPI e BA'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG10_6_RND_NGR': 'Índice: Razão do rendimento médio real entre PP e BA'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG10_4_ACEQP': 'Índice: Acesso a equipamentos da atenção básica à saúde'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG10_35_VLC_LGBT': 'Índice: Violência contra a população LGBTQIA+ (100 mil habitantes)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG10_PVCM_NNN': 'Índice: Percentual de vereadoras e vereadores PPI nas Câmaras Municipais (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG11_3_VN1H': 'Índice: Percentual da população de baixa renda com tempo de deslocamento ao trabalho superior a uma hora (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG11_33_M_TRNS': 'Índice: Mortes no trânsito (100 mil habitantes)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG11_4_P_P_SUBN': 'Índice: População residente em aglomerados subnormais (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG11_5_DMC_FVL': 'Índice: Domicílios em favelas (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG11_5_EQP_ESP': 'Índice: Equipamentos esportivos municipais (100 mil habitantes)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG11_6_NGR_SUBN': 'Índice: Percentual da população negra em assentamentos subnormais (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG12_2_RSD_SLD': 'Índice: Resíduos sólidos domiciliares coletados per capita (kg/ dia/ hab)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG12_3_RSUREC': 'Índice: Recuperação de resíduos sólidos urbanos coletados seletivamente'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG12_9_CLT_SEL': 'Índice: População atendida com coleta seletiva (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG13_2_CO2': 'Índice: Emissões de CO²e per capita'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG13_3_FCCLR': 'Índice: Concentração de focos de queimadas'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG13_4_PREV': 'Índice: Estratégias para gestão de riscos e prevenção a desastres ambientais'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG13_PDAR': 'Índice: Proporção de domicílios em áreas de risco'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG13_6_TRNS_SL': 'Índice: Percentual do município desflorestado (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG13_6_TRNS_SL': 'Índice: Percentual do município desflorestado (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG14_1_ESGT': 'Índice: Esgoto tratado antes de chegar ao mar, rios e córregos (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG15_2_FLOR': 'Índice: Hectare de áreas florestadas e naturais por habitante'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG15_8_UNI_CNS': 'Índice: Unidades de conservação de proteção integral e uso sustentável (%)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG15_PRTAMB': 'Índice: Grau de maturidade dos instrumentos de financiamento da proteção ambiental'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG16_1_OB_HM': 'Índice: Homicídio juvenil masculino (100 mil habitantes)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG16_4_TX_HMC': 'Índice: Taxa de homicídio (100 mil habitantes)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG16_3_M_ARM_FG': 'Índice: Mortes por armas de fogo (100 mil habitantes)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG16_CRP': 'Índice: Grau de estruturação da política de controle interno e combate à corrupção'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG16_DRTHMN': 'Índice: Grau de estruturação das políticas de participação e promoção de direitos humanos'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG16_TRANSP': 'Índice: Grau de estruturação das políticas de transparência'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG17_1_INVST_PB': 'Índice: Investimento público (R$ per capita)'}, inplace=True)
        cidades_rs.rename(columns={'Normalizado (0-100): SDG17_3_P_RC_TRB': 'Índice: Total de receitas municipais arrecadadas (%)'}, inplace=True)
        
        return cidades_rs
GerenciamentoDados.main()
