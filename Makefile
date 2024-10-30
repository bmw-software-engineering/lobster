SYSTEM_PYTHONPATH:=$(PYTHONPATH)
export LOBSTER_ROOT=$(PWD)
export PYTHONPATH=$(LOBSTER_ROOT)

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

integration-tests: packages
	(cd integration-tests/projects/basic; make)
	(cd integration-tests/projects/filter; make)

system-tests:
	mkdir -p docs
	make -B -C test-system/lobster-json
	make -B -C test-system/lobster-python

unit-tests:
	coverage run -p \
			--branch --rcfile=coverage.cfg \
			--data-file .coverage \
			-m unittest discover -s test-unit -v

test: integration-tests system-tests unit-tests

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
	coverage report --rcfile=coverage.cfg --fail-under=57

test-ci: system-tests unit-tests coverage
	util/check_local_modifications.sh

docs:
	rm -rf docs
	mkdir docs
	@-make tracing

tracing: report.lobster
	mkdir -p docs
	make lobster/html/assets.py
	lobster-html-report report.lobster --out=docs/tracing.html
	lobster-ci-report report.lobster
	@read -p "$@ finished" input

report.lobster: lobster/tools/lobster.conf \
                code.lobster \
				unit-tests.lobster \
				requirements.lobster \
				system-tests.lobster
	lobster-report \
		--lobster-config=lobster/tools/lobster.conf \
		--out=report.lobster
	lobster-online-report report.lobster
	@read -p "$@ finished" input

requirements.lobster: lobster/tools/trlc/requirements.trlc \
                      lobster/tools/requirements.rsl
	lobster-trlc \
		--config-file=lobster/tools/lobster-trlc.conf \
		--out requirements.lobster
	@read -p "$@ finished" input

code.lobster: $(wildcard lobster/tools/trlc/*.py)
	lobster-python --out code.lobster lobster/tools/trlc
	@read -p "$@ finished" input

unit-tests.lobster: $(wildcard test-unit/lobster-trlc/*.py)
	lobster-python --activity --out unit-tests.lobster test-unit/lobster-trlc
	@read -p "$@ finished" input

system-tests.lobster: $(wildcard test-system/*/*.rsl) \
                      $(wildcard test-system/*/*.trlc) \
                      $(wildcard test-system/*/tracing)
	python3 test-system/lobster-trlc/lobster-trlc-system-test.py
