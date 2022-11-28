
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
        obj_json = ocr.to_json()
        jsonStr = obj_json.encode("utf-8")
        print(obj_json)

        #save to database -
        cur = conn.cursor()
        
        # print(jsonStr['nama'])
        # for key, value in obj_json:
            # nik_ = item['nik']
            # print(key)
            
        cur.close()        
        conn.close()
        
        print("Database closed & Save data!")
    except Exception as error:
        print(error)    