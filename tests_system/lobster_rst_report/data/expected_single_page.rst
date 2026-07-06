##################################
L.O.B.S.T.E.R. Traceability Report
##################################

| Analyzed commit: aaaa1111bbbb2222cccc3333dddd4444eeee5555
| LOBSTER Version: 1.0.4-dev

.. rubric:: Coverage Summary

.. grid:: 1 1 2 2
   :gutter: 3

   .. grid-item::
      :columns: 12 12 7 7

      .. list-table::
         :header-rows: 1
         :widths: 35 15 15 15

         * - Category
           - Coverage
           - OK Items
           - Total Items
         * - :ref:`System Requirements <lobster-level-system-requirements>`
           - 100.0%
           - 1
           - 1
         * - :ref:`Software Requirements <lobster-level-software-requirements>`
           - 50.0%
           - 3
           - 6
         * - :ref:`Code <lobster-level-code>`
           - 60.0%
           - 6
           - 10
         * - :ref:`Verification Test <lobster-level-verification-test>`
           - 100.0%
           - 2
           - 2

   .. grid-item::
      :columns: 12 12 5 5

      .. graphviz::

         digraph tracing_policy {
            rankdir=TB;
            node [shape=box, style=filled, fontname="Helvetica", margin="0.3,0.1"];
            edge [arrowhead=open];

            "System Requirements" [fillcolor="#2196F3", fontcolor="white"];
            "Software Requirements" [fillcolor="#2196F3", fontcolor="white"];
            "Code" [fillcolor="#4CAF50", fontcolor="white"];
            "Verification Test" [fillcolor="#FF9800", fontcolor="white"];
            "Software Requirements" -> "System Requirements";
            "Code" -> "Software Requirements";
            "Verification Test" -> "Software Requirements";
         }

.. rubric:: Issues

* [MISSING — no upward trace] :ref:`exclusive\_or <lobster-item-f44a5e4c051c43e14dc1c71d4a3818a0b038597e>`
* [MISSING — no upward trace] :ref:`exclusive\_or/MATLAB Function <lobster-item-abac171105982dd5a053572a6f4d88ef30fbfc42>`
* [MISSING — no upward trace] :ref:`exclusive\_or <lobster-item-3412bc95eb06ccb9400eaa49f58bd0bfc7a08d60>`
* [MISSING — no upward trace] :ref:`potato <lobster-item-4bf9a73c0893a50410b0817f54c7d89c696fa9a6>`
* [MISSING — version mismatch] :ref:`example.req\_xor <lobster-item-5c0948f96e743a0c3ab3c14ecac0f5d10609f324>`
* [MISSING — no upward trace] :ref:`example.req\_nor <lobster-item-714c0c22dee57a69c9425cff0c0bd4ca9ebe5d1f>`
* [MISSING — no trace to: Verification Test] :ref:`example.req\_nor <lobster-item-714c0c22dee57a69c9425cff0c0bd4ca9ebe5d1f>`
* [MISSING — no trace to: Code] :ref:`example.req\_important <lobster-item-fbfa01aa359da14836c3fe53cd7363bfb1ffb782>`
* [MISSING — no trace to: Verification Test] :ref:`example.req\_important <lobster-item-fbfa01aa359da14836c3fe53cd7363bfb1ffb782>`

Requirements and Specification
==============================

.. _lobster-level-system-requirements:

System Requirements
-------------------

**Coverage:** 100.0% (1 of 1 items OK)

.. _lobster-item-d499f1e2ff6c8662012d4c4bfe35060a5eda7b6c:

.. dropdown:: [OK] codebeamer Functional requirement LOBSTER demo
   :class-title: sd-bg-success sd-text-white

   **Status:** Potato

   .. pull-quote::

      Provide a nice demonstration of LOBSTER through four examples

   .. raw:: html

      <hr>

   **Traces to:**

   * :ref:`example.req\_implication <lobster-item-1bb1a5e571e24eebc94d2572ab385ee34e338995>`
   * :ref:`example.req\_xor <lobster-item-5c0948f96e743a0c3ab3c14ecac0f5d10609f324>`
   * :ref:`example.req\_nand <lobster-item-3e885dd2f9f061dedab93f44634897ace7f770c8>`

   .. raw:: html

      <hr>

   **Source:** `cb item 666 'LOBSTER demo' <https://potato.kitten/issue/666?version=42>`__

.. _lobster-level-software-requirements:

Software Requirements
---------------------

**Coverage:** 50.0% (3 of 6 items OK)

.. _lobster-item-5c0948f96e743a0c3ab3c14ecac0f5d10609f324:

.. dropdown:: [MISSING] TRLC Tagged\_requirement example.req\_xor
   :open:
   :class-title: sd-bg-danger sd-text-white

   .. pull-quote::

      text: provide a utility function for logical exclusive or

   .. raw:: html

      <hr>

   **Traces to:**

   * :ref:`exclusive\_or/My Exclusive Or <lobster-item-d330ebddaa1ec4c761ec0c070c6f6c71fd4cbb4e>`

   .. card::
      :class-card: lobster-issue-card

      * tracing destination req 12345 has version 42 (expected 5)

   .. raw:: html

      <hr>

   **Derived from:**

   * :ref:`LOBSTER demo <lobster-item-d499f1e2ff6c8662012d4c4bfe35060a5eda7b6c>`

   .. raw:: html

      <hr>

   **Source:** `potato.trlc:10:20 <potato.trlc>`__

.. _lobster-item-714c0c22dee57a69c9425cff0c0bd4ca9ebe5d1f:

.. dropdown:: [MISSING] TRLC Requirement example.req\_nor
   :open:
   :class-title: sd-bg-danger sd-text-white

   .. pull-quote::

      provide a utility function for logical negated or

   .. raw:: html

      <hr>

   **Traces to:**

   * :ref:`nor.Example.helper\_function <lobster-item-44aca84976176f453e178bdd3323e7e9813dcebe>`
   * :ref:`nor.Example.nor <lobster-item-4fe151cfc168f08ff6bc308291ecbee34309b652>`

   .. card::
      :class-card: lobster-issue-card

      * missing reference to Verification Test

   .. raw:: html

      <hr>

   **Derived from:**

   .. card::
      :class-card: lobster-issue-card

      * missing up reference

   .. raw:: html

      <hr>

   **Source:** `potato.trlc:24:13 <potato.trlc>`__

.. _lobster-item-fbfa01aa359da14836c3fe53cd7363bfb1ffb782:

.. dropdown:: [MISSING] TRLC Linked\_requirement example.req\_important
   :open:
   :class-title: sd-bg-danger sd-text-white

   .. pull-quote::

      this is important

   .. raw:: html

      <hr>

   **Traces to:**

   .. card::
      :class-card: lobster-issue-card

      * missing reference to Code
      * missing reference to Verification Test

   .. raw:: html

      <hr>

   **Derived from:**

   * :ref:`example.req\_nor <lobster-item-714c0c22dee57a69c9425cff0c0bd4ca9ebe5d1f>`
   * :ref:`example.req\_implication <lobster-item-1bb1a5e571e24eebc94d2572ab385ee34e338995>`

   .. raw:: html

      <hr>

   **Source:** `potato.trlc:42:20 <potato.trlc>`__

.. _lobster-item-3e885dd2f9f061dedab93f44634897ace7f770c8:

.. dropdown:: [OK] TRLC Tagged\_requirement example.req\_nand
   :class-title: sd-bg-success sd-text-white

   .. pull-quote::

      text: provide a utility function for logical negated and

   .. raw:: html

      <hr>

   **Traces to:**

   * :ref:`nand <lobster-item-05717df9b8ee784715376855d7afeabeaa6cd1f5>`
   * :ref:`nand\_test::test\_1 <lobster-item-39288653f9b39978deae407a61549f53151857b7>`

   .. raw:: html

      <hr>

   **Derived from:**

   * :ref:`LOBSTER demo <lobster-item-d499f1e2ff6c8662012d4c4bfe35060a5eda7b6c>`

   .. raw:: html

      <hr>

   **Source:** `potato.trlc:16:20 <potato.trlc>`__

.. _lobster-item-21cffb8e9b92e4133844f4752a7c8100cf3166c4:

.. dropdown:: [JUSTIFIED] TRLC Requirement example.req\_implies
   :class-title: sd-bg-success sd-text-white

   .. pull-quote::

      provide a utility function for logical implication

   .. raw:: html

      <hr>

   **Justifications:** not needed; also not needed

   .. raw:: html

      <hr>

   **Source:** `potato.trlc:30:13 <potato.trlc>`__

.. _lobster-item-1bb1a5e571e24eebc94d2572ab385ee34e338995:

.. dropdown:: [OK] TRLC Tagged\_requirement example.req\_implication
   :class-title: sd-bg-success sd-text-white

   .. pull-quote::

      text: provide a utility function for logical implication

   .. raw:: html

      <hr>

   **Traces to:**

   * :ref:`implication <lobster-item-804973db4a4754175b5c3d8df2d938918dc8cae6>`
   * :ref:`ImplicationTest:BasicTest <lobster-item-0c9dd74b464f7be6456f3d14e144ba8b116dc9b3>`

   .. raw:: html

      <hr>

   **Derived from:**

   * :ref:`LOBSTER demo <lobster-item-d499f1e2ff6c8662012d4c4bfe35060a5eda7b6c>`

   .. raw:: html

      <hr>

   **Source:** `tests\_integration/projects/basic/potato.trlc:3 <https://github.com/bmw-software-engineering/lobster/blob/main/tests_integration/projects/basic/potato.trlc#L3>`__

Implementation
==============

.. _lobster-level-code:

Code
----

**Coverage:** 60.0% (6 of 10 items OK)

.. _lobster-item-f44a5e4c051c43e14dc1c71d4a3818a0b038597e:

.. dropdown:: [MISSING] Simulink Block exclusive\_or
   :open:
   :class-title: sd-bg-danger sd-text-white

   **Derived from:**

   .. card::
      :class-card: lobster-issue-card

      * missing up reference

   .. raw:: html

      <hr>

   **Source:** `exclusive\_or.slx <exclusive_or.slx>`__

.. _lobster-item-abac171105982dd5a053572a6f4d88ef30fbfc42:

.. dropdown:: [MISSING] MATLAB Function exclusive\_or/MATLAB Function
   :open:
   :class-title: sd-bg-danger sd-text-white

   **Derived from:**

   .. card::
      :class-card: lobster-issue-card

      * missing up reference

   .. raw:: html

      <hr>

   **Source:** `exclusive\_or.slx:1:13 <exclusive_or.slx>`__

.. _lobster-item-3412bc95eb06ccb9400eaa49f58bd0bfc7a08d60:

.. dropdown:: [MISSING] C/C++ Function exclusive\_or
   :open:
   :class-title: sd-bg-danger sd-text-white

   **Derived from:**

   .. card::
      :class-card: lobster-issue-card

      * missing up reference

   .. raw:: html

      <hr>

   **Source:** `foo.cpp:9 <foo.cpp>`__

.. _lobster-item-4bf9a73c0893a50410b0817f54c7d89c696fa9a6:

.. dropdown:: [MISSING] C/C++ Function potato
   :open:
   :class-title: sd-bg-danger sd-text-white

   **Derived from:**

   .. card::
      :class-card: lobster-issue-card

      * missing up reference

   .. raw:: html

      <hr>

   **Source:** `foo.cpp:14 <foo.cpp>`__

.. _lobster-item-d330ebddaa1ec4c761ec0c070c6f6c71fd4cbb4e:

.. dropdown:: [OK] Simulink Block exclusive\_or/My Exclusive Or
   :class-title: sd-bg-success sd-text-white

   **Derived from:**

   * :ref:`example.req\_xor <lobster-item-5c0948f96e743a0c3ab3c14ecac0f5d10609f324>`

   .. raw:: html

      <hr>

   **Source:** `exclusive\_or.slx <exclusive_or.slx>`__

.. _lobster-item-804973db4a4754175b5c3d8df2d938918dc8cae6:

.. dropdown:: [OK] C/C++ Function implication
   :class-title: sd-bg-success sd-text-white

   **Derived from:**

   * :ref:`example.req\_implication <lobster-item-1bb1a5e571e24eebc94d2572ab385ee34e338995>`

   .. raw:: html

      <hr>

   **Source:** `foo.cpp:3 <foo.cpp>`__

.. _lobster-item-05717df9b8ee784715376855d7afeabeaa6cd1f5:

.. dropdown:: [OK] MATLAB Function nand
   :class-title: sd-bg-success sd-text-white

   **Derived from:**

   * :ref:`example.req\_nand <lobster-item-3e885dd2f9f061dedab93f44634897ace7f770c8>`

   .. raw:: html

      <hr>

   **Source:** `nand.m:1:14 <nand.m>`__

.. _lobster-item-716e7482019e79473ec2b20555b90c6183ef62a2:

.. dropdown:: [JUSTIFIED] Python Function nor.trlc\_reference
   :class-title: sd-bg-success sd-text-white

   **Justifications:** helper function

   .. raw:: html

      <hr>

   **Source:** `nor.py:5 <nor.py>`__

.. _lobster-item-44aca84976176f453e178bdd3323e7e9813dcebe:

.. dropdown:: [OK] Python Method nor.Example.helper\_function
   :class-title: sd-bg-success sd-text-white

   **Derived from:**

   * :ref:`example.req\_nor <lobster-item-714c0c22dee57a69c9425cff0c0bd4ca9ebe5d1f>`

   .. raw:: html

      <hr>

   **Source:** `nor.py:13 <nor.py>`__

.. _lobster-item-4fe151cfc168f08ff6bc308291ecbee34309b652:

.. dropdown:: [OK] Python Method nor.Example.nor
   :class-title: sd-bg-success sd-text-white

   **Derived from:**

   * :ref:`example.req\_nor <lobster-item-714c0c22dee57a69c9425cff0c0bd4ca9ebe5d1f>`

   .. raw:: html

      <hr>

   **Source:** `nor.py:17 <nor.py>`__

Verification and Validation
===========================

.. _lobster-level-verification-test:

Verification Test
-----------------

**Coverage:** 100.0% (2 of 2 items OK)

.. _lobster-item-39288653f9b39978deae407a61549f53151857b7:

.. dropdown:: [OK] MATLAB Test nand\_test::test\_1
   :class-title: sd-bg-success sd-text-white

   **Derived from:**

   * :ref:`example.req\_nand <lobster-item-3e885dd2f9f061dedab93f44634897ace7f770c8>`

   .. raw:: html

      <hr>

   **Source:** `nand\_test.m:3:13 <nand_test.m>`__

.. _lobster-item-0c9dd74b464f7be6456f3d14e144ba8b116dc9b3:

.. dropdown:: [OK] GoogleTest Test ImplicationTest:BasicTest
   :class-title: sd-bg-success sd-text-white

   **Derived from:**

   * :ref:`example.req\_implication <lobster-item-1bb1a5e571e24eebc94d2572ab385ee34e338995>`

   .. raw:: html

      <hr>

   **Source:** `test.cpp:7 <test.cpp>`__

