import spacy
from spacy import displacy
from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_sm')
# for rule based matching
matcher = Matcher(nlp.vocab)
# this is the message text
message_text = "Dear Customer, Your 110##01978 has been withdrawn debited credited deposited by NPR 100.00 on 08/Jan/2022 " \
               "21:00:32, Remarks: MPAY " \
               "9861168873 " \
               "Activate bit.ly/2U2dzlO for a/c balance "
# Variable name ending with the suffix _doc are spaCy’s language model objects.
message_doc = nlp(message_text)


def extract_date(nlp_doc):
    pattern = [[{'TEXT': {'REGEX': r'^\d{1,2}/\d{1,2}/\d{2}(?:\d{2})?$'}}]]
    pattern2 = [[{'TEXT': {'REGEX': r'^\d{1,2}/[a-zA-Z]+/\d{2}(?:\d{2})?$'}}]]
    matcher.add('DATE', pattern2)
    matches = matcher(nlp_doc)
    for match_id, start, end in matches:
        span = nlp_doc[start:end]
        return span.text


Date = extract_date(message_doc)
#print(Date)

sentences = list(message_doc.sents)
# this is used as . as sentence delimiter . le chaii sentences haru xuttaidinxa(sentence detection)
for sentence in sentences:
    singleSentence = sentence
# identify the basic units in text =>breaks texts into meaningful units ,these are used for POS(tokenization)
for token in message_doc:
    singleToken = token
# stop words are removed because they aren’t significant and distort the word frequency analysis(Stop Words Removal)
for singleToken in message_doc:
    if not singleToken.is_stop:
        tokenAfterStopWord = singleToken
        # print(tokenAfterStopWord)
# this prints tokens in list after removing stop word
about_no_stopword_doc = [token for token in message_doc if not token.is_stop]
# this find the root word of the text message tokens like withdraw for withdrawn
for token in about_no_stopword_doc:
    tokenAfterLemma = token.lemma_
    # print(tokenAfterLemma)
# this prints token list after lemmentization
after_lemma_doc = [token for token in about_no_stopword_doc if token.lemma_]
# print(after_lemma_doc)
words = [token.text for token in after_lemma_doc
         if not token.is_stop and not token.is_punct]
# print(words)
# for token in after_lemma_doc:
# print(token, token.tag_, token.pos_, spacy.explain(token.tag_))
# this does the POS tagging of tokens (Part of Speech Tagging)
nouns = []
verbs = []
for token in after_lemma_doc:
    if token.pos_ == 'NOUN':
        nouns.append(token)
    if token.pos_ == 'VERB':
        verbs.append(token)
# print(nouns)
print(verbs)  # this prints the tokens like debited withdrawn deposited credited
# displacy.serve(message_doc, style='dep') # to visualize POS in browser http://127.0.0.1:5000/
"""
        Only allow valid tokens which are not stop words
       and punctuation symbols.
   """


def is_token_allowed(token):
    if not token or token.is_stop or token.is_punct:
        return False
    return True


def preprocess_token(token):
    # Reduce token to its lowercase lemma form
    return token.lemma_.strip().lower()


complete_filtered_tokens = [preprocess_token(token) for token in message_doc if is_token_allowed(token)]
print(complete_filtered_tokens)


# to extract phone number
def extract_amount(nlp_doc):
    pattern = [[{'POS': 'NUM'}]]
    matcher.add('Amount', pattern)
    matches = matcher(nlp_doc)
    for match_id, start, end in matches:
        span = nlp_doc[start:end]
        return span.text


Amount = extract_amount(message_doc)
print(Amount)
