from selenium import webdriver
import pandas as pd


class EoDataScraper:
    """EoDataScraper

        Parameters
        ----------
            chromedriver_path(path) : full path to chromedriver.exe
            exchange(str) : valid exchange symbol - tsx, nasdaq, nyse

        Examples
        --------
            Example 1:
                scrape = EoDataScraper("C:\\Users\\john\\PycharmProjects\\chromedriver.exe", 'nasdaq')

        Attributes
        ----------
            x(bool) : default True

        Methods
            -------
            get_stock_data(to_csv=False)
                gets all data from website based on specified exchange

    """

    # Attributes
    x = True
    exchanges_list = ['tsx', 'nasdaq', 'nyse']

    # Constructor
    def __init__(self, chromedriver_path, exchange):

        self.driver = webdriver.Chrome(executable_path=f'{chromedriver_path}')

        if exchange.lower() in self.exchanges_list:
            self.exchange = exchange.lower()
        else:
            raise Exception('Sorry that exchange has not been added yet')

    # methods
    def get_stock_data(self, to_csv=False):
        """ Parses xml to a OrderedDict

            Parameters
            ----------
                to_csv(bool): Saves copy of scrape as csv - Default False

            Returns
            -------
                dict: scraped website data

        """
        # page count
        page = 2
        # row count
        counter = 2

        self.driver.get("https://eoddata.com/symbols.aspx")

        if self.exchange == "tsx":
            # click tsx
            tsx = self.driver.find_element_by_xpath("//*[@id='ctl00_cph1_cboExchange']/option[17]")
            tsx.click()
        elif self.exchange == "nasdaq":
            # click nasdaq
            nasdaq = self.driver.find_element_by_xpath("//*[@id='ctl00_cph1_cboExchange']/option[12]")
            nasdaq.click()
        elif self.exchange == "nyse":
            # click nyse
            nyse = self.driver.find_element_by_xpath("//*[@id='ctl00_cph1_cboExchange']/option[14]")
            nyse.click()

        stock_dict = {"Ticker": [],
                      "Company": [],
                      "High": [],
                      "Low": [],
                      "Close": [],
                      "Volume": [],
                      "Change": [],
                      "Percent Change": []}

        while self.x:
            try:

                # get ticker
                ticker = self.driver.find_element_by_xpath(
                    f"//*[@id='ctl00_cph1_divSymbols']/table/tbody/tr[{counter}]/td[1]/a").text
                stock_dict["Ticker"].append(ticker)
                # Get company name
                company = self.driver.find_element_by_xpath(
                    f"//*[@id='ctl00_cph1_divSymbols']/table/tbody/tr[{counter}]/td[2]").text
                stock_dict["Company"].append(company)
                # Get high
                high = self.driver.find_element_by_xpath(f"//*[@id='ctl00_cph1_divSymbols']/table/tbody/"
                                                         f"tr[{counter}]/td[3]").text
                stock_dict["High"].append(high)
                # Get low
                low = self.driver.find_element_by_xpath(f"//*[@id='ctl00_cph1_divSymbols']/table/tbody/"
                                                        f"tr[{counter}]/td[4]").text
                stock_dict["Low"].append(low)
                # get close
                close = self.driver.find_element_by_xpath(f"//*[@id='ctl00_cph1_divSymbols']/table/tbody/"
                                                          f"tr[{counter}]/td[5]").text
                stock_dict["Close"].append(close)
                # get volume
                volume = self.driver.find_element_by_xpath(
                    f"//*[@id='ctl00_cph1_divSymbols']/table/tbody/tr[{counter}]/td[6]").text
                stock_dict["Volume"].append(volume)
                # get change $$$
                change = self.driver.find_element_by_xpath(
                    f"//*[@id='ctl00_cph1_divSymbols']/table/tbody/tr[{counter}]/td[7]").text
                stock_dict["Change"].append(change)
                # get percent change
                percent = self.driver.find_element_by_xpath(
                    f"//*[@id='ctl00_cph1_divSymbols']/table/tbody/tr[{counter}]/td[9]").text
                stock_dict["Percent Change"].append(percent)

                counter += 1

            except:

                counter = 2

                # next
                if page < 27:
                    next_page = self.driver.find_element_by_xpath(f"//*[@id='ctl00_cph1_divLetters']/table/tbody/"
                                                                  f"tr/td[{page}]/a")
                    href = next_page.get_attribute("href")
                    self.driver.get(href)
                    page += 1
                else:
                    self.x = False

        if to_csv:
            df = pd.DataFrame(stock_dict)
            df.to_csv(f'{self.exchange}_data.csv', index=False)


        else:
            return stock_dict
