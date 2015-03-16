import unittest
import pdb
from gff3toembl.EMBLContig import EMBLFeature, EMBLHeader

class TestEMBLHeader(unittest.TestCase):

  def test_initialize_header_object(self):
    header = EMBLHeader(
      authors="John Doe",
      classification="UNC",
      genome_type="circular",
      organism="My organism",
      project="PRJ1234",
      publication="Unpublished",
      sequence_identifier="**contig123",
      sequence_length=8,
      sequence_name="chromX",
      taxon_id=5678,
      title="My title"
    )

    self.assertEqual(header.authors, "John Doe")
    self.assertEqual(header.classification, "UNC")
    self.assertEqual(header.genome_type, "circular")
    self.assertEqual(header.organism, "My organism")
    self.assertEqual(header.project, "PRJ1234")
    self.assertEqual(header.publication, "Unpublished")
    self.assertEqual(header.sequence_identifier, "contig123") # Removed non-word characters
    self.assertEqual(header.sequence_length, 8)
    self.assertEqual(header.sequence_name, "chromX")
    self.assertEqual(header.taxon_id, 5678)
    self.assertEqual(header.title, "My title")

  def test_remove_non_word_characters(self):
    header = EMBLHeader()
    test_cases = [
      ('foo', 'foo'),
      ('#foo', 'foo'),
      ('#fo!o', 'foo'),
      ('fo#o', 'foo'),
      ('foo##', 'foo'),
      ("*!#foo", 'foo')
    ]
    for test_string, expected_result in test_cases:
      self.assertEqual(header.remove_non_word_characters(test_string), expected_result)

  def test_format(self):
    header = EMBLHeader()

    header.authors="John Doe"
    header.classification="UNC"
    header.genome_type="circular"
    header.organism="My organism"
    header.project="PRJ1234"
    header.publication="Unpublished"
    header.sequence_identifier="contig123"
    header.sequence_length=1234
    header.sequence_name="chromX"
    header.taxon_id=5678
    header.title="My title"

    expected_header = """\
ID   XXX; XXX; circular; genomic DNA; STD; UNC; 1234 BP.
XX
AC   XXX;
XX
AC * _contig123
XX
PR   Project:PRJ1234;
XX
DE   XXX;
XX
RN   [1]
RA   John Doe;
RT   "My title";
RL   Unpublished.
XX
FH   Key             Location/Qualifiers
FH
FT   source          1..1234
FT                   /organism="My organism"
FT                   /mol_type="genomic DNA"
FT                   /db_xref="taxon:5678"
FT                   /note="chromX"
"""
    calculated_header = header.format()
    for calculated_line,expected_line in zip(calculated_header.split('\n'), expected_header.split('\n')):
      self.assertEqual(calculated_line, expected_line)
    self.assertEqual(len(calculated_header), len(expected_header))

class TestEMBLFeature(unittest.TestCase):

  def create_uninitialized_feature(self):
    # In most cases I don't want tests to run the __init__
    # This creates an otherwise identical EMBLFeature object
    return EMBLFeature.__new__(EMBLFeature)

  def test_initializer(self):
    feature = EMBLFeature(
        feature_type='tRNA',
        start = 100,
        end = 200,
        strand = '+',
        feature_attributes =  {'some_attribute': 'ABC' }
    )
    self.assertEqual(feature.feature_type, 'tRNA')
    self.assertEqual(feature.start, 100)
    self.assertEqual(feature.end, 200)
    self.assertEqual(feature.strand, '+')
    self.assertEqual(feature.locus_tag, None)
    self.assertEqual(feature.translation_table, 11)

    expected_attributes = [('some_attribute', 'ABC')]
    self.assertItemsEqual(feature.attributes, expected_attributes)

  def test_initializer_for_ignored_features(self):
    feature = EMBLFeature(
        feature_type='ncRNA',
        start = 100,
        end = 200,
        strand = '+',
        feature_attributes =  {'some_attribute': 'ABC' }
    )
    self.assertEqual(feature.format(), None)

  def test_format(self):
    feature = self.create_uninitialized_feature()
    feature.feature_type = "feature_type"
    feature.start = 1
    feature.end = 10
    feature.strand = ''
    feature.attributes = [
      ("attributeA", "foo"),
      ("attributeB", 'bar'),
      ("attributeB", 'baz')
    ]
    calculated_string = feature.format()
    expected_string = """\
FT   feature_type    1..10
FT                   /attributeA="foo"
FT                   /attributeB="bar"
FT                   /attributeB="baz"
"""

    for calculated_line,expected_line in zip(calculated_string.split('\n'), expected_string.split('\n')):
      self.assertEqual(calculated_line, expected_line)
    self.assertEqual(len(calculated_string), len(expected_string))

  def test_pick_feature_builder(self):
    feature = self.create_uninitialized_feature()
    self.assertEqual(feature.pick_feature_builder('CDS'), feature.create_CDS_feature)
    self.assertEqual(feature.pick_feature_builder('ncRNA'), feature.create_empty_feature)
    self.assertEqual(feature.pick_feature_builder('other'), feature.create_default_feature)

  def test_create_empty_feature(self):
    feature = self.create_uninitialized_feature()
    feature.create_empty_feature(
        feature_type='ncRNA',
        start = 100,
        end = 200,
        strand = '+',
        feature_attributes =  {'some_attribute': 'ABC' },
        locus_tag = None,
        translation_table = 11
    )
    self.assertEqual(feature.format(), None)

  def test_create_default_feature(self):
    feature = self.create_uninitialized_feature()
    feature.create_default_feature(
        feature_type='tRNA',
        start = 100,
        end = 200,
        strand = '+',
        feature_attributes =  {'some_attribute': 'ABC' },
        locus_tag = None,
        translation_table = 11
    )
    self.assertEqual(feature.feature_type, 'tRNA')
    self.assertEqual(feature.start, 100)
    self.assertEqual(feature.end, 200)
    self.assertEqual(feature.strand, '+')
    self.assertEqual(feature.locus_tag, None)
    self.assertEqual(feature.translation_table, 11)

    expected_attributes = [('some_attribute', 'ABC')]
    self.assertItemsEqual(feature.attributes, expected_attributes)

  def test_create_default_feature_with_locus_tag(self):
    feature = self.create_uninitialized_feature()
    feature.create_default_feature(
        feature_type='tRNA',
        start = 100,
        end = 200,
        strand = '+',
        feature_attributes =  {'some_attribute': 'ABC', 'locus_tag': 'XYZ_123'},
        locus_tag = 'A_LOCUS_TAG',
        translation_table = 11
    )
    self.assertEqual(feature.feature_type, 'tRNA')
    self.assertEqual(feature.start, 100)
    self.assertEqual(feature.end, 200)
    self.assertEqual(feature.strand, '+')
    self.assertEqual(feature.locus_tag, 'A_LOCUS_TAG')
    self.assertEqual(feature.translation_table, 11)

    expected_attributes = [('some_attribute', 'ABC'), ('locus_tag', 'A_LOCUS_TAG_123')]
    self.assertItemsEqual(feature.attributes, expected_attributes)

  def test_create_CDS_feature(self):
    feature = self.create_uninitialized_feature()
    feature.create_CDS_feature(
        feature_type='tRNA',
        start = 100,
        end = 200,
        strand = '+',
        feature_attributes =  {'some_attribute': 'ABC' },
        locus_tag = None,
        translation_table = 11
    )
    self.assertEqual(feature.feature_type, 'tRNA')
    self.assertEqual(feature.start, 100)
    self.assertEqual(feature.end, 200)
    self.assertEqual(feature.strand, '+')
    self.assertEqual(feature.locus_tag, None)
    self.assertEqual(feature.translation_table, 11)

    expected_attributes = [('some_attribute', 'ABC'), ('transl_table', 11)]
    self.assertItemsEqual(feature.attributes, expected_attributes)

  def test_format_attribute(self):
    feature = self.create_uninitialized_feature()
    calculated_string = feature.format_attribute('attributeA', 'foo')
    expected_string = 'FT                   /attributeA="foo"'
    self.assertEqual(calculated_string, expected_string)

    calculated_string = feature.format_attribute('transl_table', 11)
    expected_string = 'FT                   /transl_table=11'
    self.assertEqual(calculated_string, expected_string)

  def test_lookup_attribute_formatter(self):
    feature = self.create_uninitialized_feature()
    formatter = feature.lookup_attribute_formatter('attributeA')
    self.assertEqual(formatter, feature.default_attribute_formatter)

    feature = self.create_uninitialized_feature()
    formatter = feature.lookup_attribute_formatter('transl_table')
    self.assertEqual(formatter, feature.translation_table_attribute_formatter)

  def test_translation_table_attribute_formatter(self):
    feature = self.create_uninitialized_feature()
    calculated_string = feature.translation_table_attribute_formatter('transl_table', 11)
    expected_string = 'FT                   /transl_table=11'
    self.assertEqual(calculated_string, expected_string)

  def test_format_multiline_attribute(self):
    feature = self.create_uninitialized_feature()
    long_attribute = 'abc efg hij klm nop qrs tuvw xyz abc efg hij klm nop qrs tuvw xyz'
    calculated_string = feature.format_attribute('product', long_attribute)
    expected_string = """\
FT                   /product="abc efg hij klm nop qrs tuvw xyz abc efg hij klm
FT                   nop qrs tuvw xyz"\
"""
    self.assertEqual(calculated_string, expected_string)

    long_attribute = """\
abc efg hij klm nop qrs tuvw xyz abc efg hij klm nop qrs tuvw xyz \
abc efg hij klm nop qrs tuvw xyz abc_efg hij klm nop qrs tuvw xyz\
"""
    calculated_string = feature.format_attribute('product', long_attribute)
    expected_string = """\
FT                   /product="abc efg hij klm nop qrs tuvw xyz abc efg hij klm
FT                   nop qrs tuvw xyz abc efg hij klm nop qrs tuvw xyz abc_efg
FT                   hij klm nop qrs tuvw xyz"\
"""
    self.assertEqual(calculated_string, expected_string)

  def test_lookup_attribute_creator(self):
    feature = self.create_uninitialized_feature()
    self.assertEqual(feature.lookup_attribute_creator('some_key'),
                     feature.create_default_attributes)
    self.assertEqual(feature.lookup_attribute_creator('product'),
                     feature.create_product_attributes)
    self.assertEqual(feature.lookup_attribute_creator('locus_tag'),
                     feature.create_locus_tag_attributes)
    self.assertEqual(feature.lookup_attribute_creator('eC_number'),
                     feature.create_EC_number_attributes)
    self.assertEqual(feature.lookup_attribute_creator('inference'),
                     feature.create_inference_attributes)
    self.assertEqual(feature.lookup_attribute_creator('protein_id'),
                     feature.ignore_attributes)
    self.assertEqual(feature.lookup_attribute_creator('ID'),
                     feature.ignore_attributes)


  def test_create_product_attributes(self):
    feature = self.create_uninitialized_feature()
    test_cases = [
      ('abc,efg,hij', [('product', "abc")]),
      ('hypothetical protein,efg,hij', [('product', "efg")]),
      ('efg,hypothetical protein,hij', [('product', "efg")]),
      ('hypothetical protein,hypothetical protein,hij', [('product', "hij")]),
      ('hypothetical protein', [('product', "Uncharacterised protein")]),
      ('hypothetical protein,Unknown protein abc', [('product', "Uncharacterised protein abc")]),
      ('hypothetical protein,unknown protein abc', [('product', "uncharacterised protein abc")])
    ]
    for test_case, expected_result in test_cases:
      calculated_result = feature.create_product_attributes('product', test_case)
      self.assertEqual(calculated_result, expected_result)

  def test_create_locus_tag_attributes(self):
    feature = self.create_uninitialized_feature()
    feature.locus_tag = None

    calculated_attributes = feature.create_locus_tag_attributes('locus_tag', 'ABC123')
    expected_attributes = [('locus_tag', 'ABC123')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_locus_tag_attributes('locus_tag', 'ABC123_XYZ')
    expected_attributes = [('locus_tag', 'ABC123_XYZ')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_locus_tag_attributes('locus_tag', 'ABC_123_XYZ')
    expected_attributes = [('locus_tag', 'ABC_123_XYZ')]
    self.assertEqual(calculated_attributes, expected_attributes)

    feature.locus_tag = "some_other_tag"

    calculated_attributes = feature.create_locus_tag_attributes('locus_tag', 'ABC123')
    expected_attributes = [('locus_tag', 'some_other_tag_ABC123')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_locus_tag_attributes('locus_tag', 'ABC123_XYZ')
    expected_attributes = [('locus_tag', 'some_other_tag_XYZ')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_locus_tag_attributes('locus_tag', 'ABC_123_XYZ')
    expected_attributes = [('locus_tag', 'some_other_tag_XYZ')]
    self.assertEqual(calculated_attributes, expected_attributes)

  def test_create_EC_number_attributes(self):
    feature = self.create_uninitialized_feature()
    calculated_attributes = feature.create_EC_number_attributes('eC_number', '123')
    expected_attributes = [('EC_number', '123')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_EC_number_attributes('eC_number', '123,ABC')
    expected_attributes = [('EC_number', '123'), ('EC_number', 'ABC')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_EC_number_attributes('eC_number', '123,123')
    expected_attributes = [('EC_number', '123')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_EC_number_attributes('eC_number', '123,ABC,123')
    expected_attributes = [('EC_number', '123'), ('EC_number', 'ABC')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_EC_number_attributes('eC_number', 'B,A,A')
    expected_attributes = [('EC_number', 'B'), ('EC_number', 'A')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_EC_number_attributes('eC_number', 'B,A,B')
    expected_attributes = [('EC_number', 'B'), ('EC_number', 'A')]
    self.assertEqual(calculated_attributes, expected_attributes)

  def test_create_inference_attributes(self):
    feature = self.create_uninitialized_feature()
    calculated_attributes = feature.create_inference_attributes('inference', '123')
    expected_attributes = [('inference', '123')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_inference_attributes('inference', '123,ABC')
    expected_attributes = [('inference', '123'), ('inference', 'ABC')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_inference_attributes('inference', '123,123')
    expected_attributes = [('inference', '123'), ('inference', '123')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_inference_attributes('inference', '123,ABC,123')
    expected_attributes = [('inference', '123'), ('inference', 'ABC'), ('inference', '123')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_inference_attributes('inference', 'B,A,A')
    expected_attributes = [('inference', 'B'), ('inference', 'A'), ('inference', 'A')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_inference_attributes('inference', 'B,A,B')
    expected_attributes = [('inference', 'B'), ('inference', 'A'), ('inference', 'B')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_inference_attributes('inference', '123,similar to AA sequence:UniProtKB:Q2G282')
    expected_attributes = [('inference', '123'), ('db_xref', "UniProtKB/Swiss-Prot:Q2G282")]
    self.assertEqual(calculated_attributes, expected_attributes)

  def test_should_convert_to_db_xref(self):
    feature = self.create_uninitialized_feature()
    self.assertTrue(feature.should_convert_to_db_xref('similar to AA sequence:UniProtKB:Q2G282'))
    self.assertTrue(feature.should_convert_to_db_xref('protein motif:Pfam:PF01475.13'))
    self.assertTrue(feature.should_convert_to_db_xref('protein motif:CLUSTERS:PRK09462'))
    self.assertTrue(feature.should_convert_to_db_xref('protein motif:TIGRFAMs:TIGR01327'))
    self.assertTrue(feature.should_convert_to_db_xref('protein motif:Cdd:COG1932'))
    self.assertTrue(feature.should_convert_to_db_xref('SOME_PREFIX protein motif:Cdd:COG1932'))
    self.assertTrue(feature.should_convert_to_db_xref('protein motif:Cdd:COG1932i SOME_SUFFIX'))
    self.assertTrue(feature.should_convert_to_db_xref('SOME_PREFIX protein motif:Cdd:COG1932i SOME_SUFFIX'))
    self.assertFalse(feature.should_convert_to_db_xref('protein'))
    self.assertFalse(feature.should_convert_to_db_xref('something else'))
    self.assertFalse(feature.should_convert_to_db_xref('motif:Cdd:COG1932i'))

  def test_convert_to_db_xref(self):
    feature = self.create_uninitialized_feature()
    test_cases = [
      ('similar to AA sequence:UniProtKB:Q2G282', "UniProtKB/Swiss-Prot:Q2G282"),
      ('protein motif:Pfam:PF01475.13', "PFAM:PF01475.13"),
      ('protein motif:CLUSTERS:PRK09462', "CDD:PRK09462"),
      ('protein motif:TIGRFAMs:TIGR01327', "TIGRFAM:TIGR01327"),
      ('protein motif:Cdd:COG1932', "CDD:COG1932"),
      ('SOME_PREFIX protein motif:Cdd:COG1932', "SOME_PREFIX CDD:COG1932"),
      ('protein motif:Cdd:COG1932 SOME_SUFFIX', "CDD:COG1932 SOME_SUFFIX"),
      ('SOME_PREFIX protein motif:Cdd:COG1932 SOME_SUFFIX', "SOME_PREFIX CDD:COG1932 SOME_SUFFIX")
    ]
    for test_input, expected_output in test_cases:
      self.assertEqual(feature.convert_to_db_xref(test_input), expected_output)
    for test_input in ['protein', 'something else', 'motif:Cdd:COG1932i']:
      self.assertRaises(ValueError, feature.convert_to_db_xref, test_input)

  def test_create_translation_table_attribute(self):
    feature = self.create_uninitialized_feature()
    calculated_attributes = feature.create_translation_table_attributes('transl_table', '11')
    expected_attributes = [('transl_table', '11')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_translation_table_attributes('transl_table', 'something_else')
    expected_attributes = [('transl_table', 'something_else')]
    self.assertEqual(calculated_attributes, expected_attributes)

  def test_create_default_attributes(self):
    feature = self.create_uninitialized_feature()
    calculated_attributes = feature.create_default_attributes('some_value', 'A')
    expected_attributes = [('some_value', 'A')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_default_attributes('some_value', 'A,B')
    expected_attributes = [('some_value', 'A')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_default_attributes('some_value', 'B,A')
    expected_attributes = [('some_value', 'B')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_default_attributes('some_value', 'A,A')
    expected_attributes = [('some_value', 'A')]
    self.assertEqual(calculated_attributes, expected_attributes)

    calculated_attributes = feature.create_default_attributes('some_value', 'A,A,B')
    expected_attributes = [('some_value', 'A')]
    self.assertEqual(calculated_attributes, expected_attributes)

  def test_format_coordinates(self):
    feature = self.create_uninitialized_feature()
    calculated_coordinates = feature.format_coordinates(1, 10, '')
    expected_coordinates = '1..10'
    self.assertEqual(calculated_coordinates, expected_coordinates)

    calculated_coordinates = feature.format_coordinates(1, 10, '-')
    expected_coordinates = 'complement(1..10)'
    self.assertEqual(calculated_coordinates, expected_coordinates)

    calculated_coordinates = feature.format_coordinates(1, 10, '***NONSENCE***')
    expected_coordinates = '1..10'
    self.assertEqual(calculated_coordinates, expected_coordinates)
