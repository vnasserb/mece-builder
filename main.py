import pandas as pd
import streamlit as st
from MeceBuilder import *

aggregation_functions = []
agrregations_dict = {
    "Soma": "sum",
    "Contagem": "count",
    "Mínimo": "min",
    "Máximo": "max",
    "Mediana": "median",
    "Média": "mean"
}


def generate_boxes(counter: int, possible_columns):
    columns = st.columns(2)
    with columns[0]:
        aggregation = st.selectbox(label="Agregação",
                                   index=None,
                                   options=list(agrregations_dict.keys()),
                                   key=f"{counter}_select1",
                                   label_visibility="hidden")

    with columns[1]:
        aggregation_column = st.selectbox(label="Coluna",
                                          index=None,
                                          options=possible_columns,
                                          key=f"{counter}_select2",
                                          label_visibility="hidden")

    if aggregation and aggregation_column:
        aggregation_functions.append([aggregation, aggregation_column])
        counter += 1
        generate_boxes(counter, possible_columns)


def main():
    st.set_page_config(page_title="Montador de MECE", layout="wide", page_icon="📊")
    st.title("Montador de MECE")
    st.header("Utilize este aplicativo para inserir uma base de dados e criar um MECE da maneira que você quiser")
    file = st.file_uploader("Insira o arquivo CSV")

    if file is not None:
        data = uploaded_file_to_dataframe(file)

        indexes = st.multiselect(label="Selecione as colunas que deseja agrupar, começanando pela mais abrangente",
                                 options=data.columns)

        counter = 0

        st.header("Insira as métricas que deseja visualizar")

        generate_boxes(counter, data.columns.tolist())

        # add_aggregation_button = st.button(label="Adicionar métrica", key=f"{counter}_btn")
        # if add_aggregation_button:

        aggregation_functions_dict = {
            aggregation_functions[i][1]: [agrregations_dict.get(aggregation_functions[j][0])
                                          for j in range(len(aggregation_functions))
                                          if aggregation_functions[j][1] == aggregation_functions[i][1]]
            for i in range(len(aggregation_functions))
        }

        if len(aggregation_functions) > 0 and len(indexes) > 0:
            with st.columns(7)[3]:
                st.write("<br>", unsafe_allow_html=True)
                build_mece_button = st.button("Construir MECE")
            if build_mece_button:
                mece = build_mece(df=data, categories=indexes, aggregation_functions=aggregation_functions_dict)

                st.write("<br><br>", unsafe_allow_html=True)
                st.dataframe(mece, hide_index=True)
                st.download_button(
                    label="Baixar",
                    data=mece.astype(int).to_csv().encode("utf-8"),
                    file_name="mece.csv",
                    mime="text/csv",
                )


main()

