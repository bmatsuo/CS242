#!/bin/bash
datadir="ex1_data"

if [[ -d $datadir ]]; then
    echo "Experiment outdir $datadir already exists." 2>&1
    exit 1
fi

mkdir $datadir

for i in {1..100}; do
    train="$datadir/$i-clean.txt"
    ./genset.py -n 50 > $train
    gap=`./gap.py "$train"`
    summ=`./Perceptron.py -cts "$train" \
            | head -n 2 \
            | tail -n 1 \
            | awk '{print $2 " " $3}'`
    echo "$train $gap $summ" >> "$datadir/ex1.out"
done
