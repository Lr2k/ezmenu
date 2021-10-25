from OriginalMenu import Select_menu
import time

titles = [
    "獅白ぼたん",
    "猫又おかゆ",
    "犬神ころね",
    "大神ミオ",
    "白上フブキ"
]

message = "推しを選択してください。"
confirm_message = "決定しますか？"

menu = Select_menu(
    titles=titles,
    position=0,
    numbers=True,
    consor=">"
)

index = menu.start(
    message=message,
    confirm_message=confirm_message,
    confirm_yes="はい",
    confirm_no="いいえ",
    reply="index"
)

print(index)
print(titles[index])

time.sleep(10)