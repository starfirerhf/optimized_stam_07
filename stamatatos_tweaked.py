from collections import Counter

import argparse
import jsonhandler
import logging
import codecs
import os
import sys


# take a list and parse into n_grams of size n
def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])


# d0 function from stamatatos - author identification using imbalanced and limited training texts
def d0(corpus_profile, corpus_size, unknown_profile, unknown_size):
    keys = set(unknown_profile.keys()) | set(corpus_profile.keys())
    summe = 0.0
    for k in keys:
        f1 = float(corpus_profile[k]) / corpus_size
        f2 = float(unknown_profile[k]) / unknown_size
        summe = summe + (2 * (f1 - f2) / (f1 + f2)) ** 2
    return summe


# d1 function from stamatatos - author identification using imbalanced and limited training texts
def d1(corpus_profile, corpus_size, unknown_profile, unknown_size):
    keys = set(unknown_profile.keys())
    summe = 0.0
    for k in keys:
        f1 = float(corpus_profile[k]) / corpus_size
        f2 = float(unknown_profile[k]) / unknown_size
        summe = summe + (2 * (f1 - f2) / (f1 + f2)) ** 2
    return summe


# d2 function from stamatatos - author identification using imbalanced and limited training texts
def d2(corpus_profile, corpus_size, unknown_profile, unknown_size,
       norm_profile, norm_size):
    keys = set(unknown_profile.keys())
    summe = 0.0
    for k in keys:
        if corpus_size != 0 and unknown_size != 0 and norm_size != 0:
            f1 = float(corpus_profile[k]) / corpus_size
            f2 = float(unknown_profile[k]) / unknown_size
            f3 = float(norm_profile[k]) / norm_size
        elif corpus_size == 0:
            f1 = float(corpus_profile[k]) / 1
            f2 = float(unknown_profile[k]) / unknown_size
            f3 = float(norm_profile[k]) / norm_size
        elif unknown_size == 0:
            f1 = float(corpus_profile[k]) / corpus_size
            f2 = float(unknown_profile[k]) / 1
            f3 = float(norm_profile[k]) / norm_size
        else:
            f1 = float(corpus_profile[k]) / corpus_size
            f2 = float(unknown_profile[k]) / unknown_size
            f3 = float(norm_profile[k]) / 1

        summe = summe + (2 * (f1 - f2) / (f1 + f2)) ** 2 * (2 * (f2 - f3) / (f2 + f3)) ** 2
    return summe


# SPI function described by frantzeskou et al in Effective Identification of Source Code Authors Using Byte-Level Info
def SPI(corpus_profile, unknown_profile):
    return -len(set(unknown_profile.keys()) &
                set(corpus_profile.keys()))


def create_ranking(n, L, method="d1"):
    # If you want to do training:
    bigram_profile = []
    counts = []  # summ of all n-gram
    if method == "d2":
        norm_text = ''
    for cand in jsonhandler.candidates:
        text = ''
        for file in jsonhandler.trainings[cand]:
            # Get content of training file 'file' of candidate 'cand'
            # as a string with:
            text = text + jsonhandler.getTrainingText(cand, file)
        bigram_all = Counter(find_ngrams(text, n))

        counts.append(sum(bigram_all.values()))
        bigram_profile.append(Counter(dict(bigram_all.most_common(L))))
        if method == "d2":
            norm_text = norm_text + text
        text = ''
    if method == "d2":
        norm_all = Counter(find_ngrams(norm_text, n))
        norm_size = sum(norm_all.values())
        norm_profile = Counter(dict(norm_all.most_common(L)))

    # Create lists for your answers (and scores)
    authors = []
    scores = []

    for file in jsonhandler.unknowns:
        result = []
        # Get content of unknown file 'file' as a string with:
        test = ''
        test = jsonhandler.getUnknownText(file)
        # Determine author of the file, and score (optional)
        bigram_all = Counter(find_ngrams(test, n))
        counts_test = sum(bigram_all.values())
        bigram_test = Counter(dict(bigram_all.most_common(L)))

        for cand_nu in range(len(jsonhandler.candidates)):
            dissimilarity = 0
            if method == "d0":
                dissimilarity = d0(bigram_profile[cand_nu],
                                   counts[cand_nu], bigram_test, counts_test)
            elif method == "d1":
                dissimilarity = d1(bigram_profile[cand_nu],
                                   counts[cand_nu], bigram_test, counts_test)
            elif method == "d2":
                dissimilarity = d2(bigram_profile[cand_nu],
                                   counts[cand_nu], bigram_test, counts_test,
                                   norm_profile, norm_size)
            elif method == "SPI":
                dissimilarity = SPI(bigram_profile[cand_nu], bigram_test)
            else:
                raise Exception("unknown method for create_ranking")
            result.append(dissimilarity)
        print(result)
        author = jsonhandler.candidates[result.index(min(result))]

        #    author = "oneAuthor"
        score = 1
        logging.debug("%s attributed to %s", file, author)
        authors.append(author)
        scores.append(score)
        print("Author: "+author+" Score: "+str(score))
    return (authors, scores)


def create_ranking_new(n, L, method="d1"):
    # If you want to do training:
    bigram_profile = []
    counts = []  # summ of all n-gram
    if method == "d2":
        norm_text = ''
    for cand in jsonhandler.candidates:
        text = ''
        for file in jsonhandler.trainings[cand]:
            # Get content of training file 'file' of candidate 'cand'
            # as a string with:
            text = text + jsonhandler.getTrainingText(cand, file)
        bigram_all = Counter(find_ngrams(text, n))

        counts.append(sum(bigram_all.values()))
        bigram_profile.append(Counter(dict(bigram_all.most_common(L))))
        if method == "d2":
            norm_text = norm_text + text
        text = ''
    if method == "d2":
        norm_all = Counter(find_ngrams(norm_text, n))
        norm_size = sum(norm_all.values())
        norm_profile = Counter(dict(norm_all.most_common(L)))

    # Create lists for your answers (and scores)
    authors = []
    scores = []

    for file in jsonhandler.unknowns:
        result = []
        # Get content of unknown file 'file' as a string with:
        test = ''
        test = jsonhandler.getUnknownText(file)
        # Determine author of the file, and score (optional)
        bigram_all = Counter(find_ngrams(test, n))
        counts_test = sum(bigram_all.values())
        bigram_test = Counter(dict(bigram_all.most_common(L)))

        for cand_nu in range(len(jsonhandler.candidates)):
            dissimilarity = 0
            if method == "d0":
                dissimilarity = d0(bigram_profile[cand_nu],
                                   counts[cand_nu], bigram_test, counts_test)
            elif method == "d1":
                dissimilarity = d1(bigram_profile[cand_nu],
                                   counts[cand_nu], bigram_test, counts_test)
            elif method == "d2":
                dissimilarity = d2(bigram_profile[cand_nu],
                                   counts[cand_nu], bigram_test, counts_test,
                                   norm_profile, norm_size)
            elif method == "SPI":
                dissimilarity = SPI(bigram_profile[cand_nu], bigram_test)
            else:
                raise Exception("unknown method for create_ranking")
            result.append(dissimilarity)
        # print(result)
        author = jsonhandler.candidates[result.index(min(result))]

        #    author = "oneAuthor"
        score = 1
        logging.debug("%s attributed to %s", file, author)
        authors.append(author)
        scores.append(score)
        try:
            print("Author: "+author+" Score: "+str(score))
        except UnicodeEncodeError:
            try:
                print("Author: " + author + " Score: " + str(score).encode('utf8').decode(sys.stdout.encoding))
            except UnicodeEncodeError:
                print("Author: error Score: " + str(score))
    # adding to evaluate accuracy - RF
    jsonhandler.loadGroundTruth()
    logging.info("Test parameters: n=%d, l=%d", n, L)
    evaluation = evalTesting(jsonhandler.unknowns, authors)
    print(evaluation)
    return (authors, scores)


# evaluation of various parameters for the algorithms
def fit_parameters():
    # n_gram lengths
    n_range = [3, 4, 5, 6]
    # profile lengths
    L_range = [500, 1000, 2000, 3000, 5000]
    #    n_range = [2,3]
    #    L_range = [20, 50, 100]
    # load the ground truth for the test set
    jsonhandler.loadGroundTruth()
    results = []
    for n in n_range:
        for L in L_range:
            logging.info("Test parameters: n=%d, l=%d", n, L)
            authors, scores = create_ranking(n, L)
            evaluation = evalTesting(jsonhandler.unknowns, authors)
            results.append((evaluation["accuracy"], n, L))
    return results


def evalTesting(texts, cands, scores=None):
    succ = 0
    fail = 0
    sucscore = 0
    failscore = 0
    for i in range(len(texts)):
        if jsonhandler.trueAuthors[i] == cands[i]:
            succ += 1
            if scores != None:
                sucscore += scores[i]
        else:
            fail += 1
            if scores != None:
                failscore += scores[i]
    result = {"fail": fail, "success": succ, "accuracy":
        succ / float(succ + fail)}
    return result


def optimize(corpusdir, outputdir):
    parameters = fit_parameters()
    acc, n, L = max(parameters, key=lambda r: r[0])
    logging.info("Choose parameters: n=%d, l=%d", n, L)
    logging.disable(logging.DEBUG)
    authors, scores = create_ranking(n, L)
    jsonhandler.storeJson(outputdir, jsonhandler.unknowns, authors, scores)


# def test_method(corpusdir, outputdir, method="d1", n=3, L=2000):
def test_method(corpusdir, outputdir, method="d2", n=5, L=2000):
    logging.info("Test method %s with L=%d", method, L)
    authors, scores = create_ranking(n, L, method)
    jsonhandler.storeJson(outputdir, jsonhandler.unknowns, authors, scores)


# def test_method(corpusdir, outputdir, method="d1", n=3, L=2000):
def test_method_new(corpusdir, outputdir, method="d2", n=5, L=2000):
    logging.info("Test method %s with L=%d", method, L)
    authors, scores = create_ranking_new(n, L, method)
    jsonhandler.storeJson(outputdir, jsonhandler.unknowns, authors, scores)


def compare_methods(corpusdir, outputdir):
    n = 3
    logging.disable(logging.DEBUG)
    for L in range(500, 10500, 500):
        for m in ["d0", "d1", "d2", "SPI"]:
            test_method(corpusdir, outputdir, method=m, n=n, L=L)


def compare_methods_new(corpusdir, outputdir):
    n = 3
    logging.disable(logging.DEBUG)
    for L in range(500, 10500, 500):
        for m in ["d0", "d1", "d2", "SPI"]:
            test_method_new(corpusdir, outputdir, method=m, n=n, L=L)


# proposed method for finding L parameter for Stamatatos algorithm
# take training files, combine into one corpus per author
# divide into n-grams (currently 5-grams)
# find average number of n-grams for all authors
# divide by 4 to get top 25%
# return the L value of top 25% of average number of n-grams of all authors
def getTrainingMax(corpusdir,n):
    train_grams = []
    for cand in jsonhandler.candidates:
        text = ''
        for file in jsonhandler.trainings[cand]:
            # Get content of training file 'file' of candidate 'cand'
            # as a string with:
            text = text + jsonhandler.getTrainingText(cand, file)
        bigram_all = Counter(find_ngrams(text, n))
        try:
            print(cand)
        except UnicodeEncodeError:
            print(cand.encode('utf8').decode(sys.stdout.encoding))
        print('Number of {}-grams: {}'.format(n,len(bigram_all)))
        train_grams.append(len(bigram_all))
    #change the divided by number to get top percentages e.g. /10 = top 10% - remove divisor for raw average
    recommended_L = int((sum(train_grams)/len(train_grams))/4)
#    recommended_L = int((sum(train_grams)/len(train_grams)))
    print('Recommended L size: {}'.format(recommended_L))
    return (recommended_L)
#    for cand in jsonhandler.candidates:
#        cand_chars = 0
#        for file in jsonhandler.trainings[cand]:
#            lines = words = chars = 0
#            with open(os.path.join(corpusdir, cand, file), 'r') as in_file:
#                for line in in_file:
#                    lines += 1
#                    words += len(line.split())
#                    chars += len(line)
#            print(os.path.join(cand, file))
#            print("lines: {}, words: {}, chars: {}".format(lines, words, chars))
#            cand_chars += chars
#        print(cand + " total: " + str(cand_chars))
#        train_chars.append(cand_chars)
#    return(max(train_chars), int(sum(train_chars)/len(train_chars)))


def main():
    parser = argparse.ArgumentParser(description='Tira submission for' +
                                                 ' "Author identification using imbalanced and limited training texts."')
    parser.add_argument('-i',
                        action='store',
                        help='Path to input directory')
    parser.add_argument('-o',
                        action='store',
                        help='Path to output directory')

    args = vars(parser.parse_args())

    corpusdir = args['i']
    outputdir = args['o']

    jsonhandler.loadJson(corpusdir)
    jsonhandler.loadTraining()
    # max_profile_len = avg_profile_len = 0

    # test_method(corpusdir, outputdir)
    # compare_methods(corpusdir, outputdir)
    # optimize(corpusdir, outputdir)
    # optimize_new(corpusdir, outputdir)

    n=5
    recommended_L = getTrainingMax(corpusdir,n)
#    print('Maximum training profile length: {}'.format(max_profile_len))
#    print('Average training profile length: {}'.format(avg_profile_len))
    print('Recommended L: {}'.format(recommended_L))
    test_method_new(corpusdir, outputdir,method='d2', n=5, L=recommended_L)

if __name__ == "__main__":
    # execute only if run as a script
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s')
    main()
