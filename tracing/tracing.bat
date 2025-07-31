REM Generate Use Cases
lobster-trlc --config=tracing/use-cases.lobster-trlc.yaml --out=tracing-out/use-cases.lobster

REM Generate artifacts for lobster-codebeamer
lobster-trlc --config=tracing/codebeamer.potential-errors.lobster-trlc.yaml --out=tracing-out/codebeamer.potential-errors.lobster
lobster-trlc --config=tracing/codebeamer.system-requirements.lobster-trlc.yaml --out=tracing-out/codebeamer.system-requirements.lobster
lobster-trlc --config=tracing/codebeamer.software-requirements.lobster-trlc.yaml --out=tracing-out/codebeamer.software-requirements.lobster
lobster-python lobster/tools/codebeamer --out=tracing-out/codebeamer.code.lobster
lobster-python tests-system/lobster-codebeamer --activity --out=tracing-out/codebeamer.system-tests.lobster
lobster-python tests-unit/lobster-codebeamer --activity --out=tracing-out/codebeamer.unit-tests.lobster

REM Generate artifacts for lobster-cpptest
lobster-trlc --config=tracing/cpptest.potential-errors.lobster-trlc.yaml --out=tracing-out/cpptest.potential-errors.lobster
lobster-trlc --config=tracing/cpptest.system-requirements.lobster-trlc.yaml --out=tracing-out/cpptest.system-requirements.lobster
lobster-trlc --config=tracing/cpptest.software-requirements.lobster-trlc.yaml --out=tracing-out/cpptest.software-requirements.lobster
lobster-python lobster/tools/cpptest --out=tracing-out/cpptest.code.lobster
lobster-python tests-system/lobster-cpptest --activity --out=tracing-out/cpptest.system-tests.lobster
lobster-python tests-unit/lobster-cpptest --activity --out=tracing-out/cpptest.unit-tests.lobster

REM Generate artifacts for lobster-trlc
lobster-trlc --config=tracing/trlc.potential-errors.lobster-trlc.yaml --out=tracing-out/trlc.potential-errors.lobster
lobster-trlc --config=tracing/trlc.system-requirements.lobster-trlc.yaml --out=tracing-out/trlc.system-requirements.lobster
lobster-trlc --config=tracing/trlc.software-requirements.lobster-trlc.yaml --out=tracing-out/trlc.software-requirements.lobster
lobster-python lobster/tools/trlc --out=tracing-out/trlc.code.lobster
lobster-python tests-system/lobster-trlc --activity --out=tracing-out/trlc.system-tests.lobster
lobster-python tests-unit/lobster-trlc --activity --out=tracing-out/trlc.unit-tests.lobster

REM Generate report
lobster-report --lobster-config=tracing/tracing_policy.conf --out=tracing-out/tracing.lobster
lobster-html-report tracing-out/tracing.lobster --out=tracing-out/tracing.html
