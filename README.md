# dada2_to_qiime
Convert DADA2 Seqtabs to QIIME files

## Instructions
After creating your bimeric filtered seqtab in DADA2, write it out to a CSV
```
seqtab.nochim <- removeBimeraDenovo(seqtab, verbose=TRUE, multithread=TRUE)
write.csv(seqtab.nochim, file = "seqtab.nochim.csv")
```

Next run the `dada2_to_qiime.py` script
```
dada2_to_qiime.py -i seqtab.nochim.csv
```
This will create:
* **seqtab.nochim.otutable**
* **seqtab.nochim.repset**
* **dada_to_qiime.sh**

### Outputs explained

**seqtab.nochim.otutable**  
A transposed version of the `seqtab.nochim.csv` with each fill length sequence variant replaced with a simple numerical notation, i.e. `node1`

**seqtab.nochim.repset**  
A mapping between the numerical notations and the actual sequence variants

**dada_to_qiime.sh**  
A shell script that will
* Build a tree
* Assign taxonomy
* Create a biom
* Create a new level of taxa for looking at sequence variants
