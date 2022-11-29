
import psycopg2
from ktp_ocr import KTPOCR
import os 
import json
import re


def mid(s, offset, amount):
    return s[offset-1:offset+amount-1]

sistem_operasi = os.name
if sistem_operasi == "posix":
    os.system("clear")
else:
    os.system("cls")


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
        # jsonStr = obj_json.encode("utf-8")
        # print(obj_json)    
        # print(obj_json.format('nik'))
        data = json.loads(obj_json)
        
        print(f"-----------------------------------------")
        print(f"N I K          : {data['nik'].strip()}")
        print(f"Nama           : {data['nama'].strip()}")
        print(f"Tempat Lahir   : {data['tempat_lahir']}")
        print(f"Tanggal Lahir  : {data['tanggal_lahir']}")
        print(f"Jenis Kelamin  : {data['jenis_kelamin']}")
        print(f"Golongan Darah : {data['golongan_darah']}")
        print(f"Alamat Tinggal : {data['alamat']}")
        print(f"R T            : {data['rt']}")
        print(f"R W            : {data['rw']}")
        print(f"Kelurahan/Desa : {data['kelurahan_atau_desa'].strip()}")
        print(f"Kecamatan      : {data['kecamatan'].strip()}")
        print(f"Agama          : {data['agama'].strip()}")
        print(f"Status Kawin   : {data['status_perkawinan'].strip()}")
        print(f"Pekerjaan      : {data['pekerjaan'].strip()}")
        print(f"Kewarganegaraan: {data['kewarganegaraan']}")        
                
        print(f"-----------------------------------------")
        print("")
        
        num = re.search(r'-?\d+', data['nik'])  #regex only get number nik        
        print(f"{num}")
        print("Matching word: ", num.group())
        niknew = print(num.group())
        print(niknew)
        
        if len(niknew) > 16 :
              nik_ = mid(num,1, 16)
              print(f'{nik_}')
                             
        #save to database ---
        cursor = conn.cursor()
        
        postgres_insert_query = """ INSERT INTO datascan_ktp (NIK, NAMA, TEMPAT_LAHIR,TANGGAL_LAHIR,
        JENIS_KELAMIN,GOLONGAN_DARAH,ALAMAT,RT,RW,KELURAHAN_ATAU_DESA,KECAMATAN,AGAMA,STATUS_PERKAWINAN,
        PEKERJAAN,KEWARGANEGARAAN) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (niknew.strip(),data['nama'].strip(), data['tempat_lahir'],data['tanggal_lahir'],
                            data['jenis_kelamin'],data['golongan_darah'],data['alamat'],data['rt'],data['rw'],
                            data['kelurahan_atau_desa'].strip(),data['kecamatan'].strip(),data['agama'].strip(),
                            data['status_perkawinan'].strip(),data['pekerjaan'].strip(),data['kewarganegaraan'])
        cursor.execute(postgres_insert_query, record_to_insert)

        conn.commit()
            
        cursor.close()        
        conn.close()
        
        print("Database closed & Save data!")
        print(" ")
    except Exception as error:
        print(error)