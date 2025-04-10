
dataset = "service_data_set.txt"

if __name__ == '__main__':
    
    f = open(dataset, 'r')

    sql ='''
    use Talbook;
    insert Service (skills)
    values '''
    
    delim = '("'
    
    for line in f:
        sql += delim + line.replace('\n', '")')
        delim = ',\n("'
    sql += ';'
    f = open('service.sql', 'w')
    f.writelines(sql)
    print(sql)
