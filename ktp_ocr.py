import cv2
import json
import re
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
from ktp_data import KTPData
from PIL import Image

class KTPOCR(object):
    def __init__(self, image):
        self.image = cv2.imread(image)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.th, self.threshed = cv2.threshold(self.gray, 127, 255, cv2.THRESH_TRUNC)
        self.result = KTPData()
        self.master_process()

    def process(self, image):
        raw_extracted_text = pytesseract.image_to_string((self.threshed), lang="ind")
        return raw_extracted_text

    def word_to_number_converter(self, word):
        word_dict = {
            '|' : "1"
        }
        res = ""
        for letter in word:
            if letter in word_dict:
                res += word_dict[letter]
            else:
                res += letter
        return res


    def nik_extract(self, word):
        word_dict = {
            'b' : "6",
            'e' : "2",
            'D' : "0",
            'U' : "0",
            '?' : "7",
        }
        res = ""
        for letter in word:
            if letter in word_dict:
                res += word_dict[letter]
            else:
                res += letter
        if "O6" in res:
            res = res.replace("O6", "2")
        return res
    
    def extract(self, extracted_result):
        for word in extracted_result.split("\n"):
            if "NIK" in word:
                word = word.split(':')
                self.result.nik = self.nik_extract(word[-1].replace(" ", ""))
                continue

            if "Nama" in word:
                word = word.split(':')
                self.result.nama = word[-1].replace('Nama ','')
                self.result.nama = self.result.nama.replace('1','').strip()
                continue

            if "Tempat" in word:
                if ':' in word:
                    word = word.split(':')
                    tgl = re.findall(r'\d+', word[1]) # array of number
                    tgl = '-'.join(tgl)
                    tmpt_lahir = re.sub(r'[^a-zA-Z]', '', word[1])
                    self.result.tanggal_lahir = tgl
                    self.result.tempat_lahir = tmpt_lahir
                                        
                    # print(re.search("([0-9]{2}\-[0-9]{2}\-[0-9]{4})", word)[0])
                    # self.result.tanggal_lahir = re.search("([0-9]{2}\-[0-9]{2}\-[0-9]{4})", word[-1])[0]
                    # self.result.tempat_lahir = word[-1].replace(self.result.tanggal_lahir, '')
                continue

            if 'Darah' in word:
                kel = re.search("(LAKI-LAKI|LAKI LAKI|LAKI|LELAKI|PEREMPUAN|WANITA)", word)
                if kel == None:
                    self.result.jenis_kelamin = '-'
                else:
                    self.result.jenis_kelamin = re.search("(LAKI-LAKI|LAKI LAKI|LAKI|LELAKI|PEREMPUAN|WANITA)", word)[0]
                
                word = word.split(':')
                try:
                    if '-' in word[-1]:
                        self.result.golongan_darah = '-'
                    else:
                        self.result.golongan_darah = re.search("(O|A|B|AB)", word[-1])[0]
                except:
                    self.result.golongan_darah = '-'
                    
            if 'Alamat' in word:
                self.result.alamat = self.word_to_number_converter(word).replace("Alamat ","")
                self.result.alamat = self.result.alamat.replace(": ", "")
                self.result.alamat = self.result.alamat.replace("1", "").strip()
                
            if 'NO.' in word:
                self.result.alamat = self.result.alamat + ' '+word
                
            if "Kecamatan" in word:
                if ':' in word:
                    self.result.kecamatan = word.split(':')[1].strip()
                else:
                    self.result.kecamatan = word
                    
            if "Desa" in word:
                wrd = word.split()
                desa = []
                for wr in wrd:
                    if not 'desa' in wr.lower():
                        desa.append(wr)
                self.result.kelurahan_atau_desa = ''.join(wr)
                
            if 'Kewarganegaraan' in word:
                if ':' in word:
                    self.result.kewarganegaraan = re.sub(r'[^-zA-Z]', '', word.split(':')[1].strip())    
                else:
                    self.result.kewarganegaraan = word.strip()
                    
            if 'Pekerjaan' in word:
                wrod = word.split()
                pekerjaan = []
                for wr in wrod:
                    if not '-' in wr:
                        pekerjaan.append(wr)
                job = ' '.join(pekerjaan).replace('Pekerjaan', '').strip()
                self.result.pekerjaan = re.sub(r'[^a-zA-Z]', ' ', job)
                
            if 'Agama' in word:
                agama = word.replace('Agama',"").strip()
                self.result.agama = re.sub(r'[^a-zA-Z]', '', agama)
                
            if 'Status' in word or 'Perkawinan' in word:
                status_perkawinan = re.search("(BELUM KAWIN|KAWIN|CERAI HIDUP|CERAI MATI|DUDA|BUJANG)", word)
                if status_perkawinan == None:
                    self.result.status_perkawinan = '-'
                else:
                    self.result.status_perkawinan = status_perkawinan[0]
                    self.result.status_perkawinan = re.search("(BELUM KAWIN|KAWIN|CERAI HIDUP|CERAI MATI|DUDA|BUJANG)", word)[0]
                    
            if "RTRW" in word:
                word = word.replace("RTRW",'')
                if self.has_numbers(word):
                    rt_rw = re.findall(r'\d+', word) # array of number
                    self.result.rt = rt_rw[0]
                    self.result.rw = rt_rw[1]
                    
    def master_process(self):
        raw_text = self.process(self.image)
        self.extract(raw_text)

    def to_json(self):
        return json.dumps(self.result.__dict__, indent=4)
    
    def has_numbers(self, inputString):
        return bool(re.search(r'\d', inputString))