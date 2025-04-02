# Talbook

tables used

user -|
       user_id
       username
       hash
       salt
       composite_key(user_id, username)

good -|
       good_id
       good_name

service -|
          service_id
          service_offer

category -|
           category_id
           good_id
           service_id
product -|
          product_id
          user_id as seller
          price

transaction -|
              product_id
              user_id

Functions that would be used

add_user_db(tuple(username, password, email))

get_user_id(username, password)

is_valid_username(username)

is_valid_password(Password)

get_id_from_email_username(input)

get_user_hash(id)

is_valid_login()

is_valid_signin()

is_valid_code()
