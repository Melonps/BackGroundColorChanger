import random


def get_random_color_code(file_path):
    # ファイルを読み取りモードで開く
    with open(file_path, "r", encoding="Shift-JIS") as file:
        # ファイルから行ごとにデータを読み込む
        lines = file.readlines()

    # 行から不要な空白文字を削除
    lines = [line.strip() for line in lines if line.strip()]

    if not lines:
        # ファイルが空または無効な行がない場合はNoneを返す
        return None

    # ランダムに行を選択
    random_line = random.choice(lines)

    # 選択された行をスペースで分割して色コードとその他のデータに分ける
    color_code, _ = random_line.split(" ", 1)

    return color_code


# # テキストファイルのパスを指定してランダムな色コードを取得
# file_path = "color_data.txt"  # ファイルパスを実際のファイルパスに変更してください
# random_color = get_random_color_code(file_path)

# if random_color:
#     print("ランダムな色コード:", random_color)
# else:
#     print("無効なデータが含まれているか、ファイルが空です。")
