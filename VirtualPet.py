import sys, pickle,datetime,os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import ftp
#UI

formclass = uic.loadUiType("virtualpet.ui")[0]
#宠物类
class VirtualPetWindow(QtWidgets.QMainWindow, formclass):
    #初始化
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.doctor = False
        # Initializes values
        self.walking = False
        self.sleeping = False
        self.playing = False
        self.eating = False
        self.time_cycle = 0
        self.hunger = 0
        self.happiness  = 8
        self.health = 8
        self.forceAwake = False
        #成长值
        self.growth = 0
        self.year = 0
        # Lists images for animations
        self.sleepImages = ["img/sleep1.gif","img/sleep2.gif","img/sleep3.gif",
                            "img/sleep4.gif"]
        self.eatImages = ["img/eat1.gif", "img/eat2.gif", "img/eat3.gif", "img/eat4.gif", "img/eat5.gif", "img/eat6.gif", "img/eat7.gif", "img/eat8.gif", "img/eat9.gif"]
        self.walkImages = ["img/walk1.gif", "img/walk2.gif", "img/walk3.gif", "img/walk4.gif", "img/walk5.gif", "img/walk6.gif", "img/walk7.gif", "img/walk8.gif", "img/walk9.gif", "img/walk10.gif", "img/walk11.gif", "img/walk12.gif"]
        self.playImages = ["img/play1.gif", "img/play2.gif", "img/play3.gif", "img/play4.gif", "img/play5.gif", "img/play6.gif", "img/play7.gif", "img/play8.gif"]
        self.doctorImages = ["img/doc1.gif", "img/doc2.gif"]
        self.nothingImages  = ["img/pet1.gif", "img/pet2.gif", "img/pet3.gif", "img/pet4.gif", "img/pet5.gif", "img/pet6.gif", "img/pet7.gif", "img/pet8.gif", "img/pet9.gif", "img/pet10.gif", "img/pet11.gif", "img/pet12.gif", "img/pet13.gif", "img/pet13.gif"]

        self.imageList = self.nothingImages
        self.imageIndex = 0

        # Connects event handlers for toolbar buttons
        self.actionStop.triggered.connect(self.stop_Click)
        self.actionFeed.triggered.connect(self.feed_Click)
        self.actionWalk.triggered.connect(self.walk_Click)
        self.actionPlay.triggered.connect(self.play_Click)
        self.actionDoctor.triggered.connect(self.doctor_Click)

        # Sets up timers
        self.myTimer1 = QtCore.QTimer(self)
        self.myTimer1.start(500)
        self.myTimer1.timeout.connect(self.animation_timer)
        self.myTimer2 = QtCore.QTimer(self)
        self.myTimer2.start(5000)
        self.myTimer2.timeout.connect(self.tick_timer)

        filehandle = True
        # Tries to open pickle file
        try:
            file = open("savedata_vp.pkl", "rb")
        except:
            filehandle = False
        if filehandle:
            os.remove("savedata_vp.pkl")
            ftp.down()
            file = open("savedata_vp.pkl", "rb")
            save_list = pickle.load(file)  # Reads from pickle file if open
            file.close()
        else:
            save_list = [8, 8, 0, datetime.datetime.now(), 0, 0, 0]  # Uses default values if pickle file not open
        # Pulls individual values out of list
        self.happiness = save_list[0]
        self.health    = save_list[1]
        self.hunger    = save_list[2]
        timestamp_then = save_list[3]
        self.time_cycle = save_list[4]
        self.growth = save_list[5]
        self.year = save_list[6]

        # Checks how long since last run
        difference = datetime.datetime.now() - timestamp_then
        ticks = int(difference.seconds / 50)
        for i in range(0, ticks):
            # Simulates all ticks that happened during down time
            self.time_cycle += 1
            if self.time_cycle % 5 == 0:
                self.growth += 1
            if self.growth >= 365:
                self.growth = 0
                self.year += 1
            if self.time_cycle == 60:
                self.time_cycle = 0
            if self.time_cycle <= 48:  # Awake
                self.sleeping = False
                if self.hunger < 8:
                    self.hunger += 1
            else:  # Sleeping
                self.sleeping = True
                if self.hunger < 8 and self.time_cycle % 3 == 0:
                    self.hunger += 1
            if self.hunger == 7 and (self.time_cycle % 2 ==0) \
                                and self.health > 0:
                self.health -= 1
            if self.hunger == 8 and self.health > 0:
                self.health -=1
        # Uses correct animation—awake or sleeping
        if self.sleeping:
            self.imageList = self.sleepImages
            self.label_state.setText("状态:睡觉")
        else:
            self.imageList = self.nothingImages
            self.label_state.setText("状态:无事")

    def sleep_test(self):
        # Checks if pet is sleeping before doing an action
        if self.sleeping:
            result = (QtWidgets.QMessageBox.warning(self, '警告', "你确定要将你的宠物叫醒?这样太没良心了!",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,  # Buttons to show
                    QtWidgets.QMessageBox.No))  # Default button

            if result == QtWidgets.QMessageBox.Yes:
                self.sleeping = False
                self.happiness -= 4
                self.forceAwake = True
                return True
            else:
                return False
        else:
            return True

    # The doctor button event handler
    def doctor_Click(self):
        if self.sleep_test():
            self.imageList = self.doctorImages
            self.doctor = True
            self.walking = False
            self.eating = False
            self.playing = False
            self.label_state.setText("状态:寻医")

    # The feed button event handler
    def feed_Click(self):
        if self.sleep_test():
            self.imageList = self.eatImages
            self.eating = True
            self.walking = False
            self.playing = False
            self.doctor = False
            self.label_state.setText("状态:喂食")

    # The play button event handler
    def play_Click(self):
        if self.sleep_test():
            self.imageList = self.playImages
            self.playing = True
            self.walking = False
            self.eating = False
            self.doctor = False
            self.label_state.setText("状态:玩耍")

    # The walk button event handler
    def walk_Click(self):
        if self.sleep_test():
            self.imageList = self.walkImages
            self.walking = True
            self.eating = False
            self.playing = False
            self.doctor = False
            self.label_state.setText("状态:散步")

    # The stop button event handler
    def stop_Click(self):
        if not self.sleeping:
            self.imageList = self.nothingImages
            self.walking = False
            self.eating = False
            self.playing = False
            self.doctor = False
            self.label_state.setText("状态:无事")

    def animation_timer(self):
        # The animation timer (every 0.5 sec) event handler
        if self.sleeping and not self.forceAwake:
            self.imageList = self.sleepImages
        self.imageIndex += 1
        if self.imageIndex >= len(self.imageList):
            self.imageIndex = 0
        icon = QtGui.QIcon()
        # Updates pet’s image (animation)
        current_image = self.imageList[self.imageIndex]
        icon.addPixmap(QtGui.QPixmap(current_image),
                       QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.petPic.setIcon(icon)
        self.label_hunger.setText("饱食度:"+str((8-self.hunger)*(100/8.0)))
        self.label_happiness.setText("愉悦度:"+str(self.happiness*(100/8.0)))
        self.label_health.setText("健康度:"+str(self.health*(100/8.0)))
        self.label_growth.setText("天数:"+str(self.growth))
        self.label_year.setText("年数:"+str(self.year))


    def tick_timer(self):  # Start of main 5 sec timer event handler
        # Checks if sleeping or awake
        self.time_cycle += 1
        if self.time_cycle == 60:
            self.time_cycle = 0
        if self.time_cycle <= 48 or self.forceAwake:
            self.sleeping = False
        else:
            self.sleeping = True
            self.label_state.setText("状态:睡觉")
        if self.time_cycle == 0:
            self.forceAwake = False
        if self.time_cycle % 5 == 0:
            self.growth += 1
        if self.growth >= 365:
            self.growth == 0
            self.year += 1
        if self.doctor:
            # Adds or subtracts units depending on activity
            self.health += 1
            self.hunger += 1
        elif self.walking and (self.time_cycle % 2 == 0):
            self.happiness += 1
            self.health += 1
            self.hunger += 1
        elif self.playing:
            self.happiness += 1
            self.hunger += 1
        elif self.eating:
            self.hunger -= 2
        elif self.sleeping:
            if self.time_cycle % 3 == 0:
                self.hunger += 1
        else:
            self.hunger += 1
            if self.time_cycle % 2 == 0:
                self.happiness -= 1
        # Makes sure values are not out of range
        if self.hunger > 8:  self.hunger = 8
        if self.hunger < 0:  self.hunger = 0
        if self.hunger == 7 and (self.time_cycle % 2 ==0) :
            self.health -= 1
        if self.hunger == 8:
            self.health -=1
        if self.health > 8:  self.health = 8
        if self.health < 0:  self.health = 0
        if self.happiness > 8:  self.happiness = 8
        if self.happiness < 0:  self.happiness = 0
        if self.growth > 365:  self.growth = 365
        if self.growth < 0:  self.growth = 0
        # Updates label
        self.label_hunger.setText("饱食度:"+str((8-self.hunger)*(100/8.0)))
        self.label_happiness.setText("愉悦度:"+str(self.happiness*(100/8.0)))
        self.label_health.setText("健康度:"+str(self.health*(100/8.0)))
        self.label_growth.setText("天数:"+str(self.growth))
        self.label_year.setText("年数:"+str(self.year))
            

    def closeEvent(self, event):
        # Saves status and timestamp to pickle file
        file = open("savedata_vp.pkl", "wb")  # Line-continuation character
        save_list = [self.happiness, self.health, self.hunger, \
                     datetime.datetime.now(), self.time_cycle, self.growth, self.year]
        pickle.dump(save_list, file)
        event.accept()

    def menuExit_selected(self):
        self.close()

app = QtWidgets.QApplication(sys.argv)
myapp = VirtualPetWindow()
myapp.show()
app.exec_()
