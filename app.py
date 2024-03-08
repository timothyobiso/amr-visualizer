import streamlit as st
import pandas as pd
import altair as alt
import graphviz
from collections import Counter


def parse_amr(amr):
    graph = graphviz.Digraph()
    amr = amr.replace("(", " ( ").replace(")", " ) ").replace(' / ', '/')
    tokens = amr.split()
    stack = []
    nodes = {}
    waiting = []
    parent = []
    for token in tokens:

        if token == "(":
            stack.append(token)
        elif token == ")":
            stack.pop()
            parent = parent[:len(parent)-1]
        elif token.startswith(':'):
            # print("PARENT", parent)
            waiting.append((parent[-1], token))
        else:
            flag = True
            if waiting:
                for p, e in waiting:
                    if "/" not in token:
                        token = nodes[token]
                        flag = False
                    graph.edge(p, token, label=e)
                waiting = []
            nodes[token.split("/")[0]] = token
            graph.node(token)
            if flag:
                parent.append(token)

    return graph


st.markdown("# AMR Visualizer")
text = st.text_area("Enter an AMR graph", height=150, value="(a / and :op1 (b / big) :op2 (c / cat))")

st.graphviz_chart(parse_amr(text))



