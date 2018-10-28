#!/bin/bash

echo "Creating Vocabulary....\n "

python vocab.py \
--train_src  ../storyFile.txt \
--train_tgt ../summFile.txt \
--output ./vocab_v1.bin

echo "Done.\n"

echo "train_begin"

python nmt.RL.py \
--mode RL_train \
--lr 0.0001 \
--save_to models/RL.test4 \
--cuda \
--train_src ./data/train_story \
--train_tgt ./data/train_summ \
--dev_src ./data/dev_story \
--dev_tgt ./data/dev_summ \
--test_src ./data/test_story \
--test_tgt ./data/test_summ \
--vocab vocab_v1.bin

echo "train_end."