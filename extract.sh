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

echo "Leipzig..."
for corpus in corpus/leipzig/*.tar.gz
do
    file=$(basename $corpus)
    name=${file%.*.*}
    echo "...  $name"
    tar -xzf $corpus "$name"/"$name"-sentences.txt -O \
        | awk '!($1="")' > txt/"$name".txt
done
