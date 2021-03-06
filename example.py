from ezmenu import SelectMenu
import time

choices = [
    "獅白ぼたん",
    "猫又おかゆ",
    "戌神ころね",
    "大神ミオ",
    "白上フブキ"
]

# 選択肢を縦に並べた場合
message = "推しを選択してください。"
menu = SelectMenu(choices, cursor=">", message=message, return_kinds='title')

reconfirm_choices = ["Yes", "No"]
reconfirm = SelectMenu(choices=reconfirm_choices)

while True:
    title = menu.start()
    reconfirm_message = title + "でよろしいですか？"

    # menuに戻ってきた際に必ずカーソルの位置を一番上の選択肢に置きたい場合はstart(position=0)
    # 前回選択した位置を引き継がせたい場合は、引数を指定しない
    if reconfirm.start(message=reconfirm_message, position=1)==0:
        break

print(title)

time.sleep(3)

# 選択肢を横に並べた場合
message = "推しを選択してください。"
menu = SelectMenu(choices, cursor=">", message=message, return_kinds='title', side_by_side=True)

reconfirm_choices = ["Yes", "No"]
reconfirm = SelectMenu(choices=reconfirm_choices, side_by_side=True)

while True:
    title = menu.start()
    reconfirm_message = title + "でよろしいですか？"

    # menuに戻ってきた際に必ずカーソルの位置を一番上の選択肢に置きたい場合はstart(position=0)
    # 前回選択した位置を引き継がせたい場合は、引数を指定しない
    if reconfirm.start(message=reconfirm_message, position=1)==0:
        break

print(title)

time.sleep(3)


