import pytest
from googleads_housekeeper.services.exclusion_specification import AdsExclusionSpecification, ContentExclusionSpecification
from googleads_housekeeper.services.rules_parser import RulesParser


@pytest.fixture
def rules_parser():
    return RulesParser()


@pytest.fixture
def raw_rules():
    return [
        "GOOGLE_ADS_INFO:clicks > 0,cost > 100",
        "GOOGLE_ADS_INFO:placement_type = MOBILE_APPLICATION,ctr = 0",
        "GOOGLE_ADS_INFO:conversions = 0,WEBSITE_INFO:title regexp game"
    ]


@pytest.fixture
def implicit_raw_rules():
    return [
        "clicks > 0,cost > 100", "placement_type = MOBILE_APPLICATION,ctr = 0",
        "conversions = 0,WEBSITE_INFO:title regexp game"
    ]


@pytest.fixture
def rules_expression():
    return (
        "GOOGLE_ADS_INFO:clicks > 0 AND GOOGLE_ADS_INFO:cost > 100"
        " OR GOOGLE_ADS_INFO:placement_type = MOBILE_APPLICATION AND GOOGLE_ADS_INFO:ctr = 0"
        " OR GOOGLE_ADS_INFO:conversions = 0 AND WEBSITE_INFO:title regexp game"
    )


@pytest.fixture
def expected_specifications():
    return [
        [
            AdsExclusionSpecification("clicks > 0"),
            AdsExclusionSpecification("cost > 100")
        ],
        [
            AdsExclusionSpecification("placement_type = MOBILE_APPLICATION"),
            AdsExclusionSpecification("ctr = 0")
        ],
        [
            AdsExclusionSpecification("conversions = 0"),
            ContentExclusionSpecification(expression="title regexp game")
        ]
    ]


def test_parser_generate_rules_explicit_types(rules_parser, raw_rules,
                                              expected_specifications):
    specifications = rules_parser.generate_specifications(raw_rules)
    assert specifications == expected_specifications


def test_parser_generate_rules_implicit_types(rules_parser, implicit_raw_rules,
                                              expected_specifications):
    specifications = rules_parser.generate_specifications(implicit_raw_rules)
    assert specifications == expected_specifications


def test_parser_generate_rules_from_expression(rules_parser, rules_expression,
                                               expected_specifications):
    specifications = rules_parser.generate_specifications(rules_expression)
    assert specifications == expected_specifications
