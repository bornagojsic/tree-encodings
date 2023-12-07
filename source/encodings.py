import copy
import networkx as nx
import matplotlib.pyplot as plt

from icecream import ic


class Leaves:
	def check_parameters(self, tree, root, type):
		if not isinstance(tree, nx.Graph):
			raise ValueError("The tree must be a networkx Graph object")
		
		if not nx.is_tree(tree):
			raise ValueError("The graph is not a tree")
		
		if len(tree) < 2:
			raise ValueError("The tree must have at least 2 nodes")
		
		if not isinstance(root, int):
			raise ValueError("The root node must be an integer")

		if root > len(tree):
			raise ValueError("The root node must be in the tree")
		
		if not isinstance(type, str):
			raise ValueError("The type must be a string")

		if type not in ["list", "set"]:
			raise ValueError("The type must be either 'list' or 'set'")


	def __init__(self, tree, root: int=0, type: str="list", ascending: bool=True):
		self.check_parameters(tree, root, type)
		
		self.type = type
		self.ascending = ascending
		self.tree = tree
		self.root = root

		self.leaves_list = self.leaves_list(tree, root)
		self.leaves_set = self.leaves_set(tree, root)

		self.leaves = self.get_from_type()

	def leaves_list(self, tree, root: int=0):
		if (tree is None):
			tree = self.tree

		if (root is None):
			root = self.root

		return [i for i in tree.nodes() if tree.degree(i) == 1 and i != root]
	
	def leaves_set(self, tree, root: int=0):
		if (tree is None):
			tree = self.tree

		if (root is None):
			root = self.root

		return {i for i in tree.nodes() if tree.degree(i) == 1 and i != root}
	
	def from_tree(self, type: str, tree, root: int=0):
		if (tree is None):
			tree = self.tree

		if (root is None):
			root = self.root
		
		if type == "set":
			return self.leaves_set(tree, root)
		else:
			return self.leaves_list(tree, root)
	
	def get_from_type(self):
		if self.type == "set":
			return self.leaves_set
		else:
			return self.leaves_list

	def pop(self, index: int=0):
		if not isinstance(index, int):
			raise ValueError("The index must be an integer")
		
		if index < 0 or index > len(self.leaves):
			index = index % len(self.leaves)

		if self.type == "set":
			if index != 0:
				raise ValueError("The index must be 0 for a set")
			
			if self.ascending:
				return self.leaves.pop()
			
			s_list = list(self.leaves)
			result = s_list.pop(-1)
			
			self.leaves = set(s_list)
			
			return result
		
		if self.ascending:
			return self.leaves.pop(index)
		
		return self.leaves.pop(- index - 1)
	
	def append(self, node):
		if node in self.leaves:
			raise ValueError(f"The node is already in {self}")
		
		self.leaves_list = self.leaves_list + [node]
		self.leaves_set = self.leaves_set | {node}
		self.leaves = self.get_from_type()
	
	def prepend(self, node):
		if node in self.leaves:
			raise ValueError(f"The node is already in {self}")
		
		self.leaves_list = [node] + self.leaves_list
		self.leaves_set = {node} | self.leaves_set
		self.leaves = self.get_from_type()
	
	def insert(self, node):
		if node in self.leaves:
			raise ValueError(f"The node is already in {self}")
		
		# if self.type == "list":
		# 	self.leaves_list = self.leaves_list[:len(self.leaves_list)//2] + [node] + self.leaves_list[len(self.leaves_list)//2:]
		self.leaves_set = self.leaves_set | {node}
		self.leaves = self.get_from_type()
			

	def __str__(self):
		return str(self.leaves)


class TreeEncoding:
	def __init__(self, tree):
		self.vertices_mapping = self.get_vertices_mapping(tree.nodes())
		self.reverse_vertices_mapping = self.get_reverse_vertices_mapping(tree.nodes())
		self.tree = self.parse_tree(tree)

	def get_vertices_mapping(self, vertices):
		return {vertex: i for i, vertex in enumerate(vertices)}

	def get_reverse_vertices_mapping(self, vertices):
		return {i: vertex for i, vertex in enumerate(vertices)}

	def parse_tree(self, tree):
		if not nx.is_tree(tree):
			raise ValueError("The graph is not a tree")

		if len(tree) < 2:
			raise ValueError("The tree must have at least 2 nodes")
		
		tree_ = copy.deepcopy(tree)

		if tree.nodes() != list(range(len(tree))):
			tree_ = nx.convert_node_labels_to_integers(tree_, first_label=0, ordering="sorted")

		return tree_

	def encode(self, tree):
		encoding = []
		encoding.append(tree.nodes())
		encoding.append(tree.edges())
		return encoding

	def parse_encoded_vertices(self, encoding):
		return [self.reverse_vertices_mapping[vertex] for vertex in encoding]
	
	def __str__(self):
		return str(self.encoding)
		


class PruferEncoding(TreeEncoding):
	def __init__(self, tree):
		super().__init__(tree)

		self.encoding = self.encode(self.tree)

	def encode(self, tree):
		encoding = nx.to_prufer_sequence(tree)
		return self.parse_encoded_vertices(encoding)


class OneListEncoding(TreeEncoding):
	def __init__(self, tree, root: int=0, ascending: bool=True):
		super().__init__(tree)

		if root > len(tree):
			raise ValueError("The root node must be in the tree")
		
		self.root = root
		self.ascending = ascending

		self.encoding = self.encode()

	def get_leaves(self, tree):
		return Leaves(tree, self.root, "list", self.ascending)
	
	def add_leaf(self, leaves: Leaves, leaf):
		leaves.append(leaf)

	def encode(self):
		n = len(self.tree.nodes())
		tree_ = copy.deepcopy(self.tree)

		C = []
		L = self.get_leaves(tree_)
		
		for _ in range(n-2):
			u = L.pop()
			v = get_leaf_parent(tree_, u) # u is a leaf, so it has only one neighbor
			
			C.append(v) # add v to the encoding
			tree_.remove_node(u)
			
			if tree_.degree(v) == 1 and v != self.root:
				self.add_leaf(L, v)
		
		return self.parse_encoded_vertices(C)


class OTXEncoding(OneListEncoding):
	def __init__(self, tree, root: int=0, ascending: bool=True):
		super().__init__(tree, root, ascending)


class OTAEncoding(OTXEncoding):
	def __init__(self, tree, root: int=0):
		super().__init__(tree, root, True)


class OTDEncoding(OTXEncoding):
	def __init__(self, tree, root: int=0):
		super().__init__(tree, root, False)


class OSXEncoding(OneListEncoding):
	def __init__(self, tree, root: int=0, ascending: bool=True):
		super().__init__(tree, root, ascending)

	def get_leaves(self, tree):
		return Leaves(tree, self.root, "set", self.ascending)
	
	def add_leaf(self, leaves: Leaves, leaf):
		leaves.insert(leaf)


class OSAEncoding(OSXEncoding):
	def __init__(self, tree, root: int=0):
		super().__init__(tree, root, True)

# BUG: this is causing an KeyError
class OSDEncoding(OSXEncoding):
	def __init__(self, tree, root: int=0):
		super().__init__(tree, root, False)


class OHXEncoding(OneListEncoding):
	def __init__(self, tree, root: int=0, ascending: bool=True):
		super().__init__(tree, root, ascending)



## FIXME: this is not working
class OHAEncoding(OneListEncoding):
	def __init__(self, tree, root: int=0):
		super().__init__(tree, root, True)

	def get_leaves(self, tree):
		return Leaves(tree, self.root, "list", True)
	
	def add_leaf(self, leaves: Leaves, leaf):
		leaves.prepend(leaf)



def get_leaf_parent(tree, leaf):
	return list(tree[leaf])[0]


def main():
	# T = nx.random_labeled_tree(6)
	T = nx.Graph()
	# T.add_nodes_from([0, 1, 2, 3, 4, 5])
	# T.add_edges_from([(1, 0), (0, 2), (2, 5), (5, 4), (4, 3)])

	vertices = [1,2,3,4,5,6,7,8]
	edges = [(1,2),(2,7),(3,6),(6,7),(7,8),(4,5),(5,8)]

	# vertices = [vertex - 1 for vertex in vertices]
	# edges = [(edge[0] - 1, edge[1] - 1) for edge in edges]

	T.add_nodes_from(vertices)
	T.add_edges_from(edges)

	print(T.nodes())
	print(T.edges())
	
	# pos = nx.spring_layout(T)
	# nx.draw(T, pos, with_labels=True, node_color="skyblue", font_color="black", font_weight="bold", edge_color="gray", linewidths=1, alpha=0.7)
	# plt.show()
	
	# print("Prufer:", PruferEncoding(T))
	# print("OHA0  :", OHAEncoding(T))
	# print("OTA0  :", OTAEncoding(T))
	# print("OSA0  :", OSAEncoding(T))
	print("OHA8  :", OHAEncoding(T, 7))
	print("OTA8  :", OTAEncoding(T, 7))
	print("OSA8  :", OSAEncoding(T, 7))
	# print("OHD8  :", OHDEncoding(T, 7))
	print("OTD8  :", OTDEncoding(T, 7))
	# print("OSD8  :", OSDEncoding(T, 7))


if __name__ == '__main__':
	main()
