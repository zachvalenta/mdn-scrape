help:
	@echo
	@echo "🕸 🕷 🕸  APP"
	@echo
	@echo "crawl:   crawl MDN domain and store data in Algolia"
	@echo
	@echo "search:  use UI for Algolia search"
	@echo
	@echo "📊 CODE QUALITY"
	@echo
	@echo "lint:    lint using flake8"
	@echo
	@echo "📦 DEPENDENCIES"
	@echo
	@echo "pipfr:   freeze dependencies into requirements.txt"
	@echo "pipin:   install dependencies from requirements.txt"
	@echo "piprs:   remove any installed pkg *not* in requirements.txt"
	@echo

crawl:
	cd mdn; scrapy crawl mdn_spider -s LOG_ENABLED=0

search:
	cd frontend; open index.html

lint:
	flake8 src

pipfr:
	pip freeze > requirements.txt

pipin:
	pip install -r requirements.txt

piprs:
	@echo "🔍 - DISCOVERING UNSAVED PACKAGES\n"
	pip freeze > pkgs-to-rm.txt
	@echo
	@echo "📦 - UNINSTALL ALL PACKAGES\n"
	pip uninstall -y -r pkgs-to-rm.txt
	@echo
	@echo "♻️  - REINSTALL SAVED PACKAGES\n"
	pip install -r requirements.txt
	@echo
	@echo "🗑  - UNSAVED PACKAGES REMOVED\n"
	diff pkgs-to-rm.txt requirements.txt | grep '<'
	@echo
	rm pkgs-to-rm.txt
	@echo
