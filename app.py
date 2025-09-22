import cv2
import time
from datetime import datetime, time as dt_time
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- CONFIGURAR PLANILHA GOOGLE SHEETS ---
def salvar_google_sheets(data_atual, diferenca):
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("ContagemPessoas").sheet1
    sheet.append_row([data_atual, diferenca])

# --- FUNÇÃO DE CONTAGEM ---
def rodar_contagem():
    cap = cv2.VideoCapture("rtsp://usuario:senha@ipcamera/stream")  # câmera IP
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter("output.mp4", fourcc, 20.0, (640,480))

    start_time = time.time()

    while cap.isOpened():
        success, im0 = cap.read()
        if not success:
            print("Vídeo indisponível ou finalizado.")
            break

        # Exemplo: YOLO (ajuste para seu modelo real)
        # results = counter(im0)
        # entradas = results.in_count
        # saidas = results.out_count
        # diferenca = entradas - saidas
        diferenca = 1  # <<< MOCK - substitua pelo seu cálculo real

        agora = datetime.now().time()
        if agora > dt_time(7, 45):
            break

        # salva no Google Sheets
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        salvar_google_sheets(data_atual, diferenca)

        video_writer.write(im0)

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()

# --- LOOP INFINITO ---
if __name__ == "__main__":
    while True:
        agora = datetime.now().time()
        if dt_time(6, 40) <= agora <= dt_time(7, 45):
            print("Rodando contagem de pessoas...")
            rodar_contagem()
        else:
            print("Aguardando horário certo...")
            time.sleep(60)
