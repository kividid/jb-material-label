class Label (object):
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



    #TODO: Refactor with builder structure
    
    def __init__(self, materialName, materialDescription, vendor, orderDate, orderQty, po, line, misc, purchaseUnit, stockUnit, job, jobCustomer, jobDescription, jobPart):
        self.materialName = materialName
        self.materialDescription = materialDescription
        self.vendor = vendor
        self.orderDate = orderDate
        self.orderQty = orderQty
        self.po = po
        self.line = line
        self.misc = misc
        self.purchaseUnit = purchaseUnit
        self.stockUnit = stockUnit
        self.job = job
        self.jobCustomer = jobCustomer
        self.jobDescription = jobDescription
        self.jobPart = jobPart

    def __repr__(self):
        return '<PoLine {0}, {1}, {2}>'.format(self.materialName, self.materialDescription, self.orderQty)
