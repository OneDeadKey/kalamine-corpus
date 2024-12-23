#!/usr/bin/sh

mkdir -p txt

echo "Gutenberg..."
for corpus in corpus/gutenberg/*.txt
do
    file=$(basename $corpus)
    name=${file%.*}
    echo "...  $name"
    cp $corpus txt/$name.txt
done
sed -i '/\[Illustration\]/d'  txt/*.txt
sed -i '1,/START/d' txt/*.txt
sed -i '/END OF THE PROJECT GUTENBERG/,$d' txt/*.txt
sed -i '/^End of Project Gutenberg/d' txt/*.txt
sed -i '/\*       \*/d' txt/*.txt 
for f in txt/*-[1-9].txt
do
    volume=$(echo "$f" | sed 's/-[1-9].txt//g');
    cat "$volume"-[1-9].txt > "$volume".txt
done
if [ -f "$volume".txt ]
then
    rm "$volume"-[1-9].txt
fi

echo "Leipzig..."
for corpus in corpus/leipzig/*.tar.gz
do
    file=$(basename $corpus)
    name=${file%.*.*}
    echo "...  $name"
    tar -xzf $corpus "$name"/"$name"-sentences.txt -O \
        | awk '!($1="")' > txt/"$name".txt
done

