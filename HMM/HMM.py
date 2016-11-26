
from __future__ import division
import os, sys
import string
import numpy
import sys
import random

TAG_SET = set()
TAG_LIST = []
V = set()

transition = {}
emission = {}
context = {}


def preprocessData(in_file,labled_file,out_file):
    ftxt=open(in_file,'r')
    fann=open(labled_file,'r')
    out=open(out_file,'w')
    #Assume text file in single line.
    tagseq=[]
    txt=ftxt.readline().strip()
    words=txt.split(' ')

    #initialise tag sequence
    for word in words:
        tagseq.append([word,"None"])
    #print(tagseq)

    #read labeled file.
    lines=[line.strip() for line in fann.readlines()]
    ann_lst=[]
    for line in lines:
        fields=line.split("\t")
        if fields[0].startswith("T"):
            ann_lst.append(fields[1].split(' '))
    ann_lst.sort(key=lambda x: int(x[1]))

    #generate tag sequence using annotated sequence.
    for ann in ann_lst:
        tslice=txt[0:int(ann[1])]
        windex=tslice.count(' ')
        try:
            tslice=txt[int(ann[1]):int(ann[2])+1]
        except:
            print("\nOops!!! Couldn't process "+str(ann)+" in file : "+labled_file)
            continue
        
        cnt=tslice.strip().count(' ')
        for i in range(cnt+1):
            if ann[0]=="Material":
                if i==0:
                    if tagseq[windex+i][1]=="None":
                        tagseq[windex+i][1]=["M_B"]
                    else:
                        tagseq[windex+i][1].append("M_B")
                else:
                    if tagseq[windex+i][1]=="None":
                        tagseq[windex+i][1]=["M_I"]
                    else:
                        tagseq[windex+i][1].append("M_I")
            elif ann[0]=="Task":
                if i==0:
                    if tagseq[windex+i][1]=="None":
                        tagseq[windex+i][1]=["T_B"]
                    else:
                        tagseq[windex+i][1].append("T_B")
                else:
                    if tagseq[windex+i][1]=="None":
                        tagseq[windex+i][1]=["T_I"]
                    else:
                        tagseq[windex+i][1].append("T_I")
            elif ann[0]=="Process":
                if i==0:
                    if tagseq[windex+i][1]=="None":
                        tagseq[windex+i][1]=["P_B"]
                    else:
                        tagseq[windex+i][1].append("P_B")
                else:
                    if tagseq[windex+i][1]=="None":
                        tagseq[windex+i][1]=["P_I"]
                    else:
                        tagseq[windex+i][1].append("P_I")

    #print(tagseq)

    
    #write in output file
    out.write("<sen_BEG>"+"|"+"<sen_BEG>\n")
    for seq in tagseq:
        out.write(str(seq[0])+"|")
        if seq[1]=="None":
            out.write("None")
        else:
        	seq[1].sort()
        	out.write('_'.join(seq[1]))
        out.write("\n")
    out.write("<sen_END>|<sen_END>\n")
    out.close()
    
def training(sentences):
	global V, transition, context, emission
	for sentence in sentences:
		for word in sentence:
			V.add(word[0])
			TAG_SET.add(word[1])
	
	for sentence in sentences:
		tag_gram = ('<sen_BEG>', sentence[0][0])
		transition[tag_gram] = transition.get(tag_gram, 0) + 1		
		i = 1		
		while i < len(sentence):
			tag_gram = (sentence[i-1][1], sentence[i][1])		
			transition[tag_gram] = transition.get(tag_gram, 0) + 1
			i += 1
	
	for sentence in sentences:		
		context['<sen_BEG>'] = context.get('<sen_BEG>', 0) + 1
		for word in sentence:
			context[word[1]] = context.get(word[1], 0) + 1
	
	for sentence in sentences:
		for word in sentence:
			word_gram = (word[1], word[0])
			emission[word_gram] = emission.get(word_gram, 0) + 1
	
def laplace(ngram, dictionary, type):
	k = 0.5
	wn_0 = ngram[0]
	wn_1 = ngram[1]	
	bgram = (wn_0, wn_1)		
	if type == 0:
		total = len(TAG_SET)		
	else:
		total = len(V)
	prob = 1.0*(dictionary.get(bgram, 0) + k)/(context.get(wn_0, 0) + k*total)
	return prob

def viterbi(sentence):
	best_score = {}
	best_edge = {}
	best_score["0:<sen_BEG>"]=0
	best_edge["0:<sen_BEG>"]=None
	
	i=0
	for i in range(len(sentence)):
		for prev_tag in TAG_LIST:			
			for cur_tag in TAG_LIST:				
				if(best_score.get(str(i)+":"+prev_tag,-1)!=-1 and transition.get((prev_tag,cur_tag),-1)!=-1):					
					tag_gram = (prev_tag, cur_tag)
					trans = laplace(tag_gram,transition, 0)
					word_gram = (cur_tag,sentence[i][0])
					emit = laplace(word_gram,emission, 1)		
					score = best_score[str(i)+":"+prev_tag]+(-1*numpy.log10(trans))+(-1*numpy.log10(emit))										
					if(best_score.get(str(i+1)+":"+cur_tag,-1)==-1 or  best_score.get(str(i+1)+":"+cur_tag,-1)>score):
						best_score[str(i+1)+":"+cur_tag]=score
						best_edge[str(i+1)+":"+cur_tag]=str(i)+":"+prev_tag					
	cur_tag="<sen_END>"		
	for prev_tag in TAG_LIST:					
		if(best_score.get(str(i)+":"+prev_tag,-1)!=-1 and transition.get((prev_tag,cur_tag),-1)!=-1):					
			tag_gram = (prev_tag, cur_tag)			
			trans = laplace(tag_gram,transition, 0)			
			score = best_score[str(i)+":"+prev_tag]+(-1*numpy.log10(trans))			
			if(best_score.get(str(i+1)+":"+cur_tag,-1)==-1 or  best_score.get(str(i+1)+":"+cur_tag,-1)>score):				
				best_score[str(i+1)+":"+cur_tag]=score
				best_edge[str(i+1)+":"+cur_tag]=str(i)+":"+prev_tag								
				
	tags = []
	tags.append("<sen_END>")
	i=len(sentence)-1
	next_edge = best_edge[str(i)+":<sen_END>"]
	
	while(next_edge!="0:<sen_BEG>"):
		position= next_edge.split(":")[0]
		tag= next_edge.split(":")[1]
		tags.append(tag)
		next_edge=best_edge[next_edge]
	
	tags.reverse()	
	return tags	

if __name__=='__main__':
    files=os.listdir(sys.argv[1])
    train=[]
    test=[]
    if not os.path.exists("preprocessed_data"):
    	os.makedirs("preprocessed_data");
    for file in files:
        if file.endswith(".txt"):
            file=file[:-4]
            #print("Processing file : "+file+" status -> ",end='')
            try:
                if random.random() > 0.15:
                    train.append("preprocessed_data/"+file+".data")
                else:
                    test.append("preprocessed_data/"+file+".data")
                preprocessData("data/"+file+".txt","data/"+file+".ann","preprocessed_data/"+file+".data")
                #print("Done !!")
            except:
                print("Oops!  Something went Wrong !!")
    
    
    #reading training and test files in lists
    train_sentences=[]
    test_sentences=[]
    for i in range(len(train)):
        sentence = []
        with open(train[i], "r") as ins:        
            for line in ins:
                line=line.rstrip()
                sentence.append(line.split('|'))
        train_sentences.append(sentence)
    for i in range(len(test)):
        sentence = []
        with open(test[i], "r") as ins:
            for line in ins:
                line=line.rstrip()
                sentence.append(line.split('|'))
        test_sentences.append(sentence)
        
    #training phase
    training(train_sentences)
    
    #testing phase
    TAG_LIST = list(TAG_SET)
    for sent in test_sentences:
        for x,y in sent:
            sys.stdout.write(y+" ")
        print("\n")
        token_accuracy = 0
        
        result = viterbi(sent)
        print(' '.join(result))
        match =0
        total = len(sent)
        i=0
        for i in range(len(sent)-1):
            if (sent[i][1]==result[i]):
                match=match+1
        
        print("Accuracy : "+str((match/total)*100))
        print("\n")
    