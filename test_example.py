import re
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("https://www.saucedemo.com/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Swag Labs"))

def test_login(page):
    page.goto("https://www.saucedemo.com/")

    page.locator('input[data-test="username"]').fill("standard_user")
    page.locator('input[data-test="password"]').fill("secret_sauce")
    page.locator('input[data-test="login-button"]').click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.locator('.title')).to_have_text("Products")
