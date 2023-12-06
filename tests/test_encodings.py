import pytest
import source.tree_generator as treegen
import source.encodings as encodings

## TODO: add the test for Errors when encoding a non-tree graph
test_data_exceptions = [
	(encoding_class, treegen.generate_tree(1)) for encoding_class in
	[encodings.PruferEncoding, encodings.OSAEncoding, encodings.OHAEncoding, encodings.OTAEncoding]
]

test_data_trivial = [
	(encoding_class, treegen.generate_tree(2), []) for encoding_class in
	[encodings.PruferEncoding, encodings.OSAEncoding, encodings.OHAEncoding, encodings.OTAEncoding]
]


@pytest.mark.parametrize("encoding_class, tree, expected_encoding", test_data_trivial)
def test_encodings_trivial(encoding_class, tree, expected_encoding):
	assert encoding_class(tree).encoding == expected_encoding


@pytest.mark.parametrize("encoding_class, tree", test_data_exceptions)
def test_encodings_exceptions(encoding_class, tree):
	with pytest.raises(ValueError):
		encoding_class(tree).encoding