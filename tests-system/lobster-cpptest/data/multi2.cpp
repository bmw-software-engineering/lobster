/** ensure requirement tags are parse correctly */

/// @requirement CB-#0815
TEST(RequirementTagTestB, RequirementB) {}

/** @requirement CB-#0815 CB-#0816 */
TEST(RequirementTagTestB1, RequirementAsOneLineCommentsB) {}

/**
 * @requirement CB-#0815 CB-#0816
 */
TEST(RequirementTagTestB1, RequirementAsCommentsB) {}

/**
 * @requirement CB-#0815, CB-#0816,
 * 				CB-#0817
 * @requirement CB-#0818 CB-#0819
 * 				CB-#0820
 */
TEST(RequirementTagTestB1, RequirementsAsMultipleCommentsB) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815
///
TEST(RequirementTagTestB2, URLRequirementB) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815,
///              https://codebeamer.company.net/cb/issue/0816
///
TEST(RequirementTagTestB2, URLRequirementsCommaSeparatedB) {}

/**
 *  @requirement https://codebeamer.company.net/cb/issue/0815
 *               https://codebeamer.company.net/cb/issue/0816
 */
TEST(RequirementTagTestB2, URLRequirementsAsCommentsSpaceSeparatedB) {}

/**
 *  @requirement https://codebeamer.company.net/cb/issue/0815, https://codebeamer.company.net/cb/issue/0816
 *  @requirement https://codebeamer.company.net/cb/issue/0817
 *               https://codebeamer.company.net/cb/issue/0818
 */
TEST(RequirementTagTestB2, MultipleURLRequirementsB) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815
/// @requirement CB-#0816
///
TEST(RequirementTagTestB3, MixedRequirementsB) {}

///
/// @requirement something_arbitrary
///
TEST(RequirementTagTestB4, InvalidRequirementB) {}

///
/// @requirement 
///
TEST(RequirementTagTestB4, MissingRequirementReferenceB) {}
