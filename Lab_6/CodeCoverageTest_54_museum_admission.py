    
import pytest
from museum_admission import ticket_price, group_discount, gallery_entry


# ---------------- TICKET PRICE TESTS ----------------

def test_invalid_category():
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("invalid", 25, "tuesday", False)


def test_negative_age():
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -1, "tuesday", False)


def test_free_entry_below_five():
    assert ticket_price("adult", 3, "tuesday", False) == 0


def test_monday_discount():
    assert ticket_price("adult", 30, "monday", False) == 150


def test_weekend_extra_charge():
    assert ticket_price("adult", 30, "saturday", False) == 350


def test_student_guided_tour():
    assert ticket_price("student", 20, "tuesday", True) == 200


def test_adult_guided_tour():
    assert ticket_price("adult", 30, "tuesday", True) == 400


def test_regular_weekday_ticket():
    assert ticket_price("senior", 60, "tuesday", False) == 200


# ---------------- GROUP DISCOUNT TESTS ----------------

def test_invalid_group_size():
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(0, False)


def test_school_group_twenty_or_more():
    assert group_discount(20, True) == 40


def test_school_group_below_twenty():
    assert group_discount(10, True) == 25


def test_non_school_group_fifteen_or_more():
    assert group_discount(15, False) == 20


def test_non_school_group_eight_to_fourteen():
    assert group_discount(10, False) == 10


def test_non_school_group_below_eight():
    assert group_discount(4, False) == 0


# ---------------- GALLERY ENTRY TESTS ----------------

def test_gallery_full():
    assert gallery_entry(100, 100, False) == "wait"


def test_gallery_nearly_full_without_slot():
    assert gallery_entry(95, 100, False) == "queue"


def test_gallery_nearly_full_with_slot():
    assert gallery_entry(95, 100, True) == "enter"


def test_gallery_with_enough_space():
    assert gallery_entry(50, 100, False) == "enter"
