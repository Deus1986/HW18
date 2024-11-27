import logging
import os

import allure
import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from selene import browser, have


def demowebshop_api_post(url, **kwargs):
    with step("API Requset"):
        response = requests.post("https://demowebshop.tricentis.com/" + url, **kwargs)
        allure.attach(
            body=response.text,
            name="Response",
            attachment_type=AttachmentType.TEXT,
            extension="txt")
        allure.attach(
            body=str(response.cookies),
            name="Cookies",
            attachment_type=AttachmentType.TEXT,
            extension="txt")
        allure.attach(
            body=str(response.request.headers),
            name="Request headers",
            attachment_type=AttachmentType.TEXT,
            extension="txt")
        logging.info(response.status_code)
        logging.info(response.url)
    return response


def test_add_product_authorized_user(setup_browser):
    with allure.step("получить авторизационную куку используя апи"):
        payload = {
            "Email": os.getenv("LOGIN"),
            "Password": os.getenv("PASSWORD"),
            "RememberMe": True
        }
        response = demowebshop_api_post("login", data=payload, allow_redirects=False)
        cookie = response.cookies.get("NOPCOMMERCE.AUTH")

    with allure.step("Добавить товар в корзину, используя апи"):
        demowebshop_api_post("addproducttocart/catalog/31/1/1", cookies={"NOPCOMMERCE.AUTH": cookie})

    with allure.step("Открыть корзину в браузере и проверить, что товар добавлен"):
        browser.open("cart")
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open("cart")
        browser.element('//a[@class="product-name"]').should(have.text("14.1-inch Laptop"))
