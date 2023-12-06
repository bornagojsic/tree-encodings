
# class OSAEncoding(TreeEncoding):
# 	def __init__(self, tree):
# 		super().__init__(tree)

# 		self.encoding = self.encode(tree)

# 	def encode(self, tree, root: int=0):
# 		new_tree = copy.deepcopy(tree)
# 		return to_osa_sequence(new_tree)


# class OHAEncoding(TreeEncoding):
# 	def __init__(self, tree):
# 		super().__init__(tree)

# 		self.encoding = self.encode(tree)

# 	def encode(self, tree, root: int=0):
# 		new_tree = copy.deepcopy(tree)
# 		return to_oha_sequence(new_tree)

# def to_ota_sequence(tree, root=0):
# 	C = []
# 	nodes = tree.nodes()
# 	L = [i for i in nodes if tree.degree(i) == 1]
# 	for _ in range(len(nodes)-2):
# 		# ic(C)
# 		# ic(L)
# 		# ic(tree)
# 		# ic(tree.nodes())
# 		u = L.pop(0)
# 		v = list(tree[u])[0]
# 		C.append(v)
# 		L.append(v)
# 		tree.remove_node(u)
# 		if tree.degree(v) == 1 and v != root and v not in L:
# 			L.append(v)
# 	return C


# def to_oha_sequence(tree, root=0):
# 	C = []
# 	nodes = tree.nodes()
# 	L = [i for i in nodes if tree.degree(i) == 1]
# 	for _ in range(len(nodes)-2):
# 		ic(C)
# 		ic(L)
# 		ic(tree)
# 		ic(tree.nodes())
# 		u = L.pop(0)
# 		v = list(tree[u])[0]
# 		C.append(v)
# 		L = [v] + L
# 		tree.remove_node(u)
# 		if tree.degree(v) == 1 and v != root and v not in L:
# 			L = [v] + L
# 	return C


# def to_osa_sequence(tree, root=0):
# 	C = []
# 	nodes = tree.nodes()
# 	L = {i for i in nodes if tree.degree(i) == 1}
# 	for _ in range(len(nodes)-2):
# 		# ic(C)
# 		# ic(L)
# 		# ic(tree)
# 		# ic(tree.nodes())
# 		u = L.pop()
# 		v = list(tree[u])[0]
# 		C.append(v)
# 		L.add(v)
# 		tree.remove_node(u)
# 		if tree.degree(v) == 1 and v != root and v not in L:
# 			L.add(v)
# 	return C