README 
=================

This is the dataset annotated and used in the following paper (referred to as "WinoCoref" dataset in the paper) 
"Solving Hard Co-reference Problems", Haoruo Peng★, Daniel Khashabi★ and Dan Roth, NAACL HLT 2015.  

The original dataset is due to the following paper: 
Rahman, Altaf, and Vincent Ng. "Resolving complex cases of definite pronouns: the winograd schema challenge." EMNLP, 2012. 
and accessible here: http://www.hlt.utdallas.edu/~vince/papers/emnlp12.html 

In addition to (Rahman&Ng, 2012) dataset, this contains any additional pronouns. There are mentions which are grouped together inside mention groups. 
Therefore the annotation is for general co-reference systems, although with Winograd instances. 

The dataset is in the ACE-2004 format. For each instance there are two files. For example for instance zero there are 0.apf.xml and 0.sgm files. 
The .xml file contains the character offsets of the mentions and mention-groups, while the .sgm file contains the raw text. The field "TYPE" determines whether the mention is a 
nominal mention (or "NAM") or a pronoun (or "PRO"). As mentioned before, the "START" and "END" fields are character offsets of the mentions. 
The rest of the fields in the .xml file can be ignored. The raw text is defined inside .sgm file, between <TEXT></TEXT> tags. 
The dataset includes 1886 documents (each containing a single sentence), and altogether 6404 mentions, 2595 of which are pronouns.

Note: in the character offset defined by .xml, is counting the size of the text in all of the tags in the .sgm file (for example in between <DOCNO></DOCNO> tags). 

If you have any questions or suggestions, contact the authors.  

In case you use this dataset, please cite using the following: 
@inproceedings{PengKhRo15,
  title={Solving Hard Co-reference Problems},
  author={Peng, Haoruo and Khashabi, Daniel and Roth, Dan},
  booktitle={Conference of the North American Chapter of the Association for Computational Linguistics – Human Language Technologies},
  year={2015}
}
