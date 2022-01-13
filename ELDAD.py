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
            sub_win.title("Preview (PNG)")
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

# TXT読込み
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

# 編集ウインドウ
def editor_window():
    global edt_win, plot_image, levels_image, edges_image, set_image
    # 複数ウインドウの禁止
    if edt_win is None or not edt_win.winfo_exists():
        ##### 関数 #####
        def pcb_func():
            a = f"p = plot([{box1.get()}, {box2.get()}], vbuf={box3.get()}, hbuf={box4.get()}, bgcolour=None, qualified={cb1.get()})"
            b = f"p + baseline(energy({box5.get()}, '{cb2.get()}'), colour={value4[cb4.get()]}, mode={cb3.get()}, opacity={box6.get()})"
            txtbox.insert("insert", a + "\n" + b + "\n")

        def levels_func():
            c = f"p + level(energy({f1_box3.get()}, '{f1_cb1.get()}'), {f1_box1.get()}, '{f1_box2.get()}', {f1_value2[f1_cb2.get()]})"
            txtbox.insert("insert", c + "\n")

        def edges_func():
            d = f"p + edge('{f2_box1.get()}', '{f2_box2.get()}', {f2_value2[f2_cb2.get()]}, {f2_box3.get()}, {f2_cb1.get()})"
            txtbox.insert("insert", d + "\n")

        ##### GUI #####
        edt_win = tk.Toplevel(root)
        edt_win.title("Code Editor")
        edt_win.configure(bg = "white")
        edt_win.resizable(width = False, height = False)

        ##### Plotエリア #####
        plot_image = tk.PhotoImage(file="Images/plot.png")
        plot_label = tk.Label(edt_win, image = plot_image, text = " Plot & Baseline", bg = "white", compound = tk.LEFT)
        frame = tk.LabelFrame(edt_win, labelwidget = plot_label, bg = "white", padx=15, pady=15)
        frame.pack(padx = 15, pady = 5, fill = tk.BOTH)
        # ラベル1
        lb1 = tk.Label(frame, text = "Width", bg = "white")
        lb1.grid(row = 0, column = 0)
        # エントリーボックス1
        box1 = tk.Entry(frame, justify = "center", relief="solid", width = 18)
        box1.insert(0, 25.0)
        box1.grid(row = 1, column = 0)
        # ラベル2
        lb2 = tk.Label(frame, text = "Height", bg = "white")
        lb2.grid(row = 0, column = 1)
        # エントリーボックス2
        box2 = tk.Entry(frame, justify = "center", relief="solid", width = 18)
        box2.insert(0, 10.0)
        box2.grid(row = 1, column = 1, padx = 10)
        # ラベル3
        lb3 = tk.Label(frame, text = "V-Margin", bg = "white")
        lb3.grid(row = 0, column = 2)
        # エントリーボックス3
        box3 = tk.Entry(frame, justify = "center", relief="solid", width = 18)
        box3.insert(0, 10.0)
        box3.grid(row = 1, column = 2)
        # ラベル4
        lb4 = tk.Label(frame, text = "H-Margin", bg = "white")
        lb4.grid(row = 0, column = 3)
        # エントリーボックス4
        box4 = tk.Entry(frame, justify = "center", relief="solid", width = 18)
        box4.insert(0, 5.0)
        box4.grid(row = 1, column = 3, padx = 10)
        # ラベル5
        lb5 = tk.Label(frame, text = "Qualified", bg = "white")
        lb5.grid(row = 0, column = 4)
        # コンボボックス1
        value1 = ["True", "False", "'sortof'"]
        cb1 = ttk.Combobox(frame, values = value1, justify = "center", width = 15)
        cb1.current(2)
        cb1.grid(row = 1, column = 4)

        ##### Baselineエリア #####
        # ラベル6
        lb6 = tk.Label(frame, text = "Energy", bg = "white")
        lb6.grid(row = 2, column = 0)
        # エントリーボックス5
        box5 = tk.Entry(frame, justify = "center", relief="solid", width = 18)
        box5.insert(0, 0.0)
        box5.grid(row = 3, column = 0)
        # ラベル7
        lb7 = tk.Label(frame, text = "Unit", bg = "white")
        lb7.grid(row = 2, column = 1)
        # コンボボックス2
        value2 = ["kjmol", "kcal", "eh", "ev", "wavenumber"]
        cb2 = ttk.Combobox(frame, values = value2, justify = "center", width = 15)
        cb2.current(0)
        cb2.grid(row = 3, column = 1)
        # ラベル8
        lb8 = tk.Label(frame, text = "Mode", bg = "white")
        lb8.grid(row = 2, column = 2)
        # コンボボックス3
        value3 = ["'normal'", "'dashed'"]
        cb3 = ttk.Combobox(frame, values = value3, justify = "center", width = 15)
        cb3.current(1)
        cb3.grid(row = 3, column = 2)
        # ラベル9
        lb9 = tk.Label(frame, text = "Opacity", bg = "white")
        lb9.grid(row = 2, column = 3)
        # エントリーボックス6
        box6 = tk.Entry(frame, justify = "center", relief="solid", width = 18)
        box6.insert(0, 0.1)
        box6.grid(row = 3, column = 3)
        # ラベル10
        lb10 = tk.Label(frame, text = "Colour", bg = "white")
        lb10.grid(row = 2, column = 4)
        # コンボボックス4
        value4 = {"Black": "0x0", "Red": "0xff0000", "Blue": "0x0000ff", "Green": "0x00ff00"}
        cb4 = ttk.Combobox(frame, values = list(value4.keys()), justify = "center", width = 15)
        cb4.current(0)
        cb4.grid(row = 3, column = 4)

        # Setボタン
        set_image = tk.PhotoImage(file = "Images/set.png")
        set_button = tk.Button(frame, text = " Set", command = pcb_func, image = set_image, bg = "white", compound = tk.LEFT)
        set_button.grid(row = 3, column = 5, padx = 10, ipadx = 20)

        ##### Levelsエリア #####
        levels_image = tk.PhotoImage(file="Images/levels.png")
        levels_label = tk.Label(edt_win, image = levels_image, text = " Levels", bg = "white", compound = tk.LEFT)
        frame1 = tk.LabelFrame(edt_win, labelwidget = levels_label, bg = "white", padx=15, pady=15)
        frame1.pack(padx = 15, pady = 5, fill = tk.BOTH)
        # ラベル1
        f1_lb1 = tk.Label(frame1, text = "Location", bg = "white")
        f1_lb1.grid(row = 0, column = 0)
        # エントリーボックス1
        f1_box1 = tk.Entry(frame1, justify = "center", relief="solid", width = 18)
        f1_box1.insert(0, 1)
        f1_box1.grid(row = 1, column = 0)
        # ラベル2
        f1_lb2 = tk.Label(frame1, text = "Name", bg = "white")
        f1_lb2.grid(row = 0, column = 1)
        # エントリーボックス2
        f1_box2 = tk.Entry(frame1, justify = "center", relief="solid", width = 18)
        f1_box2.grid(row = 1, column = 1, padx = 10)
        # ラベル3
        f1_lb3 = tk.Label(frame1, text = "Energy", bg = "white")
        f1_lb3.grid(row = 0, column = 2)
        # エントリーボックス3
        f1_box3 = tk.Entry(frame1, justify = "center", relief="solid", width = 18)
        f1_box3.insert(0, 0)
        f1_box3.grid(row = 1, column = 2)
        # ラベル4
        f1_lb4 = tk.Label(frame1, text = "Unit", bg = "white")
        f1_lb4.grid(row = 0, column = 3)
        # コンボボックス1
        f1_value1 = ["kjmol", "kcal", "eh", "ev", "wavenumber"]
        f1_cb1 = ttk.Combobox(frame1, values = f1_value1, justify = "center", width = 15)
        f1_cb1.current(0)
        f1_cb1.grid(row = 1, column = 3, padx = 10)
        # ラベル5
        f1_lb5 = tk.Label(frame1, text = "Colour", bg = "white")
        f1_lb5.grid(row = 0, column = 4)
        # コンボボックス2
        f1_value2 = {"Black": "0x0", "Red": "0xff0000", "Blue": "0x0000ff", "Green": "0x00ff00"}
        f1_cb2 = ttk.Combobox(frame1, values = list(f1_value2.keys()), justify = "center", width = 15)
        f1_cb2.current(0)
        f1_cb2.grid(row = 1, column = 4)

        # Setボタン
        set_button1 = tk.Button(frame1, text = " Set", command = levels_func, image = set_image, bg = "white", compound = tk.LEFT)
        set_button1.grid(row = 1, column = 5, padx = 10, ipadx = 20)

        ##### Edgesエリア #####
        edges_image = tk.PhotoImage(file="Images/edges.png")
        edges_label = tk.Label(edt_win, image = edges_image, text = " Edges", bg = "white", compound = tk.LEFT)
        frame2 = tk.LabelFrame(edt_win, labelwidget = edges_label, bg = "white", padx=15, pady=15)
        frame2.pack(padx = 15, pady = 5, fill = tk.BOTH)
        # ラベル1
        f2_lb1 = tk.Label(frame2, text = "Start (Name)", bg = "white")
        f2_lb1.grid(row = 0, column = 0)
        # エントリーボックス1
        f2_box1 = tk.Entry(frame2, justify = "center", relief="solid", width = 18)
        f2_box1.grid(row = 1, column = 0)
        # ラベル2
        f2_lb2 = tk.Label(frame2, text = "End (Name)", bg = "white")
        f2_lb2.grid(row = 0, column = 1)
        # エントリーボックス2
        f2_box2 = tk.Entry(frame2, justify = "center", relief="solid", width = 18)
        f2_box2.grid(row = 1, column = 1, padx = 10)
        # ラベル3
        f2_lb3 = tk.Label(frame2, text = "Mode", bg = "white")
        f2_lb3.grid(row = 0, column = 2)
        # コンボボックス1
        f2_value1 = ["'normal'", "'dashed'"]
        f2_cb1 = ttk.Combobox(frame2, values = f2_value1, justify = "center", width = 15)
        f2_cb1.current(0)
        f2_cb1.grid(row = 1, column = 2)
        # ラベル4
        f2_lb4 = tk.Label(frame2, text = "Opacity", bg = "white")
        f2_lb4.grid(row = 0, column = 3)
        # エントリーボックス3
        f2_box3 = tk.Entry(frame2, justify = "center", relief="solid", width = 18)
        f2_box3.insert(0, 0.4)
        f2_box3.grid(row = 1, column = 3, padx = 10)
        # ラベル5
        f2_lb5 = tk.Label(frame2, text = "Colour", bg = "white")
        f2_lb5.grid(row = 0, column = 4)
        # コンボボックス2
        f2_value2 = {"Black": "0x0", "Red": "0xff0000", "Blue": "0x0000ff", "Green": "0x00ff00"}
        f2_cb2 = ttk.Combobox(frame2, values = list(f2_value2.keys()), justify = "center", width = 15)
        f2_cb2.current(0)
        f2_cb2.grid(row = 1, column = 4)

        # Setボタン
        set_button2 = tk.Button(frame2, text = " Set", command = edges_func, image = set_image, bg = "white", compound = tk.LEFT)
        set_button2.grid(row = 1, column = 5, padx = 10, ipadx = 20)

##### GUI #####
# ウインドウの作成
root = tk.Tk()
root.title("ELDAD Ver.2.0.0")
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
editmenu.add_command(label = "Open Editor...", command = editor_window)
editmenu.add_command(label = "Reset Code", command = ic_func)
editmenu.add_command(label = "Clear", command = lambda: txtbox.delete("1.0","end"))
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
edt_win = None

# ウインドウ状態の維持
root.mainloop()