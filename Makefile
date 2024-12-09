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
	@echo "...  de_leipzig"
	@bin/merge.py json/deu_* > json/de_leipzig.json
	@echo "...  en_leipzig"
	@bin/merge.py json/eng_* > json/en_leipzig.json
	@echo "...  es_leipzig"
	@bin/merge.py json/spa_* > json/es_leipzig.json
	@echo "...  fr_leipzig"
	@bin/merge.py json/fra_* > json/fr_leipzig.json
	@echo "...  it_leipzig"
	@bin/merge.py json/ita_* > json/it_leipzig.json
