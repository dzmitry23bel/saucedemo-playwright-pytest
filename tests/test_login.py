import allure
import pytest

from data.users import INVALID_PASSWORD_USER, LOCKED_OUT_USER, STANDARD_USER, UNKNOWN_USER

pytestmark = pytest.mark.feature("Login")


@allure.title("Standard user can log in successfully")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.smoke
def test_successful_login(login_page):
    inventory_page = login_page.login(STANDARD_USER.username, STANDARD_USER.password)

    assert inventory_page.is_loaded()
    assert "/inventory.html" in inventory_page.current_url


@allure.title("Locked out user is rejected with an error")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_locked_out_user_cannot_login(login_page):
    login_page.login(LOCKED_OUT_USER.username, LOCKED_OUT_USER.password)

    assert login_page.has_error()
    assert "locked out" in login_page.get_error_text().lower()


@allure.title("Wrong password shows a mismatch error")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_invalid_password_shows_error(login_page):
    login_page.login(INVALID_PASSWORD_USER.username, INVALID_PASSWORD_USER.password)

    assert login_page.has_error()
    assert "do not match" in login_page.get_error_text().lower()


@allure.title("Unknown username shows a mismatch error")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_unknown_user_shows_error(login_page):
    login_page.login(UNKNOWN_USER.username, UNKNOWN_USER.password)

    assert login_page.has_error()
    assert "do not match" in login_page.get_error_text().lower()


@allure.title("Login requires both username and password")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password, expected_message",
    [
        ("", "", "Username is required"),
        (STANDARD_USER.username, "", "Password is required"),
    ],
)
def test_login_requires_credentials(login_page, username, password, expected_message):
    login_page.login(username, password)

    assert login_page.has_error()
    assert expected_message in login_page.get_error_text()


@allure.title("Logout returns the user to the login page")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.regression
def test_logout_returns_to_login_page(logged_in_page):
    login_page = logged_in_page.logout()

    assert login_page.username_input.is_visible()
