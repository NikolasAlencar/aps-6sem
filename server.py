import cv2
from flask_cors import CORS
import mysql.connector
from flask import Flask, request

app = Flask(__name__)
CORS(app)

@app.post('/enviar-digital')
def enviarDigital():
    data = request.data.__str__()
    caminho = data[11:64]
    id = data[59]
    entrada = cv2.imread(caminho)
    print(entrada)
    con = mysql.connector.connect(host='localhost',database='Digital',user='nikolau',password='12345678')

    if con.is_connected():
        cursor = con.cursor()
        cursor.execute("select * from func;")
        linha = cursor.fetchall()

        for i in linha:
            original = cv2.imread("{}".format(i[6]))

            sift = cv2.xfeatures2d.SIFT_create()

            keypoints_1, descriptors_1 = sift.detectAndCompute(original, None)
            keypoints_2, descriptors_2 = sift.detectAndCompute(entrada, None)

            comp = cv2.FlannBasedMatcher(dict(algorithm=1, trees=10),
                                        dict()).knnMatch(descriptors_1, descriptors_2, k=2)
            ponts = []

            for x, y in comp:
                if x.distance < 0.1 * y.distance:
                    ponts.append(x)
            keypoints = 0
            if len(keypoints_1) <= len(keypoints_2):
                keypoints = len(keypoints_1)
            else:
                keypoints = len(keypoints_2)

            compt = (len(ponts) / keypoints)

            if compt > 0.95:
                print(id)
                return { 'success': True, 'result': compt * 100, 'imagePath': "{}".format(i[6]), 'caminhoUsado': caminho, 'dadosFuncionario': linha[int(id)-1] }      
    
    return { 'success': False, 'result': compt * 100, 'imagePath': "{}".format(i[6]), 'caminhoUsado': caminho }            

if __name__ == '__main__':
    app.run()