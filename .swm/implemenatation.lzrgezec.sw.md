---
title: Implemenatation
---
# Introduction

This document will walk you through the implementation of the grain segmentation feature.

The feature is designed to handle image processing for grain segmentation, including UI elements for user interaction and various image processing techniques.

We will cover:

1. Initialization of UI components and parameters.
2. Handling of image acquisition and processing.
3. User interactions and manual adjustments.
4. Saving and exporting results.

# Initialization of UI components and parameters

<SwmSnippet path="/griansegmentationV2.py" line="146">

---

We start by defining the main window and initializing various parameters and UI components.

```

    # 最小化窗口函数
    def button_min_clicked(self):
        self.parent.showMinimized()

# 主窗口
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
```

---

</SwmSnippet>

<SwmSnippet path="/griansegmentationV2.py" line="155">

---

The <SwmToken path="/griansegmentationV2.py" pos="152:2:2" line-data="class MainWindow(QtWidgets.QWidget):">`MainWindow`</SwmToken> class initializes various parameters related to image processing and UI components.

```

        # Parameter initialization
        self.trigger_camera = 0
        self.trigger_camera_initial = 1
        self.trigger_image = 0
        self.trigger_acquisition = 0
        self.trigger_manual = 0
        self.trigger_line = 0
        self.trigger_acquisition_start = 0
        self.trigger_lightsignal = 0
        self.trigger_light_normal = 0
        self.trigger_lightoff = 0
        self.ret_cam = 0
        self.trigger_csv_head = 0
```

---

</SwmSnippet>

<SwmSnippet path="/griansegmentationV2.py" line="169">

---

We also initialize lists to store contours and other processing states.

```

        self.contours_add = []
        self.contours_normal = []
        self.contours_abnormal = []
        self.contours_remove = []
        self.contours_remove_normal_copy = []
        self.contours_remove_abnormal = []
        self.contours_remove_abnormal_copy= []
        self.contours_remove_normal = []
        self.line_manual = []
```

---

</SwmSnippet>

# Handling of image acquisition and processing

<SwmSnippet path="/griansegmentationV2.py" line="199">

---

The <SwmToken path="/griansegmentationV2.py" pos="202:3:3" line-data="        self.initUI()">`initUI`</SwmToken> method sets up the UI, including adapting the window size to the screen.

```

        self.mouseButton = 0

        self.initUI()

    # Create control function
    def initUI(self):
        # Get the screen size and make the window adapt to the screen. The default window size is 1260 * 750
        self.desktop = QtWidgets.QApplication.desktop()
        self.available_rect = self.desktop.availableGeometry()
        self.width_window = self.available_rect.width()
        self.height_window = self.available_rect.height()
        self.ratio_width_window = self.width_window / 1260
        self.ratio_height_window = self.height_window / 750
```

---

</SwmSnippet>

<SwmSnippet path="/griansegmentationV2.py" line="213">

---

We set the window size based on the screen dimensions.

```

        # Window size setting
        if self.ratio_width_window >= self.ratio_height_window:
            self.height_window = self.available_rect.height()
            self.width_window = self.height_window * 1.68
            self.ratio_window = self.ratio_height_window
        else:
            self.width_window = self.available_rect.width()
            self.height_window = self.width_window / 1.68
            self.ratio_window = self.ratio_width_window
```

---

</SwmSnippet>

<SwmSnippet path="/griansegmentationV2.py" line="223">

---

The image display area is configured to fit within the window.

```

        # Image display area size setting
        self.height_display_image = self.height_window * 19 / 20
        self.width_display_image = self.height_display_image * 4 / 3

        # Image size settings
        self.image_height = ceil(self.height_display_image) - 1
        if self.image_height % 3 == 0:
            self.image_height = self.image_height
        elif self.image_height % 3 == 1:
            self.image_height = self.image_height + 2
        else:
            self.image_height = self.image_height + 1
        self.image_width = int(self.image_height * (4 / 3))
        self.height_window=int(self.height_window)
        self.width_window=int(self.width_window)
```

---

</SwmSnippet>

<SwmSnippet path="/griansegmentationV2.py" line="239">

---

We set up the image display container and configure its properties.

```

        # Ratio of actual window size to default window size
        self.ratio_pixel = self.image_width * self.image_height / (936 * 702)

        # Image display area container
        self.display_image_box = QLabel(self)
        self.display_image_box.setStyleSheet(
            "QLabel{background:white;font-size:%dpx;font-family:Times New Roman;font-weight:500;}" % int(30 * self.ratio_window))
        self.display_image_box.setAlignment(QtCore.Qt.AlignCenter)
        self.display_image_box.setFixedSize(self.image_width, self.image_height)
        self.display_image_box.move(1, int(self.height_window / 20))
```

---

</SwmSnippet>

<SwmSnippet path="/griansegmentationV2.py" line="660">

---

The <SwmToken path="/griansegmentationV2.py" pos="662:3:3" line-data="    def opencamera(self):">`opencamera`</SwmToken> method handles opening the camera and setting up the video capture.

```

    # 打开相机函数
    def opencamera(self):
        self.ret, _ = self.cap.read()
        if self.ret == False:
            if language == 'zh_CN':
                message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "提示", "请检查相机与电脑是否正确连接！")
                Qyes = message.addButton(self.tr("确定"), QtWidgets.QMessageBox.YesRole)
                Qyes.setStyleSheet(
                    '''QPushButton{background:#90EE90;font-size:%dpx;font-family:宋体;font-weight:500;border-radius:5px;border:1px solid gray;}''' % int(18 * self.ratio_window))
                message.setStyleSheet('''QMessageBox{font-size:%dpx;font-family:宋体;}''' % int(20 * self.ratio_window))
            else:
                message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Tip",
                                                "Please check whether the camera and computer are connected correctly!")
                Qyes = message.addButton(self.tr("OK"), QtWidgets.QMessageBox.YesRole)
                Qyes.setStyleSheet(
                    '''QPushButton{background:#90EE90;font-size:%dpx;font-family:Times New Roman;font-weight:500;border-radius:5px;border:1px solid gray;}''' % int(18 * self.ratio_window))
                message.setStyleSheet('''QMessageBox{font-size:%dpx;font-family:Times New Roman;}''' % int(20 * self.ratio_window))
            Qyes.setFixedSize(80, 40)
            message.setWindowIcon(QIcon("%s/icon/messagebox.ico" % path_icon))
            message.setIcon(0)
```

---

</SwmSnippet>

<SwmSnippet path="/griansegmentationV2.py" line="681">

---

If the camera is not connected correctly, a warning message is displayed.

```

            if message.exec_() == QtWidgets.QMessageBox.ActionRole:
                pass
        else:
            self.display_image.resize(self.image_width, self.image_height)
            self.display_image.move(0, 0)
            self.trigger_zoom = 0
```

---

</SwmSnippet>

<SwmSnippet path="/griansegmentationV2.py" line="609">

---

The <SwmToken path="/griansegmentationV2.py" pos="617:3:3" line-data="    def showcamera(self):">`showcamera`</SwmToken> method continuously captures frames from the camera and processes them.

```

    def openRecord(self):
        win_x = self.x()
        win_y = self.y()
        self.window_allRecord = Record(self.width_window, self.height_window, win_x, win_y, self.ratio_window)
        self.window_allRecord.show()

    # 连续显示图像函数
    def showcamera(self):
        self.ret_cam, self.cam = self.cap.read()
        if self.ret_cam:
            try:
                with open("boxratio.txt", "r") as f:
                    self.widthRatio = float(f.readline())
                    self.heightRatio = float(f.readline())
                    if self.widthRatio >= 1:
                        self.widthRatio = 1
                    if self.heightRatio >= 1:
                        self.heightRatio = 1
```

---

</SwmSnippet>

# User interactions and manual adjustments

<SwmSnippet path="/griansegmentationV2.py" line="2281">

---

The <SwmToken path="/griansegmentationV2.py" pos="2282:3:3" line-data="    def mousePressEvent(self, event):">`mousePressEvent`</SwmToken>, <SwmToken path="/griansegmentation.py" pos="129:3:3" line-data="    def mouseMoveEvent(self, event):">`mouseMoveEvent`</SwmToken>, and <SwmToken path="/griansegmentation.py" pos="140:3:3" line-data="    def mouseReleaseEvent(self, QMouseEvent):">`mouseReleaseEvent`</SwmToken> methods handle user interactions for manual adjustments.

```

    def mousePressEvent(self, event):
        self.press_X = event.windowPos().x()
        self.press_Y = event.windowPos().y()
        number_contour = 0
        if event.buttons() == QtCore.Qt.LeftButton:
            self.mouseButton = 1
            try:
                self.mouse_X = event.globalPos().x()
                self.mouse_Y = event.globalPos().y()
                self.win_X = self.x()
                self.win_Y = self.y()
                self.marking_X = ((self.mouse_X - self.win_X) - self.labelx) / self.scale
                self.marking_Y = ((self.mouse_Y - self.win_Y) - self.labely - self.height_window / 20) / self.scale
```

---

</SwmSnippet>

<SwmSnippet path="/griansegmentationV2.py" line="3055">

---

The <SwmToken path="/griansegmentationV2.py" pos="3056:3:3" line-data="    def manual(self):">`manual`</SwmToken> method allows users to manually mark and adjust contours.

```

    def manual(self):
        if self.trigger_manual == 1:
            self.display_image_box.setCursor(QtCore.Qt.ArrowCursor)
            self.button_acquisition.setEnabled(True)

            if language == 'zh_CN':
                self.button_manual.setStyleSheet(
                '''QPushButton{color:white;font-size:%dpx;font-family:宋体;font-weight:500;border-radius:10px}QPushButton:hover{background:#90EE90;}''' % int(
                    24 * self.ratio_window))
            else:
                self.button_manual.setStyleSheet(
                '''QPushButton{text-align: left;color:white;font-size:%dpx;font-family:Times New Roman;font-weight:500;border-radius:10px}QPushButton:hover{background:#90EE90;}''' % int(
                    18 * self.ratio_window))
```

---

</SwmSnippet>

# Saving and exporting results

<SwmSnippet path="/griansegmentationV2.py" line="977">

---

The <SwmToken path="/griansegmentationV2.py" pos="978:3:3" line-data="    def saveimage(self):">`saveimage`</SwmToken> method saves the processed image and related data.

```

    def saveimage(self):
        if self.trigger_acquisition == 1 or self.trigger_manual:
            self.button_restore.setStyleSheet(
                '''QPushButton{border-radius:%dpx;background:#DCDCDC;}''' % int(8 * self.ratio_window))
            self.trigger_line = 0

            self.localTime = strftime("%Y-%m-%d %H:%M:%S", localtime())
            self.localTime = ''.join(filter(str.isalnum, self.localTime))
            self.localTime = self.localTime[6:]
```

---

</SwmSnippet>

<SwmSnippet path="/griansegmentationV2.py" line="746">

---

The <SwmToken path="/griansegmentation.py" pos="3619:3:3" line-data="    def exportFile(self):">`exportFile`</SwmToken> method allows users to export results to a specified directory.

```

        if self.flag == False:
            self.trigger_camera_initial = 0
            self.trigger_camera = 0
            if way == 1:
                if language == 'zh_CN':
                    message = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "提示", "请检查相机与电脑是否正确连接！")
                    Qyes = message.addButton(self.tr("确定"), QtWidgets.QMessageBox.YesRole)
                    Qyes.setStyleSheet(
                        '''QPushButton{background:#90EE90;font-size:%dpx;font-family:宋体;font-weight:500;border-radius:5px;border:1px solid gray;}''' % int(18 * self.ratio_window))
                    message.setStyleSheet('''QMessageBox{font-size:%dpx;font-family:宋体;}''' % int(20 * self.ratio_window))
```

---

</SwmSnippet>

<SwmMeta version="3.0.0" repo-id="Z2l0aHViJTNBJTNBZ3JhaW4tc2VnbWVudGF0aW9uJTNBJTNBYW5rb2p1YmhhbnVwcmFrYXNo" repo-name="grain-segmentation"><sup>Powered by [Swimm](https://app.swimm.io/)</sup></SwmMeta>
