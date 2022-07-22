from pynput import keyboard
import copy
import os


class SelectMenu(object):
    '''
    複数の選択肢を提示し、矢印キーの入力を受けカーソルを動かす。
    エンターで選択肢を確定すると返り値として、選択肢のindexもしくは選択した選択肢を返す。
    
    Atributes
    ---------
    message : str.
        選択肢の上部に表示するメッセージを指定する。
    choices : list or tuple.
        選択肢を指定する。配列の先頭から順に表示される。
    bottom_message : str.
        選択肢の下部に表示するメッセージを指定する。
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

    def __init__(self, choices=None, message=None, bottom_message=None, position=0, numbers=False, cursor='>', side_by_side=False, return_kinds='index'):
        '''
        Parameters
        choices : list or tuple.
            選択肢を指定する。配列の先頭から順に表示される。
        position : int. Default is 0.
            カーソルの初期位置を指定する。
            0から始まり、0は一番上部に位置する選択肢を示す。
        bottom_message : str. Default is None.
            選択肢の下部に表示するメッセージを指定する。
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
        self.choices = choices if choices is not None else list()
        self.bottom_message = bottom_message
        self.choices_tmp = list()
        self.cursor = cursor
        self.position = self.fix_position(position)
        self.choice = None
        self.numbers = numbers
        self.side_by_side = side_by_side
        self.sbs_tmp = side_by_side # pressメソッドに引数を渡せないため、self.side_by_sideを変更せずに共有する
        self.return_kinds = return_kinds
    
    def start(self, choices=None, message=None, bottom_message=None, return_kinds=None, side_by_side=None, position=None, numbers=None):
        '''
        メニューを表示し、入力を待機する。
        選択肢が選ばれれば選択肢のindexもしくは選ばれた選択肢を返す。
        
        Parameters
        ----------
        message : str. Default is None.
            選択し上部に表示するメッセージ。
            省略可能。
        bottom_message : str. Default is None.
            選択肢の下部に表示するメッセージを指定する。
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
        if choices is None:
            choices = self.choices
        if message is None:
            message = self.message
        if bottom_message is None:
            bottom_message = self.bottom_message
        if return_kinds is None:
            return_kinds = self.return_kinds
        if side_by_side is None:
            side_by_side = self.side_by_side
        self.sbs_tmp = side_by_side
        if position is not None:
            self.position = position
        if numbers is None:
            numbers = self.numbers
        
        if numbers == True:
            self.choices_tmp = [str(i) + " " + choices[i] for i in range(len(choices))]
        else:
            self.choices_tmp = copy.copy(choices)
        
        os.system('cls')
        self.confirmed = False
        self.sbs_temp = side_by_side
        while not self.confirmed:
            self.display(message, side_by_side, bottom_message)
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


    def display(self, message=None, side_by_side=None, bottom_message=None):
        '''選択肢をメッセージの下に表示する。'''

        if message is None:
            message=self.message
        if side_by_side is None:
            side_by_side=self.side_by_side
        if bottom_message is None:
            bottom_message = self.bottom_message
        
        if message is not None:
            print(message)

        if side_by_side:
            for i in range(len(self.choices_tmp)):
                if i == self.position:      #カーソルを合わせる選択肢
                    print('  ' + self.cursor + ' ' + self.choices_tmp[i], end='')
                else:
                    print("    " + self.choices_tmp[i], end='')
            print()
        else:
            for i in range(len(self.choices_tmp)):
                if i == self.position:      #カーソルを合わせる選択肢
                    print(self.cursor + " " + self.choices_tmp[i])
                else:
                    print("  " + self.choices_tmp[i])
        
        if bottom_message is not None:
            print(bottom_message)


    def fix_position(self, position):
        '''
        カーソルの位置を選択しのある範囲に収める

        Parameters
        ----------
        position : int
            現在のカーソルの位置
        
        Return
        ------
        position : int
            修正後のカーソルの位置
        '''
        num = len(self.choices_tmp)
        if num==0:
            pass
        elif position < 0:
            position = 0
        elif position >= num:
            position = num - 1
        else:
            pass

        return position


    def press(self, key):
        '''
        メニュー選択でのキー入力に対する動作の指定
        
        Parameter
        ---------
        key : keyboard.Key
            入力され得たkeyを指定するpynpt.keyboard.Keyオブジェクト。
        '''
        if self.sbs_tmp:
            if key == keyboard.Key.left:
                # 一つ前の選択肢へ
                self.position = self.fix_position(self.position - 1)
                self.confirmed = False
                return False
            
            elif key == keyboard.Key.right:
                # 次の選択肢へ
                self.position = self.fix_position(self.position + 1)
                self.confirmed = False
                return False
            
            elif key == keyboard.Key.up:
                # 最初の選択肢へ
                self.position = 0
                self.cofirmed = False
                return False

            elif key == keyboard.Key.down:
                # 最後の選択肢へ
                self.position = len(self.choices_tmp) - 1
                self.confirmed = False
                return False

            elif key == keyboard.Key.enter:
                # 確定
                self.choice = self.position
                self.confirmed = True
                # SelectMenu表示後、input()で入力を受けようとするとエンターが入力されてしまうため 
                input()
                return False        
            else:
                pass

        else:
            # 選択肢が縦に並べられている場合                
            if key == keyboard.Key.up:
                # 一つ前の選択肢へ
                self.position = self.fix_position(self.position - 1)
                self.confirmed = False
                return False
            
            elif key == keyboard.Key.down:
                # 次の選択肢へ
                self.position = self.fix_position(self.position + 1)
                self.confirmed = False
                return False
            
            elif key == keyboard.Key.left:
                # 最初の選択肢へ
                self.position = 0
                self.cofirmed = False
                return False

            elif key == keyboard.Key.right:
                # 最後の選択肢へ
                self.position = len(self.choices_tmp) - 1
                self.confirmed = False
                return False

            elif key == keyboard.Key.enter:
                # 確定
                self.choice = self.position
                self.confirmed = True
                # SelectMenu表示後、input()で入力を受けようとするとエンターが入力されてしまうため 
                input()
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
