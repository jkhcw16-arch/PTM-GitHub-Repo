"""SHACL regression tests for PTM 1.3.0 candidate additions.

Run from the same directory as:
  ptm-1.3.0-additions.ttl
  ptm-1.3.0-additions.shacl.ttl
Requires: rdflib, pyshacl
"""
from pathlib import Path
import unittest
from rdflib import Graph
from pyshacl import validate

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OWL = ROOT / "ontology" / "ptm-1.3.0-additions.ttl"
SHAPES = ROOT / "ontology" / "ptm-1.3.0-additions.shacl.ttl"
PM = "https://pairwise-memory.dev/ontology/1.0/"


def parse_turtle(text: str) -> Graph:
    return Graph().parse(data=text, format="turtle")


class PTMShaclTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ont = Graph().parse(OWL, format="turtle")
        cls.shapes = Graph().parse(SHAPES, format="turtle")

    def assertConforms(self, turtle: str):
        conforms, _, report = validate(
            parse_turtle(turtle), shacl_graph=self.shapes,
            ont_graph=self.ont, advanced=True
        )
        self.assertTrue(conforms, report)

    def assertViolates(self, turtle: str, expected_text: str | None = None):
        conforms, _, report = validate(
            parse_turtle(turtle), shacl_graph=self.shapes,
            ont_graph=self.ont, advanced=True
        )
        self.assertFalse(conforms, "Expected SHACL violation, graph conformed")
        if expected_text:
            self.assertIn(expected_text, report)

    @staticmethod
    def whole_vector_fixture() -> str:
        axes = ["a2", "a3", "a7", "a11", "a13"]
        delta = [-3, 0, 5, -2, 4]
        lines = [f"@prefix pm: <{PM}> ."]
        for a in axes:
            lines.append(f"pm:{a} a pm:PrimeAxis .")
        for i, (axis, dv) in enumerate(zip(axes, delta)):
            lines += [
                f"pm:d{i} a pm:SignedDeltaComponent ; pm:onPrimeAxis pm:{axis} ; pm:deltaValue {dv} .",
                f"pm:i{i} a pm:InverseExponentiationCheck ; pm:validatesDeltaComponent pm:d{i} ; "
                f"pm:onPrimeAxis pm:{axis} ; pm:positiveExponent {max(dv,0)} ; pm:negativeExponent {max(-dv,0)} .",
                f"pm:s0c{i} a pm:AxisCoordinate ; pm:onPrimeAxis pm:{axis} ; pm:exponentValue 10 .",
                f"pm:s1c{i} a pm:AxisCoordinate ; pm:onPrimeAxis pm:{axis} ; pm:exponentValue {10+dv} .",
            ]
        lines += [
            'pm:s0 a pm:State ; pm:schemaVersion "1.3.0" ; pm:hasAxisCoordinate pm:s0c0,pm:s0c1,pm:s0c2,pm:s0c3,pm:s0c4 .',
            'pm:s1 a pm:State ; pm:schemaVersion "1.3.0" ; pm:hasAxisCoordinate pm:s1c0,pm:s1c1,pm:s1c2,pm:s1c3,pm:s1c4 .',
            'pm:t0 a pm:TimePoint . pm:t1 a pm:TimePoint .',
            'pm:m a pm:PairwiseMemory ; pm:hasSourceState pm:s0 ; pm:hasTargetState pm:s1 ; pm:hasSourceTime pm:t0 ; pm:hasTargetTime pm:t1 ; pm:schemaVersion "1.3.0" ; pm:hasDeltaComponent pm:d0,pm:d1,pm:d2,pm:d3,pm:d4 .',
            'pm:rt a pm:VectorRoundTripCheck ; pm:validatesMemory pm:m ; pm:hasInverseExponentiationCheck pm:i0,pm:i1,pm:i2,pm:i3,pm:i4 .',
        ]
        return "\n".join(lines)

    def test_whole_vector_round_trip_conforms(self):
        self.assertConforms(self.whole_vector_fixture())

    def test_missing_inverse_axis_rejected(self):
        bad = self.whole_vector_fixture().replace(",pm:i4", "")
        self.assertViolates(bad, "Every delta component")

    def test_wrong_inverse_component_rejected(self):
        bad = self.whole_vector_fixture().replace(
            "pm:positiveExponent 5 ; pm:negativeExponent 0",
            "pm:positiveExponent 4 ; pm:negativeExponent 0",
        )
        self.assertViolates(bad, "Inverse exponentiation")

    def test_duplicate_inverse_axis_rejected(self):
        bad = self.whole_vector_fixture().replace(
            "pm:i0,pm:i1,pm:i2,pm:i3,pm:i4",
            "pm:i0,pm:i1,pm:i2,pm:i3,pm:i4,pm:ix",
        )
        bad += "\npm:ix a pm:InverseExponentiationCheck ; pm:validatesDeltaComponent pm:d0 ; pm:onPrimeAxis pm:a2 ; pm:positiveExponent 0 ; pm:negativeExponent 3 ."
        self.assertViolates(bad, "Duplicate inverse-exponentiation checks")

    def test_negative_factor_exponent_rejected(self):
        bad = self.whole_vector_fixture().replace(
            "pm:positiveExponent 0 ; pm:negativeExponent 3",
            "pm:positiveExponent -1 ; pm:negativeExponent 2",
        )
        self.assertViolates(bad)

    def test_wrong_delta_arithmetic_rejected(self):
        bad = self.whole_vector_fixture().replace(
            "pm:d2 a pm:SignedDeltaComponent ; pm:onPrimeAxis pm:a7 ; pm:deltaValue 5",
            "pm:d2 a pm:SignedDeltaComponent ; pm:onPrimeAxis pm:a7 ; pm:deltaValue 6",
        )
        self.assertViolates(bad, "target exponent minus source exponent")

    def test_wrong_schema_rejected(self):
        bad = self.whole_vector_fixture().replace(
            'pm:s1 a pm:State ; pm:schemaVersion "1.3.0"',
            'pm:s1 a pm:State ; pm:schemaVersion "9.9.9"',
        )
        self.assertViolates(bad, "same schemaVersion")

    def test_algebraic_composition_valid_and_invalid(self):
        p = f"@prefix pm: <{PM}> .\n"
        valid = p + '''
pm:a a pm:PrimeAxis .
pm:s0 a pm:State ; pm:schemaVersion "1.3.0" ; pm:hasAxisCoordinate pm:c0 .
pm:s1 a pm:State ; pm:schemaVersion "1.3.0" ; pm:hasAxisCoordinate pm:c1 .
pm:s2 a pm:State ; pm:schemaVersion "1.3.0" ; pm:hasAxisCoordinate pm:c2 .
pm:c0 a pm:AxisCoordinate ; pm:onPrimeAxis pm:a ; pm:exponentValue 4 .
pm:c1 a pm:AxisCoordinate ; pm:onPrimeAxis pm:a ; pm:exponentValue 7 .
pm:c2 a pm:AxisCoordinate ; pm:onPrimeAxis pm:a ; pm:exponentValue 5 .
pm:d1 a pm:SignedDeltaComponent ; pm:onPrimeAxis pm:a ; pm:deltaValue 3 .
pm:d2 a pm:SignedDeltaComponent ; pm:onPrimeAxis pm:a ; pm:deltaValue -2 .
pm:dc a pm:SignedDeltaComponent ; pm:onPrimeAxis pm:a ; pm:deltaValue 1 .
pm:t0 a pm:TimePoint . pm:t1 a pm:TimePoint . pm:t2 a pm:TimePoint .
pm:m1 a pm:PairwiseMemory ; pm:hasSourceState pm:s0 ; pm:hasTargetState pm:s1 ; pm:hasSourceTime pm:t0 ; pm:hasTargetTime pm:t1 ; pm:schemaVersion "1.3.0" ; pm:hasDeltaComponent pm:d1 .
pm:m2 a pm:PairwiseMemory ; pm:hasSourceState pm:s1 ; pm:hasTargetState pm:s2 ; pm:hasSourceTime pm:t1 ; pm:hasTargetTime pm:t2 ; pm:schemaVersion "1.3.0" ; pm:hasDeltaComponent pm:d2 .
pm:mc a pm:PairwiseMemory ; pm:hasSourceState pm:s0 ; pm:hasTargetState pm:s2 ; pm:hasSourceTime pm:t0 ; pm:hasTargetTime pm:t2 ; pm:schemaVersion "1.3.0" ; pm:hasDeltaComponent pm:dc .
pm:comp pm:composesFirst pm:m1 ; pm:composesSecond pm:m2 ; pm:compositeMemory pm:mc .
'''
        self.assertConforms(valid)
        self.assertViolates(valid.replace("pm:deltaValue 1 .", "pm:deltaValue 2 .", 1))


if __name__ == "__main__":
    unittest.main(verbosity=2)
