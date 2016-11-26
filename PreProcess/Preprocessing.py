import os

def preprocessData(in_file,labled_file,out_file):
    ftxt=open(in_file,'r')
    fann=open(labled_file,'r')
    out=open(out_file,'w+')
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
    for seq in tagseq:
        out.write(str(seq[0])+"\t")
        if seq[1]=="None":
            out.write("None")
        else:
            for cls in seq[1]:
                out.write(str(cls)+" ")

        out.write("\n")
    out.close()


if __name__=='__main__':

    files=os.listdir("./data/")
    for file in files:
        if file.endswith(".txt"):
            file=file[:-4]
            print file
            print("Processing file : "+file+" status -> ")
            try:
                preprocessData("./data/"+file+".txt","./data/"+file+".ann","./preprocessed_data/"+file+".data")
                print("Done !!")
            except:
                print("Oops!  Something went Wrong !!")
            