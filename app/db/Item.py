# File: Item.py
from app.utils import mysql_util
from app.utils import photo

def insert_item(seller_username: str, tags: list, sql: str, values: tuple, photos: list, city: str, state: str):
    # get seller id
    seller_sql = "SELECT id FROM User WHERE username=%s"
    seller_id = mysql_util.execute_sql(seller_sql, (seller_username,))
    if not seller_id:
        raise ValueError("ERROR: Seller '%s' not found" % seller_username)
    seller_id = seller_id[0]

    # insert item
    item_values = (values[0], seller_id, *values[1:])  # inject seller_id into values
    item_id = mysql_util.execute_sql(sql, item_values, commit=True, get_lastrowid=True)

    # insert tags and link them
    for tag in tags:
        mysql_util.execute_sql("INSERT IGNORE INTO Tag (name) VALUES (%s)", (tag,), commit=True)
        mysql_util.execute_sql("INSERT INTO Item_Tag (item_id, tag_id) SELECT %s, id FROM Tag WHERE name=%s", (item_id, tag), commit=True)

    # upload and link photos
    dir_path = 'app/static/images/uploads/'
    for display_order, file in enumerate(photos):
        print("inserting photo %s" % (dir_path + file))
        photo_id = photo.upload_image(dir_path + file)
        print("photo id is", photo_id)
        photo.link_item_photo(item_id, photo_id, display_order)

    # link location
    location_sql = '''
    SELECT id FROM Location WHERE city=%s AND state=%s;
    '''
    location_id = mysql_util.execute_sql(location_sql, params=(city, state))
    location_id = location_id[0]
    location_sql = '''
    INSERT INTO Item_Location (item_id, location_id) VALUES
    (%s, %s);
    '''
    mysql_util.execute_sql(location_sql, params=(item_id, location_id), commit=True)

    print("success for %s" % seller_username)
        
def insert():
    # cole
    #===========================
    seller_username = 'bigbrovc'

    # harp
    #---------------------------
    harp_tags = ['musical instrument', 'string', 'harp', 'vintage', 'classical']
    harp_sql = '''
    INSERT INTO Item (item_name, seller_id, price, `condition`, descrip) VALUES
    (%s, %s, %s, %s, %s)
    '''
    harp_values = (
        'Roosebeck 22-String Heather Harp w/ Full Chelby Levers',
        1999.99,
        'very good',
        'Roosebeck 22-String Heather Harp w/ Full Chelby Levers. It is pre-owned so it does have wear, including nicks, scratches, and scuffs consistent with previous use; however, it still remains in lovely condition. Please view the photos carefully for details and feel free to ask questions. From a smoke-free environment.'
    )
    harp_photos = ['1.png']
    harp_city = "Harrisburg"
    harp_state = "MO"
    insert_item(seller_username, harp_tags, harp_sql, harp_values, harp_photos, harp_city, harp_state)

    # Nash
    #===========================
    seller_username = 'nashydog'

    # cd
    #---------------------------
    cd_tags = ['music', 'cd', 'trigun', 'japanese', 'tsuneo imahori', 'anime', 'autographed']
    cd_sql = '''
    INSERT INTO Item (item_name, seller_id, price, `condition`, descrip) VALUES
    (%s, %s, %s, %s, %s)
    '''
    cd_values = (
        '(AUTOGRAPHED) Tsuneo Imahori "TRIGUN" Soundtrack Trigun The First Donuts Japan Music CD',
        124.50,
        'new',
        '''TV anime adaptation of the popular comic originally written by Naito Yasuhiro and broadcast in 1998.
The first soundtrack by Tsuneo Imahori (今堀恒雄, Imahori Tsuneo).
Signed by Imahori Tsuneo (今堀恒雄).
Includes OP theme "H.T" and ED theme "風は未来に吹く" among other tracks.

Tracklist:
1. NO-BEAT
2. BIG BLUFF
3. BLOOD AND THUNDER
4. KNIVES
5. Permanent Vacation
6. BLUE FUNK
7. PHILOSOPHY in a Tea Cup
8. NOT AN ANGEL
9. Cynical Pink
10. Sound Life ~LEM
11. 風は未来に吹く
12. H.T
13. WINNERS
14. Never could have been worse
15. Stories to Tell
16. People Everyday
17. Fool's Paradise
18. YELLOW ALERT
19. Carrot & Stick
20. Perfect Night'''
    )
    cd_photos = ['2.png', '3.png']
    cd_city = "Columbia"
    cd_state = "MO"
    insert_item(seller_username, cd_tags, cd_sql, cd_values, cd_photos, cd_city, cd_state)

    # robert
    #====================================
    seller_username = 'Robiefresh'
    
    # FLCL bass
    #----------------
    tags = ['musical instrument', 'bass guitar', 'guitar', 'professional gear', 'rickenbacker', "collector's item", 'blue hawaiian', '4-string bass', 'professional bass', 'right-handed bass', 'maple body', 'made in usa', 'anime', 'flcl']
    
    bass_sql = '''
    INSERT INTO Item (item_name, seller_id, price, `condition`, descrip) VALUES
    (%s, %s, %s, %s, %s)
    '''
    
    bass_values = (
        'Rickenbacker 2025 Limited Edition 4003 Fab Gear Model Bass (Blue Hawaiian)',
        3998.00,
        'new',
        '''The Rickenbacker 4001 achieved notoriety in anime when it was seen in the hands of Haruko Haruhara, a character from the legendary series FLCL (Fooly Cooly). The Rickenbacker 4001 is not your average bass guitar.

Neck
No. Frets: 20
Scale Length: 84.5 cm (33 1/4”)
Neck Width at Nut: 42.9 mm (1 11/16”)
Neck Width at 12th Fret: 54.0 mm (2 1/8”)
Crown Radius: 25.4 cm (10”)
Neck Type: Through body
Fret Marker Style: Triangle
Fingerboard Wood: Rosewood
Fingerboard Finish: Gloss
Neck Wood: Maple
Neck Binding: White
Truss Rod: Single coarse-thread two-way truss rod

Body
Body Type: Solid
Body Wood: Maple
Body Style: Cresting wave
Binding: Checkerboard

Overall Dimensions
Overall Length: 113.8 cm (44 13/16”)
Overall Width: 34.3 cm (13 1/2”)
Overall Depth: 31.8 mm (1 1/4”)

Hardware
Tailpiece: New RIC V2 bridge/tailpiece
Bridge: New RIC V2 bridge/tailpiece
Machine Heads: Schaller Deluxe

Electronics
No. of Pickups: 2
Type of Pickups: Single Coil
Output Type: Mono

Case
Case Type: Deluxe Rickenbacker Hardshell Case'''
    )
    
    photos = ["4.png", "5.png", "6.png"]
    city = "Atlanta"
    state = "GA"
    insert_item(seller_username, tags, bass_sql, bass_values, photos, city, state)
    
if __name__ == '__main__':
    insert()
