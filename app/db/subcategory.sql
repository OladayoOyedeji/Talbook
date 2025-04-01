use Talbook;

--============================================
-- Music
--============================================
SET @category_id = (SELECT id FROM Category WHERE name = 'Music' LIMIT 1);

INSERT INTO Subcategory (category_id, name) VALUES 
(@category_id, 'Audio Media Accessories'),
(@category_id, 'Cassettes'),
(@category_id, 'CDs'),
(@category_id, 'Music NFTs'),
(@category_id, 'Other Formats'),
(@category_id, 'Vinyl Records');

--============================================
-- Musical Instruments & Gear
--============================================
SET @category_id = (SELECT id FROM Category WHERE name = 'Musical Instruments & Gear' LIMIT 1);

INSERT INTO Subcategory (category_id, name) VALUES 
(@category_id, 'Brass'),
(@category_id, 'DJ Equipment'),
(@category_id, 'General Accessories'),
(@category_id, 'Guitars & Basses'),
(@category_id, 'Instruction Books, CDs & Video'),
(@category_id, 'Karaoke Entertainment'),
(@category_id, 'Other Musical Instruments'),
(@category_id, 'Percussion'),
(@category_id, 'Pianos, Keyboards & Organs'),
(@category_id, 'Pro Audio Equipment'),
(@category_id, 'Sheet Music & Song Books'),
(@category_id, 'Stage Lighting & Effects'),
(@category_id, 'String'),
(@category_id, 'Vintage Musical Instruments'),
(@category_id, 'Wholesale Lots');
