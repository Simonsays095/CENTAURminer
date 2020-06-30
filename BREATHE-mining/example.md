# BREATHE Data Mining Framework

## Installation

TODO: Update once I get this uploaded as a module on pip

Pipfile and Pipfile.lock are included so you can use pipenv to manage the required python environment automatically. You will need python version 3.8, but you can edit Pipfile use anything >3.4, I believe, if you edit Pipfile accordingly. If you do not have pipenv installed, do

`pip install pipenv`

Once you have pipenv, there are several ways to run the code in this environment. The simplest way I've found it to run

```shell
pipenv shell
pipenv install
```

to enter the shell and install the required packages. Now you can run your python script with `python my_script.py`

## Description
This python module is designed to greatly simplify the data mining process for sites containing scientific articles. It handles selenium's webdriver creation and handles errors, so you just have to focus on finding elements in pages, and extracting useful information. Let's start with a basic example, to show what this module can do automatically.

## Minimal example and explanation:
```py
import BREATHE_mining as miner

class MySiteLocations(miner.PageLocations):
    pass

class MySiteMiner(miner.ArticleScraper):
    pass

# Equivalent to
# aS = miner.ArticleScraper(miner.PageLocations)
aS = MySiteMiner(MySiteLocations)
aS.gather("url_for_article_here")
print(aS.results)  # print out the results.
```

Lets break that down...

```py
import BREATHE_mining as miner
```
Import this module, and call it `miner`

```py
class MySiteLocations(miner.PageLocations):
    pass

class MySiteMiner(miner.ArticleScraper):
    pass
```
There are two important base classes: `miner.PageLocations` and `miner.ArticleScraper` which are used together for each site.

`PageLocations` is a static class that stores the locations of all useful information for each site. It comes with some defaults built-in, based on metadata typically included with these sites:

- `PageLocations.title`
- `PageLocations.authors`
- `PageLocations.doi`
- `PageLocations.abstract`
- `PageLocations.date_publication`

`ArticleScraper` uses the locations described in `PageLocations` to extract the element from the webpage. In this case, we don't give any explicit instructions, so it falls back to its defaults for the locations given (details below).

```py
aS = MySiteMiner(MySiteLocations)
aS.gather("url_for_article_here")
print(aS.results)  # print out the results.
```
We create an article scraper instance by passing in a `PageLocations` object. We now have the locations and instructions for how to get the information, so we can use `aS.gather` to actually look at a page and get the information. This is where the magic happens - all of the selenium web accesses happens here, and stores the information in a dictionary called `aS.results`. Finally, we print out the results.

As an example, if we use [https://arxiv.org/abs/2006.14790](https://arxiv.org/abs/2006.14790) as the url in `aS.gather`, here are the results we get:

```
{
    'authors': '<item>Angelina, Emilio</item><item>Andujar, Sebastian</item><item>Parravicini, Oscar</item><item>Enriz, Daniel</item><item>Peruchena, Nelida</item>',
    'date_publication': '2020/06/26',
    'title': 'Drug Repurposing to find Inhibitors of SARS-CoV-2 Main Protease',
    'url': 'https://arxiv.org/abs/2006.14790', 'date_aquisition': '2020-06-29'
}
```
We get a lot of information for free, without any special instructions! Notice that the authors key is a string of author names, each of which is tagged by `<item>...</item>`. More details below on why and how this is done.

## Extended example

For this section, we are going to use the article at [https://arxiv.org/abs/2006.14790](https://arxiv.org/abs/2006.14790) as an example. Follow that link, and press F12 in google chrome to open the google devTools window. Look at the structure of the DOM in that window to get familiar with the structure of the page, and then come back here.

For each bit of information you want to extract, you will need 1-2 pieces of code to extract it:

1) Add an attribute to a `PageLocation` subclass to define where on the page the information can be found.
2) If you need to do extra work after extracting the raw information, you'll need to define a `get_<attribute_name>` function in an `ArticleScraper` subclass.

### Metadata!!

First thing's first, you want to look at the site's metadata to extract information, since this is often the easiest way to get it. This is found in the `<head>` section of all websites, with each bit of information inside of a `<meta>` tag there. In our example article, there are two relevant meta tags:

```html
<meta name="citation_pdf_url" content="https://arxiv.org/pdf/2006.14790">
<meta property="og:description" content="...the entire abstract here...">
```

which have a link to the pdf and the full abstract, which we want to save in our `extra_link` and `abstract` fields. We can do that simply with:

```py
class arxivLocations(miner.PageLocations):
    extra_link = miner.MetaData("citation_pdf_url")
    abstract = miner.MetaData("og:description")
```
We don't even need extra instructions to figure out how to extract it! This data will be automatically extracted and added to our results.

### Simple data not found in the metadata

If you can't find the information in the metadata, you'll need to look in the `<body>` of the html document. You can either look through the DOM in F12 manually, or you can press `ctrl + shift + c` and click on the element on the page directly, and it will show you where that is in the DOM. To start, let's look at the license and keywords.

#### License

This is found on the top-right of the page, right under the pdf link. Use `ctrl + shift + c` and then click on where it says "(license)", and it will show up in your devTools window. Now you need to figure out a way to uniquely identify this element. If it has an `id` attribute, they are always unique. This element does not have an id, so we have to go to the next best option - `class`. Although this element does not have a class, it's parent has `class="abs-license"`. In CSS selector format, this element is defined as `.abs-license > a`. Also notice that the information we want isn't the text of this element, it's the `href` attribute. We have to tell our class to get that instead of the text. And this is done simply with:

```py
class arxivLocations(miner.PageLocations):
    extra_link = miner.MetaData("citation_pdf_url")
    abstract = miner.MetaData("og:description")
    license = miner.Element("CSS_SELECTOR", ".abs-license > a").get_attribute("href")
```

Here, we say that `license` is obtained from an element that can be located using the css selector `.abs-license > a`, and that we get the information from the `href` attribute - all at once. If you want to use something other than a css selector to locate the element, look at the details below to see what options you have.

#### keywords

The keywords for arxiv are given below the license, where it says "Current browse context". In this case, it's `q-bio.BM`. Locating the element like above, you can see that this element has a class, `current`, and the information we want is the text in that element. Adding this information to our class:

```py
class arxivLocations(miner.PageLocations):
    extra_link = miner.MetaData("citation_pdf_url")
    abstract = miner.MetaData("og:description")
    license = miner.Element("CSS_SELECTOR", ".abs-license > a").get_attribute("href")
    keywords = miner.Element("CSS_SELECTOR", ".current")
```

We don't give it an attribute, so it defaults to grabbing the text in that element.

### Complex information that requires processing

If you need information that isn't directly found in a single element, you need to give a more detailed method for extracting data, and this is where the second class comes in: `ArticleScraper`. In this class, you can define ways to interpret data in the `PageLocations` class. However, our example is pretty much finished so we'll have to look at a different site for an example that requires more processing. As a final touch for this site, 

# Class descriptions