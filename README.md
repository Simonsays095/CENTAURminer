# BREATHE Data Mining Framework

This package is a wrapper on [selenium](https://pypi.org/project/selenium/), a package that "automates web browser interaction from Python". In this package, we add the following features:

 - Add a class used to identify where elements are located on the DOM
 - Add a class that specifies if any extra processing should be done to the elements in the previous class, rather than just extract an attribute.
 - Create helper classes to simplify the process of identifying elements
 
 The features are created specifically with scientific data mining in mind, in relation to the development of the [BREATHE dataset](https://cloud.google.com/blog/products/ai-machine-learning/google-ai-community-used-cloud-to-help-biomedical-researchers) but can be used elsewhere.