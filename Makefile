all: sync parse graph
update: sync parse

sync:
	rsync -av 'homepi:~/INTERGAS_DATA_2017_1*.csv' .
parse:
	./intergas_prestige_cw6.py parse ./INTERGAS_DATA_2017_12.csv > values.csv	
graph:
	kst2 ./intergas.kst

