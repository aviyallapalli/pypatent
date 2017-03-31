#!/usr/bin/env python3
import graphviz as gv


def visualize_conll_tree(tree, format="png"):
    """
    Creating an image from conll-format tree.
    :param tree: conll-format tree
    :param format: image file extension
    :return: binary data string
    """
    graph = __build_graph(tree)
    return graph.pipe(format)


def __build_graph(tree):
    graph = gv.Digraph()
    for node in tree:
        node_id = node.id
        node_info = "{}\n{} ({})\n{}".format(node.id, node.form, node.lemma, node.upostag)
        graph.node(name=node_id, label=node_info)

    for node in tree:
        if node.head == "0":
            __set_edges(graph, tree, node.id)

    return graph


def __set_edges(graph, tree, node_id):
    children = []
    for node in tree:
        if node.head == node_id:
            children.append([node.id, node.deprel])

    for child in children:
        graph.edge(head_name=child[0], tail_name=node_id, label=child[1])

    children = [child[0] for child in children]
    for child in children:
        __set_edges(graph, tree, child)
