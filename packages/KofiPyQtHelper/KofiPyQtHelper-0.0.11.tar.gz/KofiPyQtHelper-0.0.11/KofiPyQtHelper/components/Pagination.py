#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-07-12 11:07:50
LastEditors  : Kofi
LastEditTime : 2023-07-12 11:17:09
Description  : 
"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QLineEdit,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QSplitter,
)


class Pagination(QWidget):
    Signal_PageNumChange = pyqtSignal(int, int)

    def __init__(
        self,
        name: str = "pagination",
        currentPage: int = 1,
        pageSize: int = 10,
        buttonWidth: int = 60,
        buttonHeight: int = 32,
        preText: str = "上一页",
        nextText: str = "下一页",
        skipText: str = "跳转",
        pageSizeItems: list = ["10", "20", "30"],
        **kwargs
    ) -> None:
        super(Pagination, self).__init__()
        # 当前页
        self.currentPage = currentPage
        # 每页显示记录数
        self.pageSize = pageSize
        # 总页数
        self.totalPage = 0
        # 总记录数
        self.totalCount = 0

        rightLayout = QHBoxLayout()
        self.prevButton = QPushButton(preText)
        self.prevButton.setFixedSize(buttonWidth, buttonHeight)
        self.prevButton.clicked.connect(self.prevClickEvent)
        self.nextButton = QPushButton(nextText)
        self.nextButton.setFixedSize(buttonWidth, buttonHeight)
        self.nextButton.clicked.connect(self.nextClickEvent)
        self.currentPageLine = QLineEdit()
        self.currentPageLine.setFixedWidth(30)
        self.currentPageLine.setValidator(QIntValidator())
        self.currentPageLine.setText(str(self.currentPage))
        self.skipButton = QPushButton(skipText)
        self.skipButton.setFixedSize(buttonWidth, buttonHeight)
        self.skipButton.clicked.connect(self.skipClickEvent)

        rightLayout.addWidget(self.prevButton)
        rightLayout.addWidget(self.nextButton)
        rightLayout.addWidget(self.currentPageLine)
        rightLayout.addWidget(self.skipButton)
        rightLayout.setSpacing(5)

        leftLayout = QHBoxLayout()
        self.totalCountLabel = QLabel("共 {} 项,".format(self.totalCount))
        self.totalCountLabel.setContentsMargins(0, 0, 10, 0)
        self.pageSizeCommbo = QComboBox()
        self.pageSizeCommbo.addItems(pageSizeItems)
        self.pageSizeCommbo.currentIndexChanged.connect(self.pageChangeEvent)
        leftLayout.setSpacing(0)
        leftLayout.addWidget(self.totalCountLabel)
        leftLayout.addWidget(QLabel("每页"))
        leftLayout.addWidget(self.pageSizeCommbo)
        leftLayout.addWidget(QLabel("项"))

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addWidget(QSplitter())
        mainLayout.addLayout(rightLayout)

        self.setLayout(mainLayout)
        self.setObjectName(name)

    def prevClickEvent(self):
        if self.currentPage - 1 > 0:
            self.currentPage -= 1
            self.Signal_PageNumChange.emit(self.currentPage, self.pageSize)
        self.updateStatus()

    def nextClickEvent(self):
        if self.currentPage + 1 < self.totalPage:
            self.currentPage += 1
            self.Signal_PageNumChange.emit(self.currentPage, self.pageSize)
        self.updateStatus()

    def skipClickEvent(self):
        newCurrent = int(self.currentPageLine.text())
        if newCurrent != self.currentPage:
            if newCurrent > 0 and newCurrent <= self.totalPage:
                self.currentPage = newCurrent
                self.Signal_PageNumChange.emit(self.currentPage, self.pageSize)
        self.updateStatus()

    def pageChangeEvent(self):
        self.pageSize = int(self.pageSizeCommbo.getCurrentText())
        self.Signal_PageNumChange.emit(self.currentPage, self.pageSize)
        self.updateStatus()

    def updateStatus(self):
        self.totalCountLabel.setText("共 {} 项,".format(self.totalCount))
        self.currentPageLine.setText(str(self.currentPage))

    def loadPage(self, totalCount, totalPage, currentPage):
        self.currentPage = currentPage
        self.totalCount = totalCount
        self.totalPage = totalPage
        self.updateStatus()
