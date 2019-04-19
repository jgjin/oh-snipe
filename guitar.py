"""Snipe the button."""

import sys
import time
from urllib.parse import urljoin

import click
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_options(
        headless,
):
    """Set Chrome options."""
    options = Options()
    options.headless = headless

    return options


def get_driver(
        headless=False,
):
    """Get Chrome driver."""
    driver = webdriver.Chrome(options=get_options(headless))
    return driver


@click.command()
@click.option('--queue_id', type=str, help="<queue_id> in https://oh.eecs.umich.edu/course_queues/<queue_id>", required=True)
@click.option("--location", default="just around", help="location message for queue")
@click.option("--description", default="having trouble with my project", help="description message for queue")
@click.option("--auth_wait", default=(60 * 5), help="wait in seconds for authentication before TimeoutException")
@click.option("--submit_wait", default=(60 * 60), help="wait in seconds for queue submission before TimeoutException")
@click.option("--finish_wait", default=(60 * 60), help="wait in seconds before closing remote browser")
def snipe(
        queue_id,
        location,
        description,
        auth_wait,
        submit_wait,
        finish_wait,
):
    """Snipe the button."""
    driver = get_driver()

    driver.get(urljoin(
        "https://oh.eecs.umich.edu/course_queues/",
        queue_id,
    ))

    WebDriverWait(driver, auth_wait).until(
        EC.title_contains("Queue"),
    )

    submittor = WebDriverWait(driver, submit_wait).until(EC.presence_of_element_located((
        By.XPATH,
        "//div[@class='ui fluid button']",
    )))

    fields = driver.find_elements_by_xpath("//div[@class='field']")
    fields[0].find_element_by_xpath("//input").send_keys(
        location,
    )
    fields[1].find_element_by_xpath("//textarea").send_keys(
        description,
    )
    submittor.click()
    
    time.sleep(finish_wait)


if __name__ == "__main__":
    snipe()
