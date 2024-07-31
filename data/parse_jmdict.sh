#!/bin/bash

sed -nr "s/<reb>(.*)<\/reb>/\1/p" JMdict_e | sort | uniq > jmdict_reading_list.txt