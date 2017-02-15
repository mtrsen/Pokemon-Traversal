<<<<<<< Updated upstream
#!/bin/bash

tspFiles=`ls ./boston_test/ | grep .tsp`

for tsp_int in $tspFiles
do
	filename=`echo $tsp_int | cut -d'.' -f1`
	echo $tsp_int $filename

<<<<<<< HEAD
    # runs main file (change alg to BnB or MSTApprox etc, add cutoff time and random seed)
	python3 ./algorithms/main.py -inst ./boston_test/$tsp_int -alg MSTApprox -time 30 -seed 123456

done
=======
  # runs main file (change alg to BnB or MSTApprox etc, add cutoff time and random seed)
	python3 ./algorithms/main.py -inst ./boston_test/$tsp_int -alg MSTApprox -time 30 -seed 123456

done
>>>>>>> origin/master
=======
#!/usr/bin/env bash

for i in `seq 1 8`;
    do
        echo $i
        # runs main file (change alg to BnB or MSTApprox etc, add cutoff time and random seed
        python3 ./algorithms/main.py -inst ./tsp_all/UMissouri.tsp -alg LS1 -time 600
	done
done
>>>>>>> Stashed changes
