import os
from lxml import etree
import numpy as np
from tqdm import tqdm

from BackGroundColorChanger.help_function.util import get_random_color_code
from BackGroundColorChanger.S3Interface.s3_data_manipulation import S3Interface

file_count = 1
page_width = 1000
x_start = 0
file_path = "color_data.txt"


def check_svg_directory(directory: str, fontsize: float, color: str, s3_instance):
    """
    指定されたディレクトリ内のSVGファイルを処理し、フォントサイズに基づいてバックグラウンドカラーを追加します。

    Parameters:
        directory (str): 処理対象のディレクトリパス。
        fontsize (float): フォントサイズの最小値。このサイズ以上のフォントが処理対象となります。
        color (str): 背景カラーの16進数表記。

    Returns:
        None
    """
    for root, dirs, files in os.walk(directory):
        for dir_path in dirs:
            for file_name in tqdm(files, desc="Processing SVG Files"):
                if file_name.lower().endswith(".svg") and "txt" not in file_name:
                    file_path_in = os.path.join(root, file_name)
                    dir_path_out = os.path.dirname(file_path_in)
                    file_process(file_path_in, fontsize, color, s3_instance)


def file_process(
    file_path_in: str, fontsize: float, color: str, s3_instance: S3Interface
):
    """
    単一のSVGファイルを処理し、フォントサイズに基づいてバックグラウンドカラーを追加します。

    Parameters:
        file_path_in (str): 処理対象のSVGファイルパス。
        fontsize (float): フォントサイズの最小値。このサイズ以上のフォントが処理対象となります。
        color (str): 背景カラーの16進数表記。
        dir_path_out (str): 出力ディレクトリパス。

    Returns:
        None
    """
    if color is None:
        color = get_random_color_code(file_path)
    is_changed = 0
    rectangles = []

    tree = etree.parse(file_path_in)
    root = tree.getroot()

    for i in root.findall(".//{http://www.w3.org/2000/svg}desc"):
        char_info = i.attrib
        if "fontName" in char_info and "fontRect" in char_info:
            font_rect = char_info["fontRect"]
            split_data = list(map(float, font_rect.split(",")))
            font_size = split_data[3] - split_data[1]
            if font_size > fontsize:
                i.set("frag", "T")
                if not rectangles or abs(rectangles[-1][1] - split_data[1]) > (
                    fontsize / 2
                ):
                    char_count = 1
                    new_rectangle = split_data + [char_count]
                    rectangles.append(new_rectangle)
                else:
                    rectangles[-1][4] += 1
                    rectangles[-1][2] = split_data[2]

    for i in root.findall(".//{http://www.w3.org/2000/svg}desc"):
        char_info = i.attrib
        if (
            "fontName" in char_info
            and "fontRect" in char_info
            and "frag" not in char_info
        ):
            font_rect = char_info["fontRect"]
            split_data = list(map(float, font_rect.split(",")))

            for j in range(len(rectangles)):
                if rectangles[j][4] > 3:
                    if rectangles[j][1] < split_data[1] < rectangles[j][3]:
                        i.set("frag", "T")
                else:
                    if (
                        rectangles[j][1] < split_data[1] < rectangles[j][3]
                        and rectangles[j][0] < split_data[0] < rectangles[j][2]
                        and rectangles[j][0] < split_data[2] < rectangles[j][2]
                    ):
                        i.set("frag", "T")

    for i in range(len(rectangles)):
        if rectangles[i][4] > 3:
            new_rect = etree.Element("{http://www.w3.org/2000/svg}rect")
            new_rect.set("width", str(page_width))
            new_rect.set("height", str(rectangles[i][3] - rectangles[i][1] + 10))
            new_rect.set("x", str(x_start))
            new_rect.set("y", str(rectangles[i][1] - 5))
            new_rect.set("fill", color)
            root.append(new_rect)
        else:
            new_rect = etree.Element("{http://www.w3.org/2000/svg}rect")
            new_rect.set("width", str(rectangles[i][2] - rectangles[i][0] + 10))
            new_rect.set("height", str(rectangles[i][3] - rectangles[i][1] + 10))
            new_rect.set("x", str(rectangles[i][0] - 5))
            new_rect.set("y", str(rectangles[i][1] - 5))
            new_rect.set("fill", color)
            root.append(new_rect)

    for i in root.findall(".//{http://www.w3.org/2000/svg}desc"):
        char_info = i.attrib
        if "fontName" in char_info and "fontRect" in char_info and "frag" in char_info:
            path = i.getnext()
            char_info = path.attrib
            new_path = etree.Element("{http://www.w3.org/2000/svg}path")
            new_path.set("d", char_info["d"])
            new_path.set("fill", "#FFFFFF")
            root.append(new_path)
            is_changed = 1

    tree = etree.ElementTree(root)
    if is_changed == 1:
        write_path = file_path_in.replace(".svg", f"_changed_#{color}.svg")
        print(f"Writing to {write_path}")
        tree.write(write_path, encoding="UTF-8", xml_declaration=True)
        s3_instance.upload_svg_to_s3(write_path)
        os.remove(write_path)
