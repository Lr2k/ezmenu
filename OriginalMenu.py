from pynput import keyboard
import copy
import os


class Select_menu:

    # titles:リスト型で選択肢を渡す
    # position=0:カーソルの初期位置を指定する。0は一番上、titlesの長さから1引いた値を渡すと一番下になる。
    # numbers=False:Trueにすると選択肢の頭に通し番号をつける。
    # curosr=">":カーソルとして使う文字を指定する。半角推奨。
    def __init__(self, titles, position=0, numbers=False, consor=">"):
        self.titles = titles
        if numbers == True:
            self.titles_temp = [str(i) + " " + titles[i] for i in range(len(titles))]
        else:
            self.titles_temp = copy.copy(titles)

        self.consor = consor
        self.position = self.fix_position(position)
        self.selection = None
        self.numbers = numbers
    

    # キー入力の制御
    # message=None:選択画面上部に質問として表示するメッセージ
    # confirm_message=None:選択後の確認画面で表示するメッセージ
    # confirm_yes="Yes":選択後の確認画面で承認を意味する選択肢を指定する
    # confirm_no="No": 選択後の確認画面で否定を意味する選択肢を指定する
    # reply="title":戻り値の形式を指定する。titleを選択すると選択肢が返る。indexを選択するとindexが返る。
    def start(self, message=None, confirm_message=None, confirm_yes="Yes", confirm_no="No", reply="title"):
        # self.confirm...確認画面でYesを選択するとFalseになる。
        # 
        
        os.system('cls')
        self.confirm = True

        while self.confirm:

            self.display(message)
            with keyboard.Listener(on_press=self.press) as listener:
                listener.join()
            
            if self.selection != None:
                os.system('cls')
                self.confirmation(confirm_message, confirm_yes, confirm_no)

                if self.confirm == True:
                    self.selection = None
            
            os.system('cls')
        
        out = None
        if reply == "title":
            out = self.titles[self.position]
        elif reply == "index":
            out = self.position

        return out


    # 選択肢を表示する
    def display(self, message):
        
        if message != None:
            print(message)

        for i in range(len(self.titles_temp)):
            if i == self.position:      #カーソルを合わせる選択肢
                print(self.consor + " " + self.titles_temp[i])
            else:
                print("  " + self.titles_temp[i])
        
    # カーソルの位置を制限する
    def fix_position(self, position):
        while True:
            num = len(self.titles)
            if position < 0:
                position += num
            
            elif position >= num:
                position -=num

            else:
                break

        return position   

    # 選択を確定するか確認する
    def confirmation(self, confirm_message, Yes, No):

        self.confirm_conf = True
        while self.confirm_conf:
            
            if confirm_message != None:
                print(confirm_message + " : ", end="")
            print(self.selection)
            
            # self.confirm...True:No False:Yes
            if self.confirm == True:
                print("   " + Yes + "    " + self.consor + " " + No)
            else:
                print(" " + self.consor + " " + Yes + "    " + "  " + No)

            with keyboard.Listener(on_press=self.press_confirm) as listener:
                listener.join()
            
            os.system('cls')


    def press(self, key):
        if key == keyboard.Key.up:
            self.position = self.fix_position(self.position - 1)
            return False
        
        elif key == keyboard.Key.down:
            self.position = self.fix_position(self.position + 1)
            return False
        
        elif key == keyboard.Key.left:
            self.position = 0
            return False

        elif key == keyboard.Key.right:
            self.position = len(self.titles) - 1
            return False

        elif key == keyboard.Key.enter:
            self.selection = self.titles[self.position]
            return False
        
        else:
            pass
    def press_confirm(self, key):
        if (key == keyboard.Key.right) or (key == keyboard.Key.left):
            self.confirm = not self.confirm     # bool値反転
            return False
        
        elif key == keyboard.Key.enter:
            self.confirm_conf = False
            return False
        
        else:
            pass
