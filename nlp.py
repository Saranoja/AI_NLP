from unidecode import unidecode
import json
import re


def output_probabilities(input_file, output_file):
    with open("stopwords-ro.txt") as file:
        stopwords_with_accents = file.read().split("\n")
        # strip accents
        stopwords = set(map(lambda word: unidecode(word), stopwords_with_accents))

    word_tokenizer = re.compile("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+")
    with open(input_file) as file:
        corpus_non_lowered = word_tokenizer.findall(file.read())
        corpus_not_diacritics_stripped = map(lambda word: word.lower(), corpus_non_lowered)
        corpus_with_stopwords = map(lambda word: unidecode(word), corpus_not_diacritics_stripped)
        corpus = list(filter(lambda word: word not in stopwords, corpus_with_stopwords))

    no_of_words = len(corpus)
    occurrences = {}
    for word in corpus:
        if occurrences.get(word) is None:
            occurrences[word] = 1
        else:
            occurrences[word] += 1
    # print(sorted(occurrences.items(), key=lambda k: k[1]))

    probabilities = {}
    for word, occurrence in occurrences.items():
        probabilities[word] = (occurrence / no_of_words) * 1000000

    with open(output_file, "w") as file:
        probabilities_json = json.dumps(probabilities, indent=2)
        file.write(probabilities_json)

    return no_of_words


no_of_words1 = output_probabilities("lucian_blaga_poemele_luminii.txt", "probabilities_lucian_blaga_poemele_luminii.json")
no_of_words2 = output_probabilities("eminescu_poezii.txt", "probabilities_eminescu_poezii.json")

def calculate_similarity(path_to_json1, path_to_json2):
    with open(path_to_json1) as json1:
        probabilities1 = json.load(json1)

    with open(path_to_json2) as json2:
        probabilities2 = json.load(json2)

    score = 0.0
    for word1 in probabilities1.keys():
        if word1 in probabilities2.keys():
            score += abs(probabilities1.get(word1) - probabilities2.get(word1))
        else:
            score += abs(probabilities1.get(word1) - 0)

    print(f'Similarity = {score}')
    print(f'Similarity / no_of_words = {score/no_of_words2}')


calculate_similarity("probabilities_lucian_blaga_poemele_luminii.json",
                     "./probabilities_eminescu_poezii.json")
