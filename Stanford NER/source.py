import nltk
import re
from nltk.tag import StanfordNERTagger
st = StanfordNERTagger('english.nowiki.3class.caseless.distsim.crf.ser.gz')
stanford_dir = st._stanford_jar[0].rpartition('/')[0]
from nltk.internals import find_jars_within_path
stanford_jars = find_jars_within_path(stanford_dir)
st._stanford_jar = ':'.join(stanford_jars)
tokenizer='[, \n\r:;\'\"-<>(){}\[\]/!=]'
f=open("test.data","rb")
# f=open("t.data","rb")
f1=open("result.data","wb")
count=0
for line in f:
	# sentence=line.split(":")
	# f1.write(str(sentence[0])+" : ")
	words=re.split(tokenizer,line)
	# print words
	ner=st.tag(words)
	res=[]
	for i in range(len(ner)):
		if(ner[i][1]!='O'):
			res.append(ner[i])
	f1.write(str(res).strip('[]')+"\n")
	count+=1
	if(count==10):
		break
f1.close()