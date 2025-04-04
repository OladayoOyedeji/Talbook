# Location.py
from app.utils.mysql_util import execute_many_sql
import csv

def insert(raw_csv_path):
    """
    Processes raw city data CSV and imports only city_ascii and state_id
    """
    insert_sql = '''
    INSERT INTO Location (city, state)
    VALUES (%s, %s)
    '''
    
    try:
        with open(raw_csv_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            batch = []
            batch_size = 1000
            seen = set()
            
            for row in csv_reader:
                city = row['city_ascii'].strip()
                state = row['state_id'].strip().upper()[:2]
                
                # create unique key to detect duplicates
                unique_key = "%s_%s" % (city, state)
                
                if unique_key not in seen:
                    batch.append((city, state))
                    seen.add(unique_key)
                    
                    if len(batch) >= batch_size:
                        execute_many_sql(insert_sql, param_list=batch, commit=True)
                        batch = []
            
            if batch:
                execute_many_sql(insert_sql, param_list=batch, commit=True)
        
        print("successfully imported %s unique locations" % len(seen))
        return True
        
    except Exception as e:
        print("ERROR: import failed: %s" % str(e))
        return False

if __name__ == '__main__':
    raw_csv_path = 'app/db/Location/uscities.csv'
    insert(raw_csv_path)
