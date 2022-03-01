vue: frontend/src/App.vue frontend/src/components/Login.vue frontend/src/components/UserStatus.vue
	cd frontend && yarn build

nginx-config: config/nginx/nginx.conf config/nginx/mime.types
	sudo cp -r config/nginx/* /etc/nginx/

nginx: nginx-config vue
	sudo rm -r /usr/share/nginx/html
	sudo cp -r frontend/dist /usr/share/nginx/html
	sudo nginx -s reload

backend: backend/pyproject.toml
	cd backend && poetry env use python3.10 &&
	poetry install

#run: backend nginx
#
#	(bash config/.env && cd backend && poetry run python telegram.py && poetry run uvicorn api:app --port 5000)
#
#
