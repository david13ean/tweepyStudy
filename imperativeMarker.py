# https://stackoverflow.com/questions/29473169/approach-for-identifying-whether-a-sentence-includes-an-imperative-within-it
# Credit to stackoverflow user nischi for the bulk of this script

from nltk import RegexpParser
from nltk.tree import Tree

def is_imperative(tagged_sent):
    # if the sentence is not a question...
    if tagged_sent[-1][0] != "?":
        # catches simple imperatives, e.g. "Open the pod bay doors, HAL!"
        if tagged_sent[0][1] == "VB" or tagged_sent[0][1] == "MD":
            return True

        # catches imperative sentences starting with words like 'please', 'you',...
        # E.g. "Dave, stop.", "Just take a stress pill and think things over."
        else:
            chunk = get_chunks(tagged_sent)
            # check if the first chunk of the sentence is a VB-Phrase
            if type(chunk[0]) is Tree and chunk[0].label() == "VB-Phrase":
                return True

    # Questions can be imperatives too, let's check if this one is
    else:
        # check if sentence contains the word 'please'
        pls = len([w for w in tagged_sent if w[0].lower() == "please"]) > 0
        # catches requests disguised as questions
        # e.g. "Open the doors, HAL, please?"
        chunk = get_chunks(tagged_sent)
        if pls and (tagged_sent[0][1] == "VB" or tagged_sent[0][1] == "MD"):
            return True

        # catches imperatives ending with a Question tag
        # and starting with a verb in base form, e.g. "Stop it, will you?"
        elif type(chunk[-1]) is Tree and chunk[-1].label() == "Q-Tag":
            if (chunk[0][1] == "VB" or
                (type(chunk[0]) is Tree and chunk[0].label() == "VB-Phrase")):
                return True
    
    return False

# chunks the sentence into grammatical phrases based on its POS-tags
def get_chunks(tagged_sent):
    chunkgram = r"""VB-Phrase: {<DT><,>*<VB>}
                    VB-Phrase: {<RB><VB>}
                    VB-Phrase: {<UH><,>*<VB>}
                    VB-Phrase: {<UH><,><VBP>}
                    VB-Phrase: {<PRP><VB>}
                    VB-Phrase: {<NN.?>+<,>*<VB>}
                    Q-Tag: {<,><MD><RB>*<PRP><.>*}"""
    chunkparser = RegexpParser(chunkgram)
    return chunkparser.parse(tagged_sent)