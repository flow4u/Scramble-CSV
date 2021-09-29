# Scramble CSV - real but fake

A Jupyter Notebook to scramble a CSV. When scrambled, no meaningful statistics can be performed.
It provides a good 'representative' dataset to test Extract, Transform, and Load, or for other
demonstrative purposes.

Functions:
* Can replace the key/ID with <tstxxxxxxxx>: id_column
* Can skip scrambling variables based on a list: dont_scramble
* Can remove variables based on a list: drop_variables
* Outputs a scrambled data set into a CSV

 ## Example
 Source:
 
        subjid	date_1          var_1	var_2	date_2      	skip_1	skip_2	var_3
    1	'0001'	'2021-11-01'	1	    'a'	    '2021-12-12'	'skip'	1   	a
    2	'0002'		            1					
    3	'0003'	'2021-11-02'	3	    'b'	    '2021-12-11'	'skip'	1	
    4	'0003'	'2021-11-03'	3	    'b'	    '2021-12-11'	'skip'	1   	b
    5	'0003'	'2021-11-04'	3   	'c'	    '2021-12-11'	'skip'	1   	c
    6	'0005'	'2021-11-02'	5   	'b'	    '2021-12-11'	'skip'	1   	d
    7	'0005'		            6   	'b'	    '2021-12-11'	'skip'	1   	e
    8	'0008'	'2021-11-02'	2   	'b'	    '2021-12-11'	'skip'	1   	f


Settings:
    
    input_file = './Source/test.csv'
    output_file = './Scrambled/scrambled.csv'
    id_column = 'subjid'
    dont_scramble = ['date_1', 'date_2']
    drop_variables = ['skip_1', 'skip_2']

    
Output (your results might differ due to randomness):
    
        subjid  	date_1      	var_1	var_2	date_2      	var_3
    1	tst00000003	'2021-11-01'	6   	'c' 	'2021-12-12'	c
    2	tst00000005	            	5			
    3	tst00000001	'2021-11-02'	2   	'a' 	'2021-12-11'	
    4	tst00000001	'2021-11-03'	2   	'c' 	'2021-12-11'	a
    5	tst00000001	'2021-11-04'	6   	'b' 	'2021-12-11'	f
    6	tst00000004	'2021-11-02'	6   	'c' 	'2021-12-11'	a
    7	tst00000004	            	3   	'a' 	'2021-12-11'	e
    8	tst00000002	'2021-11-02'	3   	'b' 	'2021-12-11'	d