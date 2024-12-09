.PHONY: all txt extract fancy json

all: extract fancy json

txt: extract fancy

extract:
	@./extract.sh

fancy:
	@echo "Making the text fancier..."
	@./fancify.sh

json:
	@mkdir -p json
	@echo "Creating JSON dicts..."
	@./chardict.py
	@echo "...  de_leipzig"
	@./merge.py json/deu_* > json/de_leipzig.json
	@echo "...  en_leipzig"
	@./merge.py json/eng_* > json/en_leipzig.json
	@echo "...  es_leipzig"
	@./merge.py json/spa_* > json/es_leipzig.json
	@echo "...  fr_leipzig"
	@./merge.py json/fra_* > json/fr_leipzig.json
	@echo "...  it_leipzig"
	@./merge.py json/ita_* > json/it_leipzig.json
