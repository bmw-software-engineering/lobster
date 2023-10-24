# --activity --parse-decorator pytest.mark.metadata verifies_tds

@pytest.mark.metadata(
    description="Potato",
    verifies=[],
    ASIL="QM",
    domain="Vegetables",
    testType="Requirements-based test",
    derivationTechnique="Analysis of requirements",
    verifies_tds=[12345],
)
@pytest.mark.supported_potato(["wibble"])
@pytest.mark.supported_os(["wobble"])
class TestFrameServerProcessesStart(BaseTestClass):
    def setup_test(self):
        pass

    def teardown_test(self):
        pass

    def test_1(self):
        self.assertTrue(1 < 2)

    def test_2(self):
        # lobster-trace: 666
        self.assertTrue(1 < 2)
