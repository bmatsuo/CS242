#!/bin/bash
datadir="ex2_data"

if [[ -d $datadir ]]; then
    echo "Experiment outdir $datadir already exists." 2>&1
    exit 1
fi

mkdir $datadir

cleantest="$datadir/test-clean.txt"
./genset.py -n 100 > $cleantest
noisytest="$datadir/test-noisy.txt"
./genset.py -n 100 --noisy > $noisytest

for i in {1..20}; do
    echo "Beginning experiment iteration $i"
    train="$datadir/$i-train.txt"
    ./genset.py -n 100 > $train
    cleanpred_prefix="$datadir/$i-clean"
    noisypred_prefix="$datadir/$i-noisy"
    for rule in "last" "voted" "longest" "last50" ; do
        cleanpred="$cleanpred_prefix-$rule.txt"
        ./Perceptron.py -S500 --rule=$rule "$train" "$cleantest" > $cleanpred
        noisypred="$noisypred_prefix-$rule.txt"
        ./Perceptron.py -S500 --rule=$rule "$train" "$noisytest" > $noisypred
    done
done

