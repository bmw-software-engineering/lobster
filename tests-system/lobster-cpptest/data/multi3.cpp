/** ensure requirement tags are parse correctly */

/// @requirement CB-#0815
TEST(RequirementTagTestC, RequirementC) {}

/** @requirement CB-#0815 CB-#0816 */
TEST(RequirementTagTestC1, RequirementAsOneLineCommentsC) {}

/**
 * @requirement CB-#0815 CB-#0816
 */
TEST(RequirementTagTestC1, RequirementAsCommentsC) {}

/**
 * @requirement CB-#0815, CB-#0816,
 * 				CB-#0817
 * @requirement CB-#0818 CB-#0819
 * 				CB-#0820
 */
TEST(RequirementTagTestC1, RequirementsAsMultipleCommentsC) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815
///
TEST(RequirementTagTestC2, URLRequirementC) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815,
///              https://codebeamer.company.net/cb/issue/0816
///
TEST(RequirementTagTestC2, URLRequirementsCommaSeparatedC) {}

/**
 *  @requirement https://codebeamer.company.net/cb/issue/0815
 *               https://codebeamer.company.net/cb/issue/0816
 */
TEST(RequirementTagTestC2, URLRequirementsAsCommentsSpaceSeparatedC) {}

/**
 *  @requirement https://codebeamer.company.net/cb/issue/0815, https://codebeamer.company.net/cb/issue/0816
 *  @requirement https://codebeamer.company.net/cb/issue/0817
 *               https://codebeamer.company.net/cb/issue/0818
 */
TEST(RequirementTagTestC2, MultipleURLRequirementsC) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815
/// @requirement CB-#0816
///
TEST(RequirementTagTestC3, MixedRequirementsC) {}

///
/// @requirement something_arbitrary
///
TEST(RequirementTagTestC4, InvalidRequirementC) {}

///
/// @requirement 
///
TEST(RequirementTagTestC4, MissingRequirementReferenceC) {}
