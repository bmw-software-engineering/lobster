# LOBSTER Safety Manual

---

## Disclaimer

> This document does not replace a proper tool qualification in your context. This document aims to guide you and reduce the tool qualification effort on your side.

> LOBSTER, including this safety manual, is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.** See the AGPL Affero General Public License for more details.

> This document shall become a safety manual in the sense of ISO26262 ("Road vehicles – Functional safety"). It might well apply to IEC 61508 ("Functional Safety of Electrical/ Electronic/ Programmable Electronic Safety-related Systems"), too. However, the safety manual is incomplete as of today.

## Safety Manual
### Introduction

You shall follow the instructions given in this document in order to qualify the LOBSTER tool for the following context:
This safety manual assumes use of LOBSTER tool for the following purposes:

- Analysing traceability and coverage information
- Generating reports regarding traceability status
- Supporting verification activities in a Continuous Integration (CI) pipeline
- Identifying gaps in requirements traceability

Other purposes are not in the scope of this safety manual.

**Note:**

This safety manual applies only to the use of the LOBSTER tool.
The correctness and completeness of the input data provided to LOBSTER remain the responsibility of the user.
This safety manual is incomplete as of today and may be extended in future versions.


### Instructions
#### Verify Input Data Completeness

You shall verify that all intended input artifacts have been provided to LOBSTER.

**Rationale:**

LOBSTER can only analyse artifacts that are available as input.
Missing input artifacts may result in incomplete traceability analysis and misleading coverage results.

**Example:**

A test specification file is not included in the LOBSTER analysis.
The generated report may indicate missing traceability even though the corresponding test specifications exist elsewhere.

#### Review Warnings and Errors

You shall review all warnings and errors reported by LOBSTER.
A successfully generated report shall not be considered sufficient evidence that the analysis results are correct.
Warnings and errors shall be investigated before the report results are used for verification or qualification activities.

**Rationale:**

Warnings and errors may indicate problems in the input data, traceability relationships, partial traceability, justification of the missing traceability, tool configuration.
Such problems can affect the completeness or correctness of the generated analysis results.
Ignoring warnings or errors may lead to incorrect conclusions based on the generated report.

**Example:**

A report contains 90 OK items, 5 Partial items, and 5 Justified items.
The user shall review the Partial and Justified items and shall not assume that all 100 items provide the same level of traceability evidence.

#### Verify Coverage Results

You shall not rely solely on the coverage percentage reported by LOBSTER.
If LOBSTER reports a coverage value of 100.0%, then you shall verify that the number of "OK items" is identical to the number of "total items".
A coverage result shall only be considered complete if both values are identical.

**Rationale:**

LOBSTER calculates coverage values using floating point arithmetic.
For very large data sets, rounding effects may occur during the coverage calculation.
As a result, a coverage value displayed as 100.0% does not necessarily guarantee that all items are covered.
The displayed percentage may not always precisely reflect the relationship between the reported "OK Items" and "Total Items" values.

The comparison of "OK items" and "total items" provides the most reliable indication of complete coverage.

**Example:**

The coverage table displays the columns "Coverage", "OK Items", and "Total Items".
If a category shows `Coverage = 100.0%`, then the user shall verify that `OK Items = Total Items`.

This is mainly in case of large numbers.
Consider a large number as `L_num`, then:

```text
Coverage = (L_num) – 1/(L_num)
         = 0.9999999999999 (actual value)
         ~ 1 (computer's approximation of that value in memory)
```

This is incorrect when `OK Items != Total Items`.

**Example:**

A report displays the following values:

- Coverage: 100.0%
- OK Items: 999999
- Total Items: 1000000

Although the displayed coverage is 100.0%, the user shall conclude that coverage is not complete because the number of OK Items is not identical to the number of Total Items.

**Example:**

A report displays the following values:

- Coverage: 100.0%
- OK Items: 1000000
- Total Items: 1000000

The user may conclude that coverage is complete because the number of OK Items is identical to the number of Total Items.

