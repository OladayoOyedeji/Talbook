SELECT * FROM Items
WHERE
       MATCH(item_name, descrip)
       AGAINST('%s' WITH IN BOOLEAN MODE)
select * from Item_Tag
join Tag on Item_Tag.tag_id = Tag.id
join Item on Item_Tag.item_id = Item.id
where MATCH(Tag.name)
       AGAINST('anime' WITH IN BOOLEAN MODE)

SELECT Item.id, count(Item.id) FROM Item_Tag
JOIN Tag ON Item_Tag.tag_id = Tag.id
JOIN Item ON Item_Tag.item_id = Item.id
WHERE 
(Tag.name LIKE '%anime%' OR Item.descrip LIKE '%anime%' OR Item.item_name LIKE '%anime%')
 OR (Tag.name LIKE '%away%' OR Item.descrip LIKE '%away%' OR Item.item_name LIKE '%away%')

GROUP BY Item.id
