import os
import tarfile
import csv
import io


from flask import Flask, render_template, send_file
from operator import itemgetter
from zipfile import ZipFile

def count_Result(file_name):
    count1 = 0
    count0 = 0
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
                        count0 += 1
    return [count0,count1]


app = Flask(__name__)

@app.route('/index')
def index():
    file_list = os.listdir("F:\python\Astrome_FTP_Server\download")
    FTP_Data = [[file[0:8],file[9:15],file[16:34],file[35:],count_Result(file)] for file in file_list]
    return render_template('index.html', FTP_Data = FTP_Data)

@app.route('/index/<date_time>')
def date_file(date_time):
    if not date_time.endswith('tar'):
        date_time += '.tar'
        #print(date_time)
    tar = tarfile.open("download/"+date_time)
    tar_list = [member for member in tar.getmembers()]
    for member_csv in tar.getnames():
        if member_csv.endswith('csv'):
            Result_file = tar.extractfile(member_csv)
            Result_content=Result_file.read()

    out_V_file = tar.extractfile(tar_list[3])
    out_V_content=out_V_file.read()

    yml1=tar.extractfile(tar_list[4])
    with ZipFile(yml1) as myzip1:
        files=myzip1.namelist()
        yml1_content = myzip1.read(files[-1])

    yml2=tar.extractfile(tar_list[5])
    with ZipFile(yml2) as myzip1:
        files=myzip1.namelist()
        yml2_content = myzip1.read(files[-1])

    return render_template('date_template.html',date_value=date_time,out_V = out_V_content,Result = Result_content,yml1 = yml1_content,yml2 = yml2_content)

@app.route('/index/<date_value>/download')
def download_file(date_value):
    path = 'download/'+ date_value
    return send_file(path, as_attachment = True)

@app.route('/sort_by_date')
def sort_by_date():
    file_list = os.listdir("F:\python\Astrome_FTP_Server\download")
    FTP_Data = [[file[0:8],file[9:15],file[16:34],file[35:],count_Result(file)] for file in file_list]
    FTP_Data = sorted(FTP_Data, key=itemgetter(1),reverse=False)
    return render_template('index.html', FTP_Data = FTP_Data)

@app.route('/sort_by_time')
def sort_by_time():
    file_list = os.listdir("F:\python\Astrome_FTP_Server\download")
    FTP_Data = [[file[0:8],file[9:15],file[16:34],file[35:],count_Result(file)] for file in file_list]
    FTP_Data = sorted(FTP_Data, key=itemgetter(2),reverse=False)
    return render_template('index.html', FTP_Data = FTP_Data)

if __name__ == '__main__':
    app.debug = True
    app.run()
    #app.run(host="192.168.43.69",port=5000)
