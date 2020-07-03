from PIL import Image
import pytesseract
import cv2
import re
from data.get_date_int import get_date_int
from data.init_database import get_connection
import datetime
import random

SCREENSHOT_PATH = 'screenshots/screen.png'


def preprocess(img_path: str, crop: (float, float, float, float), ex_color: str='YELLOW'):
    """
    :param ex_color: YELLOW/BLUE 需要加强的颜色
    :param img_path: relative path of image
    :type crop: tuple (minX, minY, maxX, maxY)
    """
    img = Image.open(img_path).convert('RGB')
    width, height = img.size
    img = img.crop((width*crop[0], height*crop[1], width*crop[2], height*crop[3]))  # 截取需要的部分

    data = img.getdata()
    new_data = []
    for item in data:
        if ex_color == 'YELLOW' and (item[0] + item[1]) / (item[2] + 1) >= 3:  # 将图片黄色部分替换为纯黑
            new_data.append((0, 0, 0))
            continue
        if ex_color == 'BLUE' and (item[0] + item[1]) / (item[2] + 1) <= 1.4:
            new_data.append((0, 0, 0))
            continue
        else:
            new_data.append(item)  # 其余部分不变
            continue
    img.putdata(new_data)
    img.save("intermediate.jpg", "JPEG")

    image = cv2.imread("intermediate.jpg")
    gray = image * 1.5 - 100  # 增加对比度
    if ex_color == 'BLUE':
        gray = image * 1.5

    filename = "output.png"  # 写至 output.png
    cv2.imwrite(filename, gray)


def recognize_text_to_record_list(img_path: str, crop: (float, float, float, float) = (0.7, 0.25, 0.9, 0.9)) -> list:
    """
        :param img_path: relative path of image
        :type crop: tuple (minX, minY, maxX, maxY)
    """

    preprocess(img_path, crop)

    text: str = recognize_text('output.png')
    # print(text)
    record_list: list = process_text(text)

    preprocess(img_path=img_path, crop=(0.1, 0.16, 0.225, 0.23), ex_color='BLUE')
    text = recognize_text('output.png')
    rank_number = int(''.join(filter(str.isdigit, text)))
    date = datetime.datetime.now()
    date_int: int = get_date_int(date, with_hour=True)
    c = get_connection()
    c.execute('INSERT INTO rank_record (date, rank)'
              'VALUES (?, ?)'
              'ON CONFLICT(date)'
              'DO UPDATE SET rank=?', (date_int, rank_number, rank_number))
    c.commit()
    print(rank_number)

    return record_list


def recognize_text(img_path) -> str:
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
    tessdata_dir_config = '--tessdata-dir "C:/Program Files (x86)/Tesseract-OCR/tessdata"'
    img = Image.open(img_path)
    return pytesseract.image_to_string(img, lang='chi_sim', config=tessdata_dir_config)


def process_text(text: str) -> list:
    # 下面将（和{替换成了1，因为有时候1会被识别成这两个字符
    text = text.replace(' ', '')
    split = re.split('\n\n+', text)  # 以空白行分割字符串
    filtered = list(filter(lambda t: '伤害' in t or '造成了' in t, split))  # 必须包含伤害 或 造成了
    record_list = list()
    for record in filtered:
        record_split = re.split('\n', record)
        if len(record_split) != 3:  # 必须是3行
            continue
        username = record_split[0].replace('对', '')
        target = record_split[1].replace('造成了', '')
        damage_text = record_split[2].replace('{', '1').replace('(', '1').replace('）', '1')
        damage_search = re.findall(r'\d+', damage_text)
        if len(damage_search) > 0:
            damage = damage_search[0]
        else:
            continue
        # if '击破' in damage_text:
        #     damage = JSONEditor().get_remaining_health()
        record_list.append([username, target, damage])
    return record_list


def image_to_position(image) -> (float, float):
    image_path = 'templates/' + str(image) + '.png'
    print(image_path)
    screen = cv2.imread(SCREENSHOT_PATH, 0)
    template = cv2.imread(image_path, 0)
    methods = [cv2.TM_CCOEFF_NORMED, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED]
    image_x, image_y = template.shape[:2]
    result = cv2.matchTemplate(screen, template, methods[0])
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.8:
        random_x = random.randint(-5, 5)
        random_y = random.randint(-5, 5)
        center = (max_loc[0] + image_y / 2 + random_y, max_loc[1] + image_x / 2 + random_x)
        print(center)
        return center
    else:
        return None


if __name__ == '__main__':
    recognize_text_to_record_list('../../screenshots/screen.png')
