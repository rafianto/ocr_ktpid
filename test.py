from ktp_ocr import KTPOCR
import os

if __name__ == "__main__":
    ktppath = os.path.dirname(os.path.realpath(__file__)) + "/dataset/ktp.jpg"
    ocr = KTPOCR(ktppath)
    text = ocr.to_json()
    print(text)