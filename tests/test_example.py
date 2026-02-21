import re
from time import sleep

from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("https://www.saucedemo.com/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Swag Labs"))

def test_login_standard_user(page: Page):
    page.goto("https://www.saucedemo.com/")

    page.locator('input[data-test="username"]').fill("standard_user")
    page.locator('input[data-test="password"]').fill("secret_sauce")
    page.get_by_role('button', name='Login').click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.locator('.title')).to_have_text("Products")


def test_login_locked_out_user(page: Page):
    page.goto("https://www.saucedemo.com/")

    page.locator('input[data-test="username"]').fill("locked_out_user")
    page.locator('input[data-test="password"]').fill("secret_sauce")
    page.get_by_role('button', name='Login').click()

    result = page.locator("//div[contains(@class, 'error')]")
    expect(result).to_have_text("Epic sadface: Sorry, this user has been locked out.")

def test_negative_login(page: Page):
    page.goto("https://www.saucedemo.com/")

    page.locator('input[data-test="username"]').fill("user")
    page.locator('input[data-test="password"]').fill("secret_sauce")
    page.get_by_role('button', name='Login').click()

    result = page.locator("//div[contains(@class, 'error')]")
    expect(result).to_have_text("Epic sadface: Username and password do not match any user in this service")

def test_negative_password(page: Page):
    page.goto("https://www.saucedemo.com/")

    page.locator('input[data-test="username"]').fill("standard_user")
    page.locator('input[data-test="password"]').fill("secret")
    page.get_by_role('button', name='Login').click()

    result = page.locator("//div[contains(@class, 'error')]")
    expect(result).to_have_text("Epic sadface: Username and password do not match any user in this service")



def test_add_products(page: Page):
    page.goto("https://www.saucedemo.com/")

    page.locator('input[data-test="username"]').fill("standard_user")
    page.locator('input[data-test="password"]').fill("secret_sauce")
    page.get_by_role('button', name='Login').click()

    product = page.locator("(//button[contains(text(), 'Add to cart')])[1]")
    product.click()

    add_product = page.locator("(//button[@data-test='remove-sauce-labs-backpack'])[1]")
    expect(add_product).to_have_text("Remove")


def test_remove_products(page: Page):
    page.goto("https://www.saucedemo.com/")

    page.locator('input[data-test="username"]').fill("standard_user")
    page.locator('input[data-test="password"]').fill("secret_sauce")
    page.get_by_role('button', name='Login').click()

    product = page.locator("(//button[contains(text(), 'Add to cart')])[1]")
    product.click()

    add_product = page.locator("(//button[@data-test='remove-sauce-labs-backpack'])[1]")
    add_product.click()

    shopping = page.locator('//a[@data-test="shopping-cart-link"]')
    expect(shopping).not_to_have_text("1")

def test_logout(page: Page):
    page.goto("https://www.saucedemo.com/")

    page.locator('input[data-test="username"]').fill("standard_user")
    page.locator('input[data-test="password"]').fill("secret_sauce")
    page.get_by_role('button', name='Login').click()

    open_menu = page.get_by_text("Open Menu")
    open_menu.click()

    loguot = page.locator('#logout_sidebar_link')
    loguot.click()

    expect(page).to_have_url("https://www.saucedemo.com/")


def test_goto_shopping(page: Page):
    page.goto("https://www.saucedemo.com/")

    page.locator('input[data-test="username"]').fill("standard_user")
    page.locator('input[data-test="password"]').fill("secret_sauce")
    page.get_by_role('button', name='Login').click()

    product = page.locator("(//button[contains(text(), 'Add to cart')])[1]")
    product.click()

    shopping = page.locator(".shopping_cart_link")
    shopping.click()

    checkout = page.locator("#checkout")
    checkout.click()
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")


def test_end2end(page: Page):
    page.goto("https://www.saucedemo.com/")

    page.locator('input[data-test="username"]').fill("standard_user")
    page.locator('input[data-test="password"]').fill("secret_sauce")
    page.get_by_role('button', name='Login').click()

    product = page.locator("(//button[contains(text(), 'Add to cart')])[1]")
    product.click()

    shopping = page.locator(".shopping_cart_link")
    shopping.click()

    checkout = page.locator("#checkout")
    checkout.click()
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")
    page.get_by_placeholder("First Name").fill("Ivan")
    page.get_by_placeholder('Last Name').press_sequentially("Petrov")
    page.get_by_placeholder("Zip/Postal Code").type("Moscow, 12345")

    page.get_by_role("button", name="Continue").click()

    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")
    page.get_by_role("button", name="finish").click()
    expect(page).to_have_url("https://www.saucedemo.com/checkout-complete.html")
    page.get_by_role("button", name="Back Home").click()
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
