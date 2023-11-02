#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-06-28 10:08:56
LastEditors  : Kofi
LastEditTime : 2023-06-28 10:30:32
Description  : 
"""
from pdf2docx import Converter


class PdfCommand:
    def __init__(self) -> None:
        self.commands.update(
            {
                "convertWord": self.convertWord,
            }
        )

    def convertWord(self, args):
        pdf_file = self.parameterSearchByName(args, "pdf")
        file_name = pdf_file.split(".")[0]
        docx_file = self.parameterSearchByName(args, "doc") + file_name + ".docx"

        start = self.parameterSearchByName(args, "start")
        start = start if start != "" else 0
        end = self.parameterSearchByName(args, "end")
        end = end if end != "" else None
        pages = self.parameterSearchByName(args, "pages")
        pages = pages.split(",") if pages != "" else None

        cv = Converter(pdf_file)
        cv.convert(docx_file, start=start, end=end, pages=pages)
        cv.close()
