.PHONY: serve drop-db

serve:
	cd whosin; python server.py

drop-db:
	rm whosin/whos_in.db
