ASSETS=$(wildcard assets/*.svg)

lobster/report/assets.py: $(ASSETS) util/mkassets.py
	@util/mkassets.py lobster/report/assets.py $(ASSETS)

lint: style
	@python3 -m pylint --rcfile=pylint3.cfg \
		--reports=no lobster_* lobster

style:
	@python3 -m pycodestyle lobster_* lobster --exclude=assets.py
