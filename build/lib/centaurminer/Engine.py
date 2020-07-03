import os
import sys
from datetime import date
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from .DOM_elements import PageLocations


def TagList(str_list, tag="item"):
    '''
    Tags a list and converts to a string - avoids data corruption by using a more complex tag.

    Attributes:
        str_list : list
            List of strings to be joined with tags.
        tag : str
            Tag to use for the list. This tag will be wrapped in `<...>` and `</...>` to close.
    '''
    result = ""
    for string in str_list:
        result += "<item>" + string + "</item>"
    return result


class MiningEngine:
    '''
    A simple mining engine to gather information from article-hosting websites.

    The locations in the DOM for each element are given by a PageLocations object
    in the constructor. This class then uses those instructions to gather the info.

    To give instructions to mine data for a location stored in :code:`PageLocations.xyz`,
    you should create/override the :code:`get_xyz()` function, like so:

    .. code-block:: python

       def get_xyz(self, element):
           \'\'\'
           Arguments:

           * element: (centaurminer.Element) Location of the given element in the page.
           \'\'\'
           # Add instructions here, using self.wd and self.get
           # Below is equivalent to what happens without this override function
           return self.get(element)

    Attributes :
        site : :class:`PageLocations <centaurminer.PageLocations>`
            Stores the location of the elements you want to extract information from.
        wd : :class:`selenium.webdriver`
            The webdriver used to connect to and collect DOM elements from the URL you specify.
        results : dict
            Storage dictionary for the results from data gathering.
    '''

    def __init__(self, site_locations: PageLocations):
        '''
        Arguments:
          site: Should be a class reference, not a class object. PageLocations are static classes, so you never need to instantiate them.
        '''
        self.site = site_locations
        self.wd = self._init_selenium()
        self.results = {}

    def gather(self, url):
        '''
        Gather the information denoted in self.site from a single page.

        Arguments:

        * url: (string) URL for the site you want to mine data from.
        '''
        self.wd.get(url)
        for info in self.site._elements():
            get_func = getattr(self, "get_" + info, None)
            element = getattr(self.site, info)
            
            # Check for strings - just store them directly
            if isinstance(element, str):
                self.results[info] = element
                continue
            
            if get_func is None and element.needsInstructions:
                print(self.site.__name__ + "." + info, "needs further instructions to process - add it to the engine.")
                continue
            elif get_func is None:
                get_func = self.get
            result = get_func(element)
            if result is None:
                print("Unable to find element defined by", self.site.__name__ + "." + info)
            else:
                self.results[info] = result
        self.results['url'] = url
        self.results['date_aquisition'] = date.today().strftime("%Y-%m-%d")

    def get_authors(self, element):
        '''
        Override for author collection instructions.

        Simply gets the list of authors and joins them together, using :func:`TagList`

        Attributes:
            element : :class:`centaurminer.Element`
                The location of the element to mine data from - in this case, it's several elements located with the same identifier.
        '''
        objs = self.get(element, several=True)
        return TagList(objs)

    def get(self, element, several=False):
        '''
        Default method for extracting an element from the page.

        Handles errors gracefully and waits for the element to become visible before grabbing it.
        When creating custom :code:`get_*****` functions, use this function to grab the data from the element, before doing additional processing on it.

        Attributes:
            element: :class:`centaurminer.Element`
                The location of the element to mine data from.
            several: Boolean
                Use to indicate that we should get all elements of this type, instead of the first one on the page.

                .. note::
                   You should only use :code:`several=True` in a custom ``get_*`` method, so you can do more processing
                   after getting this list of elements.

        '''
        if element is not None:
            try:
                if several:
                    pageObj = self.wd.find_elements(element.method, element.selector)
                    return [self._extract(element, obj) for obj in pageObj]
                else:
                    pageObj = self.wd.find_element(element.method, element.selector)
                    return self._extract(element, pageObj)
            except NoSuchElementException:
                return None
        return None

    def _extract(self, element, obj):
        if element.attribute is None:
            return obj.text
        else:
            return obj.get_attribute(element.attribute)

    def _init_selenium(self, headless=True):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("log-level=3")
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
        return webdriver.Chrome(ChromeDriverManager().install(),
                                options=chrome_options)


if __name__ == "__main__":
    print(sys.path)
    miner = MiningEngine(PageLocations)
    miner.gather("https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(20)31352-0/fulltext")
    print(miner.results)
    print(miner.results.keys())
