rm db.sqlite3 
rm -rf ./BeautyBarterAPI/migrations 
python3 manage.py migrate 
python3 manage.py makemigrations BeautyBarterAPI 
python3 manage.py migrate BeautyBarterAPI 
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata admins
python3 manage.py loaddata professions
python3 manage.py loaddata license_states
# python3 manage.py loaddata notification_type
# python3 manage.py loaddata member
# python3 manage.py loaddata notification
# python3 manage.py loaddata message
# python3 manage.py loaddata service 
# python3 manage.py loaddata product_type
# python3 manage.py loaddata product
# python3 manage.py loaddata license_check
# python3 manage.py loaddata barter
# python3 manage.py loaddata potential_barter
# python3 manage.py loaddata barter_product