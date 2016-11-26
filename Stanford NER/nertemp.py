import nltk
import re
from nltk.tag import StanfordNERTagger
st = StanfordNERTagger('english.nowiki.3class.caseless.distsim.crf.ser.gz')
stanford_dir = st._stanford_jar[0].rpartition('/')[0]
from nltk.internals import find_jars_within_path
stanford_jars = find_jars_within_path(stanford_dir)
st._stanford_jar = ':'.join(stanford_jars)
print "enter total number of sentences: "
n=input()
tokenizer='[, \n\r;\'\"-<>(){}\[\]/]'
while(n>0):
	sentence=raw_input()
	# words=sentence.split()
	words=re.split(tokenizer,sentence)
	# print words
	ner=st.tag(words)
	print ner
	n-=1
