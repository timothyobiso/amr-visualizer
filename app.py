import streamlit as st
import graphviz


example = """(a / and
      :op1 (r / run-02
            :ARG0 (p / person
                  :ARG0-of (s / shepherd-01))
            :direction (u / up))
      :op2 (c / catch-01
            :ARG0 p
            :ARG1 (h2 / he))
      :time (s2 / see-01
            :ARG0 p
            :ARG1 (e / event)))"""


def parse_amr(amr):
    graph = graphviz.Digraph()
    amr = amr.replace("(", " ( ").replace(")", " ) ").replace(' / ', '/')
    tokens = amr.split()
    nodes = {}
    parent = []
    waiting = None

    for token in tokens:
        if token == ")":
            parent.pop()
        elif token == "(":
            continue
        elif token.startswith(':'):
            waiting = (parent[-1], token)
        else:
            parent.append(token)
            if waiting:
                if "/" not in token:
                    token = nodes[token]
                    parent.pop()
                graph.edge(waiting[0], token, label=waiting[1])
                waiting = None
            nodes[token.split("/")[0]] = token
            graph.node(token)
    return graph


st.markdown("# AMR Visualizer")
text = st.text_area("Enter an AMR graph", height=300, value=example)

st.graphviz_chart(parse_amr(text))



