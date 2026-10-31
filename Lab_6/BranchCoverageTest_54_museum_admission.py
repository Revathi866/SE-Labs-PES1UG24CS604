
import pytest
from museum_admission import ticket_price, group_discount, gallery_entry


# ---------------- TICKET PRICE BRANCH TESTS ----------------

def test_category_valid_and_invalid():
    with pytest.raises(ValueError):
        ticket_price("invalid", 25, "tuesday", False)

    assert ticket_price("adult", 25, "tuesday", False) == 300


def test_age_negative_and_non_negative():
    with pytest.raises(ValueError):
        ticket_price("adult", -1, "tuesday", False)

    assert ticket_price("adult", 25, "tuesday", False) == 300


def test_age_below_five_and_at_least_five():
    assert ticket_price("adult", 4, "tuesday", False) == 0
    assert ticket_price("adult", 5, "tuesday", False) == 300


def test_monday_branch():
    assert ticket_price("adult", 25, "monday", False) == 150


def test_weekend_branch():
    assert ticket_price("adult", 25, "saturday", False) == 350


def test_normal_weekday_branch():
    assert ticket_price("adult", 25, "wednesday", False) == 300


def test_guided_tour_student_branch():
    assert ticket_price("student", 20, "tuesday", True) == 200


def test_guided_tour_non_student_branch():
    assert ticket_price("adult", 25, "tuesday", True) == 400


def test_no_guided_tour_branch():
    assert ticket_price("student", 20, "tuesday", False) == 150


# ---------------- GROUP DISCOUNT BRANCH TESTS ----------------

def test_invalid_group_size_branch():
    with pytest.raises(ValueError):
        group_discount(0, False)


def test_school_group_large_branch():
    assert group_discount(20, True) == 40


def test_school_group_small_branch():
    assert group_discount(19, True) == 25


def test_non_school_group_fifteen_or_more():
    assert group_discount(15, False) == 20


def test_non_school_group_eight_to_fourteen():
    assert group_discount(8, False) == 10


def test_non_school_group_below_eight():
    assert group_discount(7, False) == 0


# ---------------- GALLERY ENTRY BRANCH TESTS ----------------

def test_gallery_full_branch():
    assert gallery_entry(100, 100, False) == "wait"


def test_gallery_exactly_ninety_percent_without_slot():
    assert gallery_entry(90, 100, False) == "queue"


def test_gallery_exactly_ninety_percent_with_slot():
    assert gallery_entry(90, 100, True) == "enter"


def test_gallery_below_ninety_percent():
    assert gallery_entry(89, 100, False) == "enter"
