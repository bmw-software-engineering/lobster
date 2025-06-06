/** ensure requirement tags are parse correctly */

/// @requirement CB-#0815
TEST(RequirementTagTestA, RequirementA) {}

/** @requirement CB-#0815 CB-#0816 */
TEST(RequirementTagTestA1, RequirementAsOneLineCommentsA) {}

/**
 * @requirement CB-#0815 CB-#0816
 */
TEST(RequirementTagTestA1, RequirementAsCommentsA) {}

/**
 * @requirement CB-#0815, CB-#0816,
 * 				CB-#0817
 * @requirement CB-#0818 CB-#0819
 * 				CB-#0820
 */
TEST(RequirementTagTestA1, RequirementsAsMultipleCommentsA) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815
///
TEST(RequirementTagTestA2, URLRequirementA) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815,
///              https://codebeamer.company.net/cb/issue/0816
///
TEST(RequirementTagTestA2, URLRequirementsCommaSeparatedA) {}

/**
 *  @requirement https://codebeamer.company.net/cb/issue/0815
 *               https://codebeamer.company.net/cb/issue/0816
 */
TEST(RequirementTagTestA2, URLRequirementsAsCommentsSpaceSeparatedA) {}

/**
 *  @requirement https://codebeamer.company.net/cb/issue/0815, https://codebeamer.company.net/cb/issue/0816
 *  @requirement https://codebeamer.company.net/cb/issue/0817
 *               https://codebeamer.company.net/cb/issue/0818
 */
TEST(RequirementTagTestA2, MultipleURLRequirementsA) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815
/// @requirement CB-#0816
///
TEST(RequirementTagTestA3, MixedRequirementsA) {}

///
/// @requirement something_arbitrary
///
TEST(RequirementTagTestA4, InvalidRequirementA) {}

///
/// @requirement 
///
TEST(RequirementTagTestA4, MissingRequirementReferenceA) {}
