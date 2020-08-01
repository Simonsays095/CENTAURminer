Minimal Example
===============

Here, we're going to go over the basic use case, without delving too deeply
into the advanced fatures. For this example, we're going to use the article
`here`_ for our data collection. Please go there now and look at the page.

.. _here: https://arxiv.org/abs/1701.00673

If you are unfamiliar with a DOM and how to locate elements in a page using
Google DevTools, please read :ref:`Intro to Data Mining`.


Let's start with the complete example, and then we'll break it down:

.. code-block:: python
   :linenos:

   import centaurminer as mining

   class MyLocations(mining.PageLocations):
       pass

   class MyEngine(mining.MiningEngine):
       pass


   miner = MyEngine(MyLocations)
   miner.gather("https://arxiv.org/abs/1701.00673")


   print(miner.results)


* Lines 1-2 are just importing this module.
* Lines 3-5 are where we set up a :class:`centaurminer.PageLocations` subclass,
  where we can specify where to find all of the elements we want on the DOM.
* Lines 6-9 are where we set up a :class:`centaurminer.MiningEngine` subclass,
  where we can specify extra instructions for how to collect complex data.
* Finally, lines 10-13 are where we create the miner and tell it to gather the
  information from the site above.
* Line 14 is where we print out the results from this mining operation.

As of writing this documentation, here is the output from the script above:

.. code-block:: console

   [WDM] - Current google-chrome version is 83.0.4103     
   [WDM] - Get LATEST driver version for 83.0.4103         
   [WDM] - Get LATEST driver version for 83.0.4103       
   [WDM] - Trying to download new driver from http://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_win32.zip   
   [WDM] - Driver has been saved in cache [C:\Users\simon\.wdm\drivers\chromedriver\win32\83.0.4103.39]     

   DevTools listening on ws://127.0.0.1:63600/devtools/browser/39bc9ac2-f612-4f30-8380-8d8e211a057c           
   [0702/001141.086:INFO:CONSOLE(0)] "A cookie associated with a cross-site resource at https://arxiv-org.atlassian.net/ was set without the `SameSite` attribute. A future release of Chrome will only deliver cookies with cross-site requests if they are set with `SameSite=None` and `Secure`. You can review cookies in developer tools under Application>Storage>Cookies and see more details at https://www.chromestatus.com/feature/5088147346030592 and https://www.chromestatus.com/feature/5633521622188032.", source: https://arxiv.org/abs/1701.00673 (0)                                     
   Unable to find element defined by MyLocations.abstract          
   Unable to find element defined by MyLocations.doi
   {
       'authors': '<item>Riazanov, Andrii</item><item>Karasikov, Mikhail</item><item>Grudinin, Sergei</item>',
       'date_publication': '2017/01/03',
       'title': 'Inverse Protein Folding Problem via Quadratic Programming',
       'url': 'https://arxiv.org/abs/1701.00673',
       'date_aquisition': '2020-07-02'
   }

I added formatting to the output dictionary for clarity. We got 5 pieces of information for free (if you include ``url`` and ``date_acquisition``)! Notice toward the end, it also says ``unable to find element defined by MyLocations.abstract`` and ``Unable to find element defined by MyLocations.doi``. This indicates that we either messed up how we defined those locations, or this site is missing that information. It gracefully accepts that error and continues with the rest of the data mining. Because both of these bits of information are gathered by default, you know that they come from the Metadata - sure enough, you can look at the DOM and see that this information isn't found in the Metadata!

Up next is a more in-depth example for a different site, where we need to define specific locations for elements, as well as additional post-processing after extraction.
