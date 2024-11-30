#!/usr/bin/env python
# -*- coding:utf-8 -*-

import xlsxwriter
import xlrd


class FileImport(object):
    """
        文件导入
    """
    def __init__(self, filename):
        self.filename = filename

    def read_file(self):
        info = {"code": False, "msg": "", "data": ""}
        try:
            workbook = xlrd.open_workbook(self.filename)
            for sheet_name in workbook.sheet_names():
                sheet = workbook.sheet_by_name(sheet_name)
                field = sheet.row_values(1)
                for num in range(2, sheet.nrows):
                    rows = sheet.row_values(num)
                    info["data"] = dict(zip(field, rows))
                    info["code"] = True
                    yield info
        except Exception as e:
            info["msg"] = str(e)
        return info


class FileExport(object):
    """
        文件导出
    """
    def __init__(self, filename, model):
        self.filename = filename
        self.model = model

    def write_file(self):
        info = {"code": False, "msg": ""}
        try:
            export_fields = ["ID", "序列号", "主机名称", "IP地址", "CPU", "内存(G)", "磁盘(G)", "供应商",
                             "区域位置", "资产编码", "资产型号", "备注信息", "到期时间"]
            if self.model is not None:
                workbook = xlsxwriter.Workbook(self.filename)
                worksheet = workbook.add_worksheet()
                cell_format = workbook.add_format({"bold": True})
                cell_format.set_font_size(12)

                # 设置A列宽度30
                # worksheet.set_column('A:A', 30)
                # 设置第3行高度为20
                # worksheet.set_row(3, 20)

                rows, cols = 0, 0
                for n in export_fields:
                    worksheet.write(rows, cols, n, cell_format)
                    cols += 1

                rows, cols = 1, 0
                for h in self.model:
                    worksheet.write(rows, cols, h.id)
                    worksheet.write(rows, cols + 1, h.serial_number)
                    worksheet.write(rows, cols + 2, h.hostname)
                    worksheet.write(rows, cols + 3, h.ip)
                    worksheet.write(rows, cols + 4, h.cpu)
                    worksheet.write(rows, cols + 5, h.memory)
                    worksheet.write(rows, cols + 6, h.disk)
                    worksheet.write(rows, cols + 7, h.cloud)
                    worksheet.write(rows, cols + 8, h.region)
                    worksheet.write(rows, cols + 9, h.asset_number)
                    worksheet.write(rows, cols + 10, h.model_number)
                    worksheet.write(rows, cols + 11, h.comment)
                    worksheet.write(rows, cols + 12, h.deadline_time)
                    rows += 1

                workbook.close()
                info["code"] = True
            else:
                info["msg"] = "model 不能为None"
        except Exception as e:
            info["msg"] = str(e)
        return info
