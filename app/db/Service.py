
dataset = "app/db/service_data_set.txt"

if __name__ == '__main__':
    
    f = open(dataset, 'r')
    page = set(f.readlines())
    sql ='''
use Talbook;
insert into Service (skills)
values '''
    
    delim = '("'
    
    for line in page:
        sql += delim + line.replace('\n', '")')
        delim = ',\n("'
    sql += ';'
    f = open('app/db/service.sql', 'w')
    f.writelines(sql)
    print(sql)
