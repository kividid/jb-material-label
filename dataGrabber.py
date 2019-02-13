from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from models import Label
from dotenv import load_dotenv
import os
import urllib.parse
import sys

load_dotenv()

Base = automap_base()


#Connect to DB - using DSN on win32, MSFT odbc driver on Linux
if sys.platform == 'win32':
    engine = create_engine(os.getenv("ODBC_STRING"))
elif sys.platform == 'linux2':
    params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+os.getenv("DB_SERVER")+';PORT=1443;DATABASE='+os.getenv("DB_NAME")+';UID='+os.getenv("DB_USER")+';PWD='+ os.getenv("DB_PASS"))
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

Base.prepare(engine, reflect=True)

Job = Base.classes.Job
Source = Base.classes.Source
MatReq = Base.classes.Material_Req
PoDetail = Base.classes.PO_Detail
PoHeader = Base.classes.PO_Header

session = Session(engine)

class LabelBuilder (object):
    materialName = ""
    materialDescription = ""
    vendor = ""
    orderDate = ""
    orderQty = 0
    po = ""
    misc = False
    purchaseUnit = ""
    stockUnit =""
    line = ""
    job = 0
    jobCustomer = ""
    jobDescription = ""
    jobPart = ""

    def buildSingleLabel(self, po, line):
        self.resetValues()

        self.po = po
        self.line = line

        poDetail = session.query(PoDetail).filter_by(PO = po, Line = line).first()

        self.orderQty = poDetail.Order_Quantity
        self.orderUnit = poDetail.Purchase_Unit

        poHeader = session.query(PoHeader).filter_by(ObjectID = poDetail.PO_Header_OID).first()

        self.vendor = poHeader.Vendor
        self.orderDate = poHeader.Order_Date

        source = session.query(Source).filter_by(PO_Detail = poDetail.PO_Detail).first()

        if source.Misc_Material:
            self.misc = True


        #If the source lists a material requirement, it came from a job, so go grab that job and fill in the details
        if source.Material_Req:
            materialReq = session.query(MatReq).filter_by(Material_Req = source.Material_Req).first()
            self.job = materialReq.Job
            self.materialName = materialReq.Material
            self.materialDescription = materialReq.Description 
            job = session.query(Job).get(self.job)  #get job object for job details
            self.jobCustomer = job.Customer
            self.jobDescription = job.Description
            self.jobPart = job.Part_Number
        else:                                       #else the source sould list the name and description
            self.materialName = source.Material
            self.materialDescription = source.Description

        label = Label(self.materialName, self.materialDescription, self.vendor,
                     self.orderDate, self.orderQty, self.po, self.line, self.misc, 
                     self.purchaseUnit, self.stockUnit, self.job, self.jobCustomer, 
                     self.jobDescription, self.jobPart)

        print(label)

        return label

    def buildAllLabels(self, po):
        poDetail = session.query(PoDetail).filter_by(PO = po).all()
        labels = []

        for detail in poDetail:
            labels.append(self.buildSingleLabel(po, detail.Line))

        return labels

    def resetValues(self):
        self.materialName = ""
        self.materialDescription = ""
        self.vendor = ""
        self.orderDate = ""
        self.orderQty = 0
        self.po = ""
        self.misc = False
        self.purchaseUnit = ""
        self.stockUnit =""
        self.line = ""
        self.job = 0
        self.jobCustomer = ""
        self.jobDescription = ""
        self.jobPart = ""
