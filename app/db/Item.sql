use Talbook;

-- cole
--=========
SET @seller_id = (SELECT id FROM User WHERE username='bigbrovc');

-- harp
-----------
INSERT IGNORE INTO Tag (name) values
('musical instruments & gear'),
('string'),
('harp'),
('vintage'),
('classical');

INSERT INTO Item (item_name, seller_id, price, `condition`, descrip) VALUES
(
'Roosebeck 22-String Heather Harp w/ Full Chelby Levers',
@seller_id,
1999.99,
'very good', 
'Roosebeck 22-String Heather Harp w/ Full Chelby Levers. It is pre-owned so it does have wear, including nicks scratches, and scuffs consistent with previous use; however, it still remains in lovely condition. Please view the photos carefully for details and feel free to ask questions. From a smoke-free environment'
);

-- link item to tags
SET @item_id = LAST_INSERT_ID();

INSERT INTO Item_Tag (item_id, tag_id)
SELECT @item_id, id FROM Tag 
WHERE name IN
(
    'musical instruments & gear',
    'string',
    'harp',
    'vintage',
    'classical'
);

-- trigun signed cd
---------------------
INSERT IGNORE INTO Tag (name) values
('music'),
('cd'),
('trigun'),
('japanese'),
('tsuneo imahori'),
('anime'),
('autographed');

INSERT INTO Item (item_name, seller_id, price, `condition`, descrip) VALUES
(
    '(AUTOGRAPHED) Tsuneo Imahori "TRIGUN" Soundtrack Trigun The First Donuts Japan Music CD',
    @seller_id,
    124.50,
    'new', 
    'TV anime adaptation of the popular comic originally written by Naito Yasuhiro and broadcast in 1998.\n
The first soundtrack by Tsuneo Imahori (今堀恒雄, Imahori Tsuneo). \n
Signed by Imahori Tsuneo (今堀恒雄).\n
Inst\'s OP theme "H.T," ED theme "風は未来に吹く," and insert song are also included.\n\n

1. NO-BEAT\n
2. BIG BLUFF\n
3. BLOOD AND THUNDER\n
4. KNIVES\n
5. Permanent Vacation\n
6. BLUE FUNK\n
7. PHILOSOPHY in a Tea Cup\n
8. NOT AN ANGEL\n
9. Cynical Pink\n
10. Sound Life ~LEM\n
11. 風は未来に吹く\n
12. H.T\n
13. WINNERS\n
14. Never could have been worse\n
15. Stories to Tell\n
16. People Everyday\n
17. Fool\'s Paradise\n
18. YELLOW ALERT\n
19. Carot & Stick\n
20. Perfect Night'
);

-- link item to tags
SET @item_id = LAST_INSERT_ID();

INSERT INTO Item_Tag (item_id, tag_id)
SELECT @item_id, id FROM Tag 
WHERE name IN
(
    'music',
    'cd',
    'trigun',
    'japanese',
    'tsuneo imahori',
    'anime',
    'autographed'
);

