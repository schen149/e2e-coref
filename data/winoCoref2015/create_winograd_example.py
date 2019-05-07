import json
from nltk.tokenize import sent_tokenize, word_tokenize
import numpy as np

test_train_split = {}
sentences = {}
documents = []

def char_to_token_offset_extractor(tokens, sentence):
    offset = 0
    spans = []
    for token in tokens:
        offset = sentence.find(token, offset)
        spans.append([offset, offset + len(token)])
        offset += len(token)

    char_to_word_offset = {}
    for tokenIdx, (char_start, char_end) in enumerate(spans):
        # print(tokenIdx)
        for i in np.arange(char_start, char_end+1):
            char_to_word_offset[i] = tokenIdx

    return char_to_word_offset

def normalize_mention(mention):
    return mention.strip().replace("&apos;", "'").replace("&amp;", "&").replace("&quot;", "\"")

def read_rahman_ng(directory):
    # first read train-test splits
    with open(directory + 'test.txt') as file:
        for l in file.readlines():
            file_name = l.split(".apf.xml")[0]
            test_train_split[file_name] = "test"

    with open(directory + 'train.txt') as file:
        for l in file.readlines():
            file_name = l.split(".apf.xml")[0]
            test_train_split[file_name] = "train"

    # read the sentences
    with open(directory + 'sentences.tsv') as file:
        for l in file.readlines():
            lsplit = l.split("\t")
            sentences[lsplit[0]] = lsplit[1].replace("\n", "")

    # read the original questions
    vicnent_annotations = {}
    with open(directory + 'emnlp2012-original-dataset.tsv') as file:
        for l in file.readlines():
            lsplit = l.split("\t")
            vicnent_annotations[lsplit[0].strip()] = lsplit

    total_documents = 0
    total_mentions = 0
    total_pronouns = 0

    instances_train = []
    instances_test = []

    # read the annotations
    with open(directory + 'data.json') as file:
        file_json = json.load(file)
        for f in file_json['content']['document']:
            total_documents += 1

            instance = {}
            docid = f['DOCID']
            instance["doc_key"] = docid
            instance["sentences"] = []
            instance["clusters"] = []
            instance["clusters_info"] = []

            sentence = sentences[docid]
            # print(sentence)
            tokens = word_tokenize(sentence)
            instance["sentences"].append(tokens)
            instance["speakers"] = [["" for _ in tokens]]

            char_to_word_offset = char_to_token_offset_extractor(tokens, sentence)

            # print(char_to_word_offset)

            for e in f['entity']:
                cluster_info = {}
                cluster_info["entity_mentions"] = []
                cluster = []
                if isinstance(e['entity_mention'], dict):
                    e['entity_mention'] = [e['entity_mention']]
                for em in e['entity_mention']:
                    em_info = {}
                    em_info["type"] = em['TYPE']
                    em_info["ID"] = em['ID']
                    if em['TYPE'] == "PRO":
                        total_pronouns += 1
                    total_mentions += 1
                    char_start = int(em['extent']['charseq']['START']) - 9 - len(docid)
                    char_end = int(em['extent']['charseq']['END']) - 8 - len(docid)
                    content = em['extent']['charseq']['content']
                    sub_string = normalize_mention(sentence[char_start:char_end])
                    assert sub_string == content, f"expected {content}, but found {sub_string}"
                    if sub_string != content:
                        print(f"*** ERROR: expected '{content}', but found '{sub_string}'")
                    is_main_pronoun = False
                    if content == vicnent_annotations[normalize_mention(sentence)][1]:
                        is_main_pronoun = True
                    em_info["is_main_pronoun"] = is_main_pronoun
                    em_info["content"] = content
                    em_info["char_start"] = char_start
                    em_info["char_end"] = char_end
                    cluster_info["entity_mentions"].append(em_info)
                    token_start = char_to_word_offset[char_start]
                    token_end = char_to_word_offset[char_end]
                    cluster.append([token_start, token_end])
                cluster_info['eId'] = e['ID']
                instance["clusters"].append(cluster)
                instance["clusters_info"].append(cluster_info)

            # if total_documents % 2 == 0:
            #     instance["clusters"].reverse()  # reverse the order of the entities, so that the algorithms can't use this bias.
            #     instance["clusters_info"].reverse()
            is_test = (test_train_split[docid] == "test")
            if is_test:
                instances_test.append(instance)
            else:
                instances_train.append(instance)

    print("**********")
    print(f"Total documents: {total_documents}")
    print(f"Total mentions: {total_mentions}")
    print(f"Total pronouns: {total_pronouns}")
    avg_pronouns = total_pronouns / total_documents
    avg_mentions = total_mentions / total_documents
    print(f"Total pronouns / document: {avg_pronouns}")
    print(f"Total mentions / document: {avg_mentions}")

    with open(directory + "winocoref_test_lee18_format.json", 'w') as fout:
        json.dump(instances_test, fout)

    with open(directory + "winocoref_train_lee18_format.json", 'w') as fout:
        json.dump(instances_train, fout)

if __name__ == '__main__':
    read_rahman_ng("/Users/daniel/ideaProjects/e2e-coref/data/winoCoref2015/")