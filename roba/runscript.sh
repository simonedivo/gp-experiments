cp -r ${SINGULARITY_ROOTFS}/../../GP-GOMEA ./
cp -r ${SINGULARITY_ROOTFS}/../../gp-experiments ./

cd GP-GOMEA
GEN=ninja
echo ">>> Compiling GP-GOMEA source code..." && make
cd ..

cd gp-experiments
./remnants_ulysses/execute_parallel_ulysses.sh 30 ./remnants_ulysses/remnants.txt
