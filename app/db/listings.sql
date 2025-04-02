use Talbook;

-- cole
--=========
SET @seller_id = (SELECT id FROM User WHERE username='bigbrovc');

-- harp
-----------
SET @category_id = (SELECT id FROM Category WHERE name='Musical Instruments & Gear');
INSERT INTO Item (item_name, seller_id, price, `condition`, descrip) VALUES
(
'Roosebeck 22-String Heather Harp w/ Full Chelby Levers',
@seller_id,
1999.99,
'very good', 
'Roosebeck 22-String Heather Harp w/ Full Chelby Levers. It is pre-owned so it does have wear, including nicks scratches, and scuffs consistent with previous use; however, it still remains in lovely condition. Please view the photos carefully for details and feel free to ask questions. From a smoke-free environment'
);

-- link item to category
SET @item_id = LAST_INSERT_ID();
INSERT INTO Item_Category (item_id, category_id) VALUES
(@item_id, @category_id);
