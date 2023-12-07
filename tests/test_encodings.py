import pytest
import networkx as nx
import source.tree_generator as treegen
import source.encodings as encodings


# https://www.researchgate.net/profile/N-Deo/publication/228931273_Prufer-like_codes_for_labeled_trees/links/0a85e53ac70b22f152000000/Pruefer-like-codes-for-labeled-trees.pdf
@pytest.fixture
def tree1():
	T = nx.Graph()
	
	vertices = [1,2,3,4,5,6,7,8]
	edges = [(1,2),(2,7),(3,6),(6,7),(7,8),(4,5),(5,8)]
	
	T.add_nodes_from(vertices)
	T.add_edges_from(edges)
	
	return T


## TODO: add the test for Errors when encoding a non-tree graph
test_data_exceptions = [
	(encoding_class, treegen.generate_tree(1)) for encoding_class in
	[encodings.PruferEncoding, encodings.OSAEncoding, encodings.OHAEncoding, encodings.OTAEncoding]
]

test_data_trivial = [
	(encoding_class, treegen.generate_tree(2), []) for encoding_class in
	[encodings.PruferEncoding, encodings.OSAEncoding, encodings.OHAEncoding, encodings.OTAEncoding]
]

test_data_from_paper = [
	(encoding, "tree1", 8, expected_value) for encoding, expected_value in [
		# (encodings.OHAEncoding, [2, 7, 6, 7, 5, 8]), 
		(encodings.OTAEncoding, [2, 6, 5, 7, 7, 8]), 
		(encodings.OSAEncoding, [2, 7, 6, 5, 8, 7])]
]


@pytest.mark.parametrize("encoding_class, tree, expected_encoding", test_data_trivial)
def test_encodings_trivial(encoding_class, tree, expected_encoding):
	assert encoding_class(tree).encoding == expected_encoding


@pytest.mark.parametrize("encoding_class, tree, root, expected_encoding", test_data_from_paper)
def test_encodings_from_paper(encoding_class, tree, root, expected_encoding, request):
	assert encoding_class(request.getfixturevalue(tree), root).encoding == expected_encoding


@pytest.mark.parametrize("encoding_class, tree", test_data_exceptions)
def test_encodings_exceptions(encoding_class, tree):
	with pytest.raises(ValueError):
		encoding_class(tree).encoding