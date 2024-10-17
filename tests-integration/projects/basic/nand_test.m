classdef nand_test < matlab.unittest.TestCase
methods (Test, TestTags = {'example.req_nand'})
    function test_1(t)
      result = nand(1, 0);
      t.verifyEqual(result, 1);
    end
  end
end
