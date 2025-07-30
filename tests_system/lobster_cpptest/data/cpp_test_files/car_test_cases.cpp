/** ensure all desired test macros are parsed */

TEST_P_INSTANCE(TestMacrosTest, LeatherSeats) {}
TEST(TestMacrosTest, Sunroof) {}
TEST_F(TestMacrosTest1, HeatedSteeringWheel) {}
TEST_P(TestMacrosTest1, AdaptiveCruiseControl) {}
TYPED_TEST(TestMacrosTest2, SurroundSoundSystem) {}
TYPED_TEST_P(TestMacrosTest2, PanoramicRoof) {}
TYPED_TEST_SUITE(TestMacrosTest2, MassageSeats) {}
TEST_F_INSTANCE(TestMacrosTest3, AmbientLighting) {}

/** ensure test implementation is correctly parsed */

TEST(
    ImplementationTest,
    WirelessCharging
) {}

TEST(ImplementationTest, KeylessEntry) {}

TEST(ImplementationTest, AutomaticParking) {
    EXPECT_EQ(true, DummyFunctionForValidCondition());
}

TEST(ImplementationTest, HeadsUpDisplay)
{
    // Some comments
    EXPECT_EQ(true, DummyFunctionForValidCondition());
    // Some other comments
}

/** ensure test tag is correctly parsed */

/// @test foo1
TEST(TestTagTest, VentilatedSeats) {}

///
/// @test foo2
TEST(TestTagTest, DigitalCockpit) {}

/// @test foo3
///
TEST(TestTagTest, GestureControl) {}

///
/// @test foo4
///
TEST(TestTagTest, NightVision) {}

/// @test lorem ipsum
TEST(TestTagTest, PremiumSoundSystem) {}

/** ensure brief are parsed correctly */

/// @brief Some nasty bug1
TEST(BriefTagTest, AutomaticClimateControl) {}

/// @brief This is a brief field
/// with a long description
TEST(BriefTagTest, RearSeatEntertainment) {}

/** ensure requirement tags are parse correctly */

/// @requirement CB-#0815
TEST(RequirementTagTest, LaneKeepAssist) {}

/** @requirement CB-#0815 CB-#0816 */
TEST(RequirementTagTest1, BlindSpotMonitoring) {}

/**
 * @requirement CB-#0815 CB-#0816
 */
TEST(RequirementTagTest1, ParkingSensors) {}

/**
 * @requirement CB-#0815, CB-#0816,
 * 				CB-#0817
 * @requirement CB-#0818 CB-#0819
 * 				CB-#0820
 */
TEST(RequirementTagTest1, TrafficSignRecognition) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815
///
TEST(RequirementTagTest2, AutomaticEmergencyBraking) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815,
///              https://codebeamer.company.net/cb/issue/0816
///
TEST(RequirementTagTest2, DriverAttentionMonitoring) {}

/**
 *  @requirement https://codebeamer.company.net/cb/issue/0815
 *               https://codebeamer.company.net/cb/issue/0816
 */
TEST(RequirementTagTest2, RemoteStart) {}

/**
 *  @requirement https://codebeamer.company.net/cb/issue/0815, https://codebeamer.company.net/cb/issue/0816
 *  @requirement https://codebeamer.company.net/cb/issue/0817
 *               https://codebeamer.company.net/cb/issue/0818
 */
TEST(RequirementTagTest2, PowerTailgate) {}

///
/// @requirement https://codebeamer.company.net/cb/issue/0815
/// @requirement CB-#0816
///
TEST(RequirementTagTest3, MultiZoneClimateControl) {}

///
/// @requirement something_arbitrary
///
TEST(RequirementTagTest4, SoftCloseDoors) {}

///
/// @requirement 
///
TEST(RequirementTagTest4, AcousticGlass) {}

/**
 * invalid test cases
 * 	the following tests should not be parsed
 * 	as valid test cases
 */
TEST(InvalidTest1,) {}
TEST(, InvalidTest2) {}
TEST(,) {}
TEST() {}
