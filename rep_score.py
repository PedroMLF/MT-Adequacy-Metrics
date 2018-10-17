import math
import argparse
import operator
import linecache
import numpy as np
from collections import Counter

################################################################################################
###                                 AUXILIARY FUNCTIONS                                      ###
################################################################################################

def create_ngram_sentence_list(sentence_list, n_grams):
    """ Returns a list of lists of n-grams for each sentence """

    n_gram_merged_sentence_list = []

    for sentence in sentence_list:
        aux_list = [tuple(sentence[ix:ix+n_grams]) for ix in range(len(sentence)-n_grams+1)]
        n_gram_merged_sentence_list.append(aux_list)

    return n_gram_merged_sentence_list


def count_repetitions(n_gram_sentence_list, threshold):
    """ Returns a list of lists with the n-grams and its respective count """

    merged_repeated_list = []

    for line in n_gram_sentence_list:
        aux_list = [tuple((k, v)) for k,v in Counter(line).items() if v > threshold]
        merged_repeated_list.append(aux_list)

    return merged_repeated_list


def n_gram_score(n_gram_reference_repeated_list, n_gram_output_repeated_list):
    """ Returns a score accordingly to repetitions of n-grams that are not present on the target.
        Only n-grams that appear in the output more than once are checked. """

    score = [0 for _ in range(len(n_gram_reference_repeated_list))]

    found = 0

    for index, (list1, list2) in enumerate(zip(n_gram_output_repeated_list, n_gram_reference_repeated_list)):

        for item1 in list1:

            #If the predicted n-gram appears more than once
            if item1[1] > 1:

                found = 0

                #If the n-gram appears in the list of output n-grams add the difference (if positive)
                for item2 in list2:
                    if item1[0] == item2[0]:
                        score[index] += max(0, item1[1]-item2[1])
                        found = 1
                        break

                #If the n-gram doesn't appear in the list of output n-grams add its count.
                if not found:
                    score[index] += item1[1]

    return score


def consecutive_words_score(n_gram_reference_repeated_list, n_gram_output_repeated_list):
    """ Returns a score for the bi-grams that are consecutive words """

    score = [0 for _ in range(len(n_gram_output_repeated_list))]
    
    found = 0

    for index, (list1, list2) in enumerate(zip(n_gram_output_repeated_list, n_gram_reference_repeated_list)):

        for item1 in list1:
            if len(set(item1[0])) == 1:
                found = 0
                for item2 in list2:
                    if len(set(item2[0])) == 1:
                        if set(item1[0]) == set(item2[0]):
                            score[index] += max(0, item1[1]-item2[1])
                            found = 1
                            break
                if not found:
                    score[index] += item1[1]

    return score


def calculate_final_scores(n_gram_scores, consecutive_scores, w1, w2):
    """ Returns a list with the final scores for a given list of n_gram and consecutive scores """

    return [w1*score1 + w2*score2 for (score1, score2) in zip(n_gram_scores, consecutive_scores)]


def calculate_number_words(references, candidate):
    """ Returns the number of words from the reference closest to the length of the prediction 
        and the number of words in the candidate sentence """

    # Calculate the number of words for each reference file
    nw_ref = list()
    for ref in references:
        nw_ref.append(sum([len(line.strip('\n').split()) for line in open(ref, 'r').readlines()]))

    # Calculate the number of words in the candidate translation
    nw_can = sum([len(line.strip('\n').split()) for line in open(candidate, 'r').readlines()])

    # Return the reference length closest to the candidate
    diff_list = [x-nw_can for x in nw_ref]
    min_ix, min_v = min(enumerate(diff_list), key=operator.itemgetter(1))

    return nw_ref[min_ix], nw_can

################################################################################################
###                                     MAIN FUNCTION                                        ###
################################################################################################

def main():

    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-n", type=int, default=2,
                        help="Provide the value of n-grams to be used")
    parser.add_argument("-w1", type=float, default=1.0,
                        help="Provide the value of lambda 1")
    parser.add_argument("-w2", type=float, default=2.0,
                        help="Provide the value of lambda 2")
    parser.add_argument("--debug", action='store_true',
                        help="After running the script creates a pdb.set_trace()")

    # Required arguments
    required = parser.add_argument_group("required arguments")
    required.add_argument("-r", "--reference", nargs='+', required=True,
                          help="Provide a list with the paths to the tokenized reference files")
    required.add_argument("-p", "--predicted", type=str, required=True,
                          help="Provide the path to the tokenized obtained translation")

    args = parser.parse_args()

    assert args.n >= 1, "n must be strictly positive"

    # Create a list with all sentences for reference and prediction
    ref_sentence_list = [ [line.split() for line in open(path, 'r')] for path in args.reference]
    pred_sentence_list = [line.split() for line in open(args.predicted, 'r')]

    assert len(ref_sentence_list[0]) == len(pred_sentence_list), \
                "Reference and predicted text files should have the same length"

    # Create list of n-grams
    n_gram_ref_sentence_list = [create_ngram_sentence_list(ref, args.n) for ref in ref_sentence_list]
    n_gram_pred_sentence_list = create_ngram_sentence_list(pred_sentence_list, args.n)

    # Create lists with the counts of repetitions of the n-grams
    n_gram_count_ref_sentence_list = [count_repetitions(ref, 0) for ref in n_gram_ref_sentence_list]
    n_gram_count_pred_sentence_list = count_repetitions(n_gram_pred_sentence_list, 0)

    # Obtain the score for n-gram counts
    all_n_gram_scores = [n_gram_score(r, n_gram_count_pred_sentence_list) for r in n_gram_count_ref_sentence_list]    
    n_gram_scores = [min(x) for x in zip(*all_n_gram_scores)]

    # Obtain repetition score for consecutive words
    if args.n == 2:
        all_consec_scores = [consecutive_words_score(r, n_gram_count_pred_sentence_list) for r in n_gram_count_ref_sentence_list]
        consec_scores = [min(x) for x in zip(*all_consec_scores)]
    # If n is not the default, then it is necessary to repeat the previous steps with n=2
    else:
        aux_n_gram_ref_sentence_list = [create_ngram_sentence_list(ref, 2) for ref in ref_sentence_list]
        aux_n_gram_pred_sentence_list = create_ngram_sentence_list(pred_sentence_list, 2)
        aux_n_gram_count_ref_sentence_list = [count_repetitions(ref, 0) for ref in aux_n_gram_ref_sentence_list]
        aux_n_gram_count_pred_sentence_list = count_repetitions(aux_n_gram_pred_sentence_list, 0)
        consec_scores = consecutive_words_score(aux_n_gram_count_ref_sentence_list, aux_n_gram_count_pred_sentence_list)

    # Calculate list with the final scores
    repetition_scores = calculate_final_scores(n_gram_scores, consec_scores, args.w1, args.w2)

    # Print the value according to the flags provided
    total_value = sum(repetition_scores)

    # Calculate the brevity penalty
    ref_length, pred_length = calculate_number_words(args.reference, args.predicted)
    pred_length_2 = sum([len(x) for x in pred_sentence_list])
    
    if pred_length < ref_length:
        bp = 1/(math.exp(1-(ref_length/pred_length)))
    else:
        bp = 1

    # Get the final score
    normalize_constant = ref_length
    if normalize_constant != 0:
        normalized_value = bp*100*float(total_value)/normalize_constant
        print("REP_SCORE: {}, BP: {:.2f}, NORMALIZED_REP_SCORE: {:.2f}".format(total_value, bp, normalized_value))
    else:
        print("No valid reference file.")
        exit(0)

    if args.debug:
        import pdb; pdb.set_trace()

if __name__== "__main__":

    main()
