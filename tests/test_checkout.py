import pytest


@pytest.mark.smoke
def test_full_checkout_flow_completes_order(checkout_page_with_item):
    step_two = checkout_page_with_item.fill_information("John", "Doe", "12345").continue_to_overview()

    assert step_two.get_item_names() == ["Sauce Labs Backpack"]
    subtotal = step_two.get_subtotal()
    expected_tax = round(subtotal * 0.08, 2)
    assert step_two.get_total() == pytest.approx(subtotal + expected_tax, abs=0.01)

    complete_page = step_two.finish()

    assert complete_page.is_order_complete()
    assert "Thank you" in complete_page.get_complete_header_text()


@pytest.mark.regression
@pytest.mark.parametrize(
    "first_name, last_name, postal_code, expected_message",
    [
        ("", "Doe", "12345", "First Name is required"),
        ("John", "", "12345", "Last Name is required"),
        ("John", "Doe", "", "Postal Code is required"),
    ],
)
def test_checkout_requires_all_fields(
    checkout_page_with_item, first_name, last_name, postal_code, expected_message
):
    checkout_page_with_item.fill_information(first_name, last_name, postal_code)
    checkout_page_with_item.continue_button.click()

    assert expected_message in checkout_page_with_item.get_error_text()
