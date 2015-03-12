import unittest
import pdb
from gff3toembl.EMBLContig import EMBLHeader

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
