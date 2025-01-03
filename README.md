# MT-Adequacy-Metrics

Adequacy issues may have different roots, such as:

* *Over-translations*, when the same source word is translated multiple times
* *Under-translations*, when some source words are erroneously unstranslated
* *Mistranslations*, when words are not correctly translated

In this repository we present two metrics that measure over and under-translations [1], updated from the ones presented in [2].

#### REP-score:

To obtain the REP-score use the rep\_score.py script.

```
>> python3 rep_score.py -r <DATA>/ro-en/newstest.en \
                        -p <DATA>/merged.prediction.en
```

Notes:

- The reference (-r) and predicted (-p) files are **merged** (without bpe applied) files.

Optional Flags:

> **--normalize**, normalizes the score with regard to the number of words in the reference

> **-n**, to change the value of _n-grams_ (default: 2)

> **-w1**, to change the multiplier lambda 1 (default: 1.0)

> **-w2**, to change the multiplier lambda 2 (default: 2.0)

> **--debug**, to create a pdb breakpoint in the end

#### DROP-score:

To obtain the DROP-score use the drop\_score.py script.

```
>> python3 drop_score.py --src_ref_align <PATH>/src_ref.align
                         --src_mt_align <PATH>/src_mt.align
                         --ref_path <PATH>/ref.txt
                         --cnd_path <PATH>/cnd.txt
```

Optional Flags:

> **--filter\_stopwords**, to exclude counts related with provided stopwords (default: False)

> **--test\_source**, provide the path to the source file (merged).

> **--stopwords\_path**, path to the stopwords file (one stopword per line)

Notes:

- The alignments are expected to follow [fast_align](https://github.com/clab/fast_align) format.
- All the provided files should be merged (without bpe applied).
- The 3 optional flags are necessary to filter stopwords.

#### Auxiliary scripts:

_**Obtain metric values for a single predictions**_:

To obtain the values for a single prediction, use the script run\_single.sh

```
>> ./run_single.sh merged_prediction test_target src_ref_align src_mt_align
```

for example,

```
>> ./run_single.sh <PATH>/merged.prediction.en <PATH>/newstest.en <PATH>/src_ref.align <PATH>/src_mt.align
```

Notes:

- The provided files should be merged (without bpe applied).
- The alignments are expected to follow [fast_align](https://github.com/clab/fast_align) format.

_**Obtain metric values for several predictions**_:

To obtain values for several predictions at once, use the script run\_several.sh.

```
>> ./run_several.sh source_language target_language test_source test_target aligner_data_path mt_predictions_path
```

for example.

```
>> ./run_several.sh ro en <PATH>/newstest.ro <PATH>/newstest.en <AlignerDataPath> <MtPredictionsPath>
```

Notes:

- The predictions files should be merged (without bpe applied).
- The aligner data file should contain the necessary files (obtained from train\_aligner.sh).

---

**References:**

[1] - tba

[2] - tba
