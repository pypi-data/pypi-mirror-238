import pytest
from googleads_housekeeper.domain.placements import Placements


def test_placements_empty_placement_types():
    placements = Placements(placement_types = None)
    expected = '","'.join(placements._placement_types)
    assert placements.placement_types == expected


def test_placements_single_placement_type():
    placements = Placements(placement_types = ("WEBSITE", "MOBILE_APPLICATION"))
    assert placements.placement_types == 'WEBSITE","MOBILE_APPLICATION'


def test_placements_wrong_placement_type():
    with pytest.raises(ValueError):
        Placements(placement_types = ("WRONG_PLACEMENT", ))


def test_placements_wrong_start_date():
    with pytest.raises(ValueError):
        Placements(start_date="1/1/1/")


def test_placements_start_gt_end_date():
    with pytest.raises(ValueError):
        Placements(start_date="2023-01-01", end_date="2022-01-01")
