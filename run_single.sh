PRED=$1
REF=$2
SRC_REF_ALIGN=$3
SRC_MT_ALIGN=$4


if [ "$#" != "4" ]
then
    echo "Illegal number of parameters"
    echo "Usage:"
    echo "./run_metrics.sh merged_prediction test_target src_ref_align src_mt_align"
    echo "Example:"
    echo "./run_metrics.sh <PATH>/merged.prediction.en <PATH>/newstest.en <PATH>/src_ref.align <PATH>/src_mt.align"
    exit
fi
 
echo $(basename $PRED)

python3 rep_score.py \
        -r ${REF} \
        -p ${PRED}

python3 drop_score.py \
        --src_ref_align ${SRC_REF_ALIGN} \
        --src_mt_align ${SRC_MT_ALIGN} \
        --ref_path ${REF} \
        --cnd_path ${PRED}

