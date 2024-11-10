import sys
from PyQt5 import QtCore, QtWidgets, QtOpenGL, uic
from model.dcsource import dcSource
from model.vfd import vfd
from model.oscilloscope import oscilloscope
import model.devices as devices

s2i = lambda x: int(x) if x else 0
s2f = lambda x: float(x) if x else 0

f2s = lambda x: int(('%0.2f'%(x)).replace('.',''))
f2t = lambda x: int(('%0.1f'%(x)).replace('.',''))

class dashLoadCurveLog(QtWidgets.QWidget):
    def __init__(self,parent=None):
        self.dataRowsNo = 1
        self.set = False
        self.control = 'N'
        self.dir = 0
        super(dashLoadCurveLog,self).__init__(parent)

        self.container = QtWidgets.QVBoxLayout(self)
        self.container.setContentsMargins(0, 0, 0, 0)

        self.static_data = QtWidgets.QGroupBox(self)
        self.static_data_layout = QtWidgets.QVBoxLayout()
        self.static_data_layout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.static_data_layout.setSpacing(2)
        self.static_data.setLayout(self.static_data_layout)

        self.motor_data = QtWidgets.QGroupBox(self)
        self.motor_data.setTitle("Motor Parameters")
        self.motor_data_layout = QtWidgets.QHBoxLayout()
        self.motor_data_layout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.motor_data_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.motor_data_layout.setSpacing(50)
        self.motor_data.setLayout(self.motor_data_layout)
        
        self.motorID_container = QtWidgets.QHBoxLayout()
        self.motorID_lab = QtWidgets.QLabel(self)
        self.motorID_lab.setText("Motor &ID")
        self.motorID = QtWidgets.QLineEdit(self)
        self.motorID_lab.setBuddy(self.motorID)
        self.motorID_container.addWidget(self.motorID_lab,alignment=QtCore.Qt.AlignRight)
        self.motorID_container.addWidget(self.motorID    ,alignment=QtCore.Qt.AlignLeft)
        self.motorID_container.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.motor_data_layout.addLayout(self.motorID_container)

        self.motorT_container = QtWidgets.QHBoxLayout()
        self.motorT_lab = QtWidgets.QLabel(self)
        self.motorT_lab.setText("Rated &Torque")
        self.motorT = QtWidgets.QLineEdit(self)
        self.motorT_lab.setBuddy(self.motorT)
        self.motorT_container.addWidget(self.motorT_lab,alignment=QtCore.Qt.AlignRight)
        self.motorT_container.addWidget(self.motorT    ,alignment=QtCore.Qt.AlignLeft)
        self.motorT_container.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.motor_data_layout.addLayout(self.motorT_container)

        self.motorN_container = QtWidgets.QHBoxLayout()
        self.motorN_lab = QtWidgets.QLabel(self)
        self.motorN_lab.setText("Rated S&peed")
        self.motorN = QtWidgets.QLineEdit(self)
        self.motorN_lab.setBuddy(self.motorN)
        self.motorN_container.addWidget(self.motorN_lab,alignment=QtCore.Qt.AlignRight)
        self.motorN_container.addWidget(self.motorN    ,alignment=QtCore.Qt.AlignLeft)
        self.motorN_container.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.motor_data_layout.addLayout(self.motorN_container)

        self.motorV_container = QtWidgets.QHBoxLayout()
        self.motorV_lab = QtWidgets.QLabel(self)
        self.motorV_lab.setText("Rated &Voltage")
        self.motorV = QtWidgets.QLineEdit(self)
        self.motorV_lab.setBuddy(self.motorV)
        self.motorV_container.addWidget(self.motorV_lab,alignment=QtCore.Qt.AlignRight)
        self.motorV_container.addWidget(self.motorV    ,alignment=QtCore.Qt.AlignLeft)
        self.motorV_container.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.motor_data_layout.addLayout(self.motorV_container)

        self.motorI_container = QtWidgets.QHBoxLayout()
        self.motorI_lab = QtWidgets.QLabel(self)
        self.motorI_lab.setText("Max &Current")
        self.motorI = QtWidgets.QLineEdit(self)
        self.motorI_lab.setBuddy(self.motorI)
        self.motorI_container.addWidget(self.motorI_lab,alignment=QtCore.Qt.AlignRight)
        self.motorI_container.addWidget(self.motorI    ,alignment=QtCore.Qt.AlignLeft)
        self.motorI_container.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.motor_data_layout.addLayout(self.motorI_container)

        self.vfd_data = QtWidgets.QGroupBox(self)
        self.vfd_data.setTitle("VFD Parameters")
        self.vfd_data_layout = QtWidgets.QHBoxLayout()
        self.vfd_data_layout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.vfd_data_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.vfd_data_layout.setSpacing(50)
        self.vfd_data.setLayout(self.vfd_data_layout)

        self.control_container = QtWidgets.QGroupBox(self)
        self.control_container.setTitle("Mode")
        self.control_container_layout = QtWidgets.QHBoxLayout()
        self.control_container_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.control_container_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.control_container_layout.setSpacing(20)
        self.control_container.setLayout(self.control_container_layout)
        self.controlT = QtWidgets.QRadioButton(self)
        self.controlT.setText("Torque")
        self.controlT.checkStateSet
        self.controlN = QtWidgets.QRadioButton(self)
        self.controlN.setText("Speed")
        self.controlN.setChecked(True)
        self.control_container_layout.addWidget(self.controlT   ,alignment=QtCore.Qt.AlignLeft)
        self.control_container_layout.addWidget(self.controlN   ,alignment=QtCore.Qt.AlignLeft)
        self.vfd_data_layout.addWidget(self.control_container)

        self.direction_container = QtWidgets.QGroupBox(self)
        self.direction_container.setTitle("Direction")
        self.direction_container_layout = QtWidgets.QHBoxLayout()
        self.direction_container_layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.direction_container_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.direction_container_layout.setSpacing(20)
        self.direction_container.setLayout(self.direction_container_layout)
        self.directionCW = QtWidgets.QRadioButton(self)
        self.directionCW.setText("Clockwise")
        self.directionCCW = QtWidgets.QRadioButton(self)
        self.directionCCW.setText("Anti-Clockwise")
        self.directionCCW.setChecked(True)
        self.direction_container_layout.addWidget(self.directionCW  ,alignment=QtCore.Qt.AlignLeft)
        self.direction_container_layout.addWidget(self.directionCCW ,alignment=QtCore.Qt.AlignLeft)
        self.vfd_data_layout.addWidget(self.direction_container)

        self.static_data_layout.addWidget(self.motor_data,0)
        self.static_data_layout.addWidget(self.vfd_data,0)

        self.static_data.setDisabled(self.set)
        self.container.addWidget(self.static_data,0)

        self.set_btn = QtWidgets.QPushButton(self)
        self.set_btn.setText("Set")
        self.set_btn.clicked.connect(self.setStaticParams)
        self.container.addWidget(self.set_btn,alignment=QtCore.Qt.AlignRight)

        
        #===========================================================#

        spacer = QtOpenGL.QGLWidget(self)
        self.container.addWidget(spacer,alignment=QtCore.Qt.AlignHCenter)
        self.container.addSpacerItem(QtWidgets.QSpacerItem(1,30,QtWidgets.QSizePolicy.MinimumExpanding,QtWidgets.QSizePolicy.Maximum))

        self.dynamic_data = QtWidgets.QGroupBox(self)
        self.dynamic_data_layout = QtWidgets.QVBoxLayout()
        self.dynamic_data_layout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.dynamic_data_layout.setSpacing(2)
        self.dynamic_data.setLayout(self.dynamic_data_layout)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setColumnStretch(0,2)
        self.layout.setColumnStretch(1,4)
        self.layout.setColumnStretch(2,4)
        self.layout.setColumnStretch(3,4)
        self.layout.setColumnStretch(4,4)
        self.layout.setColumnStretch(5,4)
        self.layout.setColumnStretch(6,4)
        self.layout.setColumnStretch(7,4)
        self.layout.setColumnStretch(8,4)
        self.layout.setColumnStretch(9,4)
        self.layout.setColumnStretch(10,4)
        self.layout.setColumnStretch(11,3)
        self.layout.setColumnStretch(12,3)
        self.dynamic_data_layout.addLayout(self.layout,0)

        self.loadHeader()
        self.dataTable = QtWidgets.QVBoxLayout()
        self.dataTable.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.dataTable.setAlignment(QtCore.Qt.AlignCenter)
        self.dynamic_data_layout.addLayout(self.dataTable,0)

        actions = QtWidgets.QHBoxLayout()
        self.addRowbtn = QtWidgets.QPushButton(self)
        self.addRowbtn.setText("+")
        self.addRowbtn.clicked.connect(self.addLoadRow)
        actions.addWidget(self.addRowbtn,alignment=QtCore.Qt.AlignHCenter)

        self.runAllbtn = QtWidgets.QPushButton(self)
        self.runAllbtn.setText(">>")
        self.runAllbtn.clicked.connect(self.runAll)
        actions.addWidget(self.runAllbtn,alignment=QtCore.Qt.AlignHCenter)

        self.dynamic_data_layout.addSpacerItem(QtWidgets.QSpacerItem(1,1,QtWidgets.QSizePolicy.MinimumExpanding,QtWidgets.QSizePolicy.MinimumExpanding))
        self.dynamic_data_layout.addLayout(actions,0)

        [self.addRowbtn.click() for _ in range(4)]

        self.dynamic_data.setDisabled(not self.set)
        self.container.addWidget(self.dynamic_data)

        self.dcS = [dcSource(port) for port in devices.DCS]
        self.vfd = vfd(devices.VFD)
        self.osc = oscilloscope(devices.OSC)

    def loadHeader(self):
        load_l = QtWidgets.QLabel(self)
        load_l.setText("Load %")
        self.layout.addWidget(load_l,0,0,2,2,alignment=QtCore.Qt.AlignCenter)

        con_ip_l = QtWidgets.QLabel(self)
        con_ip_l.setText("Controller i/p")
        self.layout.addWidget(con_ip_l,0,2,1,3,alignment=QtCore.Qt.AlignHCenter)

        cont_op_l = QtWidgets.QLabel(self)
        cont_op_l.setText("Controller o/p")
        self.layout.addWidget(cont_op_l,0,5,1,3,alignment=QtCore.Qt.AlignHCenter)

        motor_op_l = QtWidgets.QLabel(self)
        motor_op_l.setText("Motor o/p")
        self.layout.addWidget(motor_op_l,0,8,1,3,alignment=QtCore.Qt.AlignHCenter)

        cont_v_ip_l = QtWidgets.QLabel(self)
        cont_v_ip_l.setText("Voltage i/p")
        self.layout.addWidget(cont_v_ip_l,1,2,alignment=QtCore.Qt.AlignHCenter)

        cont_i_ip_l = QtWidgets.QLabel(self)
        cont_i_ip_l.setText("Current i/p")
        self.layout.addWidget(cont_i_ip_l,1,3,alignment=QtCore.Qt.AlignHCenter)

        cont_p_ip_l = QtWidgets.QLabel(self)
        cont_p_ip_l.setText("Power i/p")
        self.layout.addWidget(cont_p_ip_l,1,4,alignment=QtCore.Qt.AlignHCenter)

        cont_v_op_l = QtWidgets.QLabel(self)
        cont_v_op_l.setText("Voltage o/p")
        self.layout.addWidget(cont_v_op_l,1,5,alignment=QtCore.Qt.AlignHCenter)

        cont_i_op_l = QtWidgets.QLabel(self)
        cont_i_op_l.setText("Current o/p")
        self.layout.addWidget(cont_i_op_l,1,6,alignment=QtCore.Qt.AlignHCenter)

        cont_p_op_l = QtWidgets.QLabel(self)
        cont_p_op_l.setText("Power o/p")
        self.layout.addWidget(cont_p_op_l,1,7,alignment=QtCore.Qt.AlignHCenter)

        motor_rpm_l = QtWidgets.QLabel(self)
        motor_rpm_l.setText("Motor RPM")
        self.layout.addWidget(motor_rpm_l,1,8,alignment=QtCore.Qt.AlignHCenter)

        motor_tor_l = QtWidgets.QLabel(self)
        motor_tor_l.setText("Motor Torque")
        self.layout.addWidget(motor_tor_l,1,9,alignment=QtCore.Qt.AlignHCenter)

        motor_pow_l = QtWidgets.QLabel(self)
        motor_pow_l.setText("Motor Power")
        self.layout.addWidget(motor_pow_l,1,10,alignment=QtCore.Qt.AlignHCenter)

        run_l = QtWidgets.QLabel(self)
        run_l.setText("Run")
        self.layout.addWidget(run_l,1,11,alignment=QtCore.Qt.AlignHCenter)

        del_l = QtWidgets.QLabel(self)
        del_l.setText("Del")
        self.layout.addWidget(del_l,1,12,alignment=QtCore.Qt.AlignHCenter)

    def setStaticParams(self):
        self.set ^= True
        self.static_data.setDisabled(self.set)
        self.dynamic_data.setDisabled(not self.set)

        if self.set:
            self.dir = 0 if self.directionCW.isChecked() else 1

            if self.controlT.isChecked():
                self.control = 'T'
                maxT = s2i(self.motorT.text())
                maxT = f2t(maxT)
                self.vfd.setTorq(maxT)
            else:
                self.control = 'N'
                maxN = s2i(self.motorN.text()) /30
                maxN = f2t(maxN)
                self.vfd.setSpeed(maxN)

            volt = s2i(self.motorV.text())
            curr = s2i(self.motorI.text())

            for dc in self.dcS:
                dc.setVoltage(volt)
                dc.setCurrent(curr//5)

            ## Setup OSC Measurements ##
            self.osc.measure('rms',1,1)
            self.osc.measure('rms',2,2)
            self.osc.measure('rms',3,3)
            self.osc.measure('rms',4,4)
            self.osc.measure('rms',5,5)
            self.osc.measure('rms',6,6)

            self.osc.start()

        else:
            [dc.turnOFF() for dc in self.dcS]
            self.vfd.stop()
        
    def addLoadRow(self):
        if self.dataRowsNo <= 8:
            row = loadRow(self)
            self.dataTable.addWidget(row)
            if self.dataRowsNo == 8:
                self.addRowbtn.setDisabled(True)
        self.dataRowsNo += 1

    def runAll(self):
        [self.dataTable.itemAt(i).widget().runbtn.click() for i in range(self.dataRowsNo)]

class loadRow(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(loadRow,self).__init__(parent)
        self.parent = parent
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)

        self.load      = QtWidgets.QLineEdit(self)
        self.load.setAlignment(QtCore.Qt.AlignHCenter)
        self.load.textEdited.connect(self.updateLoad)
        self.loadtext  = QtWidgets.QLabel(self)
        # self.loadtext.setAlignment(QtCore.Qt.AlignHCenter)
        self.loadtext.setText('0000.00')
        self.cont_v_ip = QtWidgets.QLineEdit(self)
        self.cont_v_ip.setAlignment(QtCore.Qt.AlignHCenter)
        self.cont_i_ip = QtWidgets.QLineEdit(self)
        self.cont_i_ip.setAlignment(QtCore.Qt.AlignHCenter)
        self.cont_p_ip = QtWidgets.QLineEdit(self)
        self.cont_p_ip.setAlignment(QtCore.Qt.AlignHCenter)
        self.cont_v_op = QtWidgets.QLineEdit(self)
        self.cont_v_op.setAlignment(QtCore.Qt.AlignHCenter)
        self.cont_i_op = QtWidgets.QLineEdit(self)
        self.cont_i_op.setAlignment(QtCore.Qt.AlignHCenter)
        self.cont_p_op = QtWidgets.QLineEdit(self)
        self.cont_p_op.setAlignment(QtCore.Qt.AlignHCenter)
        self.motor_rpm = QtWidgets.QLineEdit(self)
        self.motor_rpm.setAlignment(QtCore.Qt.AlignHCenter)
        self.motor_tor = QtWidgets.QLineEdit(self)
        self.motor_tor.setAlignment(QtCore.Qt.AlignHCenter)
        self.motor_pow = QtWidgets.QLineEdit(self)
        self.motor_pow.setAlignment(QtCore.Qt.AlignHCenter)
        
        self.runbtn = QtWidgets.QPushButton(self)
        self.runbtn.setText(">")
        self.runbtn.clicked.connect(self.runRow)

        self.delbtn = QtWidgets.QPushButton(self)
        self.delbtn.setText("-")
        self.delbtn.clicked.connect(self.delRow)

        self.layout.addWidget(self.load     ,alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.loadtext ,alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.cont_v_ip,alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.cont_i_ip,alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.cont_p_ip,alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.cont_v_op,alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.cont_i_op,alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.cont_p_op,alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.motor_rpm,alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.motor_tor,alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.motor_pow,alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.runbtn,alignment=QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.delbtn,alignment=QtCore.Qt.AlignLeft)

        self.running = False

    def runRow(self):
        if self.running == False:
            self.running = True
            self.runbtn.setStyleSheet("background: green")

            if self.parent.control == 'T':
                load = s2i(self.parent.motorT.text()) * s2f(self.load.text()) / 100
                load = f2t(load)
                self.parent.vfd.setTorq(load)
            else:
                load = s2i(self.parent.motorN.text()) / 30 * s2f(self.load.text()) / 100
                load = f2s(load)
                self.parent.vfd.setSpeed(load)

            [dc.turnON() for dc in self.parent.dcS]
            self.parent.vfd.run(self.parent.dir)

            ## TODO: Need this in a seprate Thread ##
            while self.running:
                con_volt = [dc.measVolt() for dc in self.parent.dcS]
                self.cont_v_ip.setText('%6.2f'%(sum(con_volt)/5))

                uv_volt = self.parent.osc.getMeasurement(1)
                vw_volt = self.parent.osc.getMeasurement(2)
                wv_volt = self.parent.osc.getMeasurement(3)
                self.cont_v_op.setText('%6.2f'%((uv_volt+vw_volt+wv_volt)/3))

                con_curr = [dc.measCurr() for dc in self.parent.dcS]
                self.cont_i_ip.setText('%6.2f'%(sum(con_curr)))

                u_curr = self.parent.osc.getMeasurement(4)
                v_curr = self.parent.osc.getMeasurement(5)
                w_curr = self.parent.osc.getMeasurement(6)
                self.cont_v_op.setText('%6.2f'%(u_curr+v_curr+w_curr))

        else:
            self.running = False
            self.runbtn.setStyleSheet("background: none")
            [dc.turnOFF() for dc in self.parent.dcS]
            self.parent.vfd.stop()

    def updateLoad(self):
        if self.parent.control == 'T':
            load = s2i(self.parent.motorT.text()) * s2f(self.load.text()) / 100
            self.loadtext.setText('%8.2f'%(load))
        else:
            load = s2i(self.parent.motorN.text()) * s2f(self.load.text()) / 100
            self.loadtext.setText('%8.2f'%(load))

    def delRow(self):
        self.parent.dataRowsNo -= 1
        self.parent.addRowbtn.setEnabled(True)
        self.deleteLater()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = dashLoadCurveLog()
    window.showMaximized()
    sys.exit(app.exec_())