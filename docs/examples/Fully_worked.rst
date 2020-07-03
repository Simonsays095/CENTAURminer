Fully Worked Example
====================

If you haven't done so already, please look at the :doc:`Minimal`, because we're going to start from where that left off, just on a different site.

For this tutorial, let's look at `The Journal of Biomedical Science <JBS>`_. Start Looking at several documents on the site. It looks like all of the articles have similar formatting, so we don't have to worry too much about giving specialized instructions to different types of articles. Let's start looking in-depth at an article that has as much information as possible:

`<https://jbiomedsci.biomedcentral.com/articles/10.1186/s12929-020-00652-z>`_

.. _JBS: https://jbiomedsci.biomedcentral.com/

And using the scaffolding from the minimal example:

.. code-block:: python

    import centaurminer as mining
    class JBSLocations(mining.PageLocations):
        source = "The Journal of Biomedical Science"
        license = "https://www.biomedcentral.com/about/open-access"

    class JBSEngine(mining.MiningEngine):
        pass

    miner = JBSEngine(JBSLocations)
    miner.gather("https://jbiomedsci.biomedcentral.com/articles/10.1186/s12929-020-00652-z")
    print(miner.results)

I've added both :code:`JBSLocations.source` and :code:`JBSLocations.license` attributes, which get stored directly in our results, since they're strings. I strongly recommend you find the licensing first, since this will help you know for sure that you can access and share the data according to the site's policy. Here is what we get so far:

.. code-block:: console

    [WDM] - Current google-chrome version is 83.0.4103
    [WDM] - Get LATEST driver version for 83.0.4103
    [WDM] - Driver [C:\Users\simon\.wdm\drivers\chromedriver\win32\83.0.4103.39\chromedriver.exe] found in cache

    DevTools listening on ws://127.0.0.1:64843/devtools/browser/3c82a3a7-b330-4a7c-96ee-cb70709a8013
    Unable to find element defined by JBSLocations.date_publication
    {
        'abstract': 'Monoclonal antibodies (mAbs) ... satisfy the unmet medical needs of mAb therapy.',
        'authors': '<item>Wen-Wei Lin</item><item>Yun-Chi Lu</item><item>Chih-Hung Chuang</item><item>Tian-Lu Cheng</item>',
        'doi': '10.1186/s12929-020-00652-z',
        'license': 'https://www.biomedcentral.com/about/open-access',
        'source': 'The Journal of Biomedical Science',
        'title': 'Ab locks for improving the selectivity and safety of antibody drugs',
        'url': 'https://jbiomedsci.biomedcentral.com/articles/10.1186/s12929-020-00652-z',
        'date_aquisition': '2020-07-02'
    }

Compare this to what's shown on the page - so far, it's all looking good. It's missing the publication date, but that's alright, we can get it now. At the same time, let's look through the metadata for more data. It looks like we have publication date, a pdf link, and references in the metadata. Publication date and the pdf link are simple, but there are many references - we need to tell the program how to gather all of these and combine them into results. Let's do all of this at once:

.. code-block:: python

    import centaurminer as mining
    class JBSLocations(mining.PageLocations):
        source = "The Journal of Biomedical Science"
        license = "https://www.biomedcentral.com/about/open-access"
        date_publication = mining.MetaData("citation_online_date")
        link_pdf = mining.MetaData("citation_pdf_url")
        references = mining.MetaData("citation_reference")


    class JBSEngine(mining.MiningEngine):
        def get_references(self, element):
            return mining.TagList(self.get(element, several=True))


    miner = JBSEngine(JBSLocations)
    miner.gather("https://jbiomedsci.biomedcentral.com/articles/10.1186/s12929-020-00652-z")
    print(miner.results)

The :code:`several` attribute here tells the engine we want all elements that match the description, and :code:`TagList` combines them into a string. Now running this again, we have three added keys to our results dictionary:

.. code-block:: console

    {
        ...,
        'date_publication': '2020/06/25',
        'link_pdf': 'https://jbiomedsci.biomedcentral.com/track/pdf/10.1186/s12929-020-00652-z'
        'references': '<item>citation_journal_title=Cancer Lett; ... over 100 references here ... citation_id=CR198</item>'
    }

Alright, let's move on to the main body of the page! Of the information presented here, let's focus on the keywords, affiliated organization, and full body text.

Keywords:
---------

All the way at the bottom of the page, you can see a group of keywords that may be useful. These are all located in divs with :code:`class="c-article-subject-list__subject"` - there's no other text in these elements, which makes it really easy to collect - we just have to collect each element, and treat it identically to how we collected the references!

.. code-block:: python

    class JBSLocations(mining.PageLocations):
        source = "The Journal of Biomedical Science"
        license = "https://www.biomedcentral.com/about/open-access"
        date_publication = mining.MetaData("citation_online_date")
        link_pdf = mining.MetaData("citation_pdf_url")
        references = mining.MetaData("citation_reference")
        keywords = mining.Element("css_selector", ".c-article-subject-list__subject")


    class JBSEngine(mining.MiningEngine):
        def get_references(self, element):
            return mining.TagList(self.get(element, several=True))

        def get_keywords(self, element):
            return mining.TagList(self.get(element, several=True))

This adds the following key-value pair to our results:

.. code-block:: console

    'keywords': '<item>Monoclonal antibody (mAb)</item><item>adverse events</item><item>Ab lock</item><item>spatial-hindrance-based approaches</item><item>affinity-based approaches</item>'

Full-body:
----------

We have a few struggles here, and a few choices to make. What should we do with figures? How should we treat headers and titles? For now, we're going to ignore figures and tables, and treat headers/titles as their own paragraph. The main struggle with this approach is that we need to throw out lots of information we don't want - figures and captions, the abstract section, and all of the subsections after the conclusions (like Abbreviations). We can do most of this directly with a css selector, but specific selector means more brittle, easily breakable code - just keep that in mind. Here is the selector I came up with, but others are possible:

:code:`section > [id^=Sec][id$=section] > .c-article-section__content > p, [id^=Sec]:not([id$=content]):not([id$=section])`

This accepts two types of elements (separated by a comma, meaning "or") - the first is the main text in the body, and the second is all of the section headers. The body text needs 4 levels of content to find it accurately, and both ids and classes are used in the selector. The section headers have a very specific signature, so they're just located by their attributes. The "^=" and "$=" are "starts_with" and "ends_with" css selectors, which we use for both types. Here's what it looks like in the code (along with the extra processing in the :class:`BMCEngine` class)

.. code-block:: python

    class JBSLocations(mining.PageLocations):
        source = "The Journal of Biomedical Science"
        license = "https://www.biomedcentral.com/about/open-access"
        date_publication = mining.MetaData("citation_online_date")
        link_pdf = mining.MetaData("citation_pdf_url")
        references = mining.MetaData("citation_reference")
        keywords = mining.Element("css_selector", ".c-article-subject-list__subject")
        body = mining.Element("css_selector", "section > [id^=Sec][id$=section] > .c-article-section__content > p, [id^=Sec]:not([id$=content]):not([id$=section])")


    class JBSEngine(mining.MiningEngine):
        def get_references(self, element):
            return mining.TagList(self.get(element, several=True))

        def get_keywords(self, element):
            return mining.TagList(self.get(element, several=True))

        def get_body(self, element):
            paragraphs = self.get(element, several=True)
            return "\n".join(paragraphs)

I would show you here what gets added to results, but it's just the full body text, which is too long to be helpful.

Affiliated organization:
------------------------

Toward the bottom of the page, you can see the list of author affiliations - it's a list of authors and organizations, alternating back and forth. Because of this, and because we want to combine both of these types of elements into one result, we need to use a :class:`centaurminer.Complex` class instead of an element. When we combine the authors + orgs, let's organize it like this: :code:`<item><author> ... </author><org> ... </org></item> ...`. Here's my solution:

.. code-block:: python

    # In JBSLocations
    organization_affiliated = mining.Complex()

    # In JBSEngine
    def get_organization_affiliated(self, element):
        orgs_loc = mining.Element("css_selector", ".c-article-author-affiliation__address")
        authors_loc = mining.Element("css_selector", ".c-article-author-affiliation__authors-list")

        orgs = self.get(orgs_loc, several=True)
        authors = self.get(authors_loc, several=True)

        result = []
        for org, author_list in zip(orgs, authors):
            res_string = "<authors>" + author_list + "</authors>"
            res_string += "<org>" + org + "</org>"
            result.append(res_string)
        return mining.TagList(result)

I extract the affiliations and authors separately, zip them together (to get them to alternate), and tag the inner elements manually.

That's it for this page! You can extract whatever elements you want, but we've already got 238 kb of data, as of writing this example. Now it's up to your goals and time you can spend, to extract information from whatever site you want!

Remember, if you're stuck on some piece of information, you can always manipulate the selenium webdriver itself at :class:`MiningEngine.wd <centaurminer.MiningEngine>`.

Happy mining!