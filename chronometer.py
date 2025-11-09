from flask import Flask, render_template_string
import serial, threading

# Opprett Flask-app
app = Flask(__name__)

# Global variabel for å lagre siste mottatte tid
latest_time = "Ingen data mottatt ennå"


# Denne funksjonen kjører i bakgrunnen og leser fra STM32
def read_serial():
    global latest_time
    ser = serial.Serial('COM3', 115200, timeout=1)
    print("Leser fra", ser.port)
    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if line:
            print("Mottatt:", line,)
            latest_time = line
            

# Flask-rute som viser nettsiden
@app.route('/')
def index():
    html = f"""
    <html>
    <head>
        <meta http-equiv="refresh" content="60">
        <title>Semester prosjekt</title>
        <style>
            body {{ font-family: Arial; text-align: center; padding-top: 50px; }}
            h1 {{ color: #1a73e8; }}
            p {{ font-size: 20px; }}
        </style>
    </head>
    <body>
        <h1>STM32 Chronometer</h1>
        <p>Siste oppdatering:</p>
        <p><b>{latest_time}</b></p>
        <p><small>(Siden oppdateres automatisk hvert 60. sekund)</small></p>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    # Start tråd som leser seriell data
    threading.Thread(target=read_serial, daemon=True).start()
    # Start Flask webserver
    app.run(host='0.0.0.0', port=5000)