#!/usr/bin/env python3
import graphviz as gv
from argparse import ArgumentParser
import os.path
import shutil


def parse_conll_text(text):
    text = text.split("\n")
    tree = []
    forest = []
    for line in text:
        node = line.split("\t")
        if len(node) != 1:
            tree.append(node)
        else:
            if len(tree) != 0:
                forest.append(tree)
                tree = []
    if len(tree) != 0:
        forest.append(tree)

    return forest


def build_graph(tree):
    graph = gv.Digraph()
    for node in tree:
        node_id = node[0]
        # node_info = "{}\n{} ({})\n{} / {}".format(node[0], node[1], node[2], node[3], node[7])
        node_info = "{}\n{} ({})\n{}".format(node[0], node[1], node[2], node[3])
        graph.node(name=node_id, label=node_info)

    for node in tree:
        if node[6] == "0":
            set_edges(graph, tree, node[0])

    return graph


def set_edges(graph, tree, node_id):
    children = []
    for node in tree:
        if node[6] == node_id:
            children.append([node[0], node[7]])

    for child in children:
        # graph.edge(head_name=node_id, tail_name=child[0], label=child[1])
        graph.edge(head_name=child[0], tail_name=node_id, label=child[1])

    children = [child[0] for child in children]
    for child in children:
        set_edges(graph, tree, child)


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')


def tree_to_png(tree, png_path):
    graph = build_graph(tree)
    graph.filename = png_path[:-4]
    graph.format = png_path[-3:]
    graph.render(cleanup=True)



if __name__ == "__main__":
    parser = ArgumentParser(
        description="Conll-file visualizer based on Graphviz. The results will be saved to ./trees directory.")
    parser.add_argument("-i", dest="filename", required=True,
                        help="input *.conll file", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()
    text = args.filename.read()
    forest = parse_conll_text(text)

    # remove non-empty folder
    if os.path.exists('./trees'):
        shutil.rmtree('./trees')

    num = 1
    for tree in forest:
        graph = build_graph(tree)
        graph.filename = "trees/" + str(num)
        graph.format = "png"
        graph.render(cleanup=True)
        num += 1