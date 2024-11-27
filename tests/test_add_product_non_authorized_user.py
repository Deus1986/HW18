import allure
from selene import browser, have
from tests.test_add_product_authorized_user import demowebshop_api_post

base_url = "https://demowebshop.tricentis.com/"


def test_add_product_non_authorized_user():
    with allure.step("Добавить товар в корзину, используя апи"):
        response = demowebshop_api_post("addproducttocart/catalog/31/1/1")
        cookie = response.cookies.get_dict()

    with allure.step("Открыть корзину в браузере и проверить, что товар добавлен"):
        browser.open(base_url + "cart")
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie["Nop.customer"]})
        browser.open(base_url + "cart")
        browser.element('//a[@class="product-name"]').should(have.text("14.1-inch Laptop"))
