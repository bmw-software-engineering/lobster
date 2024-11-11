SYSTEM_PYTHONPATH:=$(PYTHONPATH)
export LOBSTER_ROOT=$(PWD)
export PYTHONPATH=$(LOBSTER_ROOT)
export PATH:=$(LOBSTER_ROOT):$(PATH)

ASSETS=$(wildcard assets/*.svg)

lobster/html/assets.py: $(ASSETS) util/mkassets.py
	util/mkassets.py lobster/html/assets.py $(ASSETS)

lint: style
	@PYTHONPATH=$(SYSTEM_PYTHONPATH) \
	python3 -m pylint --rcfile=pylint3.cfg \
		--reports=no \
		--ignore=assets.py \
		lobster

style:
	@python3 -m pycodestyle lobster \
		--exclude=assets.py

.PHONY: packages
packages:
	git clean -xdf
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

clang-tidy:
	cd .. && \
	git clone https://github.com/bmw-software-engineering/llvm-project && \
	cd llvm-project && \
	cmake -S llvm -B build -G Ninja -DLLVM_ENABLE_PROJECTS='clang;clang-tools-extra' -DCMAKE_BUILD_TYPE=Release && \
	cmake --build build --target clang-tidy

integration-tests: packages
	(cd tests-integration/projects/basic; make)
	(cd tests-integration/projects/filter; make)
	rm -f MODULE.bazel MODULE.bazel.lock

system-tests:
	mkdir -p docs
	make -B -C tests-system/lobster-json
	make -B -C tests-system/lobster-python

unit-tests:
	coverage run -p \
			--branch --rcfile=coverage.cfg \
			--data-file .coverage \
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

coverage:
	coverage combine -q
	coverage html --rcfile=coverage.cfg
	coverage report --rcfile=coverage.cfg --fail-under=72

test: system-tests unit-tests
	make coverage
	util/check_local_modifications.sh

test-all: integration-tests system-tests unit-tests
	make coverage
	util/check_local_modifications.sh

tracing: report.lobster
	mkdir -p docs
	make lobster/html/assets.py
	lobster-html-report report.lobster --out=docs/tracing.html
	lobster-ci-report report.lobster

report.lobster: lobster/tools/lobster.conf \
                code.lobster \
				unit-tests.lobster \
				requirements.lobster \
				system-tests.lobster
	lobster-report \
		--lobster-config=lobster/tools/lobster.conf \
		--out=report.lobster
	lobster-online-report report.lobster

requirements.lobster: lobster/tools/trlc/requirements.trlc \
                      lobster/tools/requirements.rsl
	lobster-trlc lobster/tools/trlc lobster/tools/requirements.rsl \
		--config-file=lobster/tools/lobster-trlc.conf \
		--out requirements.lobster

code.lobster: $(wildcard lobster/tools/trlc/*.py)
	lobster-python --out code.lobster lobster/tools/trlc

unit-tests.lobster: $(wildcard tests-unit/lobster-trlc/*.py)
	lobster-python --activity --out unit-tests.lobster tests-unit/lobster-trlc

system-tests.lobster: $(wildcard tests-system/*/*.rsl) \
                      $(wildcard tests-system/*/*.trlc) \
                      $(wildcard tests-system/*/tracing)
	python3 tests-system/lobster-trlc/lobster-trlc-system-test.py

TOOL_FOLDERS := $(shell find ./lobster/tools -mindepth 1 -maxdepth 1 -type d -exec basename {} \;)
# TOOL_FOLDERS = python core gtest cpptest trlc cpp json __pycache__ codebeamer

TOOL_FOLDERS_3 := $(shell find ./lobster/tools -mindepth 1 -maxdepth 2 -type d | sed 's|^./lobster/tools/||')
# Tool folders 2 is: python python/__pycache__ core core/html_report core/report core/online_report core/ci_report core/__pycache__ gtest cpptest cpptest/parser trlc trlc/__pycache__ cpp json __pycache__ codebeamer

TOOL_FOLDERS_2_old := $(shell find ./lobster/tools -mindepth 1 -maxdepth 2 -type d | grep -v -E '^./lobster/tools/core$$|__pycache__' | sed 's|^./lobster/tools/||')

TOOL_FOLDERS_2 := $(shell find ./lobster/tools -mindepth 1 -maxdepth 2 -type d | grep -v -E '^./lobster/tools/core$$|__pycache__' | sed 's|^./lobster/tools/||; s|/|99|g')

$(eval EXPANDED_TOOL_FOLDERS := $(TOOL_FOLDERS_2))
$(foreach tool,$(EXPANDED_TOOL_FOLDERS),$(eval tracing_tools_$(tool): tracing_tools_% ; @echo "Running tracing_tools_$(tool)"))

CORE_TOOLS := $(shell find ./lobster/tools/core -type f -name "*.py" ! -name "__init__.py" ! -path "*/__pycache__/*" -exec basename {} .py \;)
# CORE_TOOLS = ci_report online_report report html_report

CORE_CODE_SCRIPTS := $(shell find ./lobster/tools/core -type f -name "*.py" ! -name "__init__.py" ! -path "*/__pycache__/*" -exec echo core/{} \; | sed 's|./lobster/tools/core/||')
# CORE_CODE_SCRIPTS = core/ci_report.py core/online_report.py core/report.py core/html_report.py

CORE_COUNT := $(shell echo $(CORE_CODE_SCRIPTS) | wc -w)
CORE_REPEATED := $(shell yes core | head -n $(CORE_COUNT) | tr '\n' ' ' | sed 's/ *$$//')
$(eval TOOL_FOLDERS := $(shell echo $(TOOL_FOLDERS) | sed "s/\bcore\b/$(CORE_REPEATED)/"))
# Final TOOL_FOLDERS: python core core core core gtest cpptest trlc cpp json __pycache__ codebeamer

# Target to prepare the environment for tracing (for verification)
prepare-environment-tracing:
#	@echo "Initial TOOL_FOLDERS: $(TOOL_FOLDERS)"
	@rm -f lobster-python-commands.txt
	@core_written=false; \ 
	for tool in $(TOOL_FOLDERS); do \
		if [ "$$tool" = "core" ]; then \
			if [ "$$core_written" = false ]; then \
				for script in $(CORE_CODE_SCRIPTS); do \
					echo "$$script" >> lobster-python-commands.txt; \
				done; \
				core_written=true; \
			fi; \
		else \
			echo "$$tool" >> lobster-python-commands.txt; \
		fi; \
	done
#	@echo "Generated lobster-python-commands.txt with the following content:"
#	@cat lobster-python-commands.txt
#	@echo "Final TOOL_FOLDERS: $(TOOL_FOLDERS)"

.PHONY: docs clean-docs tracing-% clean-lobster tracing_tools_%

print-var/var:
	@echo "Tool folders 2 is: $(TOOL_FOLDERS_2)"
docs-copy: clean-docs prepare-environment-tracing
	@for tool in $(TOOL_FOLDERS); do \
			echo "hi"
		else \
            $(MAKE) -B tracing-tools-$$tool; \
            read -p "Finished processing $$tool. Press Enter to continue... " input; \
        fi; \
    done
#	make clean-lobster
# read -p "Finished processing $$tool. Press Enter to continue... " input; \
tracing-tools-
docs: clean-docs
	@echo "TOOL_FOLDER_2 is: $(TOOL_FOLDERS_2)"
	@echo "EXPANDED_TOOL_FOLDERS is: $(EXPANDED_TOOL_FOLDERS)"
	make clean-lobster
	@for tool in $(EXPANDED_TOOL_FOLDERS); do \
		echo "Starting tool: $$tool"; \
		target_name=tracing_tools_$$tool; \
		echo "Invoking target: $$target_name"; \
		$(MAKE) -B $$target_name; \
		read -p "Finished processing $$tool. Press Enter to continue... " input; \
    done
	make clean-lobster
# read -p "Finished processing $$tool. Press Enter to continue... " input; \

clean-docs:
	rm -rf docs
 
tracing_tools_%: tracing_% clean-lobster
	@echo "Finished processing tool: $*"

tracing_%: report.lobster-%
	mkdir -p docs
	make lobster/html/assets.py
	lobster-html-report report.lobster --out=docs/tracing-$*.html
	lobster-ci-report report.lobster

report.lobster-%: lobster/tools/lobster.conf \
                  code.lobster-% \
                  unit-tests.lobster-% \
                  requirements.lobster-% \
                  system-tests.lobster-%
	lobster-report \
		--lobster-config=lobster/tools/lobster.conf \
		--out=report.lobster
	lobster-online-report report.lobster

requirements.lobster-%: lobster/tools/%/requirements.trlc \
                        lobster/tools/requirements.rsl
	lobster-trlc lobster/tools/$*/requirements.trlc lobster/tools/requirements.rsl \
		--config-file=lobster/tools/lobster-trlc.conf \
		--out requirements.lobster
 
# Note: Wildcard does not support recirsive search.
# eg. cpptest tool has a subfolder: parser

code.lobster-%:
	@echo "TOOL_PATH first is: $(TOOL_PATH)"
	$(eval TOOL_PATH := $(subst 99,/,$*))
	@echo "TOOL_PATH after is: $(TOOL_PATH)"
	lobster-python --out code.lobster lobster/tools/$(TOOL_PATH)

# we need four reports for core because its 4 tools
# should subfolders be considered here too??
unit-tests.lobster-%:
	@echo "TOOL_PATH first is: $(TOOL_PATH)"
	$(eval TOOL_PATH := $(subst 99,/,$*))
	@echo "TOOL_PATH after is: $(TOOL_PATH)"
	lobster-python --activity --out unit-tests.lobster test-unit/lobster-$(TOOL_PATH)

system-tests.lobster-%:
	@echo "TOOL_PATH first is: $(TOOL_PATH)"
	$(eval TOOL_PATH := $(subst 99,/,$*))
	@echo "TOOL_PATH after is: $(TOOL_PATH)"
	python3 test-system/lobster-trlc-system-test.py $(TOOL_PATH);
#should we rename the py?

# Deleet generated *.lobster files before the next tool is started
clean-lobster:
	rm -f code.lobster
	rm -f report.lobster
	rm -f requirements.lobster
	rm -f unit-tests.lobster
	rm -f system-tests.lobster
