from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import urllib

# chrome_options.add_argument("executable_path=~/Desktop/chromedriver")

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

showtimes = {}
theater_search = "https://www.google.com/search?q={theater_name}+showtimes"

with open("theaters.txt") as f:
    theaters = f.readlines()
    theaters = [urllib.parse.quote_plus(theater) for theater in theaters]

for theater in theaters:
    url = theater_search.format(theater_name=theater)
    print(url)
    driver.get(url)
    show_days = driver.find_elements_by_css_selector("li.tb_l")
    print(show_days)
    for i, day in enumerate(show_days):
        day.click()
        showings = driver.find_elements_by_css_selector("div.lr_c_fcb")
        for showing in showings:
            print(showing.text)
