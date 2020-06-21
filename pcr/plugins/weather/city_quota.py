import xlrd
import os
import config
import re

class Position(object):
    def __init__(self, file_name):
        self.file_path = os.path.join(config.PROJECT_PATH, file_name)
        excel = xlrd.open_workbook(self.file_path, encoding_override='utf8')
        self.sheet = excel.sheets()[0]  # 目标excel都只有一个sheet
        self.rows = self.sheet.nrows
        self.cols = self.sheet.ncols

    def is_exist_city(self,city)->tuple:
        for i in range(1,self.rows):
            if re.search(city,self.sheet.row_values(i)[1]) is not None:
                return True,i
        return False,-1

    def get_position(self,city)->list:
        if self.is_exist_city(city)[0]:
            line = self.is_exist_city(city)[1]
            return [self.sheet.row_values(line)[self.cols-2], self.sheet.row_values(line)[self.cols-1]]


if __name__ == '__main__':
    p = Position('adcode-release-2020-06-10.xls')
    p1 = Position('globalcities.xls')
    print(p.is_exist_city('长春市'))