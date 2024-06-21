import pandas as pd
import numpy as np
import streamlit as st
import math

@st.cache_data
def build_mece(df: pd.DataFrame, categories: list, aggregation_functions: dict):
    partial_meces_list = []
    aggregation_functions_list = [item for sublist in list(aggregation_functions.values()) for item in sublist]
    totals = {}

    for column, agg_functions in aggregation_functions.items():
        for agg_function in agg_functions:
            pivot_table = pd.pivot_table(df, values=column, index=categories, aggfunc=agg_function, margins=False)
            pivot_df = pivot_table.reset_index()
            partial_mece_with_subtotals = pivot_df
            totals_key = f"{agg_function.upper()}_{column}"

            if agg_function == "sum":
                totals[totals_key] = np.sum(df[column])
            elif agg_function == "count":
                totals[totals_key] = np.sum(np.unique(df[column], return_counts=True)[1])
            elif agg_function == "min":
                totals[totals_key] = np.min(df[column])
            elif agg_function == "max":
                totals[totals_key] = np.max(df[column])
            elif agg_function == "mean":
                totals[totals_key] = np.mean(df[column])
            elif agg_function == "median":
                totals[totals_key] = np.median(df[column])

            for i in range(len(categories) - 1):
                if agg_function == "sum":
                    subtotals = pivot_df.groupby(categories[:-1 - i])[column].sum().reset_index()
                elif agg_function == "count":
                    subtotals = pivot_df.groupby(categories[:-1 - i]).sum().reset_index()
                elif agg_function == "min":
                    subtotals = pivot_df.groupby(categories[:-1 - i])[column].min().reset_index()
                elif agg_function == "max":
                    subtotals = pivot_df.groupby(categories[:-1 - i])[column].max().reset_index()
                elif agg_function == "mean":
                    subtotals = pivot_df.groupby(categories[:-1 - i])[column].mean().reset_index()
                elif agg_function == "median":
                    subtotals = pivot_df.groupby(categories[:-1 - i])[column].median().reset_index()

                for category in categories[-1 - i:]:
                    subtotals[category] = ''

                partial_mece_with_subtotals = pd.concat([partial_mece_with_subtotals, subtotals])

            partial_mece_with_subtotals.sort_values(by=categories,
                                                    key=lambda x: x.str.replace('Subtotal', 'AAA'),
                                                    inplace=True)
            partial_mece_with_subtotals.reset_index(drop=True, inplace=True)
            partial_meces_list.append(partial_mece_with_subtotals)

    mece = partial_meces_list[0].iloc[:, 0:len(categories)]

    for i in range(len(partial_meces_list)):
        partial_mece_aggregated_values = partial_meces_list[i].iloc[:, -1].values
        partial_mece_aggregated_value_column = partial_meces_list[i].columns[-1]
        mece[f"{aggregation_functions_list[i].upper()}_{partial_mece_aggregated_value_column}"] = partial_mece_aggregated_values

    mece = pd.concat([pd.DataFrame([totals]), mece])
    return mece[categories + list(totals.keys())]


@st.cache_data
def uploaded_file_to_dataframe(uploaded_file):
    dataframe = pd.read_csv(uploaded_file)
    return dataframe


def build_abbreviated_df(df: pd.DataFrame, indexes: list):
    abbreviated_df = df.copy()
    df_values = abbreviated_df[indexes].values
    df_columns = abbreviated_df[indexes].columns
    concatenated_values = [
        ", ".join([f"{df_columns[c]}: {df_row[c]}" for c in range(len(df_columns))
                  if not ((isinstance(df_row[c], float) and math.isnan(df_row[c]))
                          or df_row[c] == '')])
        for df_row in df_values
    ]
    # st.write(concatenated_values)
    abbreviated_df['Linha'] = concatenated_values
    abbreviated_df = abbreviated_df[['Linha'] + abbreviated_df.columns[len(indexes):-1].tolist()]

    return abbreviated_df
