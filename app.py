import re
import threading
import queue
import platform
import getpass
from tkinter import *
from tkinter import colorchooser, scrolledtext
from tkinter.ttk import Combobox
from Chat_AI import *
from fanyi import *

# 一、定义主窗口
root = Tk()
root.title("自制综合成长型工具箱 - Daybreak网络安全协会")
img = PhotoImage(file='images/daybreak_logo.png')  # 替换为你的图标文件路径
root.iconphoto(True, img)  # True 表示设置为应用程序图标，适用于所有窗口
root.config(bg="white")  # 背景设置
center_window(root, 1000, 500)  # 窗体的位置和长宽
# 确保窗口已经初始化
root.update()

### 二、定义画布
# 定义画布的大小和边距
canvas_width = int(root.winfo_width() * 0.9)
canvas_height = int(root.winfo_height() * 0.9)
# 创建画布，并使用 grid 布局管理器
canvas = Canvas(root, width=canvas_width, height=canvas_height, bg="gray")
# 需要指定 row, column, padx, pady, sticky
canvas.grid(row=0, column=0, padx=int(root.winfo_width() * 0.02), pady=int(root.winfo_height() * 0.08), sticky="nsew")
# 配置主窗口，使画布居中
root.columnconfigure(0, weight=1)  # 设置列的权重
root.rowconfigure(0, weight=1)    # 设置行的权重

### 三、画布上定义文本
# 画布上定义文本
text_id = canvas.create_text(canvas_width / 2, canvas_height * 0.05, text="自制成长型工具箱首页", font=("Helvetica", 20), fill="lightgray", tags="my_text")

### 四、定义按钮的frame
# 画布上定义frame，这里应该是按钮的frame
frame = Frame(canvas, bg="grey", relief="solid", highlightbackground="red", highlightthickness=2)  # 创建 Frame

### 五、菜单栏上定义临时笔记
note_frame = None

### 六、菜单栏上定义kimi_AI
AI_ask_frame = None

### 七、菜单栏上定义本地终端
local_cmd_frame = None

### 八、菜单栏上定义百度翻译
baidu_fanyi_frame = None

# 给Entry 控件添加提示信息
def entry_Event(tool_Name,event_msg):

    # 初始显示提示文本
    tool_Name.insert(0, event_msg)
    tool_Name.configure(fg="grey")  # 文本颜色恢复为灰色

    def on_focus_out(event):
        # 当 Entry 失去焦点时，如果内容为空，则显示提示文本
        if not tool_Name.get():
            tool_Name.delete(0, END)
            tool_Name.insert(0, event_msg)
            tool_Name.configure(fg="grey")  # 文本颜色恢复为灰色

    def on_focus_in(event):
        # 当 Entry 获得焦点时，如果显示的是提示文本，则清空
        current_text = tool_Name.get()
        if current_text == event_msg:
            tool_Name.delete(0, END)
            tool_Name.configure(fg="black")  # 文本颜色恢复为灰色

    # 绑定事件
    tool_Name.bind('<FocusOut>', on_focus_out)
    tool_Name.bind('<FocusIn>', on_focus_in)

# 增加画布上的按钮
def add_Tools():
    # 一、获取全局变量

    # 二、初始化子窗口
    top = Toplevel(root)    # root的子窗口
    top.title("添加工具信息")
    # top.iconbitmap("favicon.ico")
    top.config(bg="white")  # 背景设置
    top.resizable(False, False) # 禁止改变窗体大小
    center_window(top, 400, 300)    # 窗体的位置和长宽
    top.grab_set()       # 设置子窗口为模态，阻止对主窗口的操作

    # 三、制作添加工具的子窗口
    # 1、工具名称
    label = Label(top, text="工具名称:")
    label.grid(row=0, column=0, padx=(0, 10), sticky='e')  # 对齐到列的东侧
    tool_name = Entry(top)
    tool_name.grid(row=0, column=1, padx=(0, 10), sticky='we')  # 紧随label之后
    entry_Event(tool_name,"请写入工具的名称")  # 给entry 控件添加一个提示信息

    # 2、工具路径
    color_label = Label(top, text="工具路径:")
    color_label.grid(row=1, column=0, padx=(0, 10), sticky='e')
    tool_path = Entry(top)
    tool_path.grid(row=1, column=1, padx=(0, 10), sticky='we')
    entry_Event(tool_path,"绝对/相对路径/文件夹路径/下载地址/工具地址")  # 给entry 控件添加一个提示信息

    # 3、工具分类
    command_label = Label(top, text="工具分类:")
    command_label.grid(row=2, column=0, padx=(0, 10), sticky='e')

    # 创建下拉框（Combobox），并设置为只读
    tool_menu = Combobox(top, values=get_menu_name_all(), state="readonly")
    tool_menu.grid(row=2, column=1, padx=(0, 10), sticky='we')  # 将下拉框放置在网格中

    # 4、工具作用分类
    use_label = Label(top, text="工具作用:")
    use_label.grid(row=3, column=0, padx=(0, 10), sticky='e')

    # 定义 工具分类 的选项
    def on_tool_category_change(*args):
        # 根据选中的分类（菜单栏）更新 tool_uses
        tool_navigation_bar['values'] = get_navigation_bar_one(tool_menu.get())  # 设置下拉框的选项

    tool_menu.bind("<<ComboboxSelected>>", on_tool_category_change)

    # 创建下拉框（Combobox），并设置为只读
    tool_navigation_bar = Combobox(top, values=get_navigation_bar_one(tool_menu.get()), state="readonly")
    tool_navigation_bar.grid(row=3, column=1, padx=(0, 10), sticky='we')  # 将下拉框放置在网格中

    # 5、启动方式
    run_type_label = Label(top, text="启动方式:")
    run_type_label.grid(row=4, column=0, padx=(0, 10), sticky='e')

    # 创建下拉框（Combobox），并设置为只读
    tool_run_type = Combobox(top, values=["直接打开","命令行打开","文件夹打开","链接打开","下载链接"], state="readonly")
    tool_run_type.current(0)  # 设置当前选中项为第一个
    tool_run_type.grid(row=4, column=1, padx=(0, 10), sticky='we')  # 将下拉框放置在网格中

    def run_command(*args):
        if tool_run_type.get() == "命令行打开":
            command = simpledialog.askstring("设置启动命令", "工具名称位置请用 * 号来代替:")
            if command is not None and "*" in command:
                run_command_label.config(text=command)
        elif tool_run_type.get() == "文件夹打开":
            messagebox.showinfo("设置提醒！","请确保文件路径是一个文件夹！")
        elif tool_run_type.get() == "下载链接" or tool_run_type.get() == "链接打开":
            messagebox.showinfo("设置提醒！","请确保文件路径是一个带有http的链接！")
        else:
            run_command_label.config(text="")

    tool_run_type.bind("<<ComboboxSelected>>", run_command)
    # 6、工具命令
    ''''''
    command_label = Label(top, text="启动命令:")
    command_label.grid(row=5, column=0, padx=(0, 10), sticky='e')
    run_command_label = Label(top, text="")
    run_command_label.grid(row=5, column=1, padx=(0, 10), sticky='we')

    def save_button():
        # 做保存前的校验，工具名称是一个 tools.txt 文件中唯一的标识符
        def tool_name_check(tool_names,tool_path):
            # 1、校验文件名是否重复
            for tool in get_json_txt_all(tool_path):
                if tool["工具名称"] == tool_names:
                    # 进行工具名称重复警告
                    messagebox.showinfo("保存失败！", f"数据保存失败！\n重复的工具名称：{tool_names}")
                    return False
            # 2、校验启动方式是否照应
            if tool_runs == "命令行打开" and len(tool_commands) == 0:
                messagebox.showinfo("保存失败！", f"数据保存失败！\n请确保启动命令有效：{tool_commands}")
                return False
            elif tool_runs == "下载链接" and "http" not in tool_paths:
                # 如果是下载链接则创建对应的文件夹
                create_dir(get_menu_path_one(tool_menus) + "\\" + tool_names)

                messagebox.showinfo("保存失败！", f"数据保存失败！\n工具路径需要是链接：{tool_paths}")
                return False
            return True

        tool_names = tool_name.get()
        tool_paths = tool_path.get()
        tool_menus = tool_menu.get()
        tool_navigation_bars = tool_navigation_bar.get()
        tool_runs = tool_run_type.get()
        tool_commands = run_command_label.cget("text")

        # 构建工具信息的字典
        tool_info = {
            "工具名称": tool_names,
            "工具路径": tool_paths,
            "工具分类": tool_menus,
            "工具使用": tool_navigation_bars,
            "启动方式": tool_runs,
            "工具命令": tool_commands,
            "index" :   0
        }
        txt_path = get_menu_path_one(tool_menus)    # 拿到对应的文件夹名称

        # 保存前进行校验
        if tool_name_check(tool_names,txt_path):
            # 将工具信息保存到对应的 txt 文件
            save_tool_txt(txt_path,tool_info)

            messagebox.showinfo("保存成功", f"数据已成功保存！\n保存工具信息：{tool_names}, {tool_paths}, {tool_menus}, {tool_commands}")
            top.destroy()  # 关闭窗口

    # 四、设置保存按钮，以保存信息
    save_button = Button(top, text="保存", command=save_button)
    save_button.grid(row=6, columnspan=2, pady=10)

    # 五、确保行和列被正确地拉伸以适应内容
    top.grid_columnconfigure(1, weight=1)
    top.grid_rowconfigure(0, weight=1)
    top.grid_rowconfigure(1, weight=1)
    top.grid_rowconfigure(2, weight=1)
    top.grid_rowconfigure(3, weight=1)
    top.grid_rowconfigure(4, weight=1)
    top.grid_rowconfigure(5, weight=1)
    top.grid_rowconfigure(6, weight=1)

# 增加导航栏
def add_navigation_bar():
    # 一、获取全局变量

    # 二、初始化子窗口
    add_Navigation_Bar = Toplevel(root)    # root的子窗口
    add_Navigation_Bar.title("添加导航栏信息")
    # top.iconbitmap("favicon.ico")
    add_Navigation_Bar.config(bg="white")  # 背景设置
    add_Navigation_Bar.resizable(False, False) # 禁止改变窗体大小
    center_window(add_Navigation_Bar, 400, 200)    # 窗体的位置和长宽
    add_Navigation_Bar.grab_set()     # 设置子窗口为模态，阻止对主窗口的操作

    # 三、制作添加菜单栏的子窗口
    # 1、选择要添加到的菜单栏
    menu_label = Label(add_Navigation_Bar, text="选择菜单栏:")
    menu_label.grid(row=0, column=0, padx=(0, 10), sticky='e')

    # 创建下拉框（Combobox），并设置为只读
    menu_names = get_menu_name_all()
    add_Navigation_Bar_menu = Combobox(add_Navigation_Bar, values=menu_names, state="readonly")
    add_Navigation_Bar_menu.set(menu_names[0])  # 默认选中第一项
    add_Navigation_Bar_menu.grid(row=0, column=1, padx=(0, 10), sticky='we')  # 将下拉框放置在网格中

    # 2、导航栏名称
    label = Label(add_Navigation_Bar, text="导航栏名称:")
    label.grid(row=1, column=0, padx=(0, 10), sticky='e')  # 对齐到列的东侧
    add_Navigation_Bar_name = Entry(add_Navigation_Bar)
    add_Navigation_Bar_name.grid(row=1, column=1, padx=(0, 10), sticky='we')  # 紧随label之后
    entry_Event(add_Navigation_Bar_name,"请写入要添加的导航栏的名称")  # 给entry 控件添加一个提示信息

    # 四、设置保存按钮，以保存信息
    def save_Navigation_Bar():
        # 做导航栏名称重复冲突的校验
        def Navigation_Bar_name_check(menu_names,navigation_bar_names):
            for navigation_bar_name in get_navigation_bar_one(menu_names):
                if navigation_bar_name == navigation_bar_names:
                    return False
            return True

        add_Navigation_Bar_menus = add_Navigation_Bar_menu.get()
        add_Navigation_Bar_names = add_Navigation_Bar_name.get()
        # 校验
        if Navigation_Bar_name_check(add_Navigation_Bar_menus,add_Navigation_Bar_names):
            # 构造完整的json 格式
            navigation_bar_name = get_navigation_bar_one(add_Navigation_Bar_menus)
            if len(navigation_bar_name) == 0:
                config_json[add_Navigation_Bar_menus]["navigation_bar_name"] = [add_Navigation_Bar_names]
            else:
                navigation_bar_name.append(add_Navigation_Bar_names)

            # 传入完整的json 格式进行写入，保存导航栏
            save_json_all(config_json)

            messagebox.showinfo("添加成功", f"数据已成功保存！\n添加的导航栏名称：{add_Navigation_Bar_names}\n可以继续添加！！！")

            # 对添加的菜单栏做刷新操作
            reload_canvas(add_Navigation_Bar_menus)

            add_Navigation_Bar.destroy()  # 关闭窗口
        else:
            # 进行菜单栏名称重复警告
            messagebox.showinfo("添加失败！", f"数据保存失败！\n重复的菜单栏名称：{add_Navigation_Bar_names}")

    save_button = Button(add_Navigation_Bar, text="添加", command=save_Navigation_Bar)
    save_button.grid(row=2, columnspan=2, pady=10)

    # 五、确保行和列被正确地拉伸以适应内容
    add_Navigation_Bar.grid_columnconfigure(1, weight=1)
    add_Navigation_Bar.grid_rowconfigure(0, weight=1)
    add_Navigation_Bar.grid_rowconfigure(1, weight=1)
    add_Navigation_Bar.grid_rowconfigure(2, weight=1)

# 添加菜单栏
def add_menus():
    # 一、获取全局变量

    # 二、初始化子窗口
    add_Menu = Toplevel(root)    # root的子窗口
    add_Menu.title("添加菜单栏信息")
    # top.iconbitmap("favicon.ico")
    add_Menu.config(bg="white")  # 背景设置
    add_Menu.resizable(False, False) # 禁止改变窗体大小
    center_window(add_Menu, 400, 200)    # 窗体的位置和长宽
    add_Menu.grab_set()     # 设置子窗口为模态，阻止对主窗口的操作

    # 三、制作添加菜单栏的子窗口
    # 1、菜单栏名称
    label = Label(add_Menu, text="菜单栏名称:")
    label.grid(row=0, column=0, padx=(0, 10), sticky='e')  # 对齐到列的东侧
    menu_name = Entry(add_Menu)
    menu_name.grid(row=0, column=1, padx=(0, 10), sticky='we')  # 紧随label之后
    entry_Event(menu_name,"请写入要添加的菜单栏的名称")  # 给entry 控件添加一个提示信息

    # 2、菜单栏对应的文件夹路径
    label_path = Label(add_Menu, text="对应文件夹:")
    label_path.grid(row=1, column=0, padx=(0, 10), sticky='e')  # 对齐到列的东侧
    menu_path = Entry(add_Menu)
    menu_path.grid(row=1, column=1, padx=(0, 10), sticky='we')  # 紧随label之后
    entry_Event(menu_path,"创建英文文件夹名称方便工具分类")  # 给entry 控件添加一个提示信息

    # 3、菜单栏下对应的颜色
    def choose_color():
        color_code = colorchooser.askcolor(title="选择颜色")
        if color_code[1] is not None:
            color_label.config(text=color_code[1])  # 更新颜色显示
            color_label.config(bg=color_code[1])  # 更新颜色显示

    # 调整按钮和标签的网格位置
    menu_color = Button(add_Menu, text="颜色风格", command=choose_color)
    menu_color.grid(row=2, column=0, padx=(0, 10), pady=(10, 0))  # 按钮放在第2行第0列

    color_label = Label(add_Menu, text="这里显示选择的颜色")
    color_label.grid(row=2, column=1, padx=(0, 10), pady=(10, 0), sticky='we')  # 标签放在第2行第1列

    # 四、设置保存按钮，以保存信息
    def save_button():
        # 做菜单栏名称和路径重复冲突的校验 以及其他的检验
        def menu_name_path_check(menu_names,menu_paths):
            if config_json_null_check():
                for menu_name in get_menu_name_all():
                    if menu_names == menu_name or menu_paths == get_menu_path_one(menu_name):
                        return False
            if menu_names == None or menu_paths == None or menu_colors == None:
                return False
            return True

        menu_names = menu_name.get()
        menu_paths = menu_path.get()
        menu_colors = color_label.cget("text")
        # 校验
        if menu_name_path_check(menu_names,menu_paths):
            # 构造json格式进行保存
            menu_info = {
                menu_names:{
                    "menu_path"  :   menu_paths,
                    "menu_color"    :   menu_colors,
                    "navigation_bar_name"   :   [
                        "首页"
                    ]
                }
            }

            # 合并两个JSON数据，构造完整的json 格式
            json_info = {**config_json, **menu_info}

            # 传入完整的json 格式进行写入，保存菜单栏名称
            save_json_all(json_info)

            # 创建对应的文件夹路径
            create_dir(menu_paths)

            messagebox.showinfo("添加成功", f"菜单栏添加成功！请手动重启工具箱展示\n添加的菜单栏名称：{menu_names}\n请在之后将对应的工具保存到{menu_paths}目录中")
            add_Menu.destroy()  # 关闭窗口

            root.destroy()  # 'root' 是主窗口的实例
        else:
            # 进行菜单栏名称重复警告
            messagebox.showinfo("添加失败！", f"数据保存失败！\n重复的菜单栏名称：{menu_names}或必要属性未设置！")

    save_button = Button(add_Menu, text="添加", command=save_button)
    save_button.grid(row=3, columnspan=2, pady=10)

    # 五、确保行和列被正确地拉伸以适应内容
    add_Menu.grid_columnconfigure(1, weight=1)
    add_Menu.grid_rowconfigure(0, weight=1)
    add_Menu.grid_rowconfigure(1, weight=1)
    add_Menu.grid_rowconfigure(2, weight=1)
    add_Menu.grid_rowconfigure(3, weight=1)

# 清除画布内容，做刷新操作，加载界面、导航栏、按钮等
def reload_canvas(menu_name):    # 更新画布
    global frame
    global config_ai_json

    # 如果之前按钮的frame 还存在，则销毁
    if frame is not None:
        frame.destroy() # 如果存在之前的框架，则进行销毁

    # 3、如果当前菜单是 "note_menu"，则显示 临时笔记
    if menu_name == "note_nemu":
        # 1、遍历 root 内的所有place子组件进行隐藏
        for widget in root.winfo_children():
            # 隐藏导航栏组件
            if widget.winfo_manager() == "place":
                widget.place_forget()
        # 2、隐藏 ai对话模型
        AI_ask_frame.grid_forget()

        # 3、隐藏本地终端
        local_cmd_frame.grid_forget()

        # 4、隐藏百度翻译
        baidu_fanyi_frame.grid_forget()

        # 5、显示笔记
        note_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    elif menu_name == "ai_ask":
        # 1、遍历 root 内的所有place子组件进行隐藏
        for widget in root.winfo_children():
            # 隐藏导航栏组件
            if widget.winfo_manager() == "place":
                widget.place_forget()
        # 2、隐藏 临时笔记
        note_frame.grid_forget()

        # 3、隐藏本地终端
        local_cmd_frame.grid_forget()

        # 4、隐藏百度翻译
        baidu_fanyi_frame.grid_forget()

        # 5、判断api是否配置
        if config_ai_json_null_check(): # 配置好了进行ai展示
            # 显示ai对话模型
            AI_ask_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        else:   # 没配置好，不能展示
            messagebox.showinfo("警告！","请先在工具箱配置中配置好AI的API！")
    elif menu_name == "local_cmd":
        # 1、遍历 root 内的所有place子组件进行隐藏
        for widget in root.winfo_children():
            # 隐藏导航栏组件
            if widget.winfo_manager() == "place":
                widget.place_forget()
        # 2、隐藏 临时笔记
        note_frame.grid_forget()

        # 3、隐藏ai对话
        AI_ask_frame.grid_forget()

        # 4、隐藏百度翻译
        baidu_fanyi_frame.grid_forget()

        # 4、显示本地终端
        local_cmd_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    elif menu_name == "baidu_fanyi":
        # 1、遍历 root 内的所有place子组件进行隐藏
        for widget in root.winfo_children():
            # 隐藏导航栏组件
            if widget.winfo_manager() == "place":
                widget.place_forget()
        # 2、隐藏 临时笔记
        note_frame.grid_forget()

        # 3、隐藏ai对话
        AI_ask_frame.grid_forget()

        # 4、隐藏本地终端
        local_cmd_frame.grid_forget()

        # 5、展示百度翻译
        baidu_fanyi_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    else:
        ## 隐藏 其他的菜单栏
        note_frame.grid_forget()  # 隐藏note临时笔记操作
        AI_ask_frame.grid_forget()  # 隐藏ai_ask对话模型
        local_cmd_frame.grid_forget()   # 隐藏本地终端
        baidu_fanyi_frame.grid_forget() # 隐藏百度翻译

        # 1、更新画布的文本为 菜单栏名称
        canvas.itemconfigure(text_id, text=menu_name, fill=get_menu_color_one(menu_name))

        # 2、更新画布的Frame。这里的Frame 是按钮的，导航栏的Frame是临时创建的
        new_frame = Frame(canvas, bg="grey", relief="solid", highlightbackground=get_menu_color_one(menu_name), highlightthickness=2)
        # 将 Frame 放置在 Canvas 上，居中并有一点垂直偏移
        frame_id = canvas.create_window(canvas_width / 2 + 5, canvas_height * 0.1 + 5, window=new_frame, anchor='n')

        # 3、进行不同的导航栏创建和首页显示
        create_Navigation_Bar(root,new_frame,get_navigation_bar_one(menu_name),menu_name)   # 创建导航栏
        load_tools_and_create_buttons(new_frame,menu_name)     # 展示首页

        # 4、更新 get_canvas 列表中的当前 Frame
        frame = new_frame

# 设置AI_ask 配置
def add_ai_setting():
    # 一、获取全局变量

    # 二、初始化子窗口
    ai_ask_config = Toplevel(root)    # root的子窗口
    ai_ask_config.title("设置AI对话模型信息")
    # top.iconbitmap("favicon.ico")
    ai_ask_config.config(bg="white")  # 背景设置
    ai_ask_config.resizable(False, False) # 禁止改变窗体大小
    center_window(ai_ask_config, 400, 200)    # 窗体的位置和长宽
    ai_ask_config.grab_set()     # 设置子窗口为模态，阻止对主窗口的操作

    # 三、修改AI对话模型的配置
    # 1、选择AI模型
    ai_label = Label(ai_ask_config, text="使用模型:")
    ai_label.grid(row=0, column=0, padx=(0, 10), sticky='e')

    # 创建下拉框（Combobox），并设置为只读
    ai_name = Combobox(ai_ask_config, values=get_ai_json_name_all(), state="readonly")
    ai_name.grid(row=0, column=1, padx=(0, 10), sticky='we')  # 将下拉框放置在网格中

    # 2、AI模型对应的API
    ai_API_label = Label(ai_ask_config, text="API配置:")
    ai_API_label.grid(row=1, column=0, padx=(0, 10), sticky='e')  # 对齐到列的东侧
    ai_API = Entry(ai_ask_config)
    ai_API.grid(row=1, column=1, padx=(0, 10), sticky='we')  # 紧随label之后
    entry_Event(ai_API,"请输入ai模型的API")  # 给entry 控件添加一个提示信息

    # 3、菜单栏下对应的颜色
    def choose_color():
        color_code = colorchooser.askcolor(title="选择颜色")
        if color_code[1] is not None:
            ai_color.config(text=color_code[1])  # 更新颜色显示
            ai_color.config(bg=color_code[1])  # 更新颜色显示

    # 调整按钮和标签的网格位置
    ai_color_label = Button(ai_ask_config, text="背景颜色", command=choose_color)
    ai_color_label.grid(row=2, column=0, padx=(0, 10), pady=(10, 0))  # 按钮放在第2行第0列

    ai_color = Label(ai_ask_config, text="这里显示选择的颜色")
    ai_color.grid(row=2, column=1, padx=(0, 10), pady=(10, 0), sticky='we')  # 标签放在第2行第1列

    # 四、设置保存按钮，以保存信息
    def save_button():
        # 做菜单栏名称和路径重复冲突的校验 以及其他的检验
        def menu_name_path_check(ai_names):
            for ai_name in get_ai_json_name_all():
                if ai_name == ai_names:     # 说明有这个ai名称
                    return True
            return False

        ai_names = ai_name.get()
        ai_APIs = ai_API.get()
        ai_colors = ai_color.cget("text")
        # 校验
        if menu_name_path_check(ai_names):
            # 修改ai的json文件
            update_ai_json(ai_names,ai_APIs,ai_colors)

            messagebox.showinfo("修改成功", f"API添加成功，重启使用 {ai_names} 的ai！")
            ai_ask_config.destroy()  # 关闭窗口

            root.destroy()  # 'root' 是主窗口的实例
        else:
            # 进行菜单栏名称重复警告
            messagebox.showinfo("修改失败！", f"配置文件中不存在 {ai_names} 的ai名称")

    save_button = Button(ai_ask_config, text="设置", command=save_button)
    save_button.grid(row=3, columnspan=2, pady=10)

    # 五、确保行和列被正确地拉伸以适应内容
    ai_ask_config.grid_columnconfigure(1, weight=1)
    ai_ask_config.grid_rowconfigure(0, weight=1)
    ai_ask_config.grid_rowconfigure(1, weight=1)
    ai_ask_config.grid_rowconfigure(2, weight=1)
    ai_ask_config.grid_rowconfigure(3, weight=1)

# 展示菜单栏
def show_menu():
    # 1、新建菜单栏控件
    menu_bar = Menu(root)

    # 2、添加菜单栏控件：添加控件
    menu_tool_add = Menu(menu_bar, tearoff=0)
    menu_tool_add.add_command(label="添加菜单栏", command=add_menus)
    menu_tool_add.add_command(label="添加导航栏", command=add_navigation_bar)
    menu_tool_add.add_command(label="添加工具", command=add_Tools)
    menu_tool_add.add_separator()
    menu_tool_add.add_command(label="AI模型设置", command=add_ai_setting)
    menu_tool_add.add_separator()
    menu_bar.add_cascade(label="工具箱设置", menu=menu_tool_add)

    # 3、动态的添加菜单栏
    if config_json_null_check():
        for menu_name in get_menu_name_all():
            menu_bar.add_cascade(label=menu_name, command=lambda menu_name=menu_name: reload_canvas(menu_name))

    # 4、加载已定义的控件
    # kimi_ai
    menu_bar.add_cascade(label="AI对话模型", command=lambda menu_name="ai_ask": reload_canvas(menu_name))
    # 百度翻译
    menu_bar.add_cascade(label="汉英翻译", command=lambda menu_name="baidu_fanyi": reload_canvas(menu_name))
    # 添加本地终端
    menu_bar.add_cascade(label="本地终端", command=lambda menu_name="local_cmd": reload_canvas(menu_name))
    # 临时笔记
    menu_bar.add_cascade(label="临时笔记", command=lambda menu_name="note_nemu": reload_canvas(menu_name))

    root.config(menu=menu_bar)   # 配置到菜单栏到root上

# 创建本地终端
def create_local_cmd():
    global local_cmd_frame
    global font_size

    # 进行颜色设置
    def init_tags(text_widget):
        text_widget.tag_configure("prompt", foreground="green")
        text_widget.tag_configure("cwd", foreground="blue")
        text_widget.tag_configure("orange", foreground="#9503FF")

    # 滑轮放大放小事件
    def adjust_font_size(event):
        global font_size

        if platform.system() == "Windows":
            delta = event.delta / 120
        else:
            delta = event.delta

        if delta > 0:
            font_size += 1
        elif delta < 0:
            font_size = max(8, font_size - 1)
        text_widget.config(font=("JetBrains Mono", font_size))

    # 回车enter 事件
    def handle_return(event):
        # 获取输入的命令
        input_line = text_widget.get("end-2c linestart", "end-1c").strip()
        # 使用re.search查找匹配
        match = re.search(r">\s*(.*)", input_line)  # 匹配 > 后面的内容
        # 如果找到匹配项，输出匹配的内容
        if match:
            input_line = match.group(1)
            if input_line:
                # 处理输入的命令
                execute_command(input_line)
        else:
            print("没有找到匹配的内容")
        # 插入新的提示符
        text_widget.insert(END, f"\n⚔ [ {getpass.getuser()} on", "prompt")
        text_widget.insert(END, f" ☢ {os.getcwd()}]\n", "cwd")
        text_widget.insert(END, "☣ #> ", "orange")

        text_widget.mark_set(INSERT, END)   # 将光标移动到提示符的后面
        text_widget.see(END)  # 滚动到最新行
        return "break"

    # 命令处理函数
    def execute_command(command):
        # 添加换行符以确保结果在新的一行开始
        text_widget.insert(END, "\n")
        if command.startswith('cd '):
            change_directory(command[3:].strip())
        elif command == 'ls':
            list_directory()
        elif command == 'pwd':
            print_working_directory()
        elif command == 'exit':
            # quit()
            clear_screen()
        elif command == 'clear':
            clear_screen()
        else:
            run_system_command(command)
        # 将光标移动到提示符的后面
        text_widget.mark_set(INSERT, END)
        text_widget.see(END)  # 滚动到最新行

    def change_directory(path):
        try:
            os.chdir(path)
            # prompt = f'\n☪ {getpass.getuser()} on {os.getcwd()} > '
        except FileNotFoundError:
            text_widget.insert(END, f"Directory {path} not found\n")
        except NotADirectoryError:
            text_widget.insert(END, f"{path} is not a directory\n")
        except PermissionError:
            text_widget.insert(END, f"No permission to access {path}\n")

    def list_directory():
        try:
            files = os.listdir()
            for file in files:
                text_widget.insert(END, f"{file}\n")
        except PermissionError:
            text_widget.insert(END, "No permission to list directory contents\n")

    def print_working_directory():
        text_widget.insert(END, f"{os.getcwd()}\n")

    def run_system_command(command):
        try:
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            text_widget.insert(END, result.stdout)
            if result.stderr:
                text_widget.insert(END, result.stderr)
        except Exception as e:
            text_widget.insert(END, f"Error: {e}\n")

    def complete_event(event):
        # 获取当前文本框中的单词
        index = event.widget.index("insert")
        line = event.widget.get("insert linestart", "insert lineend")
        prefix = line.split(None, 1)[0]

        # 获取所有可能的补全选项
        options = {name for name in os.listdir('.') if name.startswith(prefix)}

        # 如果只有一个选项，或者用户已经输入了路径分隔符，补全当前单词
        if len(options) == 1 or os.path.sep in prefix:
            event.widget.delete("insert linestart", END)
            event.widget.insert("insert", next(iter(options)))
        else:
            # 否则，显示所有可能的补全选项

            # 这里只是一个简单的例子，实际应用中可能需要更复杂的逻辑
            print("Options:", options)

        # 阻止Tab默认行为
        return "break"

    def clear_screen():
        # 清除文本框中的所有内容
        text_widget.delete("1.0", END)

    # 创建 local_cmd_frame 并添加到 root
    local_cmd_frame = Frame(root, bg="white", highlightbackground="black", highlightthickness=1, relief="solid")
    local_cmd_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    # 创建文本编辑区域，设置字体大小和样式
    text_widget = Text(local_cmd_frame, wrap="word", bg="#D9D9D9", fg="black", font=("JetBrains Mono", 12, "bold"), undo=True) # 字体有：Microsoft YaHei、SimSun、JetBrains Mono、Courier New
    text_widget.grid(row=0, column=0, sticky="nsew")
    # 添加滚动条
    scroll = Scrollbar(local_cmd_frame, command=text_widget.yview)
    scroll.grid(row=0, column=1, sticky="ns")
    # 将滚动条与文本编辑区域关联
    text_widget.config(yscrollcommand=scroll.set)
    # 调整 row 和 column 权重，使它们可以扩展
    local_cmd_frame.grid_rowconfigure(0, weight=1)
    local_cmd_frame.grid_columnconfigure(0, weight=1)

    # 绑定 enter 回车 和 ctrl+滑轮 事件
    text_widget.bind("<Return>", lambda event: handle_return(event))
    text_widget.bind("<Control-MouseWheel>", lambda event: adjust_font_size(event))
    # 绑定 Tab 键到补全事件
    text_widget.bind("<Tab>", complete_event)

    # 初始化标签属性
    init_tags(text_widget)

    # 展示命令提示符
    text_widget.insert(END, f"\n⚔ [ {getpass.getuser()} on", "prompt")
    text_widget.insert(END, f" ☢ {os.getcwd()}]\n", "cwd")
    text_widget.insert(END, "☣ #> ", "orange")

    local_cmd_frame.grid_forget()  # 隐藏临时笔记

# 创建临时笔记
def create_note():
    global note_frame

    def search_text(search_term):
        if search_term:
            text_area.tag_remove("highlight", '1.0', END)

            start_idx = '1.0'
            while True:
                start_idx = text_area.search(search_term, start_idx, nocase=True, stopindex=END)
                if not start_idx:
                    break
                end_idx = f"{start_idx}+{len(search_term)}c"
                text_area.tag_add("highlight", start_idx, end_idx)
                start_idx = end_idx
            text_area.tag_configure("highlight", background="yellow")
    def replace_text(search_term, replace_term):
        if search_term is not None and replace_term is not None:
            start_idx = '1.0'
            while True:
                start_idx = text_area.search(search_term, start_idx, nocase=True, stopindex=END)
                if not start_idx:
                    break
                end_idx = f"{start_idx}+{len(search_term)}c"
                text_area.delete(start_idx, end_idx)
                text_area.insert(start_idx, replace_term)
                start_idx = f"{start_idx}+{len(replace_term)}c"
    def on_search_replace():
        def apply_changes():
            search_term = search_entry.get()
            replace_term = replace_entry.get()
            if search_term:
                replace_text(search_term, replace_term)
            search_text(search_term)
            search_replace_window.destroy()

        search_replace_window = Toplevel(root)
        search_replace_window.title("搜索和替换")

        Label(search_replace_window, text="搜索内容:").grid(row=0, column=0, padx=5, pady=5)
        search_entry = Entry(search_replace_window, width=40)
        search_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(search_replace_window, text="替换内容:").grid(row=1, column=0, padx=5, pady=5)
        replace_entry = Entry(search_replace_window, width=40)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)

        replace_entry.bind("<Return>", lambda event: apply_changes())  # 给替换内容绑定回车键

        # 设置焦点到 search_entry
        search_entry.focus_set()

        Button(search_replace_window, text="全部替换", command=apply_changes).grid(row=2, column=0, columnspan=2, pady=10)

        # 调用 center_window 函数来居中窗口
        center_window(search_replace_window, 370, 120)

    def on_ctrl_f(event):
        search_term = simpledialog.askstring("搜索", "输入搜索内容:")
        if search_term:
            search_text(search_term)
    def on_ctrl_h(event):
        on_search_replace()
    def undo_action(event):
        text_area.edit_undo()

    # 创建 note_frame 并添加到 root
    note_frame = Frame(root, bg="white", highlightbackground="black", highlightthickness=1, relief="solid")
    note_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    # 创建文本编辑区域，设置字体大小和样式
    text_area = Text(note_frame, wrap="word", bg="gray90", fg="black", font=("Microsoft YaHei", 15, "bold"), undo=True) # 字体有：Microsoft YaHei、SimSun、JetBrains Mono
    def insert_spaces(event):
        text_area.insert("insert", "        ")  # 插入八个空格
        return "break"  # 阻止事件的默认行为

    text_area.bind("<Tab>", insert_spaces)
    text_area.grid(row=0, column=0, sticky="nsew")
    # 添加滚动条
    scroll = Scrollbar(note_frame, command=text_area.yview)
    scroll.grid(row=0, column=1, sticky="ns")
    # 将滚动条与文本编辑区域关联
    text_area.config(yscrollcommand=scroll.set)
    # 调整 row 和 column 权重，使它们可以扩展
    note_frame.grid_rowconfigure(0, weight=1)
    note_frame.grid_columnconfigure(0, weight=1)


    # 绑定 Ctrl+F 和 Ctrl+H 事件到 text_area
    text_area.bind("<Control-f>", on_ctrl_f)
    text_area.bind("<Control-h>", on_ctrl_h)
    text_area.bind("<Control-z>", undo_action)  # Ctrl+Z 撤销

    note_frame.grid_forget()  # 隐藏临时笔记

# 创建AI对话
def create_ai_ask():
    global AI_ask_frame

    # 创建一个线程安全的队列来存储响应数据
    response_queue = queue.Queue()

    def on_send(entry, chat_box):
        # 从文本框中获取用户输入
        question = text_box.get("1.0", END)

        # 检查用户输入消息
        if question.strip() == "" or question.strip() == placeholder_text:
            return

        # 将用户输入添加到聊天框
        chat_box.configure(state='normal')
        chat_box.insert(END, f"用户: {question}\n\n", 'user')
        chat_box.update()
        chat_box.configure(state='disabled')
        chat_box.yview(END)  # 自动滚动到文本框底部

        # 清空文本框
        text_box.delete("1.0", END)

        # 定义一个函数来处理AI的响应，支持加粗标记
        def handle_response_with_markup(chat_box, response):
            chat_box.configure(state='normal')
            chat_box.tag_configure('bold', font=('Arial', 12, 'bold'))
            chat_box.tag_configure('normal', font=('Arial', 12))
            chat_box.tag_configure('code', foreground='#414110', font=('Courier', 10))

            # 正则表达式匹配加粗和代码块
            pattern = re.compile(r'(\*\*.*?\*\*)|(```.*?```)', re.DOTALL)
            last_end = 0

            for match in pattern.finditer(response):
                start, end = match.span()
                # 插入非匹配部分
                if start > last_end:
                    chat_box.insert(END, response[last_end:start], 'normal')
                # 根据匹配类型设置标签
                if match.group(1):  # 加粗文本
                    text = match.group(1)[2:-2]  # 去除加粗标记
                    chat_box.insert(END, text, 'bold')
                elif match.group(2):  # 代码块
                    code_block = match.group(2)[3:-3]  # 去除代码块标记
                    chat_box.insert(END, code_block, 'code')
                last_end = end

            # 插入最后的文本和换行
            if last_end < len(response):
                chat_box.insert(END, response[last_end:], 'normal')

            # 插入换行符，确保文本框底部完整显示
            chat_box.insert(END, '\n')

            chat_box.configure(state='disabled')
            chat_box.yview(END)  # 自动滚动到文本框底部

        # 定义一个函数来执行ai_main，并把响应放入队列
        def ai_request_thread(chat_box, question):
            try:
                response = ai_main(ai_name="kimi_ai", msg=question)
                response_queue.put(response)  # 将响应放入队列
                handle_response_with_markup(chat_box, response)  # 直接处理响应
            except Exception as e:
                messagebox.showinfo("出错！","请检查 网络配置 和 API 配置是否正常！")

        # 创建并启动线程
        request_thread = threading.Thread(target=ai_request_thread, args=(chat_box, question))
        request_thread.start()

    # 设置文本框的标签样式
    def setup_chat_box(chat_box):
        chat_box.tag_configure('user', foreground='red')  # 用户文本红色
        chat_box.tag_configure('ai', foreground='blue')      # AI响应文本蓝色

    # 创建 AI 对话框的 Frame
    ai_frame = Frame(root, bg="white", highlightbackground="black", highlightthickness=1, relief="solid")
    ai_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    # 创建滚动文本框用于显示对话记录
    try:
        ai_color = get_ai_json_one_color(ai_name=get_ai_json_name_all()[0]) # 获取ai背景
        if len(ai_color) == 0:
            ai_color = "white"
    except Exception as e:
        ai_color = "white"
    chat_box = scrolledtext.ScrolledText(ai_frame, wrap="word", bg=ai_color, fg="black", font=("SimSun", 12))
    chat_box.grid(row=0, column=0, columnspan=2, sticky="nsew")

    # 禁止输入
    chat_box.config(state=DISABLED)

    # 创建输入框，使用 Text 组件以支持换行
    text_box = Text(ai_frame, width=50, height=4, wrap="word")
    text_box.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

    # 定义一个函数来添加和删除提示语
    def set_placeholder(text_box, placeholder_text):
        if text_box.get("1.0", END).strip() == "":
            # 如果文本框为空，则插入提示语，并设置样式
            text_box.configure(state='normal')
            text_box.insert("1.0", placeholder_text)
            text_box.tag_configure("placeholder", foreground="grey", font=("Arial", 12))
            text_box.tag_add("placeholder", "1.0", "1.end")
            text_box.configure(state='disabled')
        else:
            # 如果文本框不为空，移除提示语样式
            text_box.tag_remove("placeholder", "1.0", END)

    # 初始设置提示语
    placeholder_text = "Shift+Enter 发送消息"
    set_placeholder(text_box, placeholder_text)

    # 绑定文本框的焦点进入和离开事件，以控制提示语的显示和隐藏
    def on_focusout(event):
        set_placeholder(event.widget, placeholder_text)

    def on_focusin(event):
        if event.widget.get("1.0", END).strip() == placeholder_text:
            event.widget.configure(state='normal', background='white')
            event.widget.delete("1.0", END)

    # 绑定文本框获取与失去焦点事件
    text_box.bind("<FocusOut>", on_focusout)
    text_box.bind("<FocusIn>", on_focusin)

    # 绑定 Shift + Enter 组合键到发送消息的函数
    text_box.bind("<Shift-Return>", lambda event: on_send(text_box, chat_box))

    # 创建发送按钮
    send_button = Button(ai_frame, text="发送", command=lambda: on_send(text_box, chat_box))
    send_button.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    setup_chat_box(chat_box)

    # 配置行和列的权重
    ai_frame.grid_rowconfigure(0, weight=1)  # 让滚动文本框占据主要空间
    ai_frame.grid_rowconfigure(1, weight=0)  # 让输入框和按钮不扩展
    ai_frame.grid_columnconfigure(0, weight=1)  # 让第0列 (chat_box 和 entry) 扩展
    ai_frame.grid_columnconfigure(1, weight=0)  # 让第1列 (send_button) 不扩展

    # 更新ai 的frame
    AI_ask_frame = ai_frame
    # 隐藏ai_ask
    AI_ask_frame.grid_forget()

    # 做json配置文件的初始化
    if config_ai_json_null_check() == False: # 未配置好进行初始化
        try:
            create_ai_json()
        except Exception as e:  # 报错，说明 config 文件夹未存在
            create_dir("config")
            create_ai_json()

def baidu_fanyi():
    global baidu_fanyi_frame

    # 创建主框架
    fanyi_frame = Frame(root, bg="white", highlightbackground="black", highlightthickness=1, relief="solid")
    fanyi_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # 创建文本输入框提示和语言选择
    fanyi_label = Label(fanyi_frame, text="输入文本：", bg="white")
    fanyi_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

    # 创建翻译方向选择
    def toggle_translation_direction():
        global translation_direction
        # 切换语言对
        if translation_direction == ("en", "zh"):
            translation_direction = ("zh", "en")
            direction_button.config(text="翻译方向: 中文 -> 英文")
        else:
            translation_direction = ("en", "zh")
            direction_button.config(text="翻译方向: 英文 -> 中文")

    def get_translation_direction():
        # 获取当前语言对
        return translation_direction

    direction_button = Button(fanyi_frame, text="翻译方向: 英文 -> 中文", command=toggle_translation_direction)
    direction_button.grid(row=0, column=1, sticky="e", padx=5, pady=5)

    # 创建文本输入框
    input_textbox = Text(fanyi_frame, wrap="word", bg="gray90", fg="black")
    input_textbox.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    # 创建输出文本提示
    output_label = Label(fanyi_frame, text="翻译结果：", bg="white")
    output_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

    # 创建输出文本框
    output_textbox = Text(fanyi_frame, wrap="word", bg="white", fg="black")
    output_textbox.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    def on_translate_click(event=None):
        input_text = input_textbox.get("1.0", END).strip()
        if input_text:
            # 获取当前选择的翻译方向
            from_lang, to_lang = get_translation_direction()

            translated_text = translate_text(input_text, from_lang=from_lang, to_lang=to_lang)
            output_textbox.delete("1.0", END)
            output_textbox.insert(END, translated_text)

    # 创建翻译按钮
    translate_button = Button(fanyi_frame, text="翻译", command=on_translate_click)
    translate_button.grid(row=5, column=0, pady=10)

    # 绑定绑定文本框获取与失去焦点事件提示语
    # 初始设置提示语
    placeholder_text = "Shift+Enter 发送消息"

    def set_placeholder(widget, text):
        # 设置提示语
        widget.insert("1.0", text)
        widget.config(state='disabled', background='gray90')

    def on_focusout(event):
        # 当文本框失去焦点时，检查文本框内容是否为空，如果为空则显示提示语
        if event.widget.get("1.0", END).strip() == "":
            set_placeholder(event.widget, placeholder_text)

    def on_focusin(event):
        # 当文本框获得焦点时，如果内容是提示语，则清空文本框
        if event.widget.get("1.0", END).strip() == placeholder_text:
            event.widget.config(state='normal')
            event.widget.delete("1.0", END)
            event.widget.config(state='normal')

    input_textbox.bind("<FocusOut>", on_focusout)
    input_textbox.bind("<FocusIn>", on_focusin)
    # 设置初始提示信息
    set_placeholder(input_textbox, placeholder_text)

    # 绑定回车键事件到翻译按钮
    input_textbox.bind('<Shift-Return>', on_translate_click)

    # 配置行和列的权重
    fanyi_frame.grid_rowconfigure(0, weight=0)  # 标签行
    fanyi_frame.grid_rowconfigure(1, weight=1)  # 输入文本框行，允许扩展
    fanyi_frame.grid_rowconfigure(2, weight=0)  # 输出文本框标签行
    fanyi_frame.grid_rowconfigure(3, weight=1)  # 输出文本框行，允许扩展
    fanyi_frame.grid_columnconfigure(0, weight=1)  # 让列扩展

    # 更新百度翻译的 的frame
    baidu_fanyi_frame = fanyi_frame
    # 隐藏ai_ask
    baidu_fanyi_frame.grid_forget()

def main():
    global canvas

    # 在展示菜单栏前要先创建临时笔记
    create_note()

    # 再创建 AI 对话
    create_ai_ask()

    # 再创建本地终端
    create_local_cmd()

    # 在创建百度翻译
    baidu_fanyi()

    show_menu()     # 展示菜单栏

    # 设置菜单栏首页
    menu_names = get_menu_name_all()
    if len(menu_names) > 0:
        reload_canvas(menu_name=menu_names[0])
    else:   # 在首页上写一些标语
        canvas.create_text(canvas_width / 2 , canvas_height * 0.05 + 130, text="Daybreak网络安全协会内部成长型工具箱", font=("Helvetica", 20), fill="lightgray", tags="my_text")

    root.mainloop()  # 创建窗口视图

if __name__ == '__main__':
    main()
