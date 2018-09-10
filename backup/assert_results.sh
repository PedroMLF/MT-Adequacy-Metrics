END=8
SCORES="3.37 3.47 2.93 3.18 3.24 3.13 3.29 2.67"
for i in $(seq 1 ${END}); do
    export result=`python3 rep_score.py -r tests/test.en \
                                        -p tests/test_${i} \
                                        --normalize`
    r=`echo ${result} | cut -d: -f3 | cut -d' ' -f2`
    v=`echo ${SCORES} | cut -d' ' -f${i}`
    c=`echo "${r} == ${v}" | bc`
    if [ ${c} == 1 ]; then
        echo "Test ${i} passed"
    else
        echo "Test ${i} failed"
        exit
    fi
done            
