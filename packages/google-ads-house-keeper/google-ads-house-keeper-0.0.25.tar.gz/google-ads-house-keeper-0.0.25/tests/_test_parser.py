from dataclasses import dataclass

import pytest
from src.exclusion_specification import AdsExclusionSpecification, ContentExclusionSpecification
import src.parser as parser


@pytest.fixture
def raw_rules():
    return [
        "ads:clicks > 0,impressions > 100",
        "ads:placement_type = 'MOBILE_APPLICATION',ctr = 0",
        "ads:conversions = 0,content:title regexp 'game'"
    ]


@pytest.fixture
def implicit_raw_rules():
    return [
        "clicks > 0,impressions > 100",
        "placement_type = 'MOBILE_APPLICATION',ctr = 0",
        "conversions = 0,content:title regexp 'game'"
    ]


@pytest.fixture
def rules_expression():
    return ("ads:clicks > 0,impressions > 100"
            " OR ads:placement_type = 'MOBILE_APPLICATION',ctr = 0"
            " OR ads:conversions = 0,content:title regexp 'game'")


@pytest.fixture
def expected_specifications():
    return [
        [
            AdsExclusionSpecification("clicks > 0"),
            AdsExclusionSpecification("impressions > 100")
        ],
        [
            AdsExclusionSpecification("placement_type = 'MOBILE_APPLICATION'"),
            AdsExclusionSpecification("ctr = 0")
        ],
        [
            AdsExclusionSpecification("conversions = 0"),
            ContentExclusionSpecification("title regexp 'game'")
        ]
    ]


def test_parser_generate_rules_explicit_types(raw_rules,
                                              expected_specifications):
    prsr = parser.RulesParser()
    rules = prsr.generate_rules(raw_rules)
    assert rules == expected_specifications


def test_parser_generate_rules_implicit_types(implicit_raw_rules,
                                              expected_specifications):
    prsr = parser.RulesParser()
    rules = prsr.generate_rules(implicit_raw_rules)
    assert rules == expected_specifications


def test_parser_generate_rules_from_expression(rules_expression,
                                              expected_specifications):
    prsr = parser.RulesParser()
    rules = prsr.generate_rules(rules_expression)
    assert rules == expected_specifications

