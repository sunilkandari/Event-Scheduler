# NER 

0.  cd PreProcess. 
1. Extract scienceie2017_train.tar.gz 
2. Create a single text file(Text.txt) by merging all the text files in scienceie2017_train/train2

	```bash
	cat scienceie2017_train/train2/*.txt > Text.txt
	```

3. Create a file(Text_filtered.txt) with all the Alphabetical words present in Text.txt
	```
	cat Train.txt | sed -nr -e "s/[^A-Za-z ]+//pg"   > Text_filtered.txt
    ```
4. Move all the *.txt* and *.ann* files from *./scienceie2017_train/train2/* to ./data/
	```
	mv ./scienceie2017_train/train2/*.txt  ./scienceie2017_train/train2/*.ann ./data/
	```
5. Run the Preprocessing.py for generating the Preprocessed data.
	```
    python Preprocessing.py
    ```
    
    The Preprocessed files are saved in ./preprocessed_data/
    
6. Merge all the files under  *./preprocessed_data/* into a single file(preprocessed.txt)
	```
	f=($(ls -1))
	for f in ${f[*]}; 
	do  
		cat $f >> preprocessed.txt; 
		echo "" >>  preprocessed.txt; 
	done
    ```
7. Generate the Glove vectors of 10 dimensions using the Text_filtered.txt. Let the output file be Text_filtered.vectors.txt
8. Do
	```
    cd ..
    ```
9. Run NER_Model.ipynb
