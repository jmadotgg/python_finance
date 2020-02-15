from selenium import webdriver

url = 'https://finance.yahoo.com/gainers'
options = webdriver.ChromeOptions();
# Stop selenium from actually opening a browser window
options.add_argument('headless')
options.add_argument("--log-level=3")
browser = webdriver.Chrome(options=options)
browser.get(url)

def get_yahoo_gainers(max_iterations):
    def now_gainers(general_xpath, iterate_variable, max_iterations):
        yahoo_gainers = []
        for x in range(max_iterations):
            yahoo_gainers.append(browser.find_element_by_xpath(general_xpath.replace(iterate_variable, str(x + 1))).text)
        return yahoo_gainers

    try:
        button = browser.find_element_by_xpath('//*[@id="consent-page"]/div/div/div/div[3]/div/form/button[1]')
        
        button.click()
    except Exception as e:
        print(e)
        try:
            button = browser.find_element_by_xpath('//*[@id="consent"]/div/div/div[3]/form/div/button[1]')
            button.click()
        except Exception as e:
            print(e)
            pass
        
    gainers = now_gainers('//*[@id="scr-res-table"]/div[1]/table/tbody/tr[index]/td[1]/a', 'index', max_iterations)
    return gainers

# print(get_yahoo_gainers(5))