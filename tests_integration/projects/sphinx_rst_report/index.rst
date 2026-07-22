LOBSTER Sample Traceability Report
===================================

This sample demonstrates generating a Sphinx-based traceability report
using ``lobster-rst-report``.

The traceability data originates from the ``basic`` integration test project
and contains the same requirements, implementation items, and test activities
that are shown in the HTML report produced by ``lobster-html-report``.

Build this report by running ``make html`` in this directory.
The generated ``traceability/`` directory (index + one page per traceability
level) is then included via the toctree below.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   traceability/index
