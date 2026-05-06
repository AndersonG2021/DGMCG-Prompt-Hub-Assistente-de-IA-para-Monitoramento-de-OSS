"""
=============================================================================
DGMCG - Gerador e Biblioteca de Prompts para IA
Diretoria Geral de Monitoramento de Contratos de Gestão
Secretaria Estadual de Saúde

Autor: Anderson Guilherme Barbosa Cavalcante
Versão: 1.0.4
=============================================================================
"""

import streamlit as st
import pyperclip
from datetime import datetime
import json
import os
import uuid
import pandas as pd
from streamlit_gsheets import GSheetsConnection


# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================================================

st.set_page_config(
    page_title="DGMCG · Biblioteca de Prompts",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# ESTILOS CSS PERSONALIZADOS
# =============================================================================

st.markdown("""
<style>
    /* Importação de fontes */
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

    /* Variáveis de cor — identidade visual institucional (Pernambuco) */
    :root {
        --cor-primaria: #0038A8; /* Azul PE */
        --cor-secundaria: #C8102E; /* Vermelho PE */
        --cor-acento: #009E60; /* Verde PE */
        --cor-alerta: #C8102E; /* Vermelho PE */
        --cor-amarelo: #F1C400; /* Amarelo PE */
        --cor-fundo-card: #FFFFFF;
        --cor-borda: #D0DCE8;
        --cor-texto: #1A2B3C;
        --cor-texto-leve: #5A7080;
    }

    /* Tipografia global */
    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
        color: var(--cor-texto);
    }

    /* Cabeçalho principal */
    .cabecalho-principal {
        background: #FFFFFF;
        color: var(--cor-primaria);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid var(--cor-borda);
        border-top: 6px solid;
        border-image: linear-gradient(to right, #0038A8 25%, #FFFFFF 25%, #FFFFFF 35%, #C8102E 35%, #C8102E 65%, #F1C400 65%, #F1C400 85%, #009E60 85%) 1;
        box-shadow: 0 4px 12px rgba(0, 56, 168, 0.08);
    }

    .cabecalho-principal h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.02em;
    }
    
    .cabecalho-principal h1 span {
        color: var(--cor-primaria);
    }

    .cabecalho-principal p {
        margin: 0;
        font-size: 1rem;
        color: var(--cor-texto-leve);
        font-weight: 400;
    }

    /* Cards de prompt */
    .card-prompt {
        background: var(--cor-fundo-card);
        border: 1px solid var(--cor-borda);
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid var(--cor-secundaria);
        transition: box-shadow 0.2s ease;
    }

    .card-prompt:hover {
        box-shadow: 0 4px 16px rgba(0, 63, 114, 0.12);
    }

    .card-prompt h4 {
        color: var(--cor-primaria);
        font-size: 1rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
    }

    .card-prompt p {
        font-size: 0.85rem;
        color: var(--cor-texto-leve);
        margin: 0 0 1rem 0;
    }

    /* Badge de categoria */
    .badge-categoria {
        display: inline-block;
        background: #E0ECF8;
        color: var(--cor-primaria);
        font-size: 0.72rem;
        font-weight: 600;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.8rem;
    }

    /* Caixa de texto do prompt */
    .caixa-prompt {
        background: #FFFFFF;
        border: 1px solid var(--cor-borda);
        border-radius: 8px;
        padding: 1rem 1.2rem;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.82rem;
        line-height: 1.7;
        color: #2C3E50;
        white-space: pre-wrap;
        word-break: break-word;
    }

    /* Aviso de segurança na sidebar */
    .aviso-seguranca {
        background: #FFF3E0;
        border: 1px solid #FFB74D;
        border-radius: 8px;
        padding: 1rem;
        font-size: 0.82rem;
        line-height: 1.6;
        color: #5D4037;
        border-left: 4px solid var(--cor-alerta);
    }

    .aviso-seguranca strong {
        color: var(--cor-alerta);
        font-size: 0.85rem;
    }

    /* Resultado do construtor */
    .resultado-builder {
        background: #F4F7FB;
        border: 1px solid var(--cor-borda);
        border-radius: 10px;
        padding: 1.5rem;
        border-left: 5px solid var(--cor-acento);
    }

    .resultado-builder h4 {
        color: var(--cor-acento);
        margin: 0 0 1rem 0;
        font-size: 1rem;
    }

    /* Rodapé */
    .rodape {
        text-align: center;
        font-size: 0.75rem;
        color: var(--cor-texto-leve);
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid var(--cor-borda);
    }

    /* Ajuste nos botões do Streamlit */
    .stButton > button {
        background-color: var(--cor-primaria);
        color: white;
        border: none;
        border-radius: 6px;
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 500;
        padding: 0.45rem 1.2rem;
        transition: background 0.2s ease;
    }

    .stButton > button:hover {
        background-color: var(--cor-secundaria);
        color: white;
    }

    /* Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        border-bottom: 2px solid var(--cor-borda);
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 500;
        padding: 0.6rem 1.2rem;
        border-radius: 6px 6px 0 0;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# DADOS: BIBLIOTECA DE PROMPTS PRÉ-PRONTOS
# =============================================================================

PROMPTS_BIBLIOTECA = [
    {
        "id": "analise_prestacao_contas",
        "categoria": "Prestação de Contas",
        "titulo": "Análise de Relatório de Prestação de Contas",
        "descricao": "Análise técnica completa do relatório financeiro e operacional mensal de uma OSS.",
        "texto": """Aja como um Analista Sênior de Contratos de Gestão da Secretaria Estadual de Saúde, com profundo conhecimento em legislação de saúde pública, controle interno e governança de Organizações Sociais de Saúde (OSS).

**Tarefa:**
Realize uma análise técnica criteriosa do Relatório de Prestação de Contas referente ao mês de [MÊS DE REFERÊNCIA] da OSS [NOME DA OSS], gestora do equipamento [NOME DO EQUIPAMENTO DE SAÚDE].

**Contexto:**
O relatório foi apresentado à Diretoria Geral de Monitoramento de Contratos de Gestão (DGMCG) dentro do prazo legal estabelecido no Contrato de Gestão nº [NÚMERO DO CONTRATO]. O documento contempla o período de [DATA INÍCIO] a [DATA FIM].

**Execute as seguintes análises, nesta ordem:**

1. **Conformidade Documental:** Verifique se todos os anexos obrigatórios estão presentes (balancete, folha de pagamento, notas fiscais, relatório de produção), apontando qualquer documento ausente ou incompleto.

2. **Análise Financeira:** Examine a execução orçamentária em relação ao repasse previsto de R$ [VALOR DO REPASSE], identificando desvios acima de 5%, classificando as despesas por natureza (pessoal, custeio, capital) e sinalizando gastos sem cobertura contratual.

3. **Conformidade Legal:** Avalie a aderência às normas da Lei Federal nº 9.637/1998, às Instruções Normativas do TCE/[UF] aplicáveis e às cláusulas específicas do Contrato de Gestão vigente.

4. **Pontos de Atenção:** Liste de forma numerada todas as irregularidades, inconsistências ou itens que demandam esclarecimento, com o respectivo grau de criticidade (Alta / Média / Baixa).

5. **Recomendação Final:** Emita um parecer técnico indicando se a prestação de contas deve ser: (a) aprovada sem ressalvas, (b) aprovada com ressalvas, ou (c) devolvida para saneamento, justificando cada opção.

**Formato de saída:**
Estruture a resposta em seções numeradas com subtítulos em negrito. Utilize tabelas para comparativos financeiros. Seja objetivo e técnico, evitando linguagem ambígua. Não faça suposições sobre valores ou documentos não fornecidos."""
    },
    {
        "id": "avaliacao_metas_assistenciais",
        "categoria": "Metas Assistenciais",
        "titulo": "Avaliação de Cumprimento de Metas Assistenciais",
        "descricao": "Avaliação quantitativa e qualitativa do atingimento de metas de produção e qualidade assistencial.",
        "texto": """Aja como um Especialista em Avaliação de Desempenho de Serviços de Saúde, com experiência em indicadores assistenciais do SUS, metodologia de contratualização e análise de séries históricas de produção hospitalar e ambulatorial.

**Tarefa:**
Analise o desempenho da OSS [NOME DA OSS] no cumprimento das metas assistenciais pactuadas no Contrato de Gestão nº [NÚMERO DO CONTRATO] para o período de [MÊS/ANO DE REFERÊNCIA].

**Contexto:**
O equipamento gerido é [NOME DO EQUIPAMENTO], com perfil assistencial [PERFIL: ex. Hospital Geral de Média Complexidade / UPA / AME]. Os dados de produção foram extraídos do sistema [SISTEMA: ex. SIHD/SUS, prontuário eletrônico, relatório gerencial interno].

**Metas pactuadas para análise:**
- Consultas ambulatoriais: Meta = [VALOR META] | Realizado = [VALOR REALIZADO]
- Internações clínicas: Meta = [VALOR META] | Realizado = [VALOR REALIZADO]
- Cirurgias eletivas: Meta = [VALOR META] | Realizado = [VALOR REALIZADO]
- Taxa de ocupação de leitos: Meta = [%] | Realizado = [%]
- Tempo médio de espera na urgência: Meta = [MINUTOS] | Realizado = [MINUTOS]
- Indicador de qualidade ([NOME DO INDICADOR]): Meta = [VALOR] | Realizado = [VALOR]

**Análise solicitada:**

1. **Dashboard de Desempenho:** Construa uma tabela com todas as metas acima, calculando o percentual de execução de cada uma e classificando o resultado como: ✅ Cumprida (≥95%), ⚠️ Parcial (75–94%), ou ❌ Descumprida (<75%).

2. **Análise de Tendência:** Compare os resultados do mês atual com os dois meses anteriores ([MÊS -1] e [MÊS -2]), identificando se há tendência de melhora, estabilidade ou deterioração.

3. **Impacto Financeiro:** Com base no mecanismo de pagamento por desempenho do contrato, calcule o eventual desconto ou glosa financeira aplicável ao descumprimento de metas, conforme parâmetros do Anexo [NÚMERO DO ANEXO] do contrato.

4. **Causas e Justificativas:** Se a OSS apresentou justificativas formais para o descumprimento, avalie a pertinência de cada uma e classifique como: aceita, parcialmente aceita ou rejeitada, com fundamentação técnica.

5. **Plano de Ação:** Sugira as recomendações que devem constar na notificação formal à OSS para recuperação das metas nos próximos dois meses.

**Formato de saída:**
Responda com tabelas, análise narrativa por seção e bullet points nas recomendações. Não invente dados de produção; trabalhe apenas com os valores fornecidos acima."""
    },
    {
        "id": "elaboracao_despacho",
        "categoria": "Documentos Oficiais",
        "titulo": "Elaboração de Despacho Administrativo ou Termo de Quitação",
        "descricao": "Redação de documentos administrativos formais para encerramento ou tramitação de processos de contratos de gestão.",
        "texto": """Aja como um Assessor Jurídico-Administrativo especializado em Direito Administrativo Sanitário, com experiência na redação de documentos oficiais para órgãos da Administração Pública Estadual, incluindo despachos, pareceres, termos e ofícios relacionados a contratos de gestão com entidades do Terceiro Setor.

**Tarefa:**
Redija um [TIPO DE DOCUMENTO: Despacho Administrativo / Termo de Quitação / Notificação Extrajudicial / Ofício de Regularização] referente ao processo SEI nº [NÚMERO DO PROCESSO SEI] envolvendo a OSS [NOME DA OSS].

**Contexto do documento:**
- **Equipamento de saúde:** [NOME DO EQUIPAMENTO]
- **Contrato de Gestão nº:** [NÚMERO DO CONTRATO], celebrado em [DATA DE CELEBRAÇÃO]
- **Competência de referência:** [MÊS/ANO]
- **Motivo/Objeto:** [DESCREVA O MOTIVO: ex. quitação da prestação de contas do mês X após aprovação sem ressalvas / notificação por descumprimento da meta Y / encerramento de diligência]
- **Autoridade signatária:** [CARGO E NOME DO SERVIDOR: ex. Diretor(a) da DGMCG]
- **Destinatário:** [CARGO E NOME DO REPRESENTANTE DA OSS]

**Requisitos de redação:**

1. Utilize linguagem formal, clara e objetiva, conforme o Manual de Redação Oficial da Presidência da República (3ª edição) e as normas de comunicação administrativa do Estado de [UF].
2. Estruture o documento com: cabeçalho institucional, ementa, corpo do texto com fundamentos legais explícitos (citando artigos pertinentes da Lei nº 9.637/1998 e do Contrato de Gestão), dispositivo (decisão ou encaminhamento) e fecho.
3. Fundamente cada afirmação em dispositivos legais ou cláusulas contratuais específicas — não faça afirmações jurídicas sem embasamento.
4. O tom deve ser institucional e imparcial, sem linguagem subjetiva ou valorativa sobre a OSS.
5. Ao final do documento, indique entre colchetes os campos que ainda precisam ser preenchidos pelo servidor responsável.

**Formato de saída:**
Entregue o documento completo e formatado, pronto para revisão e assinatura. Logo abaixo, inclua uma seção separada intitulada "⚠️ Campos para Revisão" listando todos os dados que precisam ser confirmados antes da assinatura oficial."""
    },
    {
        "id": "mapeamento_bpmn",
        "categoria": "Processos e Auditoria",
        "titulo": "Mapeamento e Modelagem de Fluxos BPMN para Auditoria de Contratos",
        "descricao": "Estruturação de fluxos de processos em notação BPMN para subsídio de auditorias e revisões de processos de trabalho.",
        "texto": """Aja como um Analista de Processos e Negócios (BPM Specialist) com certificação CBPP e experiência em mapeamento de processos para órgãos públicos de saúde, com domínio da notação BPMN 2.0 e das melhores práticas de governança de processos do setor público.

**Tarefa:**
Realize o mapeamento e a modelagem do processo de [NOME DO PROCESSO: ex. "Monitoramento Mensal de Metas Assistenciais" / "Análise e Aprovação de Prestação de Contas" / "Tratamento de Inconformidades em Contratos de Gestão"] com o objetivo de subsidiar a auditoria interna da DGMCG e identificar gargalos, riscos operacionais e oportunidades de melhoria.

**Contexto organizacional:**
- **Diretoria responsável:** Diretoria Geral de Monitoramento de Contratos de Gestão (DGMCG)
- **Partes envolvidas (pools/lanes):** [LISTE OS ATORES: ex. Técnico de Monitoramento, Coordenador de Área, OSS, Assessoria Jurídica, Diretoria]
- **Sistema(s) de informação utilizados:** [SISTEMAS: ex. SEI, SIHD, e-Saúde, planilhas internas]
- **Periodicidade do processo:** [PERIODICIDADE: ex. Mensal / Trimestral / Sob demanda]
- **Ponto de início:** [EVENTO DE INÍCIO: ex. Recebimento do relatório mensal da OSS]
- **Ponto de fim:** [EVENTO DE FIM: ex. Publicação do resultado no portal da transparência / Arquivamento no SEI]

**Entregáveis solicitados:**

1. **Descrição Narrativa (AS-IS):** Descreva o fluxo atual do processo em linguagem natural, passo a passo, com os atores responsáveis por cada atividade.

2. **Estrutura BPMN em Texto:** Como não é possível renderizar diagramas aqui, represente o fluxo em formato textual estruturado, indicando:
   - Eventos de início e fim (círculos)
   - Tarefas (retângulos) com o ator responsável entre colchetes
   - Gateways de decisão (losangos) com as condições de cada caminho
   - Fluxos de sequência e de mensagem entre pools

3. **Identificação de Riscos e Gargalos:** Liste os pontos críticos do processo atual, classificando cada risco por: probabilidade (Alta/Média/Baixa) e impacto (Alto/Médio/Baixo), com uma descrição do risco operacional ou de conformidade.

4. **Recomendações de Melhoria (TO-BE):** Proponha no mínimo 3 melhorias concretas para o fluxo, indicando qual atividade seria alterada, suprimida ou automatizada, e qual o ganho esperado (tempo, conformidade, rastreabilidade).

5. **Indicadores de Desempenho do Processo (KPIs):** Sugira 3 KPIs mensuráveis para monitorar a eficiência e conformidade do processo após a implementação das melhorias.

**Formato de saída:**
Utilize seções numeradas com subtítulos em negrito. Para a estrutura BPMN textual, use recuo e símbolos (→, ◇, ○, □) para simular a notação visual. Não invente etapas que não foram descritas no contexto fornecido; indique com [A CONFIRMAR] onde informações estiverem faltando."""
    },
]

def carregar_prompts_customizados():
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # O ttl=0 garante que sempre lerá o dado mais atual da planilha sem usar cache
        df = conn.read(ttl=0)
        df = df.fillna("")
        
        # Filtra caso a planilha traga linhas vazias a mais
        if "ID" in df.columns:
            df = df[df["ID"] != ""]
        
        # O código antigo espera dicionários com chaves em minúsculo
        # A planilha do Google Sheets tem cabeçalhos em maiúsculo (ID, CATEGORIA, etc.)
        prompts = []
        for _, row in df.iterrows():
            prompts.append({
                "id": str(row.get("ID", "")),
                "categoria": str(row.get("CATEGORIA", "")),
                "titulo": str(row.get("TITULO", "")),
                "descricao": str(row.get("DESCRICAO", "")),
                "texto": str(row.get("TEXTO", ""))
            })
        return prompts
    except Exception as e:
        import traceback
        st.error(f"Erro silencioso ao carregar planilha: {e}")
        st.code(traceback.format_exc(), language="python")
        return []

def salvar_prompt_customizado(prompt_dict):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_existente = conn.read(ttl=0)
        
        # Cria um novo registro mapeando para os cabeçalhos maiúsculos da planilha
        novo_registro = {
            "ID": prompt_dict.get("id", ""),
            "CATEGORIA": prompt_dict.get("categoria", ""),
            "TITULO": prompt_dict.get("titulo", ""),
            "DESCRICAO": prompt_dict.get("descricao", ""),
            "TEXTO": prompt_dict.get("texto", "")
        }
        
        df_novo = pd.DataFrame([novo_registro])
        df_atualizado = pd.concat([df_existente, df_novo], ignore_index=True)
        
        # Atualiza a planilha no Google Drive
        conn.update(data=df_atualizado)
    except Exception as e:
        import traceback
        st.error(f"Erro ao salvar na planilha do Google Sheets: {e}")
        st.error(f"Detalhes do erro: {repr(e)}")
        st.code(traceback.format_exc(), language="python")


# =============================================================================
# SIDEBAR — AVISO DE SEGURANÇA E INFORMAÇÕES
# =============================================================================

def renderizar_sidebar():
    """Renderiza o painel lateral com avisos de segurança e informações da aplicação."""

    with st.sidebar:
        # Logotipo / identidade
        st.markdown("""
        <div style="text-align:center; padding: 1rem 0 0.5rem 0;">
            <div style="font-size:3rem; font-weight:800; color:#0038A8; letter-spacing:0.05em; margin-bottom: 0.2rem;">
                DGMCG
            </div>
            <div style="font-size:0.85rem; font-weight:600; color:#1A2B3C; letter-spacing:0.05em;">
                GERADOR DE PROMPTS
            </div>
            <div style="font-size:0.72rem; color:#5A7080; margin-top: 0.2rem;">
                Secretaria Estadual de Saúde
            </div>
        </div>
        <hr style="border:none; border-top:1px solid #D0DCE8; margin: 0.8rem 0;">
        """, unsafe_allow_html=True)

        # Aviso de segurança permanente
        st.markdown("""
        <div class="aviso-seguranca">
            <strong>🔒 Diretrizes de Segurança e Privacidade</strong><br><br>
            Ao utilizar ferramentas de IA, observe obrigatoriamente:
            <ul style="margin: 0.5rem 0 0 0; padding-left: 1.2rem;">
                <li>🚫 Não insira <strong>dados de pacientes</strong> (nome, CPF, prontuário, diagnóstico)</li>
                <li>🚫 Não inclua <strong>informações sigilosas</strong> da Secretaria de Saúde ou de terceiros</li>
                <li>🚫 Não cole <strong>documentos classificados</strong> ou com restrição de acesso</li>
                <li>✅ Use apenas <strong>dados anonimizados</strong> ou de domínio público</li>
                <li>✅ Substitua dados reais por <strong>placeholders genéricos</strong></li>
            </ul>
            <br>
            <span style="font-size:0.75rem; color:#795548;">
                ⚖️ Em conformidade com a LGPD (Lei nº 13.709/2018) e as políticas de segurança da informação da SES.
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border:none; border-top:1px solid #D0DCE8; margin: 1rem 0;'>",
                    unsafe_allow_html=True)

        # Informações da aplicação
        st.markdown(f"""
        <div style="font-size:0.75rem; color:#5A7080; line-height:1.8;">
            <strong style="color:#0038A8;">Sobre esta ferramenta</strong><br>
            Versão: 1.0.4<br>
            Uso interno — DGMCG/SES<br>
            Atualizado: {datetime.now().strftime('%d/%m/%Y')}
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# MÓDULO 1: BIBLIOTECA DE PROMPTS
# =============================================================================

def renderizar_biblioteca():
    """Renderiza o módulo de Biblioteca de Prompts pré-prontos."""

    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <h3 style="color:#0038A8; margin:0 0 0.3rem 0;">📚 Biblioteca de Prompts</h3>
        <p style="color:#5A7080; font-size:0.9rem; margin:0;">
            Prompts técnicos pré-elaborados para as principais atividades da diretoria.
            Copie, ajuste os placeholders e cole na ferramenta de IA.
        </p>
    </div>
    """, unsafe_allow_html=True)

    prompts_totais = PROMPTS_BIBLIOTECA + carregar_prompts_customizados()

    # Filtro por categoria
    categorias = ["Todas"] + sorted(list(set(p["categoria"] for p in prompts_totais)))
    categoria_selecionada = st.selectbox(
        "🔍 Filtrar por categoria:",
        categorias,
        key="filtro_categoria"
    )

    # Filtra os prompts de acordo com a categoria selecionada
    prompts_filtrados = (
        prompts_totais
        if categoria_selecionada == "Todas"
        else [p for p in prompts_totais if p["categoria"] == categoria_selecionada]
    )

    st.markdown(
        f"<p style='font-size:0.82rem; color:#5A7080; margin-bottom:1rem;'>"
        f"Exibindo {len(prompts_filtrados)} prompt(s)</p>",
        unsafe_allow_html=True
    )

    # Renderiza cada prompt em seu card
    for prompt in prompts_filtrados:
        _renderizar_card_prompt(prompt)


def _renderizar_card_prompt(prompt: dict):
    """
    Renderiza um único card de prompt com título, descrição,
    texto completo expansível e botão de cópia.
    """
    with st.container():
        st.markdown(f"""
        <div class="card-prompt">
            <span class="badge-categoria">{prompt['categoria']}</span>
            <h4>{prompt['titulo']}</h4>
            <p>{prompt['descricao']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Expansor com o texto completo do prompt
        with st.expander("👁️ Visualizar prompt completo", expanded=False):
            st.markdown(
                f"<div class='caixa-prompt'>{prompt['texto']}</div>",
                unsafe_allow_html=True
            )

            # Campo de texto oculto para facilitar a cópia via botão nativo do Streamlit
            st.text_area(
                label="Texto para cópia:",
                value=prompt["texto"],
                height=200,
                key=f"textarea_{prompt['id']}",
                help="Selecione todo o texto (Ctrl+A) e copie (Ctrl+C), "
                     "ou use o botão abaixo."
            )

            # Botão de cópia via pyperclip (funciona em ambiente local)
            if st.button(f"📋 Copiar Prompt", key=f"btn_copiar_{prompt['id']}"):
                try:
                    pyperclip.copy(prompt["texto"])
                    st.success("✅ Prompt copiado para a área de transferência!")
                except Exception:
                    # pyperclip pode não funcionar em todos os servidores;
                    # nesse caso, orienta o usuário a copiar manualmente.
                    st.info(
                        "💡 Selecione o texto acima, pressione **Ctrl+A** e depois **Ctrl+C** "
                        "para copiar manualmente."
                    )

        st.markdown("<hr style='border:none; border-top:1px solid #E8EEF4;'>",
                    unsafe_allow_html=True)


# =============================================================================
# MÓDULO 2: CONSTRUTOR DE PROMPTS (PROMPT BUILDER)
# =============================================================================

SUGESTOES = {
    "papel": [
        "Personalizado (digite abaixo)...",
        "Aja como um Auditor Sênior em Saúde Pública com 15 anos de experiência em fiscalização de contratos de gestão com OSS.",
        "Aja como um Analista Financeiro especializado em contas públicas e auditoria do SUS.",
        "Aja como um Assessor Jurídico-Administrativo especializado em Direito Administrativo Sanitário.",
        "Aja como um Especialista em Avaliação de Desempenho de Serviços de Saúde, com experiência em indicadores assistenciais do SUS."
    ],
    "tarefa": [
        "Personalizado (digite abaixo)...",
        "Analise o relatório de prestação de contas da OSS [NOME DA OSS] referente ao mês de [MÊS], identifique inconsistências financeiras e emita um parecer técnico.",
        "Avalie o cumprimento das metas assistenciais do equipamento [NOME DO EQUIPAMENTO], indicando o percentual de atingimento e possíveis justificativas.",
        "Redija um Despacho Administrativo formalizando a aprovação da prestação de contas com base nos dados fornecidos.",
        "Realize o mapeamento do processo descrito e identifique possíveis gargalos e riscos de conformidade."
    ],
    "contexto": [
        "Personalizado (digite abaixo)...",
        "O equipamento em questão é um Hospital Geral de Média Complexidade com 200 leitos. O contrato de gestão vigente é o de nº [NÚMERO]. O repasse mensal é de R$ [VALOR].",
        "A OSS tem histórico de atrasos na entrega dos relatórios mensais. Houve autuação do TCE no mês anterior por incompletude de documentos.",
        "Os dados de produção foram extraídos do sistema SIHD/SUS e do prontuário eletrônico. A meta pactuada foi revisada no último aditivo contratual."
    ],
    "restricoes": [
        "Personalizado (digite abaixo)...",
        "- Não invente dados financeiros ou valores não fornecidos\n- Não emita opiniões sobre a competência da gestão da OSS\n- Não utilize linguagem informal ou subjetiva\n- Não faça referências a legislação federal sem verificar a aplicabilidade estadual",
        "- Baseie-se apenas nas informações fornecidas no contexto.\n- Caso falte algum dado essencial, indique a lacuna em vez de presumir.",
        "- Não cite nomes de pacientes ou dados sensíveis.\n- Mantenha a estrita observância à LGPD e normativas da SES."
    ],
    "exemplos": [
        "Personalizado (digite abaixo)...",
        "O parecer deve seguir o modelo:\n'Diante da análise realizada, conclui-se que... recomenda-se...'",
        "Baseie-se nas diretrizes do Manual de Monitoramento de Contratos de Gestão da SES.",
        "Estruture a análise como a Matriz SWOT (Forças, Fraquezas, Oportunidades, Ameaças)."
    ]
}

def aplicar_sugestao(chave_sugestao, chave_texto):
    sugestao = st.session_state.get(chave_sugestao, "")
    if sugestao and sugestao != "Personalizado (digite abaixo)...":
        st.session_state[chave_texto] = sugestao

def renderizar_construtor():
    """Renderiza o módulo interativo de construção de prompts do zero."""

    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <h3 style="color:#0038A8; margin:0 0 0.3rem 0;">🛠️ Construtor de Prompts</h3>
        <p style="color:#5A7080; font-size:0.9rem; margin:0;">
            Preencha os campos abaixo para gerar um prompt estruturado e otimizado,
            garantindo que a IA retorne exatamente o que você precisa.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ---- Formulário em colunas ----
    col_esq, col_dir = st.columns([1, 1], gap="large")

    with col_esq:
        st.markdown("#### 👤 Passo 1 — Papel / Persona da IA")
        st.selectbox(
            "💡 Sugestões rápidas:", 
            SUGESTOES["papel"], 
            key="sugestao_papel", 
            on_change=aplicar_sugestao, 
            args=("sugestao_papel", "builder_papel")
        )
        papel = st.text_area(
            label="Defina o papel que a IA deve assumir:",
            placeholder=(
                "Ex: Aja como um Auditor Sênior em Saúde Pública com 15 anos de experiência "
                "em fiscalização de contratos de gestão com OSS, especializado em análise "
                "financeira e conformidade legal."
            ),
            height=130,
            key="builder_papel",
            help="Quanto mais específico o papel, mais precisa e confiável será a resposta da IA."
        )

        st.markdown("#### 🎯 Passo 2 — Tarefa Principal")
        st.selectbox(
            "💡 Sugestões rápidas:", 
            SUGESTOES["tarefa"], 
            key="sugestao_tarefa", 
            on_change=aplicar_sugestao, 
            args=("sugestao_tarefa", "builder_tarefa")
        )
        tarefa = st.text_area(
            label="Descreva claramente o que a IA deve fazer:",
            placeholder=(
                "Ex: Analise o relatório de prestação de contas da OSS [NOME DA OSS] "
                "referente ao mês de [MÊS], identifique inconsistências financeiras e "
                "emita um parecer técnico sobre a aprovação ou não do documento."
            ),
            height=130,
            key="builder_tarefa",
            help="Use verbos de ação claros: analise, elabore, avalie, classifique, redija..."
        )

        st.markdown("#### 🗂️ Passo 3 — Contexto e Informações de Fundo")
        st.selectbox(
            "💡 Sugestões rápidas:", 
            SUGESTOES["contexto"], 
            key="sugestao_contexto", 
            on_change=aplicar_sugestao, 
            args=("sugestao_contexto", "builder_contexto")
        )
        contexto = st.text_area(
            label="Forneça o contexto necessário para a IA entender o problema:",
            placeholder=(
                "Ex: O equipamento em questão é um Hospital Geral de Média Complexidade "
                "com 200 leitos. O contrato de gestão vigente é o de nº [NÚMERO], "
                "celebrado em [ANO]. O repasse mensal é de R$ [VALOR]. "
                "Houve autuação do TCE no mês anterior por incompletude de documentos."
            ),
            height=150,
            key="builder_contexto",
            help=(
                "Inclua apenas informações não sigilosas. "
                "Substitua dados reais por placeholders como [NOME DA OSS], [VALOR]."
            )
        )

    with col_dir:
        st.markdown("#### 📄 Passo 4 — Formato de Saída Esperado")
        formato_opcao = st.selectbox(
            "Escolha o formato principal da resposta:",
            options=[
                "Relatório técnico com seções numeradas",
                "Tabela comparativa",
                "Texto formal (ofício/despacho)",
                "Lista de bullet points",
                "JSON estruturado",
                "Passo a passo numerado",
                "Resumo executivo (máx. 1 página)",
                "Outro (especifique abaixo)",
            ],
            key="builder_formato_opcao"
        )

        formato_detalhes = st.text_input(
            label="Detalhes adicionais sobre o formato (opcional):",
            placeholder="Ex: com colunas 'Meta', 'Realizado', '% Execução', 'Status'",
            key="builder_formato_detalhes"
        )

        # Constrói string de formato combinada
        formato = formato_opcao
        if formato_detalhes.strip():
            formato = f"{formato_opcao} — {formato_detalhes.strip()}"

        st.markdown("#### 🚫 Passo 5 — Restrições e Limites")
        st.selectbox(
            "💡 Sugestões rápidas:", 
            SUGESTOES["restricoes"], 
            key="sugestao_restricoes", 
            on_change=aplicar_sugestao, 
            args=("sugestao_restricoes", "builder_restricoes")
        )
        restricoes = st.text_area(
            label="O que a IA NÃO deve fazer:",
            placeholder=(
                "Ex:\n"
                "- Não invente dados financeiros ou valores não fornecidos\n"
                "- Não emita opiniões sobre a competência da gestão da OSS\n"
                "- Não utilize linguagem informal ou subjetiva\n"
                "- Não faça referências a legislação federal sem verificar a aplicabilidade estadual"
            ),
            height=150,
            key="builder_restricoes",
            help="Restrições bem definidas evitam alucinações e respostas inadequadas ao contexto público."
        )

        st.markdown("#### ✨ Opcional — Exemplos ou Referências")
        st.selectbox(
            "💡 Sugestões rápidas:", 
            SUGESTOES["exemplos"], 
            key="sugestao_exemplos", 
            on_change=aplicar_sugestao, 
            args=("sugestao_exemplos", "builder_exemplos")
        )
        exemplos = st.text_area(
            label="Exemplos de saída desejada ou referências (opcional):",
            placeholder=(
                "Ex: O parecer deve seguir o modelo abaixo:\n"
                "'Diante da análise realizada, conclui-se que... recomenda-se...'\n\n"
                "Ou: Baseie-se nas diretrizes do Manual de Monitoramento de Contratos de Gestão da SES."
            ),
            height=120,
            key="builder_exemplos"
        )

    # ---- Geração do Prompt ----
    st.markdown("<br>", unsafe_allow_html=True)

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        gerar = st.button("⚡ Gerar Prompt Otimizado", use_container_width=True)

    if 'prompt_gerado' not in st.session_state:
        st.session_state.prompt_gerado = ""

    if gerar:
        # Validação mínima: papel e tarefa são obrigatórios
        campos_vazios = []
        if not papel.strip():
            campos_vazios.append("Papel / Persona")
        if not tarefa.strip():
            campos_vazios.append("Tarefa Principal")

        if campos_vazios:
            st.warning(
                f"⚠️ Preencha os campos obrigatórios: **{', '.join(campos_vazios)}**"
            )
        else:
            st.session_state.prompt_gerado = _montar_prompt(papel, tarefa, contexto, formato, restricoes, exemplos)

    if st.session_state.prompt_gerado:
        _exibir_resultado(st.session_state.prompt_gerado)


def _montar_prompt(
    papel: str,
    tarefa: str,
    contexto: str,
    formato: str,
    restricoes: str,
    exemplos: str
) -> str:
    """
    Concatena as partes do formulário em uma estrutura de prompt
    otimizada para LLMs, seguindo as melhores práticas de engenharia de prompts.
    """
    partes = []

    # Seção 1: Papel / Persona
    partes.append(f"## PAPEL\n{papel.strip()}")

    # Seção 2: Tarefa
    partes.append(f"## TAREFA\n{tarefa.strip()}")

    # Seção 3: Contexto (apenas se preenchido)
    if contexto.strip():
        partes.append(f"## CONTEXTO\n{contexto.strip()}")

    # Seção 4: Formato de saída
    if formato.strip():
        partes.append(
            f"## FORMATO DE SAÍDA\n"
            f"Estruture sua resposta no seguinte formato: {formato.strip()}"
        )

    # Seção 5: Restrições (apenas se preenchidas)
    if restricoes.strip():
        partes.append(
            f"## RESTRIÇÕES\n"
            f"Ao elaborar sua resposta, observe obrigatoriamente os seguintes limites:\n"
            f"{restricoes.strip()}"
        )

    # Seção 6: Exemplos / Referências (apenas se preenchidos)
    if exemplos.strip():
        partes.append(f"## REFERÊNCIAS E EXEMPLOS\n{exemplos.strip()}")

    # Instrução final de ancoragem
    partes.append(
        "## INSTRUÇÃO FINAL\n"
        "Baseie-se estritamente nas informações fornecidas acima. "
        "Caso alguma informação necessária para a execução da tarefa não tenha sido fornecida, "
        "indique claramente entre colchetes: [INFORMAÇÃO NECESSÁRIA: descreva o que falta]. "
        "Não preencha lacunas com suposições ou dados inventados."
    )

    return "\n\n---\n\n".join(partes)


def _exibir_resultado(prompt_gerado: str):
    """Exibe o prompt gerado em uma caixa formatada com opção de cópia."""

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="resultado-builder">
        <h4>✅ Prompt Gerado com Sucesso</h4>
    </div>
    """, unsafe_allow_html=True)

    st.text_area(
        label="📋 Seu prompt otimizado (selecione tudo e copie):",
        value=prompt_gerado,
        height=400,
        key="resultado_prompt"
    )

    col_a, col_b = st.columns([1, 3])

    with col_a:
        if st.button("📋 Copiar para Área de Transferência", use_container_width=True):
            try:
                pyperclip.copy(prompt_gerado)
                st.success("✅ Copiado!")
            except Exception:
                st.info("💡 Selecione o texto acima e pressione **Ctrl+A → Ctrl+C**.")

    # Contadores informativos
    qtd_palavras = len(prompt_gerado.split())
    qtd_chars = len(prompt_gerado)

    st.markdown(
        f"<p style='font-size:0.78rem; color:#5A7080; margin-top:0.5rem;'>"
        f"📊 {qtd_palavras} palavras · {qtd_chars} caracteres · "
        f"~{qtd_chars // 4} tokens estimados</p>",
        unsafe_allow_html=True
    )

    st.markdown("<hr style='border:none; border-top:1px solid #D0DCE8; margin: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("#### 💾 Salvar na Biblioteca")
    st.markdown("<p style='font-size:0.9rem; color:#5A7080;'>Salve este prompt para utilizá-lo posteriormente na aba <b>Biblioteca de Prompts</b>.</p>", unsafe_allow_html=True)
    
    with st.form("form_salvar_prompt"):
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            novo_titulo = st.text_input("Título do Prompt *", placeholder="Ex: Avaliação de Metas")
            nova_categoria = st.text_input("Categoria *", placeholder="Ex: Metas Assistenciais")
        with col_c2:
            nova_descricao = st.text_area("Descrição (breve)", placeholder="Ex: Avaliação quantitativa de desempenho.")
        
        btn_salvar = st.form_submit_button("Salvar Prompt")
        
        if btn_salvar:
            if novo_titulo.strip() and nova_categoria.strip():
                novo_id = str(uuid.uuid4())
                novo_prompt = {
                    "id": novo_id,
                    "categoria": nova_categoria.strip(),
                    "titulo": novo_titulo.strip(),
                    "descricao": nova_descricao.strip(),
                    "texto": prompt_gerado
                }
                salvar_prompt_customizado(novo_prompt)
                st.success("✅ Prompt salvo com sucesso na Biblioteca!")
            else:
                st.error("⚠️ Título e Categoria são obrigatórios para salvar.")


# =============================================================================
# PONTO DE ENTRADA PRINCIPAL
# =============================================================================

def main():
    """Função principal que orquestra a renderização da aplicação."""

    # Sidebar com avisos de segurança
    renderizar_sidebar()

    # Cabeçalho principal
    st.markdown("""
    <div class="cabecalho-principal">
        <h1><span>DGMCG</span> | Gerador de Prompts para IA</h1>
        <p>
            Diretoria Geral de Monitoramento de Contratos de Gestão · SES/PE
            <br>Ferramenta de uso interno para padronização do uso de Inteligência Artificial
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Abas principais
    aba_biblioteca, aba_construtor = st.tabs([
        "📚 Biblioteca de Prompts",
        "🛠️ Construtor de Prompts"
    ])

    with aba_biblioteca:
        renderizar_biblioteca()

    with aba_construtor:
        renderizar_construtor()

    # Rodapé
    st.markdown("""
    <div class="rodape">
        DGMCG · Secretaria Estadual de Saúde · Ferramenta de uso interno · 
        Todos os prompts devem ser revisados antes do uso com dados reais.
    </div>
    """, unsafe_allow_html=True)


# Ponto de entrada do script
if __name__ == "__main__":
    main()
