# Talbook

A **full-stack social platform** for musicians and music enthusiasts. Built with **Flask, MySQL, HTML/CSS, and JavaScript**.

## Features
- **User profiles**: Upload music, videos, and share skills.
- **Marketplace**: Buy and sell second-hand instruments and gear.
- **Community features**: Post content, comment, and collaborate.
- **Database-backed**: Uses MySQL for managing users, listings, and media.

## Why This Project
I created Talbook to combine my interest in **web development** and **community building**.  
It also served as practice for full-stack design and REST API development.

## How to Run
```bash
git clone https://github.com/OladayoOyedeji/Talbook.git
cd Talbook
make r
```

## Tables used

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
