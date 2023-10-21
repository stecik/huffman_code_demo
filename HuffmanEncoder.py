from heapq import heappush, heappop
from queue import Queue
from random import shuffle


class Node:
    def __init__(
        self,
        parent=None,
        value=None,
        freq=None,
        leaf=False,
        left_offspring=None,
        right_offspring=None,
    ) -> None:
        self.parent = parent
        self.value = value
        self.freq = freq
        self.leaf = leaf
        self.left_offspring = left_offspring
        self.right_offspring = right_offspring

    def __repr__(self) -> str:
        if self.leaf:
            return str(self.value)
        else:
            return f"N{self.freq}"

    def __str__(self) -> str:
        if self.leaf:
            return str(self.value)
        else:
            return f"N{self.freq}"

    def __lt__(self, other) -> bool:
        return self.freq < other.freq

    def __le__(self, other) -> bool:
        return self.freq <= other.freq

    def __gt__(self, other) -> bool:
        return self.freq > other.freq

    def __ge__(self, other) -> bool:
        return self.freq >= other.freq


class HuffmanTree:
    def __init__(self) -> None:
        self.root = None
        self.code_table = {}
        self.left_value = 0
        self.right_value = 1

    def print_tree(self) -> None:
        q_list = [Queue(), Queue()]
        q = q_list[0]
        q.put(self.root)
        while not q.empty():
            node = q.get()
            print((node, node.freq) if node.leaf else node, end=" ")
            if node.left_offspring:
                q_list[1].put(node.left_offspring)
            if node.right_offspring:
                q_list[1].put(node.right_offspring)
            if q.empty():
                q_list[0], q_list[1] = q_list[1], q_list[0]
                q = q_list[0]
                print()


class Encoder:
    def __init__(self) -> None:
        self.h_tree = HuffmanTree()
        self.heap = []
        self.tree_built = False

    def buid_tree(self) -> None:
        while len(self.heap) >= 2:
            node1 = heappop(self.heap)
            node2 = heappop(self.heap)
            freq = node1.freq + node2.freq
            parent = Node(freq=freq, right_offspring=node2, left_offspring=node1)
            node1.parent = parent
            node2.parent = parent
            heappush(self.heap, parent)
        self.h_tree.root = heappop(self.heap)
        self.tree_built = True

    def build_heap(self, text: str) -> None:
        freq_table = {}
        heap = []
        for char in text:
            if char in freq_table:
                freq_table[char] += 1
            else:
                freq_table[char] = 1
        sorted_ft = sorted(freq_table.items(), key=lambda x: x[1])
        for item in sorted_ft:
            node = Node(value=item[0], freq=item[1], leaf=True)
            self.h_tree.code_table[item[0]] = node
            heappush(heap, node)
        self.heap = heap

    def encode(self, text) -> str:
        if not self.tree_built:
            self.build_heap(text)
            self.buid_tree()
        code = ""
        for char in text:
            char_code = ""
            node = self.h_tree.code_table[char]
            while node.parent:
                if node.parent.left_offspring == node:
                    char_code += str(self.h_tree.left_value)
                elif node.parent.right_offspring == node:
                    char_code += str(self.h_tree.right_value)
                node = node.parent
            code += char_code[::-1]
        return code

    def decode(self, code: str) -> str:
        node = self.h_tree.root
        text = ""
        for char in code:
            if char == str(self.h_tree.left_value):
                node = node.left_offspring
            elif char == str(self.h_tree.right_value):
                node = node.right_offspring
            if node.leaf:
                text += node.value
                text += " "
                node = self.h_tree.root
        return text


if __name__ == "__main__":
    enc = Encoder()
    text = list("aaaaaaaaaaeeeeeeeeeeeeeeeiiiiiiiiiiiisssttttpppppppppppppn")
    shuffle(text)
    print(*text, sep=" ")
    code = enc.encode(text)
    print(code)
    decoded_text = enc.decode(code)
    print(decoded_text)
