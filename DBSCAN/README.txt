
This folder contains
- 4 classes that perfomrs Feature Extraction (BiGrams, FrequencyVector2, DictVectorizer, BitVector)
- 4 classes that performs DBSCAN algorithm(Dbscan_Freq, Dbscan_BiGram, Dbscan_Manhattan, DbscanPCA)
- 2 classes that performs PCA (PCA_Freq, PCA_BiGram)
- 4 classes that plots K-Distcane graphs (KDistance_Freq, KDistance_BiGram, KDistance_Manhattan, KDistancePCA)
- 2 classes that evaluate clusters (Evaluate_Dbscan_Freq, Evaluate_Dbscan_BiGram)
- 1 class for expierment 3 (Evlaute_exp3)


the flow of progrmas, start with 
frequencyVector2 or BiGrams, Then KDistacne_Freq or KDistacne_BiGram (dpende on which feature set is used), after that running DBSCAN_Freq or DBSCAN_BiGram. 

The next step, includes performing PCA and running KDistancePCA, and then Dbscan algorithm.
Finally one of the evaluation classes.

All code is written in python. 
libraries such as, sklearn, numpy,  matplotlib, pandas are required.


NOTE:  the string *directory_in_str* should be modified, to where the samples.zip is included.

