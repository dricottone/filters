#!/bin/sh

tmpd="$(mktemp -d)"
trap 'rm -rf "${tmpd}"' EXIT

mkfifo "${tmpd}/f1"
rng uniform -m 5 -d 2 -n 100 \
	| tee "${tmpd}/f1" \
	| filter ab -i 100 -d 2 -a 0.2 -b 0.02 \
	| paste "${tmpd}/f1" - \
	| awk 'BEGIN{OFS="\t"; print "measurements", "estimates"} {print $1, $2}' \
	| gnuplot -p -e "set terminal dumb; set autoscale; plot '-' using 1:2 with lines notitle"

rm -rf "${tmpd}"

