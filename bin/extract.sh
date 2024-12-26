#!/usr/bin/sh

mkdir -p txt
rm txt/*.txt

echo "Gutenberg..."
for corpus in corpus/gutenberg/*.txt
do
    file=$(basename $corpus)
    name=${file%.*}
    echo "...  $name"
    cp $corpus txt/$name.txt
    sed -i '/\[Illustration\]/d'                 txt/$name.txt
    sed -i '1,/START OF THE PROJECT GUTENBERG/d' txt/$name.txt
    sed -i '/END OF THE PROJECT GUTENBERG/,$d'   txt/$name.txt
    sed -i '/^End of Project Gutenberg/d'        txt/$name.txt
    sed -i '/\*       \*/d'                      txt/$name.txt
done
for file in txt/*_[1-9].txt
do
    volume=$(echo "$file" | sed 's/_[1-9].txt//g')
    cat "$file" >> "$volume".txt
    rm "$file"
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
