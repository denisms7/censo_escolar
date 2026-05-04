import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Censo Escolar 2025", layout="wide")
st.title("📊 Microdados Censo Escolar 2025")

base_path = r'dados\microdados_censo_escolar_2025\dados'

MUNICIPIO_BASE = "CENTENÁRIO DO SUL"

# ── Legendas ───────────────────────────────────────────────────────────────────
LEGENDAS_ESCOLA = {
    "CO_ENTIDADE":                 "Código da escola",
    "NO_ENTIDADE":                 "Nome da escola",
    "SG_UF":                       "Sigla da UF",
    "NO_UF":                       "Nome da UF",
    "CO_MUNICIPIO":                "Código do município",
    "NO_MUNICIPIO":                "Nome do município",
    "TP_DEPENDENCIA":              "Dependência administrativa (1=Federal, 2=Estadual, 3=Municipal, 4=Privada)",
    "TP_CATEGORIA_ESCOLA_PRIVADA": "Categoria da escola privada (1=Particular, 2=Comunitária, 3=Confessional, 4=Filantrópica)",
    "QT_SALAS_UTILIZADAS_DENTRO":  "Salas de aula utilizadas dentro do prédio",
    "QT_SALAS_UTILIZADAS_FORA":    "Salas de aula utilizadas fora do prédio",
    "QT_SALAS_UTILIZADAS":         "Total de salas de aula utilizadas (dentro e fora)",
    "Dependência":                 "Rótulo da dependência administrativa",
    "Categoria Privada":           "Rótulo da categoria da escola privada",
}

LEGENDAS_MATRICULA_TOTAL = {
    "NO_MUNICIPIO": "Nome do município",
    "QT_MAT_BAS":   "Matrículas — Educação Básica (total)",
    "QT_MAT_INF":   "Matrículas — Educação Infantil (total)",
    "QT_MAT_FUND":  "Matrículas — Ensino Fundamental (total)",
    "QT_MAT_FUND_AI": "Matrículas — Fund.: Anos Iniciais (total)",
    "QT_MAT_FUND_AF": "Matrículas — Fund.: Anos Finais (total)",
}
LEGENDAS_MATRICULA_DET = {
    "NO_MUNICIPIO":     "Nome do município",
    "QT_MAT_INF_CRE":   "Matrículas — Ed. Infantil: Creche",
    "QT_MAT_INF_PRE":   "Matrículas — Ed. Infantil: Pré-Escola",
    "QT_MAT_FUND_AI_1": "Matrículas — Fund. AI: 1º Ano",
    "QT_MAT_FUND_AI_2": "Matrículas — Fund. AI: 2º Ano",
    "QT_MAT_FUND_AI_3": "Matrículas — Fund. AI: 3º Ano",
    "QT_MAT_FUND_AI_4": "Matrículas — Fund. AI: 4º Ano",
    "QT_MAT_FUND_AI_5": "Matrículas — Fund. AI: 5º Ano",
    "QT_MAT_FUND_AF_6": "Matrículas — Fund. AF: 6º Ano",
}

LEGENDAS_DOCENTE_TOTAL = {
    "NO_MUNICIPIO":          "Nome do município",
    "QT_DOC_BAS":            "Docentes — Educação Básica (total)",
    "QT_DOC_INF":            "Docentes — Educação Infantil (total)",
    "QT_DOC_FUND":           "Docentes — Ensino Fundamental (total)",
    "QT_DOC_FUND_AI":        "Docentes — Fund.: Anos Iniciais (total)",
    "QT_DOC_FUND_AF":        "Docentes — Fund.: Anos Finais (total)",
    "QT_DOC_FUND_AI_MULTIETAPA": "Docentes — Fund.: Multietapa",
}
LEGENDAS_DOCENTE_DET = {
    "NO_MUNICIPIO":          "Nome do município",
    "QT_DOC_INF_CRE":        "Docentes — Ed. Infantil: Creche",
    "QT_DOC_INF_PRE":        "Docentes — Ed. Infantil: Pré-Escola",
    "QT_DOC_FUND_AI_1":      "Docentes — Fund. AI: 1º Ano",
    "QT_DOC_FUND_AI_2":      "Docentes — Fund. AI: 2º Ano",
    "QT_DOC_FUND_AI_3":      "Docentes — Fund. AI: 3º Ano",
    "QT_DOC_FUND_AI_4":      "Docentes — Fund. AI: 4º Ano",
    "QT_DOC_FUND_AI_5":      "Docentes — Fund. AI: 5º Ano",
    "QT_DOC_FUND_AF_6":      "Docentes — Fund. AF: 6º Ano",
}

LEGENDAS_TURMA_TOTAL = {
    "NO_MUNICIPIO":    "Nome do município",
    "QT_TUR_BAS":      "Turmas — Educação Básica (total)",
    "QT_TUR_INF":      "Turmas — Educação Infantil (total)",
    "QT_TUR_FUND":     "Turmas — Ensino Fundamental (total)",
    "QT_TUR_FUND_AI":  "Turmas — Fund.: Anos Iniciais (total)",
    "QT_TUR_FUND_AF":  "Turmas — Fund.: Anos Finais (total)",
    "QT_TUR_FUND_AI_MULTIETAPA": "Turmas — Fund.: Multietapa",
}
LEGENDAS_TURMA_DET = {
    "NO_MUNICIPIO":          "Nome do município",
    "QT_TUR_INF_CRE":        "Turmas — Ed. Infantil: Creche",
    "QT_TUR_INF_PRE":        "Turmas — Ed. Infantil: Pré-Escola",
    "QT_TUR_FUND_AI_1":      "Turmas — Fund. AI: 1º Ano",
    "QT_TUR_FUND_AI_2":      "Turmas — Fund. AI: 2º Ano",
    "QT_TUR_FUND_AI_3":      "Turmas — Fund. AI: 3º Ano",
    "QT_TUR_FUND_AI_4":      "Turmas — Fund. AI: 4º Ano",
    "QT_TUR_FUND_AI_5":      "Turmas — Fund. AI: 5º Ano",
    "QT_TUR_FUND_AF_6":      "Turmas — Fund. AF: 6º Ano",
}

LEGENDAS_RATIO = {
    "Etapa":                "Etapa / nível de ensino",
    "Município":            "Nome do município",
    "Alunos":               "Total de matrículas na etapa",
    "Docentes":             "Total de docentes na etapa",
    "Alunos por professor": "Razão: total de alunos ÷ total de docentes",
}


def exibir_legenda(legendas: dict, colunas_presentes: list):
    filtradas = {k: v for k, v in legendas.items() if k in colunas_presentes}
    if not filtradas:
        return
    with st.expander("📖 Legenda das colunas"):
        st.dataframe(
            pd.DataFrame({"Coluna": list(filtradas.keys()), "Descrição": list(filtradas.values())}),
            use_container_width=True, hide_index=True
        )


def sub_abas_dataframe(df_total, leg_total, df_det, leg_det):
    """Renderiza duas sub-abas: Totais e Detalhado."""
    s1, s2 = st.tabs(["📊 Totais", "🔍 Detalhado"])
    with s1:
        exibir_legenda(leg_total, list(df_total.columns))
        st.dataframe(df_total, use_container_width=True, height=460, hide_index=True)
    with s2:
        exibir_legenda(leg_det, list(df_det.columns))
        st.dataframe(df_det, use_container_width=True, height=460, hide_index=True)


# ── Carregamento ───────────────────────────────────────────────────────────────
@st.cache_data
def carregar_csv(nome_arquivo, colunas=None):
    caminho = f"{base_path}\\{nome_arquivo}"
    for encoding in ["utf-8", "latin1", "cp1252"]:
        try:
            return pd.read_csv(
                caminho, sep=";", encoding=encoding,
                low_memory=False, usecols=colunas
            )
        except UnicodeDecodeError:
            continue
    raise Exception(f"Erro ao ler arquivo: {nome_arquivo}")


@st.cache_data
def carregar_dados():
    escola = carregar_csv("Tabela_Escola_2025.csv", [
        "CO_ENTIDADE", "NO_ENTIDADE", "SG_UF", "NO_UF",
        "CO_MUNICIPIO", "NO_MUNICIPIO",
        "TP_DEPENDENCIA", "TP_CATEGORIA_ESCOLA_PRIVADA",
        "QT_SALAS_UTILIZADAS_DENTRO", "QT_SALAS_UTILIZADAS_FORA", "QT_SALAS_UTILIZADAS",
    ])
    matricula = carregar_csv("Tabela_Matricula_2025.csv", [
        "CO_ENTIDADE",
        "QT_MAT_BAS", "QT_MAT_INF", "QT_MAT_INF_CRE", "QT_MAT_INF_PRE",
        "QT_MAT_FUND", "QT_MAT_FUND_AI", "QT_MAT_FUND_AI_1", "QT_MAT_FUND_AI_2",
        "QT_MAT_FUND_AI_3", "QT_MAT_FUND_AI_4", "QT_MAT_FUND_AI_5",
        "QT_MAT_FUND_AF", "QT_MAT_FUND_AF_6",
    ])
    docente = carregar_csv("Tabela_Docente_2025.csv", [
        "CO_ENTIDADE",
        "QT_DOC_BAS", "QT_DOC_INF", "QT_DOC_INF_CRE", "QT_DOC_INF_PRE",
        "QT_DOC_FUND", "QT_DOC_FUND_AI", "QT_DOC_FUND_AI_1", "QT_DOC_FUND_AI_2",
        "QT_DOC_FUND_AI_3", "QT_DOC_FUND_AI_4", "QT_DOC_FUND_AI_5",
        "QT_DOC_FUND_AI_MULTIETAPA", "QT_DOC_FUND_AF", "QT_DOC_FUND_AF_6",
    ])
    turma = carregar_csv("Tabela_Turma_2025.csv", [
        "CO_ENTIDADE",
        "QT_TUR_BAS", "QT_TUR_INF", "QT_TUR_INF_CRE", "QT_TUR_INF_PRE",
        "QT_TUR_FUND", "QT_TUR_FUND_AI", "QT_TUR_FUND_AI_1", "QT_TUR_FUND_AI_2",
        "QT_TUR_FUND_AI_3", "QT_TUR_FUND_AI_4", "QT_TUR_FUND_AI_5",
        "QT_TUR_FUND_AI_MULTIETAPA", "QT_TUR_FUND_AF", "QT_TUR_FUND_AF_6",
    ])
    df = escola.merge(matricula, on="CO_ENTIDADE", how="left")
    df = df.merge(docente, on="CO_ENTIDADE", how="left")
    df = df.merge(turma,   on="CO_ENTIDADE", how="left")
    return df


with st.spinner("Carregando arquivos..."):
    df_completo = carregar_dados()

# ── Sidebar ────────────────────────────────────────────────────────────────────
st.sidebar.header("Filtros")

ufs = sorted(df_completo["SG_UF"].dropna().astype(str).unique())
uf_selecionada = st.sidebar.selectbox(
    "UF", options=ufs,
    index=ufs.index("PR") if "PR" in ufs else 0
)

DEP_MAP = {1: "Federal", 2: "Estadual", 3: "Municipal", 4: "Privada"}
dep_opcoes = st.sidebar.multiselect(
    "Dependência administrativa",
    options=list(DEP_MAP.keys()), default=list(DEP_MAP.keys()),
    format_func=lambda x: DEP_MAP[x]
)

CAT_MAP = {1: "Particular", 2: "Comunitária", 3: "Confessional", 4: "Filantrópica"}
cat_opcoes = st.sidebar.multiselect(
    "Categoria escola privada",
    options=list(CAT_MAP.keys()), default=list(CAT_MAP.keys()),
    format_func=lambda x: CAT_MAP[x]
)

# ── Filtro ─────────────────────────────────────────────────────────────────────
df = df_completo[df_completo["SG_UF"].astype(str) == uf_selecionada].copy()
df = df[df["TP_DEPENDENCIA"].isin(dep_opcoes)]
mask_priv = df["TP_DEPENDENCIA"] == 4
mask_pub  = df["TP_DEPENDENCIA"] != 4
df = df[mask_pub | (mask_priv & df["TP_CATEGORIA_ESCOLA_PRIVADA"].isin(cat_opcoes))]

municipios = sorted(df["NO_MUNICIPIO"].dropna().unique())
municipio_selecionado = st.sidebar.selectbox(
    "Município", options=["Todos"] + municipios
)
if municipio_selecionado != "Todos":
    df = df[df["NO_MUNICIPIO"] == municipio_selecionado]

df["Dependência"]       = df["TP_DEPENDENCIA"].map(DEP_MAP)
df["Categoria Privada"] = df["TP_CATEGORIA_ESCOLA_PRIVADA"].map(CAT_MAP)

# ── Abas principais ────────────────────────────────────────────────────────────
aba_escolas, aba_matriculas, aba_docentes, aba_turmas, aba_ratio = st.tabs([
    "Escolas", "Matrículas", "Docentes", "Turmas", "Alunos por Professor"
])

# ── Escolas ────────────────────────────────────────────────────────────────────
with aba_escolas:
    st.subheader("Escolas por município")

    escolas_cidade = (
        df.groupby(["NO_MUNICIPIO", "Dependência"])
        .size().reset_index(name="Total de escolas")
    )
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = px.bar(
            escolas_cidade, x="NO_MUNICIPIO", y="Total de escolas",
            color="Dependência", labels={"NO_MUNICIPIO": "Município"}, height=420,
        )
        fig.update_layout(xaxis_tickangle=-45, legend_title="Dependência")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        resumo = (
            escolas_cidade.groupby("NO_MUNICIPIO")["Total de escolas"]
            .sum().reset_index().sort_values("Total de escolas", ascending=False)
        )
        st.metric("Total de escolas",
                  f"{resumo['Total de escolas'].sum():,}".replace(",", "."))
        st.dataframe(resumo, use_container_width=True, hide_index=True)

    # Totais: uma linha por escola com colunas resumidas
    cols_total = ["NO_MUNICIPIO", "NO_ENTIDADE", "Dependência", "Categoria Privada",
                  "QT_SALAS_UTILIZADAS"]
    # Detalhado: abre salas dentro/fora
    cols_det   = ["NO_MUNICIPIO", "NO_ENTIDADE", "Dependência", "Categoria Privada",
                  "QT_SALAS_UTILIZADAS_DENTRO", "QT_SALAS_UTILIZADAS_FORA",
                  "QT_SALAS_UTILIZADAS"]

    df_esc_tot = df[[c for c in cols_total if c in df.columns]]
    df_esc_det = df[[c for c in cols_det   if c in df.columns]]

    sub_abas_dataframe(df_esc_tot, LEGENDAS_ESCOLA, df_esc_det, LEGENDAS_ESCOLA)

# ── Matrículas ─────────────────────────────────────────────────────────────────
with aba_matriculas:
    st.subheader("Matrículas por município")

    cols_mat_tot = ["NO_MUNICIPIO", "QT_MAT_BAS", "QT_MAT_INF",
                    "QT_MAT_FUND", "QT_MAT_FUND_AI", "QT_MAT_FUND_AF"]
    cols_mat_det = ["NO_MUNICIPIO", "QT_MAT_INF_CRE", "QT_MAT_INF_PRE",
                    "QT_MAT_FUND_AI_1", "QT_MAT_FUND_AI_2", "QT_MAT_FUND_AI_3",
                    "QT_MAT_FUND_AI_4", "QT_MAT_FUND_AI_5", "QT_MAT_FUND_AF_6"]

    mat_tot = (df[[c for c in cols_mat_tot if c in df.columns]]
               .groupby("NO_MUNICIPIO").sum().reset_index())
    mat_det = (df[[c for c in cols_mat_det if c in df.columns]]
               .groupby("NO_MUNICIPIO").sum().reset_index())

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total matrículas Ed. Básica",
                  f"{int(mat_tot['QT_MAT_BAS'].sum()):,}".replace(",", "."))
    with col2:
        st.metric("Total matrículas Ed. Fundamental",
                  f"{int(mat_tot['QT_MAT_FUND'].sum()):,}".replace(",", "."))

    sub_abas_dataframe(mat_tot, LEGENDAS_MATRICULA_TOTAL,
                       mat_det, LEGENDAS_MATRICULA_DET)

# ── Docentes ───────────────────────────────────────────────────────────────────
with aba_docentes:
    st.subheader("Docentes por município")

    cols_doc_tot = ["NO_MUNICIPIO", "QT_DOC_BAS", "QT_DOC_INF",
                    "QT_DOC_FUND", "QT_DOC_FUND_AI", "QT_DOC_FUND_AF",
                    "QT_DOC_FUND_AI_MULTIETAPA"]
    cols_doc_det = ["NO_MUNICIPIO", "QT_DOC_INF_CRE", "QT_DOC_INF_PRE",
                    "QT_DOC_FUND_AI_1", "QT_DOC_FUND_AI_2", "QT_DOC_FUND_AI_3",
                    "QT_DOC_FUND_AI_4", "QT_DOC_FUND_AI_5", "QT_DOC_FUND_AF_6"]

    doc_tot = (df[[c for c in cols_doc_tot if c in df.columns]]
               .groupby("NO_MUNICIPIO").sum().reset_index())
    doc_det = (df[[c for c in cols_doc_det if c in df.columns]]
               .groupby("NO_MUNICIPIO").sum().reset_index())

    st.metric("Total docentes Ed. Básica",
              f"{int(doc_tot['QT_DOC_BAS'].sum()):,}".replace(",", "."))

    sub_abas_dataframe(doc_tot, LEGENDAS_DOCENTE_TOTAL,
                       doc_det, LEGENDAS_DOCENTE_DET)

# ── Turmas ─────────────────────────────────────────────────────────────────────
with aba_turmas:
    st.subheader("Turmas por município")

    cols_tur_tot = ["NO_MUNICIPIO", "QT_TUR_BAS", "QT_TUR_INF",
                    "QT_TUR_FUND", "QT_TUR_FUND_AI", "QT_TUR_FUND_AF",
                    "QT_TUR_FUND_AI_MULTIETAPA"]
    cols_tur_det = ["NO_MUNICIPIO", "QT_TUR_INF_CRE", "QT_TUR_INF_PRE",
                    "QT_TUR_FUND_AI_1", "QT_TUR_FUND_AI_2", "QT_TUR_FUND_AI_3",
                    "QT_TUR_FUND_AI_4", "QT_TUR_FUND_AI_5", "QT_TUR_FUND_AF_6"]

    tur_tot = (df[[c for c in cols_tur_tot if c in df.columns]]
               .groupby("NO_MUNICIPIO").sum().reset_index())
    tur_det = (df[[c for c in cols_tur_det if c in df.columns]]
               .groupby("NO_MUNICIPIO").sum().reset_index())

    st.metric("Total turmas Ed. Básica",
              f"{int(tur_tot['QT_TUR_BAS'].sum()):,}".replace(",", "."))

    sub_abas_dataframe(tur_tot, LEGENDAS_TURMA_TOTAL,
                       tur_det, LEGENDAS_TURMA_DET)

# ── Alunos por Professor ───────────────────────────────────────────────────────
with aba_ratio:
    st.subheader("Alunos por professor — comparação com Centenário do Sul")

    ETAPAS_TOTAL = {
        "Ed. Básica":          ("QT_MAT_BAS",     "QT_DOC_BAS"),
        "Ed. Infantil":        ("QT_MAT_INF",     "QT_DOC_INF"),
        "Ens. Fundamental":    ("QT_MAT_FUND",    "QT_DOC_FUND"),
        "Fund. Anos Iniciais": ("QT_MAT_FUND_AI", "QT_DOC_FUND_AI"),
        "Fund. Anos Finais":   ("QT_MAT_FUND_AF", "QT_DOC_FUND_AF"),
    }
    ETAPAS_DET = {
        "Infantil — Creche":     ("QT_MAT_INF_CRE",   "QT_DOC_INF_CRE"),
        "Infantil — Pré-escola": ("QT_MAT_INF_PRE",   "QT_DOC_INF_PRE"),
        "Fund. AI — 1º Ano":     ("QT_MAT_FUND_AI_1", "QT_DOC_FUND_AI_1"),
        "Fund. AI — 2º Ano":     ("QT_MAT_FUND_AI_2", "QT_DOC_FUND_AI_2"),
        "Fund. AI — 3º Ano":     ("QT_MAT_FUND_AI_3", "QT_DOC_FUND_AI_3"),
        "Fund. AI — 4º Ano":     ("QT_MAT_FUND_AI_4", "QT_DOC_FUND_AI_4"),
        "Fund. AI — 5º Ano":     ("QT_MAT_FUND_AI_5", "QT_DOC_FUND_AI_5"),
        "Fund. AF — 6º Ano":     ("QT_MAT_FUND_AF_6", "QT_DOC_FUND_AF_6"),
    }

    def calcular_ratio(df_fonte, nome_municipio, etapas):
        sub = df_fonte[df_fonte["NO_MUNICIPIO"].str.upper() == nome_municipio.upper()]
        rows = []
        for etapa, (col_mat, col_doc) in etapas.items():
            if col_mat in sub.columns and col_doc in sub.columns:
                total_mat = sub[col_mat].sum()
                total_doc = sub[col_doc].sum()
                if total_doc > 0:
                    rows.append({
                        "Etapa":                etapa,
                        "Município":            nome_municipio.title(),
                        "Alunos":               int(total_mat),
                        "Docentes":             int(total_doc),
                        "Alunos por professor": round(total_mat / total_doc, 1),
                    })
        return pd.DataFrame(rows)

    def montar_comparacao(df_uf, municipios_comp, etapas):
        frames = [calcular_ratio(df_uf, MUNICIPIO_BASE, etapas)]
        for mun in municipios_comp:
            r = calcular_ratio(df_uf, mun, etapas)
            if not r.empty:
                frames.append(r)
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    def grafico_ratio(df_plot):
        if df_plot.empty:
            st.info("Sem dados suficientes com os filtros selecionados.")
            return
        cor_map = {
            m: "#1f77b4"
            for m in df_plot["Município"].unique()
            if m.upper() == MUNICIPIO_BASE.upper()
        }
        fig = px.bar(
            df_plot, x="Etapa", y="Alunos por professor",
            color="Município", barmode="group",
            text="Alunos por professor", height=500,
            color_discrete_map=cor_map,
        )
        fig.update_traces(textposition="outside", textfont_size=11)
        fig.update_layout(
            xaxis_tickangle=-30, xaxis_title="",
            yaxis_title="Alunos por professor", legend_title="Município",
        )
        st.plotly_chart(fig, use_container_width=True)
        exibir_legenda(LEGENDAS_RATIO, list(df_plot.columns))
        st.dataframe(
            df_plot[["Município", "Etapa", "Alunos", "Docentes", "Alunos por professor"]],
            use_container_width=True, hide_index=True
        )

    # Carregar df filtrado por UF/dep/cat mas sem filtro de município
    df_uf = df_completo[df_completo["SG_UF"].astype(str) == uf_selecionada].copy()
    df_uf = df_uf[df_uf["TP_DEPENDENCIA"].isin(dep_opcoes)]
    mp2 = df_uf["TP_DEPENDENCIA"] == 4
    mu2 = df_uf["TP_DEPENDENCIA"] != 4
    df_uf = df_uf[mu2 | (mp2 & df_uf["TP_CATEGORIA_ESCOLA_PRIVADA"].isin(cat_opcoes))]

    outros = sorted([
        m for m in df_uf["NO_MUNICIPIO"].dropna().unique()
        if m.upper() != MUNICIPIO_BASE.upper()
    ])

    st.markdown("**Centenário do Sul** é sempre exibido. Selecione os municípios para comparar:")

    col_sel1, col_sel2 = st.columns([3, 1])
    with col_sel1:
        municipios_comp = st.multiselect(
            "Municípios para comparar", options=outros, default=[],
            placeholder="Escolha um ou mais municípios..."
        )
    with col_sel2:
        todos = st.checkbox("Todos os municípios", value=False)

    if todos:
        municipios_comp = outros

    # Sub-abas Totais | Detalhado
    r1, r2 = st.tabs(["📊 Totais", "🔍 Detalhado"])

    with r1:
        df_plot_tot = montar_comparacao(df_uf, municipios_comp, ETAPAS_TOTAL)
        grafico_ratio(df_plot_tot)

    with r2:
        df_plot_det = montar_comparacao(df_uf, municipios_comp, ETAPAS_DET)
        grafico_ratio(df_plot_det)
