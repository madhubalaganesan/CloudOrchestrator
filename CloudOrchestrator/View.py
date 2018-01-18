import sys
from PyQt5 import QtWidgets, QtCore, QtGui, uic

from S3_Client import S3_client
from EC2_Client import EC2_client

Ui_MainWindow, QtBaseClass = uic.loadUiType("orchestrator_gui.ui")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        self.zones = {"US East (Ohio)": "us-east-2", "US East (N. Virginia)": "us-east-1",
                      "US West (N. California)": "us-west-1", "US West (Oregon)": "us-west-2",
                      "Asia Pacific (Mumbai)": "ap-south-1", "Asia Pacific (Seoul)": "ap-northeast-2",
                      "EU (Frankfurt)": "eu-central-1", "EU (Ireland)": "eu-west-1",
                      "EU (London)": "eu-west-2"}
        super(MainWindow, self).__init__()
        self.startMainWindow()


    def startMainWindow(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #S3 client
        self.s3=S3_client()

        #EC2 client
        self.ec2=EC2_client()

        # EC2 tab 
        types = ["t2.micro", "t2.nano"]
        for region in self.zones:
            self.ui.ec2regions.addItem(region)
        for type in types:
            self.ui.types.addItem(type)

        self.ui.getInstances.clicked.connect(self.displayInstances)
        self.ui.startInstance.clicked.connect(self.startInstance)
        self.ui.stopInstance.clicked.connect(self.stopInstance)
        self.ui.getStatus.clicked.connect(self.getStatus)
        self.ui.createInstance.clicked.connect(self.createInstance)

        #S3 tab
        for region in self.zones:
            self.ui.s3regions.addItem(region)
        self.ui.createBucket.clicked.connect(self.createBucket)
        self.ui.deleteBucket.clicked.connect(self.deleteBucket)
        self.ui.showallBucket.clicked.connect(self.displayAllBuckets)
        self.ui.chooseFile.clicked.connect(self.chooseFile)
        self.ui.uploadFile.clicked.connect(self.uploadFile)

    #list instances
    def displayInstances(self):
        region = self.zones[self.ui.ec2regions.currentText()]
        response = self.ec2.showInstances(region)
        instances = {}
        self.ui.listInstances.clear()
        if 'Reservations' in response:
            for elem in response['Reservations']:
                if (elem):
                    if 'Tags' in elem['Instances'][0]:
                        for tag in elem['Instances'][0]['Tags']:
                            if tag['Key'] == 'Name':
                                instances[tag['Value']] = elem['Instances'][0]['InstanceId']
                    else:
                        instances['NONAME'] = elem['Instances'][0]['InstanceId']
        for name in instances:
            self.ui.listInstances.addItem("Name: "+name+" ID: "+instances[name])
    # create new instance
    def createInstance(self):
        region = self.zones[self.ui.ec2regions.currentText()]
        name = self.ui.nameInstance.text()
        response = self.ec2.createInstance(name, region)
        if response=="OK":
            self.ui.status.setText("Instance created!")
        else:
            self.ui.status.setText(response.__str__())

    #start an instance
    def startInstance(self):
        if self.ui.listInstances.count() and self.ui.listInstances.selectedItems()!=[]:
            instance_row = self.ui.listInstances.selectedIndexes()[0]
            instance_id = instance_row.data().split()[3]
            region = self.zones[self.ui.ec2regions.currentText()]
            response = self.ec2.startInstance(region, instance_id)
            if response == "OK":
                self.ui.status.setText("Instance started")
            else:
                self.ui.status.setText(response.__str__())
        else:
            self.ui.status.setText("Please select an instance!")
    #stop an instance
    def stopInstance(self):
        if self.ui.listInstances.count() and self.ui.listInstances.selectedItems() != []:
            instance_row = self.ui.listInstances.selectedIndexes()[0]
            instance_id = instance_row.data().split()[3]
            region = self.zones[self.ui.ec2regions.currentText()]
            response = self.ec2.stopInstance(region, instance_id)
            if response=="OK":
                self.ui.status.setText("Instance stopped")
            else:
                self.ui.status.setText(response.__str__())
        else:
            self.ui.status.setText("Please select an instance!")

    def getStatus(self):
        if self.ui.listInstances.count() and self.ui.listInstances.selectedItems() != []:
            instance_row = self.ui.listInstances.selectedIndexes()[0]
            instance_id = instance_row.data().split()[3]
            region = self.zones[self.ui.ec2regions.currentText()]
            response = self.ec2.getStatus(region, instance_id)
            self.ui.status.setText(response.__str__())
        else:
            self.ui.status.setText("Please select an instance!")

    #handling S3
    def createBucket(self):
        region = self.zones[self.ui.s3regions.currentText()]
        name = self.ui.bucketName.text()
        response = self.s3.createBuckets(name, region)
        if response=="OK":
            self.ui.result.setText("Bucket created!")
        else:
            self.ui.result.setText(response.__str__())

    def deleteBucket(self):
        region = self.zones[self.ui.s3regions.currentText()]
        response = self.s3.deleteBucket(self.ui.bucketName.text(), region)
        if response=="OK":
            self.ui.result.setText("Bucket deleted!")
        else:
            self.ui.result.setText(response.__str__())


    def displayAllBuckets(self):
        response = self.s3.showBuckets()
        self.ui.createdBuckets.clear()
        for bucket in response:
            self.ui.createdBuckets.addItem(bucket['Name'])

    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            return fileName

    def chooseFile(self):
        self.fileName = self.openFileNameDialog()
        self.ui.fileName.setText(self.fileName)

    def uploadFile(self):
        if self.ui.createdBuckets.count() and self.ui.createdBuckets.selectedItems()!=[]:
            bucket_row = self.ui.createdBuckets.selectedIndexes()[0]
            bucket_name=bucket_row.data()
            if (self.fileName and bucket_name != ""):
                response = self.s3.addObject(self.fileName, bucket_name)
                if response=="OK":
                    self.ui.resultUpload.setText("")
                    self.ui.progressBar.setValue(100)
                    self.ui.resultUpload.setText("File uploaded to Bucket!")
                else:
                    self.ui.resultUpload.setText("")
                    self.ui.progressBar.setValue(100)
                    self.ui.resultUpload.setText(response.__str__())
            else:
                self.ui.resultUpload.setText("Specify a bucket and file to upload!")


    def downloadFile(self):
        pass





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


