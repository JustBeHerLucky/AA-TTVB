from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest

class FrequencySummarizer:
  def __init__(self, min_cut=0.1, max_cut=0.9):
    """
     Initialize the text summarizer.
     Words that have a frequency term lower than min_cut
     or higher than max_cut will be ignored.
    """
    self._min_cut = min_cut
    self._max_cut = max_cut
    self._stopwords = set(stopwords.words('vietnamese') + list(punctuation))

  def summarize(self, text):
    """
      Return a list of n sentences
      which represent the summary of text.
    """
    sents = sent_tokenize(text)
    return " ".join(sents)
   