#!/bin/bash

curl -O http://lil.cs.washington.edu/coref/char_vocab.english.txt

ckpt_file=c2f_final.tgz
curl -O http://lil.cs.washington.edu/coref/$ckpt_file
mkdir -p logs
tar -xzvf $ckpt_file -C logs
rm $ckpt_file
