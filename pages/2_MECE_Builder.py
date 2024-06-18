import pandas as pd
import streamlit as st
from MeceBuilder import *
from TreeBuilder import plot_tree
from datetime import datetime

aggregation_functions = []
agrregations_dict = {
    "Soma": "sum",
    "Contagem": "count",
    "Mínimo": "min",
    "Máximo": "max",
    "Mediana": "median",
    "Média": "mean"
}

colors_dict = {
    "Azul": 'blue',
    "Vermelho": 'red',
    "Verde": 'green',
    "Amarelo": 'yellow',
    "Laranja": 'orange',
    "Preto": 'black',
    "Roxo": 'purple',
    "Branco": 'white'
}


def main():
    st.set_page_config(page_title="MECE Builder", layout="wide", page_icon="📊")
    st.title("MECE Builder")
    st.header("Utilize este aplicativo para inserir uma base de dados e criar um MECE da maneira que você quiser")
    file = st.file_uploader("Insira o arquivo CSV")

    if file is not None:
        data = uploaded_file_to_dataframe(file)

        indexes = st.multiselect(label="Selecione as colunas que deseja agrupar. As primeiras são consideradas como as mais abrangentes",
                                 options=data.columns)

        st.header("Insira as métricas que deseja visualizar")
        aggregations = []
        columns_to_aggregate = []

        for counter in range(6):
            columns = st.columns(2)
            with columns[0]:
                aggregation = st.selectbox(label="Agregação",
                                           index=None,
                                           options=list(agrregations_dict.keys()),
                                           key=f"{counter}_select1",
                                           label_visibility="hidden")

                if aggregation:
                    aggregations.append(aggregation)

            with columns[1]:
                aggregation_column = st.selectbox(label="Coluna",
                                                  index=None,
                                                  options=data.columns.tolist(),
                                                  key=f"{counter}_select2",
                                                  label_visibility="hidden")

                if aggregation_column:
                    columns_to_aggregate.append(aggregation_column)

            if aggregation and aggregation_column:
                aggregation_functions.append([aggregation, aggregation_column])

        aggregation_functions_dict = {
            aggregation_functions[i][1]: [agrregations_dict.get(aggregation_functions[j][0])
                                          for j in range(len(aggregation_functions))
                                          if aggregation_functions[j][1] == aggregation_functions[i][1]]
            for i in range(len(aggregation_functions))
        }

        if len(aggregation_functions) > 0 and len(indexes) > 0:
            st.write("<br><br><br>", unsafe_allow_html=True)
            mece_as_table, mece_as_tree = st.tabs(["Tabela", "Diagrama"])

            with mece_as_table:
                st.header("Seu MECE como tabela")

                build_mece_button = st.button("Construir MECE",
                                              disabled=len(aggregations) != len(columns_to_aggregate))
                if build_mece_button:
                    mece = build_mece(df=data, categories=indexes, aggregation_functions=aggregation_functions_dict)

                    st.write("<br><br>", unsafe_allow_html=True)
                    st.dataframe(mece, hide_index=True)
                    st.download_button(
                        label="Baixar",
                        data=mece.to_csv().encode("utf-8"),
                        file_name=f"{datetime.utcnow()} mece.csv",
                        mime="text/csv",
                    )

            with mece_as_tree:
                st.header("Seu MECE como diagrama")

                st.subheader("Antes de criar seu diagrama, atente-se")
                diagram_controls_html = """
                    <ul>
                        <li><strong>Largura da Imagem</strong>: Quanto maior a largura, mais espaçados os elementos se dispõem. Use quando um item invade a área do outro</li>
                        <li><strong>Altura da Imagem</strong>: Quanto maior a largura, maior a distância vertical os elementos.</li>
                        <li><strong>Translação Horizontal da Métrica</strong>: Diminua o valor do slider para deslocar o texto da métrica para a esquerda e aumente seu valor para deslocá-lo para a direita.</li>
                        <li><strong>Translação Vertical da Métrica</strong>: Diminua o valor do slider para para deslocar o texto da métrica para cima e aumente seu valor para deslocá-lo para baixo.</li>
                    </ul>
                    <br>
                """

                st.write(diagram_controls_html, unsafe_allow_html=True)
                mece = build_mece(df=data, categories=indexes,
                                  aggregation_functions=aggregation_functions_dict)

                with st.form(key="form0"):
                    columns = st.columns(3)

                    with columns[0]:
                        node_color = st.selectbox("Cor dos nós", options=["Azul", "Vermelho", "Verde", "Amarelo", "Laranja", "Preto", "Roxo"])

                    with columns[1]:
                        node_font_color = st.selectbox("Cor da fonte", options=["Preto", "Branco"])

                    with columns[2]:
                        nodes_to_exclude = st.multiselect("Nós a serem excluídos", options=np.arange(0, mece.shape[0], 1))

                    columns = st.columns(3)

                    with columns[0]:
                        fig_width = st.slider("Largura da imagem", min_value=5, max_value=80, value=10, step=1)

                    with columns[1]:
                        fig_height = st.slider("Altura da imagem", min_value=5, max_value=80, value=10, step=1)

                    with columns[2]:
                        font_size = st.slider("Tamanho da fonte da métrica", min_value=1, max_value=50, value=8, step=1)

                    columns = st.columns(3)

                    with columns[0]:
                        node_font_size = st.slider("Tamanho da fonte do nó", min_value=1, max_value=50, value=10, step=1)

                    with columns[1]:
                        x_offset = st.slider("Translação horizontal da métrica", min_value=-30, max_value=30, value=10, step=1)

                    with columns[2]:
                        y_offset = st.slider("Translação vertical da métrica", min_value=-30, max_value=30, value=10, step=1)

                    with st.columns(7)[3]:
                        submitted = st.form_submit_button("Gerar diagrama")

                    if submitted:
                        plot_tree(mece, categories=indexes,
                                  node_color=colors_dict[node_color],
                                  node_font_color=colors_dict[node_font_color],
                                  nodes_to_exclude=nodes_to_exclude,
                                  fig_width=fig_width,
                                  fig_height=fig_height,
                                  x_annotation_offset=x_offset / 10,
                                  y_annotation_offset=y_offset / 10,
                                  annotation_font_size=font_size,
                                  node_font_size=node_font_size)


main()
