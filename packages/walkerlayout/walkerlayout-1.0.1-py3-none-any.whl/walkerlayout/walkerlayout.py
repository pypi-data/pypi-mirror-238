"""An implementation of Walker's algorithm for level-based tree layouting/drawing:
https://onlinelibrary.wiley.com/doi/abs/10.1002/spe.4380200705

Including improvements by Buchheim et al. (2002) to make it linear in time:
https://link.springer.com/content/pdf/10.1007/3-540-36151-0_32.pdf


Copyright 2023 Elias Foramitti

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

from typing import Any, Generic, Optional, TypeVar

try:
    import networkx as nx
except ImportError:
    nx = None


def _build_from_networkx(graph: nx.Graph, node: Any, parent: Any, layouting: WalkerLayouting[Any]) -> None:
    for child in graph.neighbors(node):
        if child == parent:
            continue
        if child in layouting:
            raise ValueError("Graph is not acyclic, i.e. not a tree")
        layouting.add(node, child)
        _build_from_networkx(graph, child, node, layouting)


T = TypeVar("T")


class WalkerLayouting(Generic[T]):
    @staticmethod
    def from_networkx(graph: nx.Graph, root_node: Any) -> WalkerLayouting[Any]:
        """Builds a WalkerLayouting object from a networkx graph given a root node.

        (if the graph should be layouted only once, it is recommended to use `layout_networkx` instead)

        Args:
            graph (nx.Graph): The tree to be layouted (an acyclic graph (i.e. tree) with all nodes reachable from `root_node`)
            root_node (Any): The key of the root node in the nx.Graph

        Raises:
            ImportError: if networkx is not installed
            ValueError: if the root node is not in the graph
            ValueError: if the graph is not acyclic
            ValueError: if not all nodes are reachable from the root node

        Returns:
            WalkerLayouting[Any]: The resulting layouting object

        Example:
            ```
            G = nx.Graph()
            G.add_nodes_from([1, 2, 3, 4, 5, 6])
            G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6)])
            layouting = WalkerLayouting.from_networkx(G, 1)
            layout = layouting.get_layout()
            ```
        """
        if nx is None:
            raise ImportError("networkx is not installed")
        if root_node not in graph.nodes:
            raise ValueError(f"Root node {root_node} not found in graph")
        layouting = WalkerLayouting(root_node)
        _build_from_networkx(graph, root_node, None, layouting)
        if len(layouting) != len(graph.nodes):
            raise ValueError(f"{len(graph.nodes) - len(layouting)} nodes are not reachable from root node {root_node}")
        return layouting

    @staticmethod
    def layout_networkx(
        graph: nx.Graph,
        root_node: Any,
        origin: tuple[float, float] = (0.0, 0.0),
        scalex: float = 1.0,
        scaley: float = 1.0,
    ) -> dict[Any, tuple[float, float]]:
        """Layouts a networkx graph.

        Args:
            graph (nx.Graph): The tree to be layouted (an acyclic graph (i.e. tree) with all nodes reachable from `root_node`)
            root_node (Any): The key of the root node in the nx.Graph
            origin (tuple[float, float], optional): The position of the root node in the layout. Defaults to (0.0, 0.0).
            scalex (float, optional): A scaling factor applied to all x-coordinates. Defaults to 1.0.
            scaley (float, optional): A scaling factor applied to all y-coordinates. (Set to -1 to flip the layout vertically.) Defaults to 1.0.

        Raises:
            ImportError: if networkx is not installed
            ValueError: if the root node is not in the graph
            ValueError: if the graph is not acyclic
            ValueError: if not all nodes are reachable from the root node

        Returns:
            dict[Any, tuple[float, float]]: The resulting layout as a mapping from node keys to coordinates (x, y)

        Example:
            ```
            G = nx.Graph()
            G.add_nodes_from([1, 2, 3, 4, 5, 6])
            G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6)])
            layouting = WalkerLayouting.from_networkx(G, 1)
            layout = layouting.get_layout()
            ```
        """
        return WalkerLayouting.from_networkx(graph, root_node).get_layout(origin, scalex, scaley)

    def __init__(self, root_key: T) -> None:
        """An object to implicitly define a tree structure and layout it using Walker's algorithm.

        Each node in the tree is defined via a unique key. The root node is defined at instantiation.

        Args:
            root_key: The key of the root node.
        """
        self.root = Node(root_key)
        self.nodes = {root_key: self.root}

    def __contains__(self, key: T) -> bool:
        return key in self.nodes

    def __len__(self) -> int:
        return len(self.nodes)

    def add(self, parent_key: T, child_key: T, index: Optional[int] = None) -> None:
        """Add a new node to the tree.

        Args:
            parent_key: The key of the existing parent node.
            child_key: The key of the new child node.
            index (Optional[int], optional): The index at which the new node
                should be inserted into the children list of the parent.
                Defaults to the end of the parent's children list.

        Raises:
            ValueError: If the parent node is not found in the tree
            ValueError: If the tree already contains a node with the given key
            ValueError: If the given index is negative
        """
        if index is not None and index < 0:
            raise ValueError(f"Index {index} out of range")
        if parent_key not in self.nodes:
            raise ValueError(f"Parent node key {parent_key} not found")
        if child_key in self.nodes:
            raise ValueError(f"Child node key {child_key} already exists")
        parent = self.nodes[parent_key]
        child = Node(child_key, parent)
        self.nodes[child_key] = child
        if index is None or index >= len(parent.children):
            parent.children.append(child)
        else:
            parent.children.insert(index, child)
    
    def add_from(self, edge_list: list[tuple[T, T] | tuple[T, T, int]]) -> None:
        """Add multiple new nodes to the tree at once.

        Args:
            edge_list: A list of tuples (parent_key, child_key) or (parent_key, child_key, index) defining the tree structure.

        Raises:
            ValueError: If the parent node is not found in the tree
            ValueError: If the tree already contains a node with the given key
        """
        # sort edge_list by index
        edge_list.sort(key=lambda x: x[2] if len(x) > 2 else -1)
        not_done = []
        for edge in edge_list:
            if edge[0] not in self: # if parent not yet in tree
                not_done.append(edge)
                continue
            if len(edge) > 2:
                self.add(edge[0], edge[1], edge[2])
            else:
                self.add(edge[0], edge[1])
        if len(not_done) >= len(edge_list):
            raise ValueError("The following parent nodes are not in the tree and not defined (connectedly) by the edge_list: " + ', '.join([e[0] for e in edge_list]))
        if len(not_done) > 0:
            self.add_from(not_done)

    def remove(self, key: T) -> None:
        """Remove a node (and all its descendants) from the tree
        (except for the root node, which cannot be removed; instead a new
        object should be instantiated in that case).

        Args:
            key: The key of the node to be removed.

        Raises:
            ValueError: If the key is not found in the tree
            ValueError: If the key refers to the root node
        """
        if key not in self:
            raise ValueError(f"Node key {key} not found")
        node = self.nodes[key]
        if node.parent is None:
            raise ValueError(f"Cannot remove root node {key}, instantiate a new object instead")
        del self.nodes[key]
        node.parent.children.remove(node)
        for child in node.children:
            self.remove(child.key)

    def get_layout(
        self, origin: tuple[float, float] = (0.0, 0.0), scalex: float = 1.0, scaley: float = 1.0
    ) -> dict[T, tuple[float, float]]:
        """Retrieve a layout for the tree.

        Args:
            origin (tuple[float, float], optional): The position of the root node in the layout. Defaults to (0.0, 0.0).
            scalex (float, optional): A scaling factor applied to all x-coordinates. Defaults to 1.0.
            scaley (float, optional): A scaling factor applied to all y-coordinates. (Set to -1 to flip the layout vertically.) Defaults to 1.0.

        Returns:
            dict[T, tuple[float, float]]: A mapping from node keys to coordinates (x, y)
        """
        self.root.first_walk()
        self.root.second_walk()
        layout = {}
        for node in self.nodes.values():
            layout[node.key] = (node.x * scalex + origin[0], node.level * scaley + origin[1])
        return layout


class Node(Generic[T]):
    def __init__(self, key: T, parent: Optional[Node[T]] = None) -> None:
        self.key: T = key
        self.children: list[Node[T]] = []
        self.parent: Optional[Node[T]] = parent
        self.level: int = 0
        if self.parent is not None:
            self.level = self.parent.level + 1
        self.x: float = 0.0
        self.modifier: float = 0.0
        self._has_left_sibling: Optional[bool] = None  # None if unknown
        self._left_sibling: Optional[Node[T]] = None
        self.shift: float = 0.0
        self.change: float = 0.0
        self.thread: Optional[Node[T]] = None
        self.ancestor: Optional[Node[T]] = None
        self.index: Optional[int] = None

    def reset(self) -> None:
        self.x = 0.0
        self.modifier = 0.0
        self._has_left_sibling = None
        self._left_sibling = None
        self.shift = 0.0
        self.change = 0.0
        self.thread = None
        self.ancestor = None
        self.index = None

    def left_sibling(self) -> Optional[Node[T]]:
        if self._has_left_sibling is None:
            # left sibling not yet computed
            if self.parent is None:  # this node is root
                self._has_left_sibling = False
            else:
                if self.index_in_parent() == 0:  # this node is left most child
                    self._has_left_sibling = False
                else:
                    self._has_left_sibling = True
                    self._left_sibling = self.parent.children[self.index_in_parent() - 1]
        return self._left_sibling if self._has_left_sibling else None

    def index_in_parent(self) -> int:
        if self.index is None:
            if self.parent is None:
                self.index = 0
            else:
                try:
                    self.index = self.parent.children.index(self)
                except ValueError:
                    raise ValueError(f"Node {self.key} is not a child of its parent {self.parent.key}")
        return self.index

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def next_left(self) -> Optional[Node[T]]:
        if self.is_leaf():
            return self.thread
        else:
            return self.children[0]

    def next_right(self) -> Optional[Node[T]]:
        if self.is_leaf():
            return self.thread
        else:
            return self.children[-1]

    def first_walk(self) -> None:
        self.reset()
        left_sibling = self.left_sibling()
        if self.is_leaf():
            if left_sibling is not None:
                self.x = left_sibling.x + 1
            # else x is kept at 0
            return
        default_ancestor = self.children[0]
        for child in self.children:
            child.first_walk()
            default_ancestor = child._apportion(default_ancestor)
        self._execute_shifts()
        midpoint = (self.children[0].x + self.children[-1].x) / 2
        if left_sibling is not None:
            self.x = left_sibling.x + 1
            self.modifier = self.x - midpoint
        else:
            self.x = midpoint

    def second_walk(self, modifier_sum: Optional[float] = None) -> None:
        if modifier_sum is None:  # only in root
            assert self.parent is None
            modifier_sum = -self.x
        self.x += modifier_sum
        for child in self.children:
            child.second_walk(modifier_sum + self.modifier)

    def _apportion(self, default_ancestor: Node[T]) -> Node[T]:
        left_sibling = self.left_sibling()
        if left_sibling is not None:
            # v ... vertex (node); s ... subtree width (modifier sum)
            # i ... inner; o ... outer; r ... right; l .. left
            vir: Node[T] = self
            vor: Node[T] = self
            vil: Node[T] = left_sibling
            assert self.parent is not None
            assert len(self.parent.children) > 0
            vol: Node[T] = self.parent.children[0]
            sir = sor = self.modifier
            sil = vil.modifier
            sol = vol.modifier
            while vil.next_right() is not None and vir.next_left() is not None:
                vil = vil.next_right()
                vir = vir.next_left()
                assert vol.next_right() is not None
                assert vor.next_left() is not None
                vol = vol.next_left()
                vor = vor.next_right()
                vor.ancestor = self
                shift = (vil.x + sil) - (vir.x + sir) + 1
                if shift > 0:
                    a = self._ancestor(vil, default_ancestor)
                    self._move_subtree(a, shift)
                    sir = sir + shift
                    sor = sor + shift
                sil += vil.modifier
                sir += vir.modifier
                sol += vol.modifier
                sor += vor.modifier
            if vil.next_right() is not None and vor.next_right() is None:
                vor.thread = vil.next_right()
                vor.modifier += sil - sor
            else:
                if vir.next_left() is not None and vol.next_left() is None:
                    vol.thread = vir.next_left()
                    vol.modifier += sir - sol
                default_ancestor = self
        return default_ancestor

    def _execute_shifts(self) -> None:
        shift = 0.0
        change = 0.0
        for child in reversed(self.children):
            child.x += shift
            child.modifier += shift
            change += child.change
            shift += child.shift + change

    def _ancestor(self, node: Node[T], default_ancestor: Node[T]) -> Node[T]:
        if node.ancestor is not None and node.ancestor.parent == self.parent:
            return node.ancestor
        return default_ancestor

    def _move_subtree(self, left_subtree: Node[T], shift: float) -> None:
        subtrees: float = float(self.index_in_parent() - left_subtree.index_in_parent())
        if subtrees == 0:
            subtrees = 0.0000001
        self.change = self.change - shift / subtrees
        self.shift = self.shift + shift
        left_subtree.change = left_subtree.change + shift / subtrees
        self.x = self.x + shift
        self.modifier = self.modifier + shift

__all__ = ["WalkerLayouting"]