import sqlite3, sys, re, requests
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from sklearn.preprocessing import LabelEncoder
from sklearn import tree


class Ui_Dialog(object):
    def __init__(self):
        try:
            self.sqlConnector = sqlite3.connect('database.db')
            self.cursor = self.sqlConnector.cursor()

            query = "SELECT * FROM data"
            self.cursor.execute(query)
            data = self.cursor.fetchall()


            cpu_list = []
            gpu_list = []
            ram_list = []
            disk_size_list = []
            disk_type_list = []
            inch_list = []
            price_list = []


            for row in data:
                cpu_list.append(row[0])
                gpu_list.append(row[1]) 
                ram_list.append(int(row[2]))  
                disk_size_list.append(int(row[3]))  
                disk_type_list.append(row[4])  
                inch_list.append(float(row[5]))  
                price_list.append(int(row[6])) 


            # Initialize and fit encoders for categorical data
            self.le_cpu = LabelEncoder()
            self.le_gpu = LabelEncoder()
            self.le_disk_type = LabelEncoder()

            # Fit encoders on the complete data
            cpu_encoded = self.le_cpu.fit_transform(cpu_list)
            gpu_encoded = self.le_gpu.fit_transform(gpu_list)
            disk_type_encoded = self.le_disk_type.fit_transform(disk_type_list)


            # Prepare training data - combine all features
            X_train = []
            for i in range(len(cpu_list)):
                features = [
                    cpu_encoded[i],
                    gpu_encoded[i],
                    ram_list[i],
                    disk_size_list[i],
                    disk_type_encoded[i],
                    inch_list[i]
                ]
                X_train.append(features)

            # Convert to numpy arrays
            X_train = np.array(X_train)
            y_train = np.array(price_list)



            # Train the model
            self.clf = tree.DecisionTreeClassifier()
            self.clf.fit(X_train, y_train)
            
            
            # Store class attributes for validation
            self.valid_cpu_values = set(cpu_list)
            self.valid_gpu_values = set(gpu_list)
            self.valid_disk_types = set(disk_type_list)
            
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Database Error", f"Could not connect to database:\n{e}")
            raise
        except Exception as e:
            QMessageBox.critical(None, "Initialization Error", f"Error during setup:\n{e}")
            raise

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(850, 840)
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet("background-color : rgb(11, 37, 69)")
        
        # Add label to display result
        self.result_label = QtWidgets.QLabel(Dialog)
        self.result_label.setGeometry(QtCore.QRect(200, 730, 500, 80))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.result_label.setFont(font)
        self.result_label.setStyleSheet("color : rgb(255, 255, 255); background-color: rgb(19, 64, 116); border-radius: 10px; padding: 10px;")
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)
        self.result_label.setObjectName("result_label")
        self.result_label.setText("قیمت پیشبینی شده اینجا نمایش داده می شود")
        self.result_label.setWordWrap(True)
        
        # Rest of your UI setup code remains the same...
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(150, 160, 61, 41))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color : rgb(141, 169, 196)")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(30, 230, 321, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.textEdit.setFont(font)
        self.textEdit.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.textEdit.setStyleSheet("background-color : rgb(19, 64, 116);\n"
" border-radius: 10px;\n"
" padding: 6px;\n"
"color : rgb(141, 169, 196)\n"
"")
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_2.setGeometry(QtCore.QRect(30, 380, 321, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.textEdit_2.setStyleSheet("background-color : rgb(19, 64, 116);\n"
" border-radius: 10px;\n"
" padding: 6px;\n"
"color : rgb(141, 169, 196)\n"
"")
        self.textEdit_2.setObjectName("textEdit_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(150, 310, 51, 41))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color : rgb(141, 169, 196)")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(120, 460, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color : rgb(141, 169, 196)")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.textEdit_3 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_3.setGeometry(QtCore.QRect(100, 530, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.textEdit_3.setFont(font)
        self.textEdit_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.textEdit_3.setStyleSheet("background-color : rgb(19, 64, 116);\n"
" border-radius: 10px;\n"
" padding: 6px;\n"
"color : rgb(141, 169, 196)\n"
"")
        self.textEdit_3.setObjectName("textEdit_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(470, 310, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color : rgb(141, 169, 196)")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.textEdit_4 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_4.setGeometry(QtCore.QRect(450, 380, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.textEdit_4.setFont(font)
        self.textEdit_4.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.textEdit_4.setStyleSheet("background-color : rgb(19, 64, 116);\n"
" border-radius: 10px;\n"
" padding: 6px;\n"
"color : rgb(141, 169, 196)\n"
"")
        self.textEdit_4.setObjectName("textEdit_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(690, 50, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color : rgb(141, 169, 196)")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(470, 160, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color : rgb(141, 169, 196)")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.textEdit_5 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_5.setGeometry(QtCore.QRect(680, 230, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.textEdit_5.setFont(font)
        self.textEdit_5.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.textEdit_5.setStyleSheet("background-color : rgb(19, 64, 116);\n"
" border-radius: 10px;\n"
" padding: 6px;\n"
"color : rgb(141, 169, 196)\n"
"")
        self.textEdit_5.setObjectName("textEdit_5")
        self.textEdit_6 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_6.setGeometry(QtCore.QRect(480, 230, 91, 51))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.textEdit_6.setFont(font)
        self.textEdit_6.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.textEdit_6.setStyleSheet("background-color : rgb(19, 64, 116);\n"
" border-radius: 10px;\n"
" padding: 6px;\n"
"color : rgb(141, 169, 196)\n"
"")
        self.textEdit_6.setObjectName("textEdit_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(100, 50, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color : rgb(141, 169, 196)")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(460, 50, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color : rgb(141, 169, 196)")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(670, 160, 151, 41))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color : rgb(141, 169, 196)")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(-10, 110, 1651, 21))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color : rgb(141, 169, 196)")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(-10, 10, 1361, 21))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("color : rgb(141, 169, 196)")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(350, 620, 210, 61))
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color : rgb(19, 64, 116);\n"
" border-radius: 7px;\n"
" padding: 5px;\n"
"color : rgb(141, 169, 196)\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.predict)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "برنامه پبشبینی قیمت لپ تاپ"))
        self.label.setText(_translate("Dialog", "Cpu"))
        self.label_2.setText(_translate("Dialog", "Gpu"))
        self.label_3.setText(_translate("Dialog", "ram size"))
        self.label_4.setText(_translate("Dialog", "Disk size"))
        self.label_5.setText(_translate("Dialog", "Display"))
        self.label_6.setText(_translate("Dialog", "Disk Type"))
        self.label_7.setText(_translate("Dialog", "Performance"))
        self.label_8.setText(_translate("Dialog", "Storage"))
        self.label_9.setText(_translate("Dialog", "Screen Size"))
        self.label_10.setText(_translate("Dialog", "=========================================================================================================================================================================================================================================================================================================================================="))
        self.label_11.setText(_translate("Dialog", "=============================================================================================================================================================================================================================="))
        self.pushButton.setText(_translate("Dialog", "پیشبینی قیمت"))

    def validate_inputs(self, inputs):
        """Validate user inputs before prediction"""
        for field, value in inputs.items():
            if not value or value.strip() == "":
                return False, f"Please fill in the {field} field"
        
        try:
            int(inputs['ram'])
            int(inputs['disk_size'])
            float(inputs['inch'])  # Changed to float for display size
        except ValueError:
            return False, "RAM, Disk Size, and Display must be numbers"
        
        return True, ""

    def validate_inputs(self, inputs):
        """Validate user inputs before prediction"""
        for field, value in inputs.items():
            if not value or value.strip() == "":
                return False, f"Please fill in the {field} field"
        
        try:
            # Try to convert RAM (handle if there are extra characters)
            ram_value = inputs['RAM'].strip()
            # Remove any non-digit characters
            ram_digits = ''.join(filter(str.isdigit, ram_value))
            if not ram_digits:
                return False, "RAM must be a number (e.g., 8, 16, 32)"
            int(ram_digits)
            
            # Try to convert Disk Size
            disk_value = inputs['Disk Size'].strip()
            disk_digits = ''.join(filter(str.isdigit, disk_value))
            if not disk_digits:
                return False, "Disk Size must be a number (e.g., 256, 512, 1024)"
            int(disk_digits)
            
            # Try to convert Display Size
            inch_value = inputs['Display Size'].strip()
            # Allow decimal points for display size
            inch_clean = ''.join(c for c in inch_value if c.isdigit() or c == '.')
            if not inch_clean:
                return False, "Display must be a number (e.g., 13.3, 15.6)"
            float(inch_clean)
        except ValueError:
            return False, "RAM, Disk Size, and Display must be valid numbers"
        
        return True, ""


    def predict(self):
        try:
            # Get input values
            input_cpu = self.textEdit.toPlainText().strip()
            input_gpu = self.textEdit_2.toPlainText().strip()
            input_ram = self.textEdit_3.toPlainText().strip()
            input_disk_size = self.textEdit_4.toPlainText().strip()
            input_disk_type = self.textEdit_6.toPlainText().strip()
            input_inch = self.textEdit_5.toPlainText().strip()


            # Clean the numeric inputs - remove any non-numeric characters except decimal point
            
            # For RAM and Disk Size (integers)
            input_ram_clean = re.sub(r'[^\d]', '', input_ram)  # Remove everything except digits
            input_disk_size_clean = re.sub(r'[^\d]', '', input_disk_size)
            
            # For inch (float)
            input_inch_clean = re.sub(r'[^\d\.]', '', input_inch)  # Keep digits and decimal point
            

            # Validate that we have valid numbers after cleaning
            if not input_ram_clean:
                QMessageBox.warning(None, "Input Error", "Please enter a valid RAM size (e.g., 8, 16, 32)")
                return
                
            if not input_disk_size_clean:
                QMessageBox.warning(None, "Input Error", "Please enter a valid Disk size (e.g., 256, 512, 1024)")
                return
                
            if not input_inch_clean:
                QMessageBox.warning(None, "Input Error", "Please enter a valid Display size (e.g., 13.3, 15.6, 17.3)")
                return

            # Convert and clean inputs
            input_cpu = input_cpu.lower()
            input_gpu = input_gpu.lower()
            
            try:
                input_ram = int(input_ram_clean)
            except ValueError:
                QMessageBox.warning(None, "Input Error", 
                    f"RAM '{input_ram}' is not a valid number. Please enter like: 8, 16, 32")
                return
                
            try:
                input_disk_size = int(input_disk_size_clean)
            except ValueError:
                QMessageBox.warning(None, "Input Error", 
                    f"Disk size '{input_disk_size}' is not a valid number. Please enter like: 256, 512, 1024")
                return
                
            try:
                input_inch = float(input_inch_clean)
            except ValueError:  
                QMessageBox.warning(None, "Input Error", 
                    f"Display size '{input_inch}' is not a valid number. Please enter like: 13.3, 15.6, 17.3")
                return
            
            input_disk_type = input_disk_type.lower()


            # Transform input using the fitted encoders
            try:
                input_cpu_encoded = self.le_cpu.transform([input_cpu])[0]
            except ValueError:
                input_cpu_encoded = -1  
            
            try:
                input_gpu_encoded = self.le_gpu.transform([input_gpu])[0]
            except ValueError:
                input_gpu_encoded = -1  
            
            try:
                input_disk_type_encoded = self.le_disk_type.transform([input_disk_type])[0]
            except ValueError:
                input_disk_type_encoded = -1

            # Prepare input data
            new_data = [[
                input_cpu_encoded,
                input_gpu_encoded,
                input_ram,
                input_disk_size,
                input_disk_type_encoded,
                input_inch
            ]]

            # Make prediction
            predicted_price = self.clf.predict(new_data)
            
            # Display result
            result_text = f"Predicted Price: {predicted_price[0]:,} تومان"
            self.result_label.setText(result_text)
        

        except Exception as e:
            QMessageBox.critical(None, "Prediction Error", 
                f"An unexpected error occurred:\n{str(e)}\n\nPlease check all inputs and try again.")
            import traceback
            traceback.print_exc()  # Print full traceback for debugging

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    sqlConnector = sqlite3.connect('database.db')
    cursor = sqlConnector.cursor()
    command = "SELECT * FROM sqlite_master WHERE type='table' AND name = 'data';"
    result = cursor.execute(command).fetchall()
    
    if result == []:
        command = """
        CREATE TABLE data (
            cpu VARCHAR(255),
            gpu VARCHAR(255),
            ram VARCHAR(255),
            diskSize INT,
            diskType VARCHAR(255),
            inch VARCHAR(255),
            price INT
        );
        """


        cursor.execute(command)
        sqlConnector.commit()
        pageNumber = 1

        # finding all the pages with  data
        while (pageNumber <= 63):
            print("======================================================" + str(pageNumber) + "======================================================")
            pageUrl = f"https://api2.zoomit.ir/catalog/api/products/search?pageNumber={pageNumber}&categorySlug=laptop&pageSize=40"

            request = requests.get(pageUrl)

            # check if request is sent to server 
            if request.status_code == 200:
                data = request.json()
            

                # check if there is data in that page
                if "products" not in data or len(data["products"]) == 0:
                    break
                else:
                    print("data in page " + str(pageNumber))
                    pageNumber += 1

                    # main object of Json, containing everything
                    products = data["products"]

                    # array containing Json data of each laptop in Json file
                    product = products["source"]
                    

                    counter = 0


                    for item in product:
                        var = list(map(item.get, item.keys()))


                        price = int(var[7])
                        specifications = var[6]
                    

                        for spec in specifications:
                            if 'help-storage-ram' in spec['title']:
                                storage_text = spec['secondaryValue']


                                # Finding ram size
                                ram_size = spec['primaryValue']
                                ram_size = ram_size.split(" ")
                                ram_size = ram_size[0]

                                # Find disk size
                                space_filter = storage_text.split(" ")
                                for i, item in enumerate(space_filter):
                                    if item.isdigit():
                                        size = int(item)
                                        # Check if next item indicates terabytes
                                        if i + 1 < len(space_filter) and 'ترابایت' in space_filter[i + 1]:
                                            disk_size = size * 1024  # Convert TB to GB
                                        else:
                                            disk_size = size  # Assume GB if no terabyte indicator  
                                # Detect disk type
                                if 'SSD' in storage_text.upper():
                                    disk_type = 'SSD'
                                elif 'HDD' in storage_text.upper() or 'هارد' in storage_text:
                                    disk_type = 'HDD'
                                elif 'NVMe' in storage_text.upper():
                                    disk_type = 'NVMe SSD'
                                elif 'M.2' in storage_text.upper():
                                    disk_type = 'M.2 SSD'
                                else:
                                    disk_type = 'Unknown'
                        
                            for spec in specifications:
                                if 'help-resolution-displaysize' in spec['title']:
                                    size = spec['primaryValue']
                                    # Extract numeric values
                                    size_inches=  size.replace('اینچ', '').strip()
                        

                            for spec in specifications:
                                # Getting cpu and gpu from api
                                if 'help-gpu-cpu' in spec['title']:
                                    cpu = spec['primaryValue']
                                    if "اینتل" in cpu:
                                        cpu = cpu.split(" ")
                                        cpu[0] = "Intel"
                                        cpu = " ".join(cpu)
                                        if "اینتل" in cpu:
                                            cpu = cpu.split(" ")
                                            cpu.remove("اینتل") 
                                            cpu = " ".join(cpu)
                                    if "کوالکام" in cpu:
                                        cpu = cpu.split(" ")
                                        cpu[0] = "Qualcomm"
                                        cpu = " ".join(cpu)
                                        if "کوالکام" in cpu:
                                            cpu = cpu.split(" ")
                                            cpu.remove("کوالکام") 
                                            cpu = " ".join(cpu)

                                    pattern = r'M\d+\s*(?:Pro|Max|Ultra|Plus)?\s*\d*'
                                    match = re.search(pattern, cpu)
                                    
                                    if match:
                                        cpu =  match.group().strip()
                                    gpu = spec['secondaryValue']
                                    if "کوالکام" in gpu:
                                        gpu = gpu.split(" ")
                                        gpu[0] = "Qualcomm"
                                        gpu = " ".join(gpu)
                                        if "کوالکام" in gpu:
                                            gpu = gpu.split(" ")
                                            gpu.remove("کوالکام") 
                                            gpu = " ".join(gpu)        
                                    if "انویدیا" in gpu:
                                        gpu = gpu.split(" ")
                                        gpu[0] = "Nvidia"
                                        gpu = " ".join(gpu)
                                        if "انویدیا" in gpu:
                                            gpu = gpu.split(" ")
                                            gpu.remove("انویدیا")
                                            gpu = " ".join(gpu)
                                    if "اینتل" in gpu:
                                        gpu = cpu.split(" ")
                                        gpu[0] = "Intel"
                                        gpu = " ".join(gpu)
                                        if gpu and ('amd' in gpu.lower()):
                                            gpu =  gpu.strip()
                                    if "گرافیک" in gpu:
                                        gpu = gpu.split(" ")
                                        for p in gpu:
                                            if p == "گرافیک":
                                                gpu.remove("گرافیک")
                                            elif p == "گرافیکی":
                                                gpu.remove("گرافیکی")
                                        gpu =" ".join(gpu)
                                    if "یکپارچه" in gpu:
                                        gpu = "onboard"

                                    if "M1" in cpu or "M2" in cpu or "M3" in cpu  or "M4" in cpu or "M5" in cpu:
                                        gpu = "onboard"

                                    if "M" in cpu and "Pro" in cpu or "pro" in cpu: 
                                        cpu = cpu.split(" ")
                                        cpu = cpu[:2]
                                        cpu = " ".join(cpu)


                        query = "INSERT INTO data (cpu, gpu, ram, diskSize, diskType, inch, price) VALUES (?, ?, ?, ?, ?, ?, ?)"
                        val = (cpu.lower(), gpu.lower(), ram_size, disk_size, disk_type.lower(), size_inches, price)
                                        
                        print(f"{cpu} - {gpu} - {ram_size} - {disk_size} - {disk_type} - {size_inches} - {price}")

                        cursor.execute(query, val)
                        sqlConnector.commit() 

            else:   
                break

        try:
            ui = Ui_Dialog()
            ui.setupUi(Dialog)
            Dialog.show()
            sys.exit(app.exec_())
        except Exception as e:
            QMessageBox.critical(None, "Fatal Error", 
                f"Failed to start application:\n{e}")
            sys.exit(1)   
    else:
        try:
            ui = Ui_Dialog()
            ui.setupUi(Dialog)
            Dialog.show()
            sys.exit(app.exec_())
        except Exception as e:
            QMessageBox.critical(None, "Fatal Error", 
                f"Failed to start application:\n{e}")
            sys.exit(1)