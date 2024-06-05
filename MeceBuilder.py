import pandas as pd
import numpy as np
import streamlit as st


def build_mece(df: pd.DataFrame, categories: list, aggregation_functions: dict):
    partial_meces_list = []

    for column, agg_functions in aggregation_functions.items():
        for agg_function in agg_functions:
            pivot_table = pd.pivot_table(df, values=column, index=categories, aggfunc=agg_function, margins=False)
            pivot_df = pivot_table.reset_index()
            partial_mece_with_subtotals = pivot_df

            for i in range(0, len(categories) - 1, 1):
                if agg_function == "sum":
                    subtotals = pivot_df.groupby(categories[:-1 - i]).sum().reset_index()
                elif agg_function == "count":
                    subtotals = pivot_df.groupby(categories[:-1 - i]).count().reset_index()
                elif agg_function == "min":
                    subtotals = pivot_df.groupby(categories[:-1 - i]).min().reset_index()
                elif agg_function == "max":
                    subtotals = pivot_df.groupby(categories[:-1 - i]).max().reset_index()
                elif agg_function == "mean":
                    subtotals = pivot_df.groupby(categories[:-1 - i])[column].mean().reset_index()
                elif agg_function == "median":
                    subtotals = pivot_df.groupby(categories[:-1 - i])[column].median().reset_index()

                for category in categories[-1 - i:]:
                    subtotals[category] = ''

                partial_mece_with_subtotals = pd.concat([partial_mece_with_subtotals, subtotals])

            partial_mece_with_subtotals.sort_values(by=categories, key=lambda x: x.str.replace('Subtotal', 'AAA'),
                                                    inplace=True)
            partial_mece_with_subtotals.reset_index(drop=True, inplace=True)
            partial_meces_list.append(partial_mece_with_subtotals)

    mece = partial_meces_list[0].iloc[:, 0:len(categories)]
    aggregation_functions_list = [item for sublist in list(aggregation_functions.values()) for item in sublist]

    for i in range(len(partial_meces_list)):
        partial_mece_aggregated_values = partial_meces_list[i].iloc[:, -1].values
        partial_mece_aggregated_value_column = partial_meces_list[i].columns[-1]
        mece[
            f"{aggregation_functions_list[i].upper()}_{partial_mece_aggregated_value_column}"] = partial_mece_aggregated_values

    return mece


@st.cache_data
def uploaded_file_to_dataframe(uploaded_file):
    dataframe = pd.read_csv(uploaded_file)
    return dataframe
