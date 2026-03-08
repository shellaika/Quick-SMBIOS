#!/usr/bin/env python3
import sys, uuid, random, string
from datetime import datetime
from PyQt6.QtWidgets import QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QComboBox,QLineEdit,QTextEdit,QGroupBox

SMBIOS_MODELS={
"iMac19,1":"iMac 27 2019",
"iMac20,1":"iMac 27 2020",
"iMacPro1,1":"iMac Pro 2017",
"MacPro7,1":"Mac Pro 2019",
"Macmini8,1":"Mac mini 2018",
"MacBookPro16,1":"MacBook Pro 16 2019",
"MacBookPro15,1":"MacBook Pro 15 2019",
"MacBookAir9,1":"MacBook Air 2020",
}

BOARD_IDS={
"MacBookPro16,1":"Mac-E1008331FDC96864",
"MacBookPro15,1":"Mac-937A206F2EE63C01",
"Macmini8,1":"Mac-7BA5B2D9E42DDD94",
"MacPro7,1":"Mac-27AD2F918AE68F61",
"iMac19,1":"Mac-AA95B1DDAB278B95",
"iMac20,1":"Mac-CFF7D910A743CAAF",
"iMacPro1,1":"Mac-7BA5B2DFE22DDD8C",
"MacBookAir9,1":"Mac-827FAC58A8FDFA22"
}

MODEL_CODES={
"iMac19,1":"A","iMac20,1":"B","iMacPro1,1":"C","MacPro7,1":"D",
"Macmini8,1":"E","MacBookPro16,1":"F","MacBookPro15,1":"G","MacBookAir9,1":"H"
}

FACTORIES=["C02","C07","C17","C1M","C3Q","CK2","DLX","F5K"]
YEAR_CODES=["K","L","M","N","P"]
BASE34="0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"

APPLE_OUIS=[
"F0:18:98","3C:07:54","A8:66:7F","AC:BC:32","28:F0:76",
"F4:5C:89","40:A6:D9","F8:FF:C2","FC:25:3F","D8:30:62"
]

SAFE_CHARS="ABCDEFGHJKLMNPQRSTUVWXYZ123456789"

def base34_encode(num,length):
    res=""
    while num>0:
        num,rem=divmod(num,34)
        res=BASE34[rem]+res
    return res.rjust(length,BASE34[0])

def generate_line_code():
    return base34_encode(random.randint(0,34**3-1),3)

def random_alphanum(n):
    return ''.join(random.choices(SAFE_CHARS,k=n))

def random_hex(n):
    return ''.join(random.choices('0123456789ABCDEF',k=n))

def generate_serial(model):
    factory=random.choice(FACTORIES)
    year=random.choice(YEAR_CODES)
    week=f"{random.randint(1,52):02d}"
    production=generate_line_code()
    model_code=MODEL_CODES.get(model,"A")
    return f"{factory}{year}{week}{production}{model_code}"

def generate_mlb(serial):
    board=random_alphanum(6)
    suffix=random_hex(8)
    return f"{serial[:4]}{board}{suffix}"[:17]

def generate_uuid(serial):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS,serial)).upper()

def generate_mac():
    prefix=random.choice(APPLE_OUIS)
    suffix=':'.join(f"{random.randint(0,255):02X}" for _ in range(3))
    return f"{prefix}:{suffix}"

def mac_to_rom(mac):
    return mac.replace(":","")

def generate_smbios(model):
    serial=generate_serial(model)
    mac=generate_mac()
    return{
        "Model":model,
        "BoardID":BOARD_IDS.get(model,""),
        "Serial":serial,
        "MLB":generate_mlb(serial),
        "SmUUID":generate_uuid(serial),
        "MAC":mac,
        "ROM":mac_to_rom(mac)
    }

class Row(QWidget):
    def __init__(self,name):
        super().__init__()
        l=QHBoxLayout(self)
        self.lbl=QLabel(name)
        self.edit=QLineEdit(); self.edit.setReadOnly(True)
        self.btn=QPushButton("Copy")
        self.btn.clicked.connect(lambda: QApplication.clipboard().setText(self.edit.text()))
        l.addWidget(self.lbl); l.addWidget(self.edit); l.addWidget(self.btn)
    def set(self,v): self.edit.setText(v)

class Win(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SMBIOS Generator")
        root=QWidget(); self.setCentralWidget(root)
        main=QVBoxLayout(root)

        top=QHBoxLayout()
        self.combo=QComboBox()
        for k,v in SMBIOS_MODELS.items():
            self.combo.addItem(f"{k} — {v}",k)
        self.gen_btn=QPushButton("Generate")
        self.gen_btn.clicked.connect(self.generate)
        top.addWidget(self.combo); top.addWidget(self.gen_btn)
        main.addLayout(top)

        box=QGroupBox("Values")
        bl=QVBoxLayout(box)
        self.rows={}
        for name in ["Serial","MLB","UUID","MAC","ROM","BoardID"]:
            r=Row(name); bl.addWidget(r); self.rows[name]=r
        main.addWidget(box)

        self.copy_all=QPushButton("Copy plist")
        self.copy_all.clicked.connect(self.copy_all_vals)
        main.addWidget(self.copy_all)

        self.view=QTextEdit(); self.view.setReadOnly(True)
        main.addWidget(self.view)

        self.status=QLabel("Ready")
        main.addWidget(self.status)

        self.current={}
        self.generate()

    def plist(self,d):
        return f"""<key>SystemProductName</key>
<string>{d['Model']}</string>
<key>SystemSerialNumber</key>
<string>{d['Serial']}</string>
<key>MLB</key>
<string>{d['MLB']}</string>
<key>SystemUUID</key>
<string>{d['SmUUID']}</string>
<key>ROM</key>
<data>{d['ROM']}</data>
<key>Board-ID</key>
<string>{d['BoardID']}</string>"""

    def generate(self):
        model=self.combo.currentData()
        d=generate_smbios(model); self.current=d
        self.rows["Serial"].set(d["Serial"])
        self.rows["MLB"].set(d["MLB"])
        self.rows["UUID"].set(d["SmUUID"])
        self.rows["MAC"].set(d["MAC"])
        self.rows["ROM"].set(d["ROM"])
        self.rows["BoardID"].set(d["BoardID"])
        self.view.setPlainText(self.plist(d))
        self.status.setText(f"Generated {model} {datetime.now().strftime('%H:%M:%S')}")

    def copy_all_vals(self):
        if not self.current: return
        QApplication.clipboard().setText(self.plist(self.current))
        self.status.setText("Copied")

app=QApplication(sys.argv)
w=Win(); w.resize(540,520); w.show()
sys.exit(app.exec())
