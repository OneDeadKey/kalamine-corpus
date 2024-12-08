#!/usr/bin/sh

# trim whitecpaces
sed -i 's/^\s\+//g' txt/*.txt
sed -i 's/\s\+$//g' txt/*.txt

# cuote marks
sed -i 's/’’/”/g' txt/*.txt
sed -i "s/'/’/g"  txt/*.txt
sed -i 's/´/’/g'  txt/*.txt

sed -i 's/\.\.\+/…/g' txt/*.txt

# common encoding mistakes
sed -i 's/â/’/g'  txt/*.txt
sed -i 's/Ã/Ç/g'      txt/*.txt
sed -i 's/Ã§/ç/g'         txt/*.txt
sed -i 's/Ã©/é/g'         txt/*.txt
sed -i 's/Ã¨/è/g'         txt/*.txt

###
# French
##

sed -i 's/ :/ :/g'  txt/*.txt
sed -i 's/ ;/ ;/g'  txt/*.txt
sed -i 's/ !/ !/g'  txt/*.txt
sed -i 's/ ?/ ?/g'  txt/*.txt

# common French mistakes
sed -i 's/boeuf/bœuf/g'   txt/fr*.txt
sed -i 's/choeur/chœur/g' txt/fr*.txt
sed -i 's/coeur/cœur/g'   txt/fr*.txt
sed -i 's/noeud/nœud/g'   txt/fr*.txt
sed -i 's/oedip/œdip/g'   txt/fr*.txt
sed -i 's/oeil/œil/g'     txt/fr*.txt
sed -i 's/oeuf/œuf/g'     txt/fr*.txt
sed -i 's/oeuvre/œuvre/g' txt/fr*.txt
sed -i 's/soeur/sœur/g'   txt/fr*.txt
sed -i 's/voeu/vœu/g'     txt/fr*.txt

# drop badly encoded lines
sed -i '/½/d' txt/fr*.txt
sed -i '/؟/d' txt/fr*.txt

