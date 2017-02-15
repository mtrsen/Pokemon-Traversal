#!/usr/bin/env bash

for i in `seq 1 8`;
    do
        echo $i
        # runs main file (change alg to BnB or MSTApprox etc, add cutoff time and random seed
        python3 ./algorithms/main.py -inst ./tsp_all/UKansasState.tsp -alg LS1 -time 600
	done
done