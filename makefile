.ONESHELL:
run:
	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
	export FLASK_APP=flask_app.py
	export FLASK_ENV=development
	firefox localhost:5000 &
	flask --app flask_app.py --debug run

init_sql i:
	mysql --user=root --password=root < app/db/init.sql;
	mysql --user=root --password=root < app/db/Tag.sql
	python -m app.db.User;
	mysql --user=root --password=root < app/db/User.sql;
	mysql --user=root --password=root < app/db/Item.sql;

git g:
	git add .
	git commit -m 'sync'
	git push

phpmyadmin p:
	bash -c 'systemctl start httpd.service && apachectl start';
	xdg-open http://localhost/phpmyadmin

reset_venv r:
	rm -rf venv
	python3 -m venv venv
	source venv/bin/activate
	python -m ensurepip
	pip install --upgrade pip
	pip install -r requirements.txt

