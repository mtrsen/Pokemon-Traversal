#!/bin/bash

<<<<<<< Updated upstream
# runs all of the files
tspfiles =`ls ./tsp_all/ | grep .tsp`
=======

tspFiles=`ls ./tsp_all/ | grep .tsp`
>>>>>>> Stashed changes

for tsp in $tspfiles
do
<<<<<<< Updated upstream
	filename=`echo $tsp | cut -d'.' -f1`
	echo $tsp $filename

    # runs main file (change alg to BnB or MSTApprox etc, add cutoff time and random seed)
	python main.py -inst ./tsp_all/$tsp -alg MSTApprox -time <cutoff time>  -seed <random seed>

=======
    filename=`echo $tsp_int | cut -d'.' -f1`
    echo $tsp_int $filename

    for i in `seq 1 10`;
        do
            echo $i
            # runs main file (change alg to BnB or MSTApprox etc, add cutoff time and random seed)
            python3 ./algorithms/main.py -inst ./tsp_all/$tsp_int -alg LS1 -time 600
        done
    done
>>>>>>> Stashed changes
done