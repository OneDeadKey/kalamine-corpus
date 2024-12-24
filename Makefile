.PHONY: all txt extract fancy json

all: extract fancy json

txt: extract fancy

extract:
	@bin/extract.sh

fancy:
	@echo "Making the text fancier..."
	@bin/fancify.sh

json:
	@mkdir -p json
	@echo "Creating JSON dicts..."
	@bin/chardict.py
	@echo "Merging JSON dicts..."
	@echo "...  de_modern"
	@bin/merge.py txt/deu_*.json > json/de_modern.json
	@echo "...  en_modern"
	@bin/merge.py txt/eng_*.json > json/en_modern.json
	@echo "...  es_modern"
	@bin/merge.py txt/spa_*.json > json/es_modern.json
	@echo "...  fr_modern"
	@bin/merge.py txt/fra_*.json > json/fr_modern.json
	@echo "...  it_modern"
	@bin/merge.py txt/ita_*.json > json/it_modern.json
	@echo "...  de_literary"
	@bin/merge.py txt/de_*.json > json/de_literary.json
	@echo "...  en_literary"
	@bin/merge.py txt/en_*.json > json/en_literary.json
	@echo "...  es_literary"
	@bin/merge.py txt/es_*.json > json/es_literary.json
	@echo "...  fr_literary"
	@bin/merge.py txt/fr_*.json > json/fr_literary.json
	@echo "...  it_literary"
	@bin/merge.py txt/it_*.json > json/it_literary.json

