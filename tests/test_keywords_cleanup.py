import unittest
from ocw_oer_export.utilities import normalize_keywords


class KeywordsCleanupTests(unittest.TestCase):
    """Test suite for verifying the functionality of the description cleanup process."""

    def test_formatting_of_keywords(self):
        """
        Test that formatting, including apostrophes, capitalization,
        and spacing, is handled correctly.
        """
        sample_text = "TCP's and UDPs,U.S.A, chemical industry"
        normalized_keywords = normalize_keywords(sample_text)
        self.assertEqual(normalized_keywords, "TCP's and UDPs|U.S.A|Chemical Industry")

    def test_single_commas_removal(self):
        """Test that single commas are normalized."""
        sample_text = "novel, short story, the city in literature,narrative voice"
        normalized_keywords = normalize_keywords(sample_text)
        self.assertEqual(
            normalized_keywords,
            "Novel|Short Story|The City in Literature|Narrative Voice",
        )

    def test_double_commas_removal(self):
        """Test that double commas are normalized."""
        sample_text = "novel,, short story,, the city in literature,,narrative voice"
        normalized_keywords = normalize_keywords(sample_text)
        self.assertEqual(
            normalized_keywords,
            "Novel|Short Story|The City in Literature|Narrative Voice",
        )

    def test_single_newlines_removal(self):
        """Test that single commas are normalized."""
        sample_text = "novel\nshort story\nthe city in literature\nnarrative voice"
        normalized_keywords = normalize_keywords(sample_text)
        self.assertEqual(
            normalized_keywords,
            "Novel|Short Story|The City in Literature|Narrative Voice",
        )

    def test_double_newlines_removal(self):
        """Test that single commas are normalized."""
        sample_text = (
            "novel\n\nshort story\n\nthe city in literature\n\nnarrative voice"
        )
        normalized_keywords = normalize_keywords(sample_text)
        self.assertEqual(
            normalized_keywords,
            "Novel|Short Story|The City in Literature|Narrative Voice",
        )

    def test_semicolons_removal(self):
        """Test that semicolons are normalized."""
        sample_text = "novel; short story, the city in literature,narrative voice"
        normalized_keywords = normalize_keywords(sample_text)
        self.assertEqual(
            normalized_keywords,
            "Novel|Short Story|The City in Literature|Narrative Voice",
        )
