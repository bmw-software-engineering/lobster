/** ensure requirement tags are parse correctly */

/// @requirement CB-#0815
TEST(RequirementTagTestE, RequirementE) {}

/** @requirement CB-#0815 CB-#0816 */
TEST(RequirementTagTestE1, RequirementAsOneLineCommentsE) {}

/**
 * @requirement CB-#0815 CB-#0816
 */
TEST(RequirementTagTestE1, RequirementAsCommentsE) {}

/**
 * @requirement CB-#0815, CB-#0816,
 * 				CB-#0817
 * @requirement CB-#0818 CB-#0819
 * 				CB-#0820
 */
TEST(RequirementTagTestE1, RequirementsAsMultipleCommentsE) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815
///
TEST(RequirementTagTestE2, URLRequirementE) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815,
///              https://codebeamer.company.net/cb/issue/0816
///
TEST(RequirementTagTestE2, URLRequirementsCommaSeparatedE) {}

/**
 *  @requirement https://codebeamer.company.net/cb/issue/0815
 *               https://codebeamer.company.net/cb/issue/0816
 */
TEST(RequirementTagTestE2, URLRequirementsAsCommentsSpaceSeparatedE) {}

/**
 *  @requirement https://codebeamer.company.net/cb/issue/0815, https://codebeamer.company.net/cb/issue/0816
 *  @requirement https://codebeamer.company.net/cb/issue/0817
 *               https://codebeamer.company.net/cb/issue/0818
 */
TEST(RequirementTagTestE2, MultipleURLRequirementsE) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815
/// @requirement CB-#0816
///
TEST(RequirementTagTestE3, MixedRequirementsE) {}

///
/// @requirement something_arbitrary
///
TEST(RequirementTagTestE4, InvalidRequirementE) {}

///
/// @requirement 
///
TEST(RequirementTagTestE4, MissingRequirementReferenceE) {}
