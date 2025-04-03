# File: Item.py
from app.utils import mysql_util
from app.utils import photo

def insert_item(seller_username: str, tags: list, sql: str, values: tuple, photos: list):
    # get seller id
    seller_sql = "SELECT id FROM User WHERE username=%s"
    seller_id = mysql_util.execute_sql(seller_sql, (seller_username,), fetchone=True)
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

    print("success for %s" % seller_username)
        
def insert():
    # cole
    #===========================
    seller_username = 'bigbrovc'

    # harp
    #---------------------------
    harp_tags = ['musical instruments & gear', 'string', 'harp', 'vintage', 'classical']
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
    insert_item(seller_username, harp_tags, harp_sql, harp_values, harp_photos)
    # cole
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
    insert_item(seller_username, cd_tags, cd_sql, cd_values, cd_photos)
    
if __name__ == '__main__':
    insert()
