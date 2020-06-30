import os
import sys
from datetime import date
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from .DOM_elements import PageLocations

# TODO: Maybe add some functionality to this?
Complex = "This element needs further directions to extract."


def Tag_List(str_list):
    result = ""
    for string in str_list:
        result += "<item>" + string + "</item>"
    return result


class ArticleScraper:
    '''
    A simple scraper to gather information from article-hosting websites.

    The locations in the DOM for each element are given by a PageLocations object
    in the constructor. This class then uses those instructions to gather the info.
    '''

    def __init__(self, site_locations: PageLocations):
        self.site = site_locations
        self.wd = self.init_selenium()
        self.results = {}

    def gather(self, url):
        '''
        Gather the information denoted in self.site from a single page.
        '''
        self.wd.get(url)
        # for info in [x for x in dir(self.site) if not inspect.ismethod(x)]:
        for info in self.site._elements():
            get_func = getattr(self, "get_" + info, self.get)
            element = getattr(self.site, info)
            result = get_func(element)
            if result is None:
                print("Unable to find element defined by", self.site.__name__ + "." + info)
            else:
                self.results[info] = result
        self.results['url'] = url
        self.results['date_aquisition'] = date.today().strftime("%Y-%m-%d")

    def get_authors(self, element):
        objs = self.get(element, several=True)
        return Tag_List(objs)

    def get(self, element, several=False):
        '''
        Default method for extracting an element from the page.

        Handles errors gracefully and waits for the element to become visible before grabbing it.

        Use the `several=True` setting if you want to grab ALL elements on the page that match the
        description given by `element`.
         - NOTE: This should only be used in a custom `get_*` method, so you can do more processing
            after getting this list of elements
        '''
        if element is not None:
            try:
                if several:
                    pageObj = self.wd.find_elements(element.by, element.selector)
                    return [self._extract(element, obj) for obj in pageObj]
                else:
                    pageObj = self.wd.find_element(element.by, element.selector)
                    return self._extract(element, pageObj)
            except NoSuchElementException:
                return None
        return None

    def _extract(self, element, obj):
        if element.attribute is None:
            return obj.text
        else:
            return obj.get_attribute(element.attribute)

    def init_selenium(self, headless=True):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--kiosk")
        chrome_options.add_argument("--disable-extensions")

        if headless:
            chrome_options.add_argument('--headless')
        else:
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--start-maximized")

        chrome_options.add_experimental_option
        (
            'prefs',
            {"download.default_directory": os.getcwd(),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True
             }
        )
        return webdriver.Chrome(ChromeDriverManager(log_level=0).install(),
                                options=chrome_options)


if __name__ == "__main__":
    print(sys.path)
    aS = ArticleScraper(PageLocations)
    print(aS.site.results['title'])
    print(aS.site.keys())
