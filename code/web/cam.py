#!/usr/bin/python

# Autor: Roberto Kenji Hiramatsu
# Copyright: Universidade de Sao Paulo/Huawei
# Processameento para separacao de dados de face coletados na camera da Huawei
# Os tratamentos executados sao a eliminacao de imagens nao detectadas com o dlib
# Registro de
# Data: 2016/08/29 - versao inicial
#       2016/10/13 - processamento usando regressao logistica para classificacao com indice de acerto
#	2017/03/21 - Envia dados via Json

import numpy as np
import cv2
import cv2.cv as cv
from imutils import paths
import argparse
import os,sys
from common import clock, draw_str
from datetime import datetime
from Recog import Classificador
import RepUtil
import time
import json
import websocket
from OpenSSL import SSL
import ssl


def detect(img, cascade):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    rects = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, #2
                                     minSize=(40, 40),  #(120, 120)
                                     flags = cv.CV_HAAR_SCALE_IMAGE)
    if len(rects) == 0:
        return [],0.0
    rects[:,2:] += rects[:,:2]
    bdisp = 0.0
    if len(rects)>0:
        x1, y1, x2, y2 = rects[0]
        bdisp  =  cv2.Laplacian(gray[y1:y2,x1:x2],cv2.CV_64F).var()
    return rects,bdisp

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

def geraResultado(lista):
    with open('scontent.json','wt') as fctx:
        resultado = []
        for  (nome,pb,reffile,tipoc) in lista:
            if reffile is None:
                return
            resultado.append({'nome':nome,
                              'proba':int(pb*100),
                              'img':os.path.join('img',"ico."+reffile),
                              'extra':tipoc})
        fctx.write(json.dumps({'resultados':resultado},separators=(',',':')))
    os.rename('scontent.json','content.json')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', type=str,
                    help="url do video",
                    #default='rtsp://admin:B30cd4Ro@127.0.0.1:8554/LiveMedia/ch1/Media1')
                    default='rtsp://admin:B30cd4Ro@127.0.0.1:8554/LiveMedia/ch1/Media2')
    parser.add_argument('--cascade', type=str,
                    help="cascade haar detector",
                    default='../../../data/haarcascades/haarcascade_frontalface_alt.xml')
    parser.add_argument('--rotateIm', type=bool, help="Rotacao da camera",
                    default=False)

    parser.add_argument('--fatorRed', type=float , help="Reducao para otimizacao de processamento",
                    default= 0.25)

    args = parser.parse_args()
    print args.rotateIm
    print args.video

    cap = cv2.VideoCapture(args.video)
    cascade = cv2.CascadeClassifier(args.cascade)
    classif = Classificador()
    classif.loadClassif()
    print cap
    try:
        while(True):
            t = clock()
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Display the resulting frame
            if ret:
                if args.rotateIm:
                    # teste com frame rotacionado
                    (h, w) = frame.shape[:2]
                    Mtr = np.float32([[0,1,0],[-1,0,w]])
                    frame = cv2.warpAffine(frame, Mtr, (h,w))
                dt = clock() - t
                print 'C Time',dt,' s'
                reduzido = cv2.resize(frame,(0,0),fx=args.fatorRed,fy=args.fatorRed)
		#detecta faces no frame
                rects,bdisp=detect(reduzido, cascade)
                dt = clock() - t
                print 'D Time',dt,' s'
                [heb,wib,pb] = frame.shape
                #xi1, yi1, xi2, yi2
                framecopy = frame.copy()
                gresp = []
                contarf = 0
		
		
		for rcar in rects:
                    contarf += 1
                    ncar = np.array(rcar)
                    ncar =  ncar / args.fatorRed
                    [xi1, yi1, xi2, yi2] = ncar.astype(int)
                    x1,y1,x2,y2 = RepUtil.novoEquad(xi1,yi1,xi2,yi2,wib,heb)
                    vis_roi = frame[y1:y2, x1:x2]
                    roih,roiw,roic = vis_roi.shape
                    if roiw > 240:
                        fator = 180.0/float(roiw)
                        vis_roi = cv2.resize(frame,(0,0),fx=fator,fy=fator)         

                    print "Recorte para processamento em ({},{})({},{})".format(x1,y1,x2,y2)
                    paraGravar = vis_roi.copy()

                    # verifica se face encontrada no haar cascade e detectado no dlib para rede neural
                    if classif.equadra(vis_roi.copy()):
                        dt = clock() - t
                        print 'E Time',dt,' s'
                        resp = classif.classifica()
                        for (nome,pb,reffile,tipoc) in resp:
                            gresp.append((nome,pb,reffile,str(contarf)+"-"+tipoc))

                        (nome,pb,reffile,tipoc) = resp[0]
                        now = datetime.now()
                        arquivo='./predic/predic_{:02d}.{:02d}.{:02d}.{:02d}.{:02d}_pb{:02.0f}_{}.jpg'.format(now.month,now.day,now.hour,now.minute,now.second,(pb*100), nome)

                        #gravar somente a imagem do rosto
                        cv2.imwrite(arquivo,paraGravar)
                        print "Encontrado {} com dispersao {} em {}".format(nome,bdisp,now)
                        textoI="{} ({})-{:2.0f}% - d:{:3.0f}".format(nome,contarf,(pb*100),bdisp)
                        cert = ssl.get_server_certificate(('192.168.10.234',8443))
                        lf = (len(ssl.PEM_FOOTER)+1)
                        if cert[0-lf] != '\n':
                            cert = cert[:0-lf]+'\n'+cert[0-lf:]                
                        ws = websocket.create_connection("wss://192.168.10.234:8443/media", sslopt={"cert_reqs": ssl.CERT_NONE})
                        payload = {'id': 'sendDetectionAlert', 'date': time.strftime('%D:%H:%M:%S'), 'name': nome, 'probability': (pb*100)}
                        data = json.dumps(payload)
                        ws.send(data)
                        print(data)
                        print">  Enviado para o Kurento"
                        cv2.putText(framecopy, textoI, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.75,
                            color=(152, 255, 204), thickness=2)
                        rects = np.array(rects)
                        rects4 =  rects / args.fatorRed
                        rects4 = rects4.astype(int)
                        if bdisp >400.0:
                            draw_rects(framecopy, rects4, (0, 255, 0))
                        else:
                            draw_rects(framecopy, rects4, (0, 255, 255))
                geraResultado(gresp)#else:
                #    draw_rects(frame, rects, (0, 0, 255))
                reduzim = cv2.resize(framecopy,(0,0),fx=0.5,fy=0.5)
                #reduzim = cv2.resize(frame,(0,0),fx=0.3333334,fy=0.3333334)
                cv2.imwrite('cameraf.jpg',reduzim)
                os.rename('cameraf.jpg','camera.jpg')
                dt = clock() - t
                print 'R Time',dt,' s'
    except KeyboardInterrupt:
        cap.release()
