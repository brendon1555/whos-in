.PHONY: serve drop-db

serve:
	cd whos_in; python server.py

drop-db:
	rm whos_in/whos_in.db