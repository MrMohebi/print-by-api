import os
import requests
import random
import win32.lib.win32con as win32con
import win32gui
from bottle import get, request, run
import pystray
import threading
from PIL import Image

SAVE_PATH = "C:\\MrM\\printer"


def setupTryIcon(icon):
    icon.visible = True


def exitProgram():
    raise SystemExit


def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = str(random.randint(111111, 999999)) + ".pdf"
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        pass
    return file_path


def printBill(filePath):
    os.system("p2p.exe /s " + filePath)
    os.system("del " + filePath)


@get('/print')
def index():
    billLink = dict(request.query.decode())["link"]
    try:
        filePath = download(billLink, SAVE_PATH)
        printBill(filePath)
    except:
        pass
    return "200"


def tryIcon():
    imageIcon = Image.open("./icon.png")
    icon = pystray.Icon('MrM-api-printer')
    icon.icon = imageIcon
    icon.menu = pystray.Menu(pystray.MenuItem('exit', exitProgram))
    icon.run(setupTryIcon)


def webServer():
    run(host='localhost', port=9751)


if __name__ == "__main__":
    # hide console
    the_program_to_hide = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(the_program_to_hide, win32con.SW_HIDE)

    tryIconThread = threading.Thread(target=tryIcon, daemon=True)
    webServerThread = threading.Thread(target=webServer, daemon=True)

    tryIconThread.start()
    webServerThread.start()

    webServerThread.join()
