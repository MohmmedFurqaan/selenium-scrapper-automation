from selenium import webdriver
from selenium.webdriver.common.by import By
from scrapper.config.paths import PathConfig

class OuterHtml:
    '''
        Args:
            query : default set to the laptop, this is the generally the keyword on which you want to scrap the data. this parameter is generally the product on which you want to scrap the data
            page_to_scrap : default set to the 10, total pages you want to scrap
    '''
    def __init__(self, query : str = "laptop", page_to_scrap : int = 10):
        
        # using the chrome as a webDriver 
        self.driver = webdriver.Chrome()

        # search query
        self.q = query

        # total number of the pages to scrap
        self.page = page_to_scrap

        # setting up the current_page to 1
        self.current_page = 1

    def scrap_outer_html(self, file_path : PathConfig) -> None:
        '''
        it will scrap the each product from the page and store it into the file path

        Args:
            file_path : the actual file path where the html data is being stored 
        ''' 

        # fetch the link of the amazon from the site
        for page in range(1, self.page):
            self.driver.get(f"https://www.flipkart.com/search?q={self.q}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page={page}")

        self.driver.implicitly_wait(2.1)
        elems = self.driver.find_elements(By.CLASS_NAME, "jIjQ8S")

        for elem in elems:
            self.driver.implicitly_wait(2.1)
            d = elem.get_attribute("outerHTML")
            with open(f"D:/PY/python/selenium-tutorial/data/scrapped_data/html_files/{self.q}_{self.current_page}.html", "w", encoding="utf-8") as f:
                f.write(d)
                self.current_page+=1

        # close the driver after the usage
        self.driver.close()
