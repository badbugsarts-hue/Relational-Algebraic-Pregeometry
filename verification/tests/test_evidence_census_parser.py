import hashlib
import unittest

from verification.scripts.evidence_census_parser import (
    CensusError,
    compare_payloads,
    git_blob_id,
    report_payload,
    scan,
)


class CensusParserTests(unittest.TestCase):
    def counts(self, source: str) -> dict[str, int]:
        counts = {key: 0 for key in ("A-", "A", "B", "C", "D", "E")}
        for item in scan(source):
            counts[item.evidence_class] += 1
        return counts

    def test_plain_markers(self):
        self.assertEqual(
            self.counts(
                r"\catmark{A-} \catmark{A} \catmark{B} "
                r"\catmark{C} \catmark{D} \catmark{E}"
            ),
            {"A-": 1, "A": 1, "B": 1, "C": 1, "D": 1, "E": 1},
        )

    def test_plain_and_pending_e(self):
        items = scan(r"\catmark{E} \catmark{E\,pending} \catmark{E pending}")
        self.assertEqual([item.evidence_class for item in items], ["E", "E", "E"])
        self.assertEqual(
            [item.qualifier for item in items],
            [None, "pending", "pending"],
        )

    def test_a_minus_is_not_a(self):
        counts = self.counts(r"\catmark{A-} \catmark{A}")
        self.assertEqual(counts["A-"], 1)
        self.assertEqual(counts["A"], 1)

    def test_comments_are_ignored(self):
        counts = self.counts("% \\catmark{E}\n\\catmark{D}\n")
        self.assertEqual(counts["E"], 0)
        self.assertEqual(counts["D"], 1)

    def test_escaped_percent_is_not_comment(self):
        self.assertEqual(self.counts(r"50\% \catmark{B}")["B"], 1)

    def test_escaped_and_longer_pseudo_invocations_are_ignored(self):
        counts = self.counts(
            r"\\catmark{E} \catmarker{E} \catmark@internal{E} \catmark{D}"
        )
        self.assertEqual(counts["E"], 0)
        self.assertEqual(counts["D"], 1)

    def test_verbatim_like_environments_are_ignored(self):
        for environment in ("verbatim", "Verbatim", "lstlisting", "minted"):
            with self.subTest(environment=environment):
                source = (
                    f"\\begin{{{environment}}}\n"
                    "\\catmark{E}\n"
                    f"\\end{{{environment}}}\n"
                    "\\catmark{C}\n"
                )
                counts = self.counts(source)
                self.assertEqual(counts["E"], 0)
                self.assertEqual(counts["C"], 1)

    def test_unbalanced_verbatim_fails_closed(self):
        with self.assertRaises(CensusError):
            scan("\\begin{verbatim}\n\\catmark{E}\n")

    def test_adjacent_markers(self):
        counts = self.counts(r"\catmark{A}\,\catmark{E}")
        self.assertEqual(counts["A"], 1)
        self.assertEqual(counts["E"], 1)

    def test_nested_balanced_braces_in_pending_qualifier(self):
        items = scan(r"\catmark{E\,\text{pending}}")
        self.assertEqual(items[0].evidence_class, "E")
        self.assertEqual(items[0].qualifier, "pending")

    def test_command_definition_is_not_an_occurrence(self):
        source = (
            r"\newcommand{\catmark}[1]{[#1]} "
            r"\renewcommand{\catmark}[1]{(#1)} "
            r"\providecommand{\catmark}[1]{#1} "
            r"\newcommand\catmark[1]{#1} "
            r"\catmark{E}"
        )
        self.assertEqual(self.counts(source)["E"], 1)

    def test_unknown_qualifier_fails_closed(self):
        with self.assertRaises(CensusError):
            scan(r"\catmark{E\,review}")

    def test_unknown_suffix_fails_closed(self):
        with self.assertRaises(CensusError):
            scan(r"\catmark{Efoo}")

    def test_unknown_class_fails_closed(self):
        with self.assertRaises(CensusError):
            scan(r"\catmark{A+}")

    def test_unclosed_argument_fails_closed(self):
        with self.assertRaises(CensusError):
            scan(r"\catmark{E")

    def test_missing_argument_fails_closed(self):
        with self.assertRaises(CensusError):
            scan(r"\catmark[optional]")

    def test_occurrences_include_source_hashes_and_locations(self):
        payload = b"line one\n\\catmark{E\\,pending}\n"
        result = report_payload("fixture.tex", payload)
        row = result["occurrences"][0]
        self.assertEqual(row["line"], 2)
        self.assertEqual(row["source_sha256"], hashlib.sha256(payload).hexdigest())
        self.assertEqual(row["source_blob"], git_blob_id(payload))

    def test_comparison_detects_addition_and_deletion(self):
        addition = compare_payloads(
            "base.tex",
            b"\\catmark{A}\n",
            "head.tex",
            b"\\catmark{A}\n\\catmark{E}\n",
        )
        self.assertEqual(addition["conservation"]["count_delta"]["E"], 1)
        self.assertEqual(len(addition["conservation"]["added_occurrences"]), 1)

        deletion = compare_payloads(
            "base.tex",
            b"\\catmark{A}\n\\catmark{E}\n",
            "head.tex",
            b"\\catmark{A}\n",
        )
        self.assertEqual(deletion["conservation"]["count_delta"]["E"], -1)
        self.assertEqual(len(deletion["conservation"]["removed_occurrences"]), 1)

    def test_same_count_changed_locations_is_reported(self):
        result = compare_payloads(
            "base.tex",
            b"\\catmark{A}\ntext\n\\catmark{E}\n",
            "head.tex",
            b"\\catmark{A}\n\\catmark{E}\ntext\n",
        )
        conservation = result["conservation"]
        self.assertTrue(conservation["counts_equal"])
        self.assertFalse(conservation["locations_equal"])
        self.assertTrue(conservation["same_count_locations_changed"])


if __name__ == "__main__":
    unittest.main()
