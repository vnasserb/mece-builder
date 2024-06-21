import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import streamlit as st
import math


def plot_tree(df: pd.DataFrame, categories, node_color='blue', node_font_color='white',
              nodes_to_exclude=None, fig_width=10, fig_height=10,
              x_annotation_offset=.1, y_annotation_offset=.1, annotation_font_size=8,
              node_font_size=10):
    def count_non_nulls(array):
        non_nulls = 0
        for element in array:
            if not ((isinstance(element, float) and math.isnan(element)) or element == ''):
                non_nulls += 1
        return non_nulls

    def prettify_name(name):
        metrics_names = {
            'SUM': 'Soma ',
            'COUNT': 'Contagem ',
            'MIN': 'Mínimo ',
            'MAX': 'Máximo ',
            "MEAN": 'Média ',
            'MEDIAN': 'Mediana '
        }
        separated_name = name.split("_", 1)
        return metrics_names[separated_name[0]] + separated_name[1]

    df_values = df.iloc[:, :len(categories)].values
    x_offset = 10
    y_offset = 2

    coordinates = {i: (0, -y_offset * count_non_nulls(df_values[i])) for i in range(df_values.shape[0])}
    checked = {i: False for i in range(df.shape[0])}
    tree_metrics_names = df.columns[len(categories):]
    nodes_to_exclude_list = [] if not nodes_to_exclude else nodes_to_exclude

    qty_leafs = np.count_nonzero([count_non_nulls(value) == len(categories) for value in df_values])

    x_count = 0
    current_position = -1 * math.floor(qty_leafs / 2) - x_offset
    previous_was_leaf = False
    leafs_x_coord = []

    # Coordenadas para as folhas
    for row in range(len(df_values) - 1, 0, -1):
        row_values = df_values[row]

        if count_non_nulls(row_values) == len(categories):
            checked[row] = True
            if previous_was_leaf:
                leaf_position = current_position + len(categories) * x_offset
            else:
                leaf_position = current_position + x_offset

            current_position = leaf_position
            leafs_x_coord.append(leaf_position)
            coordinates[row] = (leaf_position, coordinates[row][1])
        else:
            previous_was_leaf = False
            current_position += x_offset

    edges = []

    for row in range(df.shape[0] - 1, -1, -1):
        row_values = df.iloc[row, :len(categories)].values.tolist()

        if checked[row]:
            continue

        row_first_null_column = count_non_nulls(row_values)
        remaining_rows = df.iloc[row + 1:, :len(categories)].values
        children_x_coordinates = []
        children_y_coordinates = []

        for rem_row in range(len(remaining_rows)):
            selected_remaining_row = remaining_rows[rem_row].tolist()
            selected_row_first_null_column = count_non_nulls(selected_remaining_row)

            if selected_row_first_null_column <= row_first_null_column:
                break

            if (selected_remaining_row[:row_first_null_column] == row_values[:row_first_null_column]
                    and selected_row_first_null_column == row_first_null_column + 1):
                children_x_coordinates.append(coordinates[row + 1 + rem_row][0])
                children_y_coordinates.append(coordinates[row + 1 + rem_row][1])

        coordinates[row] = (int(0.5 * (max(children_x_coordinates) + min(children_x_coordinates))),
                            coordinates[row][1])
        row_edges = [
            {
                'origin': coordinates[row],
                'destination': (children_x_coordinates[j], children_y_coordinates[j])
            }
            for j in range(len(children_x_coordinates))]

        edges += row_edges

        checked[row] = True

    nodes = []

    for row in range(df.shape[0]):
        node_metrics = df[df.columns[len(categories):]].iloc[row, :].values
        node_fields = df.iloc[row, :len(categories)].values
        node_label = node_fields[count_non_nulls(node_fields) - 1]
        node_label = "Total" if (isinstance(node_label, float) and math.isnan(
            node_label)) or node_label == '' else node_label

        nodes.append({
            'label': node_label,
            'coordinates': coordinates[row],
            'annotation': [f"{prettify_name(tree_metrics_names[k])}: {node_metrics[k]}" for k in
                           range(len(tree_metrics_names))],
            'index': row
        })

    coordinates_to_delete = [coordinates[item] for item in nodes_to_exclude_list]
    edges = list(filter(lambda e: e['origin'] not in coordinates_to_delete
                                  and e['destination'] not in coordinates_to_delete, edges))

    tree_height = len(categories) + 1
    tree_length = 1

    for i in range(len(categories)):
        tree_length *= len(np.unique(df.iloc[1:, i].values))

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    enumerated_nodes = list(enumerate(nodes))

    for enumeration in enumerated_nodes:
        if enumeration[0] in nodes_to_exclude_list:
            continue

        node = enumeration[1]
        x_pos, y_pos = node['coordinates']
        label = node['label']
        index = node['index']
        annotations = node['annotation']

        txt = ax.text(x_pos, y_pos, f"({index}) {label}", ha='center', va='center', wrap=True,
                      bbox=dict(boxstyle="round,pad=0.5", edgecolor='black', facecolor=node_color),
                      color=node_font_color, fontsize=node_font_size)
        txt._get_wrap_line_width = lambda: 400
        # ax.annotate(node['index'], xy=(x_pos - node_font_size/10, y_pos + 0 / node_font_size),
        #             fontsize=annotation_font_size)

        annotation_count = 0
        for annotation in annotations:
            annotations_offset = (0 if y_pos == -1 * y_offset * len(categories) else x_annotation_offset,
                                  1 * y_annotation_offset if y_pos == -1 * y_offset * len(
                                      categories) else y_annotation_offset)

            ax.annotate(annotation, xy=(x_pos + annotations_offset[0],
                                        y_pos - annotations_offset[1] - .2 * annotation_count),
                        fontsize=annotation_font_size)
            annotation_count += 1

    for edge in edges:
        x_origin, y_origin = edge['origin']
        x_dest, y_dest = edge['destination']
        ax.annotate('', xy=(x_dest, y_dest + 0.2), xytext=(x_origin, y_origin - 0.2),
                    arrowprops=dict(arrowstyle="->", color='black'))

    ax.set_xlim(min(leafs_x_coord) - 5, max(leafs_x_coord) + 5)
    ax.set_ylim(-2 * tree_height, 1)
    ax.axis('off')

    st.pyplot(fig)
