from selenium import webdriver

class Gainers():
    url = 'https://finance.yahoo.com/gainers'
    options = webdriver.ChromeOptions();
    # Stop selenium from actually opening a browser window
    options.add_argument('headless')
    options.add_argument("--log-level=3")
    browser = webdriver.Chrome(options=options)
    browser.get(url)

    def get_yahoo_gainers(general_xpath, iterate_variable, max_iterations):
        yahoo_gainers = []
        for x in range(max_iterations):
            yahoo_gainers.append(Gainers.browser.find_element_by_xpath(general_xpath.replace(iterate_variable, str(x + 1))).text)
        return yahoo_gainers
    
    def now_gainers(max_iterations):
        try:
            button = Gainers.browser.find_element_by_xpath('/html/body/div/div/div/form/div/button[2]')
            button.click()
        except Exception as e:
            print(e)
            try:
                button = Gainers.browser.find_element_by_xpath('//*[@id="consent"]/div/div/div[3]/form/div/button[1]')
                button.click()
            except Exception as e:
                print(e)
                pass
            
        gainers = Gainers.get_yahoo_gainers('//*[@id="scr-res-table"]/div[1]/table/tbody/tr[index]/td[1]/a', 'index', max_iterations)
        return gainers
    

# new_gainers = Gainers.now_gainers(10)
# print(new_gainers)
