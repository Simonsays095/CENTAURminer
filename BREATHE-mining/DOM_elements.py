from selenium.webdriver.common.by import By


class Element:
    '''
    Simple struct to store instructions to find an element on a page.
    '''
    def __init__(self, by, selector):
        self.attribute = None
        if isinstance(by, str):
            self.by = getattr(By, by.upper())
        else:
            self.by = by
            print(type(self.by))
        self.selector = selector

    def get_attribute(self, attributeName):
        '''Chainable to tell which attribute to extract'''
        self.attribute = attributeName
        return self


class MetaData(Element):
    '''A special type of Element that's derived from the metadata'''

    def __init__(self, name):
        self.attribute = "content"
        self.by = By.XPATH
        self.selector = "html/head/meta[@name='" + name + "' or @property='" + name + "']"
        print("MetaData selector:", self.selector)


class PageLocations:
    '''
    The base class for locating article elements on a site.

    Some fields are gathered in a default way, based on standard metadata:
    - title
    - authors
    - doi
    - abstract
    - date_publication

    These *can* be overwritten if required.
    '''
    # High priority
    title = MetaData("citation_title")
    authors = MetaData("citation_author")
    doi = MetaData("citation_doi")
    abstract = MetaData("citation_abstract")
    full_body: None
    licensing: None

    # Medium priority
    date_publication = MetaData("citation_date")
    citations: None
    references: None
    extra_link: None

    # Low priority
    organization_affiliated: None
    category: None
    keywords: None
    source_impact_factor: None

    @classmethod
    def _elements(cls):
        '''Returns the elements which have locations defined'''
        return [v for v in dir(cls) if not v.startswith('_') and not callable(v)]
