# License

This document is free: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This documentation is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Affero General Public License for more details.

# Disclaimer

This document describes how the LOBSTER tools could be qualified in the context of ISO 26262.
It is important to understand that this document can only serve as inspiration.
It is by no means a complete instruction how to qualify the LOBSTER tools or tools in general.
When qualifying a tool according to ISO 26262 you should always consult an expert on that field.

# Introduction

This document provides guidance on how the LOBSTER tool suite could be qualified for use in safety-critical automotive software development, specifically in the context of ISO 26262.
The strategies and examples outlined here are intended to inspire and inform engineers, quality managers, and other stakeholders involved in tool qualification processes.

It is important to note that this document does not constitute a complete or authoritative instruction for qualifying the LOBSTER tools or any other tools.
The qualification of software tools for safety-related projects is a complex task that depends on the specific context, product, and organizational requirements.
Therefore, the approaches described herein should be adapted as necessary and always reviewed by experts in ISO 26262 and functional safety.

Furthermore, the inclusion of any strategy or example in this document should not be interpreted as an indication that BMW applies this strategy in its own processes.

# Qualification Strategy

The tool qualification strategy of LOBSTER is as follows:
1. Use cases are written down in TRLC format.
2. The use cases are analyzed and potential errors are deduced.
3. Test specifications are deduced from the potential errors.
4. System test cases are implemented according to the test specifications.
   Their goal is to demonstrate that the potential errors do not exist.

It is important to note that not every feature will be qualified.
Only use cases will be qualified.
A use case can be achieved by the user by using features in the sense of
the use case.
If a feature is being used in a way which is not foreseen by any of the use cases,
then the result of the corresponding tool is not qualified.

Example:
Imagine a tool supports a list of files and a list of directories as input.
Furthermore assume that a use case specifies that a list of files shall be given
to the tool as input.
But specifying a list of directories is not part of the use case.
Then most likely the potential errors also only consider scenarios with input files,
but not with input directories.
In this example the output of the tool is not qualified in the sense of ISO 26262
when providing a list of directories, even if the tool supports it.

## Definition of "Potential Error"

Potential errors shall describe potential bugs of the tool.
These are hypothetical, and one does not know if they exist, unless tested.

They do not describe potential misuse of the tool by users.
For example, if a user gives a wrong (but valid) configuration file to the tool, 
then this scenario will not be described by a potential error.
There is nothing the tool can do about it.
Contrary, when the specified input file is written in an invalid format,
then the tool must react properly.
A potential error in this example is that, the tool silently ignores the error
and uses a default behavior.
This could lead to consecutive errors, for example that a quality manager
releases a software product that is in fact not fulfilling all quality metrics.

In other words, a potential error describes a situation where the tool does not
behave such that an error can be detected.

These potential errors can then be tested, and one can disprove it.

### Properties of Potential Errors

Potential errors are written down in TRLC format.
Their TLRC type is `req.PotentialError`.
Their properties are described in this section.

#### Impact

The `impact` property describes how a hypothetical undiscovered bug of the tool
can lead to a dangerous situation.
This can be a financial risk for the company using the tool, or a hazard to the
end-user of the company's product.
Imagine a car company developed new software for a car.
The car software could have been developed with the assistance of the LOBSTER
tool chain to generate quality reports, but the tool(s) had generated wrong output.

What is the risk to the company or end-user?

Assume a tool like `lobster-cpptest` had an undiscovered bug and `lobster-report`
managed to create a report with 100% test-to-requirement coverage in the end, but
it should have reported 42%.

And then the quality manager looked only at the percentage value, and not at the
full list of detected tests.
The quality manager sees 100% coverage and gives clearance to release the software,
which in fact had a much lower coverage.
The new car software could have hidden undocumented features,
which could cost the company additional support effort in the best case,
or the health of a customer could be at risk in the worst case.
Maybe the customer accidentally enables the hidden feature and driving assistance
systems turn off.

Such situations shall be prevented.
ISO 26262 focuses on hazards to the end-user.

The `impacts` property shall list all these hazardous situations.

#### Affected Use Case

The `affects` property of `req.PotentialError` describes the use case which could
lead to a risky situation.
In our above example the use case is that, a quality manager wants to know whether
all tests are linked to requirements.
`lobster-report` implements that use case, and the quality manager gets an answer,
like 100%.
But what if there is a bug somewhere, the real coverage is 42%, but the final report
says 100%?
This is a situation we must prevent.
And we do so by boiling down the use case into potential errors.

One such potential error could be, that `lobster-cpptest` generates a report without
being able to read a configuration file.

The property `affects` links the potential error to the use cases.
The goal is to be able to do a review whether a use case has been broken down into
all potential errors.

### Example
```trlc
req.PotentialError Output_Despite_Missing_Config_File {
    summary = "Output generated without configuration file"
    description = '''
      The user does not provide a valid path to a configuration file,
      but the tool generates valid output nevertheless, potentially based on
      irrelevant C++ files.
      For example, the tool might consider the current working directory
      as source of C++ files, and these do in fact contain links to real requirements,
      such that lobster-report would compute a non-zero coverage value.
    '''
    impacts = [
      '''If the tool generates a valid output file, then the invalid input path could
        remain undetected, and subsequent tools of the LOBSTER tool chain
        could consume unqualified input data.''',
    ]

    affects = [
        Trace_Codebeamer_to_CPP_Tests,
        List_Codebeamer_to_CPP_Tests,
        List_Codebeamer_without_CPP_Tests,
        List_CPP_Tests_to_Codebeamer,
        List_CPP_Tests_without_Codebeamer,
        Requirements_to_CPP_Test_Coverage,
        List_Findings,
    ]
    impact_type = req.Impact_Type.Safety
}
```

# Summary
A use case generates qualified output, if:
1. it is documented,
2. it is broken down into all potential errors, and
3. all potential errors are fully disproven by system tests.

**Note:** The suitability of these steps depends on your specific product and organizational context. Always consult an ISO 26262 expert.

Hence this document can only be seen as inspiration.
