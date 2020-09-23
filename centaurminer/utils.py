def TagList(str_list, tag="item"):
    '''
    Tags a list and converts to a string - avoids data corruption by using a more complex tag.

    Arguments
    ---------
    str_list : list
        List of strings to be joined with tags.
    tag : str, optional
        Tag to use for the list. This tag will be wrapped in `<...>` and `</...>` to close.
    '''
    result = ""
    for string in str_list:
        result += f"<{tag}>{string}</{tag}>"
    return result


def CollectURLs(start_url, link_elem, next_elem=None, limit=10000, **kwargs):
    '''
    Collects a list of URLs from a search of the site.

    Arguments
    ---------
    start_url : str
        URL for the first page of a site search.
    link_elem : :class:`centaurminer.Element`
        An Element indicating where individual URL links can be found on the search page.
    next_elem : :class:`centaruminer.Element`, optional
        Indicates where on the page the "next page" button is, to navigate through search pages.
    limit : int
        If the number of URLs collected exceeds this number, it will stop searching and return the list or URLs.
    
    kwargs
        Additional arguments are passed directly into the :class:`centaurminer.Engine` constructor.
    '''
    from .DOM_elements import PageLocations
    from .Engine import MiningEngine

    urls = []
    pageNum = 1
    # Get access to a webdriver and load the page
    miner = MiningEngine(PageLocations, **kwargs)
    miner.wd.get(start_url)

    # Load all the links on this page
    elems = miner.get(link_elem, several=True)
    if next_elem is None:
        numToAdd = min(limit, len(elems))  # If this page has more than allowed by limit, just extend with some of the elements
        return elems[:numToAdd]

    # Repeatedly gather links from several pages
    while len(elems) > 0:
        print("Appending URLs from page", pageNum)
        numToAdd = min(limit - len(urls), len(elems))  # If this page has more than allowed by limit, just extend with some of the elements
        urls.extend(elems[:numToAdd])
        if len(urls) == limit:
            break

        # Go to next page
        try:
            print("Going to page", pageNum + 1)
            next_button = miner.wd.find_element(next_elem.method, next_elem.selector)
            next_button.click()
        except Exception:
            break
        elems = miner.get(link_elem, several=True)
        pageNum += 1
    return urls
