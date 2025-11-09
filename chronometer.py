from flask import Flask
import serial
import threading

app = Flask(__name__)

# Global variable to store the latest message (3 lines)
latest_message = ["Ingen data mottatt ennå", "", ""]


def read_serial():
    global latest_message
    ser = serial.Serial('COM3', 115200, timeout=1)
    print("Leser fra", ser.port)

    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if not line:
            continue

        print("Mottatt:", line)

        # When "Web_Status" appears, read next two lines
        if line == "Web_Status":
            msg = ["Web_Status"]
            for _ in range(2):
                next_line = ser.readline().decode(errors='ignore').strip()
                if next_line:
                    print(" → Ekstra linje:", next_line)
                    msg.append(next_line)
            latest_message = msg  # update the global message


@app.route('/')
def index():
    html = f"""
    <html>
    <head>
        <meta http-equiv="refresh" content="10">
        <title>STM32 Chronometer</title>
        <style>
            body {{
                font-family: Arial;
                text-align: center;
                padding-top: 50px;
            }}
            h1 {{ color: #1a73e8; }}
            p {{ font-size: 20px; margin: 5px 0; }}
        </style>
    </head>
    <body>
        <h1>STM32 Chronometer</h1>
        <p><b>{latest_message[0]}</b></p>
        <p>{latest_message[1]}</p>
        <p>{latest_message[2]}ms</p>
        <p><small>(Siden oppdateres automatisk hvert 10. sekund)</small></p>
    </body>
    </html>
    """
    return html


if __name__ == '__main__':
    threading.Thread(target=read_serial, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
