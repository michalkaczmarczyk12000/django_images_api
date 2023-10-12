## How to set up
clone repository
Go to project folder
run 'docker compose up -d --build'
run 'docker compose exec web python3 manage.py migrate'
run 'docker compose exec web python3 manage.py init_tier_users'
After that you can go to admin panel 'localhost:8000/admin/' and use API