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
		lobster util tests-system/run_tool_tests.py

trlc:
	trlc lobster --error-on-warnings --verify

style:
	@python3 -m pycodestyle lobster \
		--exclude=assets.py

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
	(cd tests-integration/projects/coverage; make)
	rm -f MODULE.bazel MODULE.bazel.lock

system-tests:
	mkdir -p docs
	make -B -C tests-system TOOL=lobster-json
	make -B -C tests-system TOOL=lobster-trlc
	make -B -C tests-system TOOL=lobster-python

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
	coverage report --rcfile=coverage.cfg --fail-under=62

test: clean-coverage system-tests unit-tests
	make coverage
	util/check_local_modifications.sh

test-all: integration-tests system-tests unit-tests
	make coverage
	util/check_local_modifications.sh

docs:
	rm -rf docs
	mkdir -p docs
	@-make tracing

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
				  requirements.lobster-% \
				  system-tests.lobster-%
	lobster-report \
		--lobster-config=lobster/tools/lobster.conf \
		--out=report.lobster
	lobster-online-report report.lobster

requirements.lobster-%: lobster/tools/requirements.rsl
	$(eval TOOL_PATH := $(subst -,/,$*))   
	lobster-trlc lobster/tools/$(TOOL_PATH)/requirements.trlc lobster/tools/requirements.rsl \
	--config-file=lobster/tools/lobster-trlc.conf \
	--out requirements.lobster

code.lobster-%:
	$(eval TOOL_PATH := $(subst -,/,$*))
	lobster-python --out code.lobster lobster/tools/$(TOOL_PATH)

unit-tests.lobster-%:
	$(eval TOOL_PATH := $(subst -,/,$*))
	lobster-python --activity --out unit-tests.lobster tests-unit/lobster-$(TOOL_PATH)

system-tests.lobster-%:
	$(eval TOOL_PATH := $(subst -,/,$*))
	python3 tests-system/lobster-trlc-system-test.py $(TOOL_PATH);

clean-coverage:
	@rm -rf htmlcov
	@find . -name '.coverage*' -type f -delete
	@find . -name '*.pyc' -type f -delete
	@echo "All .coverage, .coverage.* and *.pyc files deleted."
