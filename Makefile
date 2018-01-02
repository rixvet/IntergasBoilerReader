all: sync parse graph
update: sync parse

sync:
	rsync -av 'homepi:~/INTERGAS_DATA_20*_*.csv' .
parse:
	./intergas_prestige_cw6.py parse ./INTERGAS_DATA_$$(date -d '1 month ago' '+%Y_%m').csv ./INTERGAS_DATA_$$(date '+%Y_%m').csv > values.csv	
graph:
	kst2 ./intergas.kst

