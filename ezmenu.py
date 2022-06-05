from pynput import keyboard
import copy
import os


class SelectMenu(object):
    '''
    複数の選択肢を提示し、矢印キーの入力を受けカーソルを動かす。
    エンターで選択肢を確定すると返り値として、選択肢のindexもしくは選択した選択肢を返す。
    
    Atributes
    ---------
    message : str. Default is None.
        選択肢の上部に表示するメッセージを指定する。
    choices : list or tuple.
        選択肢を指定する。配列の先頭から順に表示される。
    choices_tmp : list.
        choicesをもとに、numbersの指定に応じて各選択肢の先頭に通しの番号を結合したもの。
    position : int
        カーソルの初期位置を指定する。
        0から始まり、0は一番上部に位置する選択肢を示す。
    numbers : bool
        Trueの場合、選択肢の先頭に通し番号をつける。
    cursor : str
        カーソルとして用いる文字を指定する。半角推奨。
    choice : int
        選択した選択肢のindex。
    confirmed : bool
        選択が確定した状態であるかを示す。
        Trueが指定された状態になると、startメソッドでreconfirm=Trueが指定されていない限り
        キー入力の待機が終了し、選択が確定したことになる。
    side_by_side : bool
        Trueを指定した場合、メッセージの下に選択肢を横並びに表示する。
        Falseを指定した場合、メッセージの下に選択肢を縦並びに表示する。
    '''

    def __init__(self, choices, message=None, position=0, numbers=False, cursor='>', side_by_side=False, return_kinds='index'):
        '''
        Parameters
        choices : list or tuple.
            選択肢を指定する。配列の先頭から順に表示される。
        position : int. Default is 0.
            カーソルの初期位置を指定する。
            0から始まり、0は一番上部に位置する選択肢を示す。
        numbers : bool. Default is False.
            Trueの場合、選択肢の先頭に通し番号をつける。
        cursor : str. Default is '>'
            カーソルとして用いる文字を指定する。半角推奨。
        side_by_side : bool
            Trueを指定した場合、メッセージの下に選択肢を横並びに表示する。
            Falseを指定した場合、メッセージの下に選択肢を縦並びに表示する。
        return_kinds : str. Default is 'index'
            返り値に渡す内容そ指定する。
            'index'を指定した場合は、選択肢のindexを返す。
            'title'を指定した場合は、選択肢を返す。
            'both'を指定した場合は、(<index>, <選択肢>)の形式で返す。
        '''
        self.message = message
        self.choices=choices
        if numbers == True:
            self.choices_temp = [str(i) + " " + choices[i] for i in range(len(choices))]
        else:
            self.choices_temp = copy.copy(choices)

        self.cursor = cursor
        self.position = self.fix_position(position)
        self.choice = None
        self.numbers = numbers
        self.side_by_side = side_by_side
        self.return_kinds = return_kinds
    
    def start(self, message=None, return_kinds=None, side_by_side=None, position=None):
        '''
        メニューを表示し、入力を待機する。
        選択肢が選ばれれば選択肢のindexもしくは選ばれた選択肢を返す。
        
        Parameters
        ----------
        message : str. Default is None.
            選択し上部に表示するメッセージ。
            省略可能。
        return_kinds : str. Default is None
            返り値に渡す内容そ指定する。
            指定がなければ、self.return_kindsの指定に従う。
            'index'を指定した場合は、選択肢のindexを返す。
            'title'を指定した場合は、選択肢を返す。
            'both'を指定した場合は、(<index>, <選択肢>)の形式で返す。
        position : int. Default is None.
            カーソルの初期位置を指定する。
            指定がなければself.positionに従う。
        '''
        if message==None:
            message = self.message
        if return_kinds==None:
            return_kinds = self.return_kinds
        if side_by_side==None:
            side_by_side = self.side_by_side
        if position!=None:
            self.position = position
        
        os.system('cls')
        self.confirmed = False
        while not self.confirmed:
            self.display(message, side_by_side)
            with keyboard.Listener(on_press=self.press) as listener:
                listener.join()

            os.system('cls')
       
        out = None
        if return_kinds == "title":
            out = self.choices[self.choice]
        elif return_kinds == "index":
            out = self.choice
        elif return_kinds == "both":
            out = (self.choice, self.choices[self.choice])
        else:
            pass

        return out


    def display(self, message=None, side_by_side=None):
        '''選択肢をメッセージの下に表示する。'''

        if message==None:
            message=self.message
        if side_by_side==None:
            side_by_side=self.side_by_side
        
        if message != None:
            print(message)

        if side_by_side:
            for i in range(len(self.choices_temp)):
                if i == self.position:      #カーソルを合わせる選択肢
                    print('  ' + self.cursor + ' ' + self.choices_temp[i], end='')
                else:
                    print("    " + self.choices_temp[i], end='')
            print()
        else:
            for i in range(len(self.choices_temp)):
                if i == self.position:      #カーソルを合わせる選択肢
                    print(self.cursor + " " + self.choices_temp[i])
                else:
                    print("  " + self.choices_temp[i])


    # カーソルの位置を制限する
    def fix_position(self, position):
        while True:
            num = len(self.choices)
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
                print("   " + Yes + "    " + self.cursor + " " + No)
            else:
                print(" " + self.cursor + " " + Yes + "    " + "  " + No)

            with keyboard.Listener(on_press=self.press_confirm) as listener:
                listener.join()
            
            os.system('cls')


    def press(self, key):
        '''
        メニュー選択でのキー入力に対する動作の指定
        
        Parameter
        ---------
        key : keyboard.Key
            入力され得たkeyを指定するpynpt.keyboard.Keyオブジェクト。
        '''
        if key == keyboard.Key.up:
            self.position = self.fix_position(self.position - 1)
            self.confirmed = False
            return False
        
        elif key == keyboard.Key.down:
            self.position = self.fix_position(self.position + 1)
            self.confirmed = False
            return False
        
        elif key == keyboard.Key.left:
            self.position = 0
            self.cofirmed = False
            return False

        elif key == keyboard.Key.right:
            self.position = len(self.choices) - 1
            self.confirmed = False
            return False

        elif key == keyboard.Key.enter:
            self.choice = self.position
            self.confirmed = True
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
