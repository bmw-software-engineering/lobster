/** ensure requirement tags are parse correctly */

/// @requirement CB-#0815
TEST(RequirementTagTestD, RequirementD) {}

/** @requirement CB-#0815 CB-#0816 */
TEST(RequirementTagTestD1, RequirementAsOneLineCommentsD) {}

/**
 * @requirement CB-#0815 CB-#0816
 */
TEST(RequirementTagTestD1, RequirementAsCommentsD) {}

/**
 * @requirement CB-#0815, CB-#0816,
 * 				CB-#0817
 * @requirement CB-#0818 CB-#0819
 * 				CB-#0820
 */
TEST(RequirementTagTestD1, RequirementsAsMultipleCommentsD) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815
///
TEST(RequirementTagTestD2, URLRequirementD) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815,
///              https://codebeamer.company.net/cb/issue/0816
///
TEST(RequirementTagTestD2, URLRequirementsCommaSeparatedD) {}

/**
 *  @requirement https://codebeamer.company.net/cb/issue/0815
 *               https://codebeamer.company.net/cb/issue/0816
 */
TEST(RequirementTagTestD2, URLRequirementsAsCommentsSpaceSeparatedD) {}

/**
 *  @requirement https://codebeamer.company.net/cb/issue/0815, https://codebeamer.company.net/cb/issue/0816
 *  @requirement https://codebeamer.company.net/cb/issue/0817
 *               https://codebeamer.company.net/cb/issue/0818
 */
TEST(RequirementTagTestD2, MultipleURLRequirementsD) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815
/// @requirement CB-#0816
///
TEST(RequirementTagTestD3, MixedRequirementsD) {}

///
/// @requirement something_arbitrary
///
TEST(RequirementTagTestD4, InvalidRequirementD) {}

///
/// @requirement 
///
TEST(RequirementTagTestD4, MissingRequirementReferenceD) {}
