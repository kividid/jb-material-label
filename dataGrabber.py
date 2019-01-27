from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

Base = automap_base()

engine = create_engine('mssql+pyodbc://metabase:metabase@pythontest')

Base.prepare(engine, reflect=True)

Job = Base.classes.Job
Source = Base.classes.Source
MatReq = Base.classes.Material_Req
PoDetail = Base.classes.PO_Detail
PoHeader = Base.classes.PO_Header

session = Session(engine)
"""
testPoOne = session.query(PoDetail).first()

print(testPoOne)

testPo = session.query(PoDetail).filter_by(PO = '41695').all()

print(testPo)

for item in testPo:
    print(item.PO_Detail)
"""

class PoLine (object):
    materialName = ""
    materialDescription = ""
    vendor = ""
    orderDate = ""
    orderQty = 0
    po = ""
    job = 0
    misc = False
    purchaseUnit = ""
    stockUnit =""
    line = ""


    #TODO: Refactor with builder structure
    
    def __init__(self, po, line):
        self.po = po
        self.line = line

        poDetail = session.query(PoDetail).filter_by(PO = po, Line = line).first()

        self.orderQty = poDetail.Order_Quantity
        self.orderUnit = poDetail.Purchase_Unit

        poHeader = session.query(PoHeader).filter_by(ObjectID = poDetail.PO_Header_OID).first()

        self.vendor = poHeader.Vendor
        self.orderDate = poHeader.Order_Date

        source = session.query(Source).filter_by(PO_Detail = poDetail.PO_Detail).first()

        if source.Misc_Material == 'true':
            self.misc = True


        #If the source lists a material requirement, it came from a job, so go grab that job and fill in the details
        if source.Material_Req:
            materialReq = session.query(MatReq).filter_by(Material_Req = source.Material_Req).first()
            self.job = materialReq.Job
            self.materialName = materialReq.Material
            self.materialDescription = materialReq.Description 
        else: #else the source sould list the name and description
            self.materialName = source.Material
            self.materialDescription = source.Description

    def __repr__(self):
        return '<PoLine {0}, {1}, {2}>'.format(self.materialName, self.materialDescription, self.orderQty)



def main():
    another = ""

    while another != 'q':
        poNumber = input('PO #?')
        line = input('Line #?')

        detail = PoLine(poNumber, line)
        print(detail)
        another = input("Press enter to try another. To quit type 'q'.")


if __name__ == "__main__":
    main()


""" aJob = session.query(Job).first()

print(aJob)

print(aJob.Customer) """
