# coding: utf-8
#インポート
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import webbrowser
import cairosvg
from rxnlvl import *

##### 関数 #####
# 描画ウインドウ
def viewer_window():
    global sub_win, png, base, frame, chart_image
    # 複数ウインドウの禁止
    if sub_win is None or not sub_win.winfo_exists():
        try:
            # コードの実行
            txt = txtbox.get("1.0", "end")
            exec(txt, globals())
            # svg作成
            with open("temp.svg","w", encoding = "utf-8") as file:
                file.write(p.write())
            # PNG変換
            cairosvg.svg2png(url = "temp.svg", write_to = "temp.png")

            ### ウインドウ作成 ###
            sub_win = tk.Toplevel(root)
            sub_win.configure(bg = "white")
            sub_win.resizable(width = False, height = False)
            # フレーム
            chart_image = tk.PhotoImage(file="Images/chart.png")
            label = tk.Label(sub_win, image = chart_image, text = "  Energy Level Diagram", bg = "white", compound = tk.LEFT)
            frame = tk.LabelFrame(sub_win, labelwidget = label, bg="white", padx=10, pady=10)
            frame.pack(padx = 10, pady = 10, fill = tk.BOTH, expand = 1)
            
            # 画像指定
            png = tk.PhotoImage(file = "temp.png")
            base = tk.Label(frame, image = png, bg = "white")
            base.pack(padx = 5, pady = 5, fill = tk.BOTH, expand = 1)
            
        except:
            # エラー通知
            messagebox.showerror("Error", "Check the code!!")

    # 表示の更新
    elif sub_win is not sub_win.winfo_exists():
        try:
            # コードの実行
            txt = txtbox.get("1.0", "end")
            exec(txt, globals())
            # svg作成
            with open("temp.svg","w", encoding = "utf-8") as file:
                file.write(p.write())
            # PNG変換
            cairosvg.svg2png(url = "temp.svg", write_to = "temp.png")

            # 既存ラベルの削除
            base.pack_forget()
            # 画像指定
            png = tk.PhotoImage(file = "temp.png")
            base = tk.Label(frame, image = png, bg = "white")
            base.pack(padx = 5, pady = 5, fill = tk.BOTH, expand = 1)
            
        except:
            # エラー通知
            messagebox.showerror("Error", "Check the code!!")

# 初期コード
def ic_func():
    # テキストボックスのデータ消去
    txtbox.delete("1.0","end")
    # テキストボックスへ書込み
    code = '''p = plot([25.0,10.0],vbuf=10.0,hbuf=5.0,bgcolour=None, qualified='sortof')

p +  level(energy(    0, 'kjmol'),  1,    '1',      0x0)
p +  level(energy(-85.5, 'kjmol'),  2,  'EC1',      0x0)
p +  level(energy(  244, 'kjmol'),  3, 'TS1a', 0xFF4444)
p +  level(energy(   51, 'kjmol'),  3, 'TS1b',      0x0)
p +  level(energy( -102, 'kjmol'),  4,  'DC1',      0x0)
p +  level(energy(  -82, 'kjmol'),  5,    '2',      0x0)

p +  edge(    '1',  'EC1', 0x0, 0.4, 'normal')
p +  edge(  'EC1', 'TS1a', 0x0, 0.2, 'normal')
p +  edge(  'EC1', 'TS1b', 0x0, 0.4, 'normal')
p +  edge( 'TS1a',  'DC1', 0x0, 0.2, 'normal')
p +  edge( 'TS1b',  'DC1', 0x0, 0.4, 'normal')
p +  edge(  'DC1',    '2', 0x0, 0.4, 'normal')

p + baseline(energy( 0.0, 'kjmol'),colour=0x0,mode='dashed',opacity=0.1)
'''
    txtbox.insert("1.end", code)

# SVG保存
def save_svg():
    # 保存ダイアログの表示
    typ = [("SVG File","*.svg")] 
    save_path = tk.filedialog.asksaveasfilename(filetypes = typ, defaultextension = "svg")
    
    # ファイルが選択された場合データを書き込み
    if len(save_path) != 0:
        try:
            # コードの実行
            txt = txtbox.get("1.0", "end")
            exec(txt, globals())
            # svg作成
            with open(save_path,"w", encoding = "utf-8") as file:
                file.write(p.write())
        except:
            # エラー通知
            messagebox.showerror("Error", "Check the code!!")
# PNG保存
def save_png():
    # 保存ダイアログの表示
    typ = [("PNG File","*.png")] 
    save_path = tk.filedialog.asksaveasfilename(filetypes = typ, defaultextension = "png")
    
    # ファイルが選択された場合データを書き込み
    if len(save_path) != 0:
        try:
            # コードの実行
            txt = txtbox.get("1.0", "end")
            exec(txt, globals())
            # svg作成
            with open("temp.svg","w", encoding = "utf-8") as file:
                file.write(p.write())
            # PNG変換
            cairosvg.svg2png(url = "temp.svg", write_to = save_path)
        except:
            # エラー通知
            messagebox.showerror("Error", "Check the code!!")

# TXT保存
def save_txt():
    # 保存ダイアログの表示
    typ = [("Text Files","*.txt")] 
    save_path = tk.filedialog.asksaveasfilename(filetypes = typ, defaultextension = "txt")
    
    if len(save_path) != 0:
        # ファイルが選択された場合データを書き込み
        with open(save_path, "w") as file:
            # テキストボックスの値を取得
            data = txtbox.get("1.0", "end")
            file.write(data)

# TXTファイル読込み
def load_txt():
    # ファイル選択ダイアログの表示
    typ = [("Text Files","*.txt")] 
    load_path = tk.filedialog.askopenfilename(filetypes = typ, defaultextension = "txt")
    
    # ファイルが選択された場合データを書き込み
    if len(load_path) != 0:
        # 既存のtxtboxデータ消去
        txtbox.delete("1.0","end")
        # ファイルのリスト取得
        with open(load_path) as f:
            txtbox.insert("1.end", f.read())

# rxnlvl_githubへアクセス
def web_1():
    url = "https://github.com/eutactic/rxnlvl"
    webbrowser.open(url)

# 操作説明ページへアクセス
def web_2():
    url = "http://pc-chem-basics.blog.jp/archives/27912691.html"
    webbrowser.open(url)

##### GUI #####
# ウインドウの作成
root = tk.Tk()
root.title("ELDAD Ver.1.0.0")
root.minsize(width=650, height=400)
root.configure(bg = "white")
root.iconphoto(True, tk.PhotoImage(file = "Images/icon.png"))

# フレーム
code_image = tk.PhotoImage(file="Images/code.png")
label = tk.Label(root, image = code_image, text = " Python Code", bg = "white", compound = tk.LEFT)
frame = tk.LabelFrame(root, labelwidget = label, bg="white", padx=15, pady=15)
frame.pack(padx = 15, pady = 5, fill = tk.BOTH, expand = 1)

# テキストボックス
txtbox = tk.Text(frame, width = 60, height = 20, bg = "white")
# スクロールバー作成
yscroll = tk.Scrollbar(frame, orient = tk.VERTICAL, bg = "white", command = txtbox.yview)
yscroll.pack(side = tk.RIGHT, fill = tk.Y)
txtbox["yscrollcommand"] = yscroll.set
# テキストボックスの配置
txtbox.pack(fill = tk.BOTH, expand =1)

# メニューバーの作成
menubar = tk.Menu(root)
root.configure(menu = menubar, bg = "white")
# Fileメニュー
filemenu = tk.Menu(menubar, bg = "white", tearoff = 0)
menubar.add_cascade(label = "File", menu = filemenu)
filemenu.add_command(label = "Open Code (*.txt)", command = load_txt)
filemenu.add_command(label = "Save Code (*.txt)", command = save_txt)
filemenu.add_command(label = "Save Image As... (*.png)", command = save_png)
filemenu.add_separator()
filemenu.add_command(label = "Exit", command = lambda: root.destroy())
# Editメニュー
editmenu = tk.Menu(menubar, bg = "white", tearoff = 0)
menubar.add_cascade(label = "Edit", menu = editmenu)
editmenu.add_command(label = "Reset Code", command = ic_func)
# Helpメニュー
helpmenu = tk.Menu(menubar, bg = "white", tearoff = 0)
menubar.add_cascade(label = "Help", menu = helpmenu)
helpmenu.add_command(label = "rxnlvl (GitHub)", command = web_1)
helpmenu.add_command(label = "Manual", command = web_2)

# SVG出力ボタン
svg_image = tk.PhotoImage(file = "Images/save.png")
button = tk.Button(root, text = "  SVG Export", command = save_svg, image = svg_image, bg = "white", compound = tk.LEFT)
button.pack(side = tk.LEFT, padx = 10, pady = 10, ipady = 10, fill = tk.BOTH, expand = 1)
# プレビューボタン
png_image = tk.PhotoImage(file = "Images/preview.png")
button2 = tk.Button(root, text = "  Preview", command = viewer_window, image = png_image, bg = "white", compound = tk.LEFT)
button2.pack(side = tk.LEFT, padx = 10, pady = 10, ipady = 10, fill = tk.BOTH, expand = 1)

# 初期コードの挿入
ic_func()
# サブウインドウ用のフラグ
sub_win = None

# ウインドウ状態の維持
root.mainloop()