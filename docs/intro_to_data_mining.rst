Intro to Data Mining
====================

This page is dedicated to explaining the basics of data mining and web page
design, so that the examples and documentation will make sense. If you already
know about DOMs and web page elements, feel free to skip this page.

.. contents::

Ethical Data Mining
===================
Informally, data mining is the act of processing data to gain insight. In this context, I'm going to refer to it more specifically as gathering information stored on webpages (commonly known as Web Scraping, but this has negative implications). This is a very valuable and vast source of information, but it has been (and certainly will continue to be) exploited by bad actors. Besides the obvious fact that someone has a server somewhere that has to send you the data, which is going to cost them to send you, there are also ethical, moral, and legal aspects of data mining to keep in mind. For more information, visit `this article <https://towardsdatascience.com/ethics-in-web-scraping-b96b18136f01>`_ written by James Densmore, about typical rules to follow when data mining.

However, keep in mind that all sites look at data mining differently - sites that contain lots of information (such as scientific publishers) will typically have a "bulk data access" or "data mining" policy, and they often have ways to help you, so you don't have to go through the work of getting information from the DOM. Ask your site administrators to see what their policy is before bombarding them with requests to their site.

Document Object Models
======================

Web pages are structured in `html <https://devdocs.io/html/>`_. The full page, represented in html, is called the `Document Object Model (DOM) <https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introductionhttps://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction>`_. Everything you can see on a web page can be found in the DOM, so this is where you need to look if you want to collect information from a website.

To view the DOM, there are several methods. The easiest and most widely used method is to use google chrome to navigate to a web page you want to see the DOM for. Press :code:`F12` to open the DevTools panel, and the DOM will show up on the right side of the page. You can also press :code:`ctrl+shift+c`, and then click on an element with your mouse to see the location in the DOM of that element.

Web Elements
============

The DOM is further broken down by `Elements <https://developer.mozilla.org/en-US/docs/Web/HTML/Elementhttps://developer.mozilla.org/en-US/docs/Web/HTML/Element>`_, which are the building blocks of a website. They usually represent small bits of information on the page (or sometimes even hidden from the page, in the case of `Metadata <https://www.w3schools.com/tags/tag_meta.asp>`_). If you can extract the information in a single element, you're well on your way to data mining!

Elements have several places to store data. The simplest is all of the text you see on the page - this is stored in the body of the element. For a standard :code:`div` element:

.. code:: html

   <div>
     This is the body of an element. Text on the page comes from here.
   </div>

However, the element itself can also store information internally. This is usually used to determine how the page displays that element, but it can also be used by sites to give more information about that element. These are called attributes, and common attributes include :code:`class`, :code:`name`, and :code:`id`. In the element, they look like this:

.. code:: html

   <div class="Attributes" name="Go" id="Here"></div>

You now have the tools and knowledge to understand the rest of this module! We use these terms frequently, so come back to this page to answer any questions that may arise throughout the process of using the module.
