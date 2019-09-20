import os
import  tarfile
import csv
import io

from flask import Flask, render_template, send_file
from operator import itemgetter
from zipfile import ZipFile

def count_Result(file_name):
    count1 = 0
    count0 = 0
    #print(file_name.endswith('tar'))
    if not file_name.endswith('tar'):
        file_name += '.tar'
        #print(file_name)
    with tarfile.open('F:/python/Astrome_FTP_Server/download/'+file_name) as tar:
        for member in tar.getnames():
            if member.endswith('csv'):
                csv_file = io.StringIO(tar.extractfile(member).read().decode('ascii'))
                for row in csv.reader(csv_file):
                    if int(row[1]) == 1:
                        count1 += 1
                    elif int(row[1]) == 0:
                        count1 += 1
    return count0,count1

file_list = os.listdir("F:\python\Astrome_FTP_Server\download")
FTP_Data = [[file[0:8],file[9:15],file[16:34],file[35:],count_Result(file)[0],count_Result(file)[1]] for file in file_list]
