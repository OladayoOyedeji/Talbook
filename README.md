# Tallbook

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
