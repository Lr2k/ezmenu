from ezmenu import SelectMenu
import time

choices = [
    "獅白ぼたん",
    "猫又おかゆ",
    "犬神ころね",
    "大神ミオ",
    "白上フブキ"
]

message = "推しを選択してください。"

menu = SelectMenu(choices, cursor=">", message=message)

index = menu.start()

reconfirm_choices = ["Yes", "No"]
reconfirm_message = choices[index] + "でよろしいですか？"

reconfirm = SelectMenu(choices=reconfirm_choices, message=reconfirm_message, side_by_side=True)

print(reconfirm.start())