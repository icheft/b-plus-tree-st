from __future__ import annotations

from .bplustree import BPlusTree, LeafNode
from graphviz import Digraph, nohtml
import streamlit as st


class GraphableBPlusTree(BPlusTree):

    def clean(self, order=5):
        self.root = LeafNode(order)
        self.order = order

    def view_graph(self, graph_name='bplustree'):
        if self.root.is_empty():
            print('The B+ Tree is empty!')
            return

        g = Digraph('g',
                    node_attr={'shape': 'record', 'height': '.1', 'color': '#198964'})
        # g.format = 'png'
        queue = [self.root]

        while len(queue) > 0:
            node = queue.pop(0)

            if not isinstance(node, LeafNode):
                queue += node.values
                # print(queue)

            design = ''
            if isinstance(node, LeafNode):
                # for i in range(len(node.keys)):
                #     design += '<f' + str(i*2) + '> | {{ <f' + str(i*2 + 1) + '> {' + str(
                #         i) + '} | {{' + ', '.join(map(str, node.values[i])) + '}} }}| '
                # design += '<f' + str(len(node.keys)*2) + '>'
                for i in range(len(node.keys)):
                    design += '<f' + str(i*2) + '> | <f' + \
                        str(i*2 + 1) + '> {' + str(i) + '} | '
                design += '<f' + str(len(node.keys)*2) + '>'
            else:
                for i in range(len(node.keys)):
                    design += '<f' + str(i*2) + '> | <f' + \
                        str(i*2 + 1) + '> {' + str(i) + '} | '
                design += '<f' + str(len(node.keys)*2) + '>'

            g.node('node'+str(node.uid), nohtml(design.format(*node.keys)))

            if not isinstance(node, LeafNode):
                for i, value in enumerate(node.values):
                    mid_key = len(value.keys)
                    g.edge('node{}:f{}'.format(node.uid, i*2),
                           'node{}:f{}'.format(value.uid, mid_key))
            else:
                pass
        return g


if __name__ == '__main__':
    print('Initializing B+ tree...')
    bplustree = GraphableBPlusTree(order=3)
    # bplustree.insert(1, 'real1')
    bplustree.insert(1, 'real3')
    bplustree.insert(1, 'real2')
    bplustree.insert(1, 'real1')
    bplustree.insert(1, '1')
    bplustree.insert(1, 'real4')
    bplustree.insert(5, '5')
    # bplustree.insert(2, '1')
    # bplustree.insert(1, '1')
    # bplustree.insert(1, '1')
    bplustree.insert(0, '0')

    # bplustree.insert(2, 'real3')
    # bplustree.insert(2, 'real4')
    # bplustree.insert(1, 'real5')
    # bplustree.insert(1, 'real5')
    # bplustree.insert(1, 'real5')
    # bplustree.insert(5)
    # bplustree.insert(5)
    # bplustree.insert(7)
    # bplustree.insert(7)
    # bplustree.insert(2)
    # bplustree.show_bfs()
    bplustree.show_all_data()

    g = bplustree.view_graph()
    st.graphviz_chart(g)
