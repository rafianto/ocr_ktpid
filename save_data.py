
import psycopg2
from ktp_ocr import KTPOCR
import os

if __name__ == "__main__":

    hostname = 'localhost'
    database = 'hr'
    username = 'hr'
    pwd = 'hr'
    port_id = 5432
    
    try:
        conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id
        )
        
        ktppath = os.path.dirname(os.path.realpath(__file__)) + "/dataset/ktp.jpg"
        ocr = KTPOCR(ktppath)
        text = ocr.to_json()
        print(text)

        # data = json.loads(api_data)
        # nodes = data['nodes']

        #save to database -
        cur = conn.cursor()
        # cur.execute("select *  from ped_crashes limit 5")
        # row = cur.fetchall() 
        # print("#---------------------------------------")
        # for r in row:
        #        print(f" id {r[0]}  {r[1]}  {r[2]} {r[3]}")
        # print("#---------------------------------------")    
        
        cur.close()        
        conn.close()
        
        print("Database closed & Save data!")
    except Exception as error:
        print(error)    