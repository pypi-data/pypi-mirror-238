

Developer guidelines
===================

Naming and style conventions
----------------------------

We follow the  `PEP 8 guidelines <https://www.python.org/dev/peps/pep-0008://www.python.org/dev/peps/pep-0008/>`_

The best way to follow this yourself is::

    <edit python file>
    black <python file>

In the future, we plan on using black in a gitlab hook to allow black to be
applied to all files automatically upon pushing.

Black however does not handle the file naming schemes of PEP 8.  PEP 8 file
guidelines are best summarized as:

 + file should have short all-lowercase names (possibly with underscores)

 + directories should have short all-lowercase names (preferably without underscores)
   

We expect developers to follow these guidelines.  For a fun way of learning
about PEP 8, we recommend the `PEP 8 Song <https://www.youtube.com/watch?v=hgI0p1zf31k>`_.

Please be aware that there is a difference between camelCase and CapWords
convention.  Classes should be CapWords and not camelCase; e.g., ExtractData and
not extractData.


We have other conventions as well:

   1. tests should be in a subdirectory called tests and have the form of
      `test_<filename>.py` per one of the pytest conventions.
   2. workflow scripts should be in a workflow subdirectory.  Workflow scripts
      represent scripts used in generating figures for publication, illustrate
      usage, but are not tested and not meant to be exposed to outsiders.
