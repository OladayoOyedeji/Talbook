-- File: init.sql
-- Description: Creates tables for the Talbook database

drop database if exists Talbook;
create database Talbook
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
use Talbook;

--==============================================================
-- NO 1. Photo: pngs for items or posts
--==============================================================
CREATE TABLE Photo
(
    id INT AUTO_INCREMENT PRIMARY KEY
) ENGINE=InnoDB;

--==============================================================
-- Video: mp4s for items or posts
--==============================================================
CREATE TABLE Video
(
    id INT AUTO_INCREMENT PRIMARY KEY
) ENGINE=InnoDB;

--==============================================================
-- NO 2. User: information about users (buyers and sellers)
--==============================================================
CREATE TABLE User
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    photo_id INT default NULL, -- profile picture
    username VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci UNIQUE NOT NULL,
    email VARCHAR(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci UNIQUE NOT NULL,
    -- state enum('MO', 'MA', ...)???
    password_hash VARCHAR(255) NOT NULL,
    descrip TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    FOREIGN KEY (photo_id) REFERENCES Photo(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--==============================================================
-- Tag: User Specified Categories
--==============================================================
CREATE TABLE Tag
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci UNIQUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--==============================================================
-- Tag: User Specified Categories
--==============================================================
CREATE TABLE Service
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    skills VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci UNIQUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE User_Service
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    service_id INT,
    FOREIGN KEY(user_id) REFERENCES User(id),
    FOREIGN KEY(service_id) REFERENCES Service(id)
) ENGINE=InnoDB;

--==============================================================
-- NO 5. Item: Profiles of sale listings
--==============================================================
CREATE TABLE Item
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(300) NOT NULL,
    seller_id INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    `condition` ENUM('new', 'like new', 'very good', 'good', 'acceptable', 'poor') DEFAULT NULL,
    descrip TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    is_available BOOLEAN DEFAULT True, 
    FOREIGN KEY (seller_id) REFERENCES User(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
-- Join Table: Link Tags to Listings (Items)
--==============================================================
CREATE TABLE Item_Tag
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    tag_id INT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES Item(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES Tag(id) ON DELETE CASCADE
) ENGINE=InnoDB;

--==============================================================
-- NO 6. User_Preference: join table linking users to their preferenc-
--                  es. weights are used to show them diff items 
--==============================================================
CREATE TABLE User_Preference
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    tag_id INT NOT NULL,
    weight INT DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (tag_id) REFERENCES Tag(id)
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

CREATE TABLE Location
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    state CHAR(2) NOT NULL,
    INDEX idx_city_state (city, state)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Item_Location
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT,
    location_id INT,
    FOREIGN KEY(item_id) REFERENCES Item(id),
    FOREIGN KEY(location_id) REFERENCES Location(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--==============================================================
-- Post: A post in the media tab of the user profile
--==============================================================
CREATE TABLE Post
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    descrip TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--==============================================================
-- Post_Photo: Join table linking one post to many photos
--==============================================================
CREATE TABLE Post_Photo
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    media_id INT,
    display_order INT,
    FOREIGN KEY(media_id) REFERENCES Photo(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--==============================================================
-- Post_Video: Join table linking one post to many videos
--==============================================================
CREATE TABLE Post_Video
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    media_id INT,
    display_order INT,
    FOREIGN KEY(media_id) REFERENCES Photo(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--==============================================================
-- Chat: a chatroom for an item listing
--==============================================================
CREATE TABLE Chat (
    id INT AUTO_INCREMENT PRIMARY KEY,
    buyer_id INT NOT NULL,
    seller_id INT NOT NULL,
    item_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id) REFERENCES User(id),
    FOREIGN KEY (seller_id) REFERENCES User(id),
    FOREIGN KEY (item_id) REFERENCES Item(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--==============================================================
-- Message: individual message within a chatroom
--==============================================================
CREATE TABLE Message (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chat_id INT NOT NULL,
    sender_id INT NOT NULL,
    photo_id INT DEFAULT NULL,
    video_id INT DEFAULT NULL,
    content TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (chat_id) REFERENCES Chat(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES User(id),
    FOREIGN KEY (photo_id) REFERENCES Photo(id),
    FOREIGN KEY (video_id) REFERENCES Video(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


