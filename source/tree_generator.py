from icecream import ic

import random
import networkx as nx
import matplotlib.pyplot as plt


def generate_tree(n: int):
	return nx.random_labeled_tree(n)


def generate_trees(n: int, k: int):
	trees = [generate_tree(n) for i in range(k)]
	return trees


def generate_random_size_trees(n: int, min_size: int=1, max_size: int|None=None):
	if max_size is None:
		max_size = n
	if min_size > max_size:
		raise ValueError("min_size cannot be greater than max_size")
	trees = [generate_tree(random.randint(min_size, max_size + 1)) for i in range(n)]
	return trees


if __name__ == '__main__':
	T = generate_random_size_trees(1, 1, 100)[0]
	ic(T.nodes())
	ic(T.edges())
	pos = nx.spring_layout(T)
	nx.draw(T, pos, with_labels=True, node_color="skyblue", font_color="black", font_weight="bold", edge_color="gray", linewidths=1, alpha=0.7)
	plt.show()