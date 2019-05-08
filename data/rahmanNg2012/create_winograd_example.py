import json
from nltk.tokenize import sent_tokenize, word_tokenize

def _find_mention_span(tokens, mention_toks):
    mention_len = len(mention_toks)
    span_start = None

    for i in range(0, len(tokens) - mention_len):
        cur_toks = tokens[i:i+mention_len]
        if mention_toks == cur_toks:
            span_start = i
            break
    if span_start is not None:
        return span_start, span_start + mention_len - 1
    else:
        return None, None


def read_rahman_ng(input_path, output_path, set_name="test"):
    """
    http://www.hlt.utdallas.edu/~vince/data/emnlp12/
    """
    instances = []
    with open(input_path, 'r') as fin:
        line_count = 0
        question_id = 0

        instance = None

        cur_sent = None
        cur_pronoun = None
        cur_mentions = None
        correct_mention = None

        for line in fin:
            line = line.strip()
            if not line:
                line_count = 0
            elif line_count == 0:
                instance = {}
                cur_sent = word_tokenize(line)
                line_count += 1
            elif line_count == 1:
                cur_pronoun = word_tokenize(line)
                line_count += 1
            elif line_count == 2:
                cur_mentions = [m.strip() for m in line.split(",")]
                line_count += 1
            elif line_count == 3:
                correct_mention = line
                line_count = 0

                # Make & add instance to list
                cur_mentions.remove(correct_mention)
                wrong_mention = cur_mentions[0]

                correct_mention_toks = word_tokenize(correct_mention)
                wrong_mention_toks = word_tokenize(wrong_mention)

                correct_mention_start, correct_mention_end = _find_mention_span(cur_sent, correct_mention_toks)
                wrong_mention_start, wrong_mention_end = _find_mention_span(cur_sent, wrong_mention_toks)

                pronoun_start, pronoun_end = _find_mention_span(cur_sent, cur_pronoun)

                print(correct_mention, correct_mention_start, correct_mention_end)
                print(wrong_mention, wrong_mention_start, wrong_mention_end)
                instance["id"] = "{}_{}".format(set_name, question_id)
                instance["tokens"] = cur_sent
                instance["pronoun"] = [pronoun_start, pronoun_end] # Assuming pronoun is always single token

                instance["correct_mention"] = [correct_mention_start, correct_mention_end]
                instance["wrong_mention"] = [wrong_mention_start, wrong_mention_end]

                instances.append(instance)

                # increment question id
                question_id += 1


    with open(output_path, 'w') as fout:
        json.dump(instances, fout)

def convert_winograd_to_e2e_format(dataset_path, output_path):
    """
    convert rahman and ng to .jsonline format
    :param dataset_path:
    :param output_path:
    :return:
    """
    with open(dataset_path) as fin, open(output_path, 'w') as fout:
        data = json.load(fin)

        for instance in data:
            sentences = [instance["tokens"]]
            json_inst = {
                "doc_key": "nw_{}".format(instance["id"]),
                "clusters": [[instance["correct_mention"], instance["pronoun"]], [instance["wrong_mention"]]],
                "sentences": sentences,
                "speakers": [["" for _ in sentence] for sentence in sentences],
            }

            inst_str = json.dumps(json_inst)
            fout.write(inst_str)
            fout.write('\n')


if __name__ == '__main__':
    read_rahman_ng("rahman_ng_test.txt", "rahman_ng_test.json", "test")
    convert_winograd_to_e2e_format("rahman_ng_test.json", "rahman_ng_test.jsonlines")