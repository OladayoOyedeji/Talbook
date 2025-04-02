-- File: init.sql
-- Description: Creates tables for the Talbook database

drop database if exists Talbook;
create database Talbook;
use Talbook;

--==============================================================
-- NO 1. Photo: photos for items or user profiles
--==============================================================
CREATE TABLE Photo
(
    id INT AUTO_INCREMENT PRIMARY KEY
    -- x INT, -- width of image
    -- y INT, -- height of image
) ENGINE=InnoDB;

--==============================================================
-- NO 2. User: information about users (buyers and sellers)
--==============================================================
CREATE TABLE User
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    photo_id INT, -- profile picture
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    -- state enum('MO', 'MA', ...)???
    password_hash VARCHAR(255) NOT NULL,
    descrip TEXT,
    FOREIGN KEY (photo_id) REFERENCES Photo(id)
) ENGINE=InnoDB;

--==============================================================
-- NO 3. Category: categories for items (e.g., Instruments, Audio
-- Equipment, etc.)
--==============================================================
CREATE TABLE Category
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name varchar(50) NOT NULL,
    type ENUM('good', 'service') DEFAULT 'good'
) ENGINE=InnoDB;

--==============================================================
-- NO 4. Subcategory: subcategories for categories (e.g., within the
-- category of "Instruments" you'd have "Brass Instruments",
-- "Stringed Instruments", etc.)
--==============================================================
CREATE TABLE Subcategory
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL, -- parent category
    name VARCHAR(50) NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Category(id)
) ENGINE=InnoDB;

--==============================================================
-- NO 5. Item: profiles of sale listings
--==============================================================
CREATE TABLE Item
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(300) NOT NULL,
    seller_id INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    `condition` ENUM('new', 'like new', 'very good', 'good', 'acceptable') DEFAULT NULL,
    -- quantity INT DEFAULT 1,
    descrip TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (seller_id) REFERENCES User(id)
) ENGINE=InnoDB;

--==============================================================
-- Join Table: Link Photos to Listings (Items)
--==============================================================
CREATE TABLE Item_Photo
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    photo_id INT NOT NULL,
    display_order INT NOT NULL, -- determines the order of photos
    FOREIGN KEY (item_id) REFERENCES Item(id),
    FOREIGN KEY (photo_id) REFERENCES Photo(id)
) ENGINE=InnoDB;

--==============================================================
-- Join Table: Link Categories to Listings (Items)
--==============================================================
CREATE TABLE Item_Category
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES Item(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Category(id) ON DELETE CASCADE
) ENGINE=InnoDB;

--==============================================================
-- Join Table: Link Subcategories to Listings (Items)
--==============================================================
CREATE TABLE Item_Subcategory
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    subcategory_id INT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES Item(id) ON DELETE CASCADE,
    FOREIGN KEY (subcategory_id) REFERENCES Subcategory(id) ON DELETE CASCADE
) ENGINE=InnoDB;

--==============================================================
-- NO 6. User_Preference: join table linking users to their preferenc-
--                  es. weights are used to show them diff items 
--==============================================================
CREATE TABLE User_Preference
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    subcategory_id INT NOT NULL,
    weight INT DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (subcategory_id) REFERENCES Subcategory(id)
) ENGINE=InnoDB;

--==============================================================
-- NO 7. Purchase_History: records of completed purchases
--==============================================================
CREATE TABLE Purchase_History
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    buyer_id INT NOT NULL,        
    item_id INT NOT NULL,
    quantity INT NOT NULL, -- should we have this here???
    transaction_completion_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),  
    FOREIGN KEY (buyer_id) REFERENCES User(id),
    FOREIGN KEY (item_id) REFERENCES Item(id)
) ENGINE=InnoDB;

--==============================================================
-- NO 8. Chat: links buyers and sellers for a specific item
--==============================================================
CREATE TABLE Chat
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    buyer_id INT NOT NULL,
    seller_id INT NOT NULL,
    item_id INT NOT NULL,
    FOREIGN KEY (buyer_id) REFERENCES User(id),
    FOREIGN KEY (seller_id) REFERENCES User(id),
    FOREIGN KEY (item_id) REFERENCES Item(id),
    UNIQUE (buyer_id, seller_id, item_id)
) ENGINE=InnoDB;

--==============================================================
-- NO 9. Message: messages sent within a chat (one mess to many chat)
--==============================================================
CREATE TABLE Message
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    chat_id INT NOT NULL,
    sender_id INT NOT NULL,
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (chat_id) REFERENCES Chat(id),
    FOREIGN KEY (sender_id) REFERENCES User(id)
) ENGINE=InnoDB;

--==============================================================
-- NO 10. Rating: ratings and reviews given by users
--==============================================================
CREATE TABLE Rating
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    rater_id INT NOT NULL,
    rated_user_id INT NOT NULL,
    score TINYINT CHECK (score BETWEEN 1 AND 5),
    -- comment TEXT,
    FOREIGN KEY (rater_id) REFERENCES User(id),
    FOREIGN KEY (rated_user_id) REFERENCES User(id)
) ENGINE=InnoDB;

--==============================================================
-- NO 11. Follow: relationships between users (if you follow a user,
-- you are able to find them easily, and their items are more
-- likely to be shown to you)
--==============================================================
CREATE TABLE Follow
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    follower_id INT NOT NULL,
    followed_id INT NOT NULL,
    FOREIGN KEY (follower_id) REFERENCES User(id),
    FOREIGN KEY (followed_id) REFERENCES User(id)
) ENGINE=InnoDB;
