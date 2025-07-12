SYSTEM_PYTHONPATH:=$(PYTHONPATH)
export LOBSTER_ROOT=$(PWD)
export PYTHONPATH=$(LOBSTER_ROOT)
export PATH:=$(LOBSTER_ROOT):$(PATH)

ASSETS=$(wildcard assets/*.svg)
TOOL_FOLDERS := $(shell find ./lobster/tools -mindepth 1 -maxdepth 2 -type d | grep -v -E '^./lobster/tools/core$$|__pycache__|parser' | sed 's|^./lobster/tools/||; s|/|-|g')

.PHONY: packages docs

lobster/html/assets.py: $(ASSETS) util/mkassets.py
	util/mkassets.py lobster/html/assets.py $(ASSETS)

lint: style
	@PYTHONPATH=$(SYSTEM_PYTHONPATH) \
	python3 -m pylint --rcfile=pylint3.cfg \
		--reports=no \
		--ignore=assets.py \
		lobster util

lint-system-tests: style
	@PYTHONPATH=$(SYSTEM_PYTHONPATH) \
	python3 -m pylint --rcfile=tests-system/pylint3.cfg \
		--reports=no \
		tests-system/system_test_case_base.py \
		tests-system/asserter.py \
		tests-system/lobster-json \
		tests-system/lobster-report \
		tests-system/lobster-meta-data-tool-base

trlc:
	trlc lobster --error-on-warnings --verify

style:
	@python3 -m pycodestyle lobster tests-system \
		--exclude=assets.py

clean-packages:
	git clean -xdf packages test_install test_install_monolithic test_install_monolithic_venv

packages: clean-packages
	make lobster/html/assets.py
	make -C packages/lobster-core
	make -C packages/lobster-tool-trlc
	make -C packages/lobster-tool-codebeamer
	make -C packages/lobster-tool-cpp
	make -C packages/lobster-tool-cpptest
	make -C packages/lobster-tool-gtest
	make -C packages/lobster-tool-json
	make -C packages/lobster-tool-python
	make -C packages/lobster-metapackage
	make -C packages/lobster-monolithic
	PYTHONPATH= \
		pip3 install --prefix test_install \
		packages/*/dist/*.whl
	PYTHONPATH= \
		pip3 install --prefix test_install_monolithic \
		packages/lobster-monolithic/meta_dist/*.whl
	diff -Naur test_install/lib/python*/site-packages/lobster test_install_monolithic/lib/python*/site-packages/lobster -x "*.pyc"
	diff -Naur test_install/bin test_install_monolithic/bin

	# Very basic smoke test to ensure the tools are packaged properly
	python3 -m venv test_install_monolithic_venv
	. test_install_monolithic_venv/bin/activate && \
		pip install --upgrade pip && \
		pip install packages/lobster-monolithic/meta_dist/*.whl && \
		lobster-report --version && \
		lobster-ci-report --version && \
		lobster-html-report --version && \
		lobster-online-report --version && \
		lobster-online-report-nogit --version && \
		lobster-cpp --version && \
		lobster-cpptest --version && \
		lobster-codebeamer --version && \
		lobster-gtest --version && \
		lobster-json --version && \
		lobster-python --version && \
		lobster-trlc --version
	
clang-tidy:
	cd .. && \
	git clone https://github.com/bmw-software-engineering/llvm-project && \
	cd llvm-project && \
	cmake -S llvm -B build -G Ninja -DLLVM_ENABLE_PROJECTS='clang;clang-tools-extra' -DCMAKE_BUILD_TYPE=Release && \
	cmake --build build --target clang-tidy

integration-tests: packages
	(cd tests-integration/projects/basic; make)
	(cd tests-integration/projects/filter; make)
	(cd tests-integration/projects/coverage; make)
	(cd tests-integration/projects/coverage-half; make)
	(cd tests-integration/projects/coverage-mix; make)
	(cd tests-integration/projects/coverage-zero; make)
	rm -f MODULE.bazel MODULE.bazel.lock

codebeamer-pem:
	@echo "🔐 Generating cert.pem and key.pem for codebeamer system tests..."
	@mkdir -p tests-system/lobster-codebeamer/data/ssl
	@openssl req -x509 -newkey rsa:2048 -nodes \
		-keyout tests-system/lobster-codebeamer/data/ssl/key.pem \
		-out tests-system/lobster-codebeamer/data/ssl/cert.pem \
		-days 365 -subj "//CN=localhost" > /dev/null 2>&1

system-tests: codebeamer-pem
	mkdir -p docs
	python -m unittest discover -s tests-system -v -t .
	make -B -C tests-system TOOL=lobster-python
	@echo "🧹 Cleaning up cert.pem and key.pem..."
	@rm -rf tests-system/lobster-codebeamer/data/ssl

unit-tests:
	coverage run -p \
			--branch --rcfile=coverage.cfg \
			--data-file .coverage.unit \
			--source=lobster \
			-m unittest discover -s tests-unit -v

upload-main: packages
	python3 -m twine upload --repository pypi packages/*/dist/*
	python3 -m twine upload --repository pypi packages/*/meta_dist/*

remove-dev:
	python3 -m util.release

github-release:
	git push
	python3 -m util.github_release

bump:
	python3 -m util.bump_version_post_release

full-release:
	make remove-dev
	git push
	make github-release
	make bump
	git push

# --- Coverage Execution Targets ---
coverage-unit:
	@echo "📊 Generating coverage report for unit tests..."
	coverage combine -q .coverage.unit*
	coverage html --directory=htmlcov-unit --rcfile=coverage.cfg
	coverage report --rcfile=coverage.cfg --fail-under=40

coverage-system:
	@echo "📊 Generating coverage report for system tests..."
	coverage combine -q .coverage.system*
	coverage html --directory=htmlcov-system --rcfile=coverage.cfg
	coverage report --rcfile=coverage.cfg --fail-under=60

# --- Clean Coverage ---
clean-coverage:
	@rm -rf htmlcov htmlcov-unit htmlcov-system
	@find . -type f -name ".coverage*" -delete
	@find . -type f -name "*.pyc" -delete
	@echo "🧹 All .coverage, .coverage.* and *.pyc files deleted."

# --- Convenience Test Targets ---
test-system: clean-coverage system-tests
	make coverage-system
	util/check_local_modifications.sh

test-unit: clean-coverage unit-tests
	make coverage-unit
	util/check_local_modifications.sh

docs:
	mkdir -p docs
	@-make tracing
	@-make tracing-stf

clean-docs:
	rm -rf docs

tracing:
	@mkdir -p docs
	@make lobster/html/assets.py
	@for tool in $(TOOL_FOLDERS); do \
		make tracing-tools-$$tool; \
	done

tracing-tools-%: tracing-%
	@echo "Finished processing tool: $*"

tracing-%: report.lobster-%
	$(eval TOOL_PATH := $(subst -,_,$*))
	lobster-html-report report.lobster --out=docs/tracing-$(TOOL_PATH).html
	lobster-ci-report report.lobster

report.lobster-%: lobster/tools/lobster.conf \
				  code.lobster-% \
				  unit-tests.lobster-% \
				  system_requirements.lobster-% \
				  software_requirements.lobster-% \
				  system-tests.lobster-%
	lobster-report \
		--lobster-config=lobster/tools/lobster.conf \
		--out=report.lobster
	lobster-online-report report.lobster

system_requirements.lobster-%: TRLC_CONFIG = lobster/tools/lobster-trlc-system.conf

system_requirements.lobster-%:
	$(eval TOOL_PATH := $(subst -,/,$*))
	@echo "inputs: ['lobster/tools/requirements.rsl', 'lobster/tools/$(TOOL_PATH)']" > lobster/tools/config.yaml
	@echo "trlc_config_file: $(TRLC_CONFIG)" >> lobster/tools/config.yaml
	lobster-trlc --config=lobster/tools/config.yaml \
	--out=system_requirements.lobster
	rm lobster/tools/config.yaml

software_requirements.lobster-%: TRLC_CONFIG = lobster/tools/lobster-trlc-software.conf

software_requirements.lobster-%:
	$(eval TOOL_PATH := $(subst -,/,$*))
	@echo "inputs: ['lobster/tools/requirements.rsl', 'lobster/tools/$(TOOL_PATH)']" > lobster/tools/config.yaml
	@echo "trlc_config_file: $(TRLC_CONFIG)" >> lobster/tools/config.yaml
	lobster-trlc --config=lobster/tools/config.yaml \
	--out=software_requirements.lobster
	rm lobster/tools/config.yaml

code.lobster-%:
	$(eval TOOL_PATH := $(subst -,/,$*))
	lobster-python --out code.lobster lobster/tools/$(TOOL_PATH)

unit-tests.lobster-%:
	$(eval TOOL_NAME := $(subst _,-,$(notdir $(TOOL_PATH))))
	lobster-python --activity --out unit-tests.lobster tests-unit/lobster-$(TOOL_NAME)

system-tests.lobster-%:
	$(eval TOOL_NAME := $(subst _,-,$(notdir $(TOOL_PATH))))
	lobster-python --activity --out=system-tests.lobster tests-system/lobster-$(TOOL_NAME)

# STF is short for System Test Framework
STF_TRLC_FILES := $(wildcard tests-system/*.trlc)
STF_PYTHON_FILES := $(filter-out tests-system/test_%.py tests-system/run_tool_tests.py, $(wildcard tests-system/*.py))

# This target is used to generate the LOBSTER report for the requirements of the system test framework itself.
tracing-stf: $(STF_TRLC_FILES)
	lobster-trlc --config=lobster/tools/lobster-trlc-system-stf.yaml --out=stf_system_requirements.lobster
	lobster-trlc --config=lobster/tools/lobster-trlc-software-stf.yaml --out=stf_software_requirements.lobster
	lobster-python --out=stf_code.lobster --only-tagged-functions $(STF_PYTHON_FILES)
	lobster-report --lobster-config=tests-system/stf-lobster.conf --out=stf_report.lobster
	lobster-online-report stf_report.lobster
	lobster-html-report stf_report.lobster --out=docs/tracing-stf.html
	@echo "Deleting STF *.lobster files..."
	rm -f stf_system_requirements.lobster stf_software_requirements.lobster stf_code.lobster stf_report.lobster
