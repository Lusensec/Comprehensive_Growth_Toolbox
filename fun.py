import shutil
import urllib.request
import urllib.parse
import json
import os
import subprocess
import urllib
from tkinter import Button, Frame, LEFT, Menu, messagebox, simpledialog
from urllib.parse import urlparse

### 一、创建全局变量
# 1、保存按钮信息
buttons = []

# 2、菜单栏、导航栏的配置文件
config_json_path = "config/config.json"

# 3、ai对话模型的配置文件
config_ai_json_path = "config/ai_ask.json"

# 4、本地终端字体大小
font_size = 15

# 5、语言环境变量的配置文件
config_env_json_path = "config/env_cofnig.json"

# 6、初始化语言翻译方向
translation_direction = ("en", "zh")

### 二、拿到用户电脑的屏幕尺寸
def center_window(win, width, height):
    # 获取屏幕的尺寸
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # 计算 x 和 y 的偏移量，使得窗口居中
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # 设置窗口的几何属性
    win.geometry(f'{width}x{height}+{x}+{y}')

### 三、有关按钮的操作
# 1、添加按钮的右键操作
def on_right_click(frame_canvas,button,tool):
    # 创建右键菜单
    def show_context_menu(event):
        context_menu.post(event.x_root, event.y_root)  # 显示菜单

    # 定义菜单项和对应的操作
    context_menu = Menu(button, tearoff=0)
    context_menu.add_command(label="加入首页", command=lambda: join_index(tool))
    context_menu.add_separator()
    context_menu.add_command(label="打开所在文件夹", command=lambda: open_tools_path(frame_canvas,tool))
    context_menu.add_command(label="修改启动命令", command=lambda: edit_tools_command(frame_canvas,tool))
    context_menu.add_command(label="删除工具", command=lambda: delete_tools(frame_canvas,tool))
    context_menu.add_separator()
    context_menu.add_command(label="刷新", command=lambda: reload_tools(frame_canvas,tool))

    # 绑定右键事件
    button.bind("<Button-3>", show_context_menu)

# 2、实现右键加入index首页操作
def join_index(tool_one):
    index = tool_one["index"]
    tool_categorie = tool_one["工具分类"]
    if index == 0:
        tools = get_tools(tool_categorie)
        # print(tools)
        # print("--------------------------")
        for tool in tools:
            if tool["工具名称"] == tool_one["工具名称"]:
                tool["index"] = 1
                break
        # 重新写入文件
        # print(tools)
        update_tools(tool_categorie,tools)
        # 提示写入成功
        messagebox.showinfo("设置成功！", "该工具成功被设置在首页！")
    else:
        messagebox.showinfo("设置失败！", "该工具已经被设置在首页！")

# 3、更新按钮: 右键加入首页的更新操作
def update_tools(tool_categorie,tool_info):
    # 1、获取这个tools文件的路径
    txt_path = get_menu_path_one(tool_categorie)

    # 2、清空这个tools文件
    with open(txt_path + "/tools.txt", 'w') as file:
        pass  # 不需要执行任何操作，直接关闭文件

    # 3、进行tools文件的追加
    for tool in tool_info:
        save_tool_txt(txt_path,tool)

# 4、创建按钮。从 TXT 加载工具信息并创建按钮的函数（刷新操作）
def load_tools_and_create_buttons(frame_canvas,tool_categorie,tool_use="首页"):   # 这里的canvas实质是按钮的frame
    global buttons

    # 清空画布按钮
    for button in buttons:
        button.destroy()
    buttons.clear()

    # 配置列权重，确保按钮居中对齐
    max_buttons_per_row = 5
    for i in range(max_buttons_per_row + 2):  # 多出两列作为空白列
        frame_canvas.grid_columnconfigure(i, weight=1)  # 设置每一列的权重

    index = 0  # 初始化按钮索引
    max_buttons_per_row = 6  # 每行最多显示6个按钮

    for tool in get_tool_uses(tool_categorie,tool_use):
        # 创建按钮之前判断是不是链接
        if tool["启动方式"] == "下载链接":
            button = Button(frame_canvas, text=tool["工具名称"], command=lambda tool=tool: create_command_function(tool), padx=20, pady=10, fg="blue")
        else:
            button = Button(frame_canvas, text=tool["工具名称"], command=lambda tool=tool: create_command_function(tool), padx=20, pady=10)
        # 给按钮添加右键功能
        on_right_click(frame_canvas,button,tool)
        # 使用 grid 布局管理器在主窗口中放置按钮
        row = index // max_buttons_per_row
        column = index % max_buttons_per_row
        button.grid(row=row + 1, column=column, padx=15, pady=10, sticky='w')  # 调整起始行以避免覆盖画布内容
        index += 1
        buttons.append(button)  # 更新全局按钮列表

# 5、创建按钮命令操作
def create_command_function(tool):
    current_directory = get_os_path()  # 当前脚本所在的文件夹路径
    run_type = ["直接打开","命令行打开","文件夹打开","链接打开","下载链接"]

    # 获取工具的信息
    tool_path = tool["工具路径"]
    tool_run_type = tool["启动方式"]
    tool_command = tool["工具命令"]

    def command_run(is_paths,tool_path,tool_command):
        if tool_run_type == run_type[2]:  # 文件夹启动
            # 判断工具路径是绝对、相对路径
            if is_paths == 2:   # 相对路径路径
                # 与绝对路径一样，只是需要进行绝对路径的拼接
                tool_path = current_directory + "\\" + get_menu_path_one(tool["工具分类"]) + "\\" + tool_path
            if os_name():   # windows打开文件夹
                # print("走文件夹启动")
                # 获取工具所在的文件夹路径
                # folder_path = os.path.dirname(tool_path)
                # 使用 explorer 打开该目录
                subprocess.Popen(f'explorer "{tool_path}"')
            else:
                subprocess.Popen(['xdg-open', tool_path])   # linux打开文件夹
        elif tool_run_type == run_type[1]:  # 命令行启动
            try:
                if " " not in tool_command: # 说明可以直接执行
                    # 判断工具路径是绝对、相对路径
                    if is_paths == 2:   # 相对路径路径
                        # print("走命令行直接执行")
                        # 与绝对路径一样，只是需要进行绝对路径的拼接
                        tool_path = current_directory + "\\" + get_menu_path_one(tool["工具分类"]) + "\\" + tool_command
                        # 尝试直接执行
                    subprocess.Popen(tool_path)
                else:
                    # print("走命令行执行")
                    # 判断工具路径是绝对、相对路径
                    if is_paths == 2:   # 相对路径路径
                        # 与绝对路径一样，只是需要进行绝对路径的拼接
                        tool_path = current_directory + "\\" + get_menu_path_one(tool["工具分类"]) + "\\" + tool_path
                        # 尝试直接执行
                    # 将工具命令中的*进行替换
                    tool_command = tool_command.replace("*", tool_path)
                    # 打开 cmd.exe 并执行命令
                    command_to_execute = f'cd "{os.path.dirname(tool_path)}" && {tool_command}'
                    subprocess.Popen(f'start cmd /k "{command_to_execute}"', shell=True)
            except Exception as e:
                messagebox.showinfo(f"命令行启动失败","请右键修改启动命令")
                # print(f"出现错误{e}")
        elif tool_run_type == run_type[0]:    # 直接启动
            # 判断工具路径是绝对、相对路径
            if is_paths == 2:   # 相对路径路径
                # 与绝对路径一样，只是需要进行绝对路径的拼接
                tool_path = current_directory + "\\" + get_menu_path_one(tool["工具分类"]) + "\\" + tool_path
            try:
                # print("走直接执行")
                subprocess.Popen(tool_path)
            except Exception as e:
                messagebox.showinfo("直接启动失败","请右键修改启动命令！")
        elif tool_run_type == run_type[3]:      # 链接打开
            try:
                subprocess.Popen(f"start msedge {tool_path}")
            except Exception as e:
                command_to_execute = f'start msedge {tool_path}'
                # print(command_to_execute)
                subprocess.Popen(f'start cmd /k "{command_to_execute}"', shell=True)

    is_paths = is_path(tool)
    # 1、先判断启动方式
    if is_paths == 3:   # 下载链接
        tool_download_local_path = current_directory + "\\" + get_menu_path_one(tool["工具分类"]) + "\\" + tool["工具名称"]
        # 创建对应的文件
        create_dir(tool_download_local_path)
        # 进行文件的下载
        download_tools(tool,tool_path,tool_download_local_path + "\\" + os.path.basename(urlparse(tool_path).path))
    else:   # 就是非下载链接
        command_run(is_paths,tool_path,tool_command)

# 6、进行链接工具下载
def download_tools(tool,url,local_filename):
    try:
        # 使用urllib.request.urlopen打开URL
        with urllib.request.urlopen(url) as response:
            # 读取响应的内容
            data = response.read()
            # 写入到本地文件
            with open(local_filename, 'wb') as out_file:
                out_file.write(data)
        # 下载成功
        if "http" in tool["工具路径"]:
            # 说明启动方式还是一个链接，然后更改 工具路径
            txt_jsons = get_json_txt_all(get_menu_path_one(tool["工具分类"]))
            for txt_json in txt_jsons:
                if tool["工具名称"] == txt_json["工具名称"]:
                    txt_json["工具路径"] = tool["工具名称"] + "\\" + os.path.basename(urlparse(tool["工具路径"]).path)
            # 进行 txt 配置文件的保存
            update_tools(tool["工具分类"],txt_jsons)

        messagebox.showinfo("下载成功！", f"工具已下载到 {local_filename}\n请右键修改对工具命令行以便使用！")
    except Exception as e:
        print(f"下载失败: {e}")

# 7、修改工具，对按钮启动命令进行修改
def edit_tools_command(frame_canvas,tool):
    command = simpledialog.askstring("修改启动命令", "可命令行启动(*代替文件名)与直接启动: ")
    if command is not None:
        # 进行 tools.txt 配置文件的保存
        txt_jsons = get_json_txt_all(get_menu_path_one(tool["工具分类"]))
        for txt_json in txt_jsons:
            if tool["工具名称"] == txt_json["工具名称"]:
                txt_json["工具命令"] = command
                txt_json["启动方式"] = "命令行打开"
        # print(txt_jsons)
        # 进行 txt 配置文件的保存
        update_tools(tool["工具分类"],txt_jsons)
        # 进入刷新函数
        load_tools_and_create_buttons(frame_canvas,tool["工具分类"],tool["工具使用"])

# 8、删除工具
def delete_tools(frame_canvas,tool):
    txt_all = get_json_txt_all(get_menu_path_one(tool["工具分类"]))
    txt_all = list(filter(lambda item: item["工具名称"] != tool["工具名称"], txt_all))  # tools.txt文件删除工具信息

    # 删除文件夹之前判断是链接还是相对路径
    is_paths = is_path(tool)
    if is_paths == 3:   # 链接
        delete_dir(get_menu_path_one(tool["工具分类"]),tool["工具名称"])
    elif is_paths == 2: # 相对路径
        # 删除相对路径前需要先询问是否删除相对路的相关工具文件夹
        if messagebox.askyesno("警告！","是否删除相对路径下对应的工具文件？"):
            delete_dir(get_menu_path_one(tool["工具分类"]),tool["工具路径"].split('\\')[0])
            messagebox.showinfo("删除成功！", "该工具及其文件成功被删除！")
    # 进行 tools 文件的更新
    update_tools(tool["工具分类"],txt_all)

    # 进入刷新函数
    load_tools_and_create_buttons(frame_canvas,tool["工具分类"],tool["工具使用"])

# 9、刷新工具
def reload_tools(frame_canvas,tool):
    # 进入刷新函数
    load_tools_and_create_buttons(frame_canvas,tool["工具分类"],tool["工具使用"])

# 10、打开工具所在文件夹
def open_tools_path(frame_canvas,tool):
    is_paths = is_path(tool)
    tool_path = '\\'.join(tool["工具路径"].split('\\')[:-1])

    # 判断工具路径是绝对、相对路径
    if is_paths == 2:   # 相对路径路径
        # 与绝对路径一样，只是需要进行绝对路径的拼接
        tool_path = get_os_path() + "\\" + get_menu_path_one(tool["工具分类"]) + "\\" + tool_path
    elif is_paths == 3 or is_paths == 4:
        messagebox.showinfo("警告！","链接工具无法在本地打开！")
        return
    if os_name():   # windows打开文件夹
        # print("走文件夹启动")
        # 获取工具所在的文件夹路径
        # folder_path = os.path.dirname(tool_path)
        # 使用 explorer 打开该目录
        subprocess.Popen(f'explorer "{tool_path}"')
    else:
        subprocess.Popen(['xdg-open', tool_path])   # linux打开文件夹

### 四、有关导航栏的操作
# 1、创建导航栏
def create_Navigation_Bar(win,canvas,navigation_bar_names,menu_name):    # 这里的canvas实质是按钮的frame，为了按钮能够显示出来
    navigation_bar = Frame(win, bg="lightgrey")  # 导航栏背景颜色
    navigation_bar.place(x=0, y=0, relwidth=1)  # 放置在菜单栏下方

    # 在导航栏中添加按钮
    for navigation_bar_name in navigation_bar_names:
        # 动态创建按钮并添加到导航栏
        button = Button(navigation_bar, text=navigation_bar_name, command=lambda tool_use=navigation_bar_name: load_tools_and_create_buttons(canvas, menu_name, tool_use=tool_use))
        button.pack(side=LEFT, padx=0.05, pady=2)  # 使用 pack 布局管理器

### 五、有关 config_json 文件的操作
# 获取 json 文件中的所有内容
def get_json_all():
    global config_json

    try:
        with open(config_json_path, 'r') as json_file:
            return json.load(json_file)     # 返回json文件所有内容，即一个json对象
    except FileNotFoundError:
        print(f"[!] 警告！{config_json_path} 配置信息文件出错")
    return {}

config_json = get_json_all()

# 判断 config.json 文件是否为空。 非空，返回True
def config_json_null_check():
    return len(config_json) != 0

# 获取 json 文件中所有的 menu 名字，返回的是数组
def get_menu_name_all():
    if config_json_null_check():
        return list(config_json.keys())
    else:
        return []

# 获取所有 menu 对应的 path 路径，返回的是 字符串。间接的判断这个菜单栏是否存在
def get_menu_path_one(menu_name):
    for menu_names in get_menu_name_all():
        if menu_names == menu_name:
            return config_json[menu_name]["menu_path"]
    return []

# 根据 menu 的名称获取对应的color颜色，返回具体的颜色值
def get_menu_color_one(menu_name):
    return config_json[menu_name]["menu_color"]

# 根据 menu 的名称获取对应的导航栏名称，返回的是一个 数组格式
def get_navigation_bar_one(menu_name):
    navigation_bar_name = config_json.get(menu_name, {}).get("navigation_bar_name")
    if navigation_bar_name == None:
        return []
    else:
        return navigation_bar_name

# 对 完整的json 进行写入，需要给一个完整的 json 格式
def save_json_all(json_info):
    with open(config_json_path, 'w') as json_file:
        json.dump(json_info, json_file, indent=4)  # indent=4 用于格式化输出

### 六、有关 工具tools 的 txt 文件的操作
# 1、进行txt 文件读取。需要是 菜单栏的路径 ，返回的是 数组
def get_json_txt_all(menu_path):
    tools = []
    try:
        with open(menu_path + '/tools.txt', 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    tool = json.loads(line.strip()) # 一行一行进行解析
                    tools.append(tool)
                except json.JSONDecodeError as e:
                    print(f"解析JSON失败：{e}")
                    return []
    except FileNotFoundError as e:
        print(f"[!] 警告！{menu_path}/tools.txt 工具配置信息文件出错")
    return tools

# 2、进行 txt文件 写入。需要的是 菜单栏的路径 和 一行的json数据
def save_tool_txt(txt_path,tool_info):
    with open(txt_path + "/tools.txt", "a", encoding='utf-8') as file:
        json.dump(tool_info, file, ensure_ascii=False)
        file.write('\n')  # 换行分隔每个工具的信息

# 3、获取tool工具的 uses使用
def get_tool_uses(tool_categorie,tool_use):
    tool_uses = []
    tools = get_tools(tool_categorie)   # 本质是获取所有tools.txt 文件内容
    if tool_use == "首页":
        for tool in tools:
            if tool_use == tool["工具使用"]:
                tool_uses.append(tool)
            elif tool["index"] == 1:
                tool_uses.append(tool)
    else:
        for tool in tools:
            if tool_use == tool["工具使用"]:
                tool_uses.append(tool)
    return tool_uses

# 4、根据工具类型获取对应目录下tools.txt 文件的所有内容
def get_tools(tool_categorie):
    tools = []
    txt_path = get_menu_path_one(tool_categorie)
    try:
        with open(txt_path + '/tools.txt', 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    tool = json.loads(line.strip()) # 一行一行进行解析
                    tools.append(tool)
                except json.JSONDecodeError as e:
                    print(f"解析 JSON 时发生错误：{e}")
    except FileNotFoundError:
        print(f"[!] 警告！{txt_path}/tools.txt 工具配置信息文件出错")
    return tools

### 七、AI对话模型设置
# 1、获取 ai_json 文件中的所有内容
def get_ai_json_all():
    global config_ai_json

    try:
        with open(config_ai_json_path, 'r') as json_file:
            return json.load(json_file)     # 返回json文件所有内容，即一个json对象
    except FileNotFoundError:
        print("警告！" + "请先在工具箱配置中配置好AI的API！")
    return {}

config_ai_json = get_ai_json_all()

# 2、校验ai的json文件是否存在
def config_ai_json_null_check():
    global config_ai_json
    config_ai_json = get_ai_json_all()
    try:
        if len(config_ai_json) == 0 or get_ai_json_one_api(get_ai_json_name_all()[0]) == "":
            return False
        else:
            return True
    except Exception as e:
        return False

# 3、获取 json 文件中所有的 menu 名字，返回的是数组
def get_ai_json_name_all():
    return list(config_ai_json.keys())

# 4、修改更新ai的json配置文件
def update_ai_json(ai_names,ai_api,ai_color):
    for ai_name in get_ai_json_name_all():
        if ai_name == ai_names:
            config_ai_json[ai_names]["AI_API"] = ai_api.strip()
            config_ai_json[ai_names]["ai_color"] = ai_color

    update_ai_all_json(config_ai_json)

# 5、全更改ai的json配置文件
def update_ai_all_json(json_info):
    # 进行tools文件的覆盖
    with open(config_ai_json_path, 'w') as json_file:
        json.dump(json_info, json_file, indent=4)  # indent=4 用于格式化输出

# 6、创建ai的json文件
def create_ai_json():
    ai_info = {
        "kimi_ai":{
            "AI_API"  :   "",
            "ai_color"    :   "",
        }
    }
    update_ai_all_json(ai_info)

# 7、获取某一个ai的api
def get_ai_json_one_api(ai_name):
    for ai_names in get_ai_json_name_all():
        if ai_names == ai_name:
            return config_ai_json[ai_name]["AI_API"]

# 8、获取某一个ai的color
def get_ai_json_one_color(ai_name):
    return config_ai_json[ai_name]["ai_color"]

### 八、其他的相关操作
# 1、判断操作系统。True为windows
def os_name():
    return os.name == 'nt'

# 2、获取脚本当前所处的系统目录
def get_os_path():
    # 获取脚本当前的绝对路径
    current_file_path = os.path.abspath(__file__)   # 当前所在的文件
    return os.path.dirname(current_file_path)  # 当前所在的文件夹路径

# 3、创建文件夹
def create_dir(path):
    if not os.path.exists(path):
        try:
            # 如果文件夹不存在，尝试创建它
            os.mkdir(path)
            print(f"文件夹 '{path}' 创建成功。")
        except OSError as error:
            # 处理创建文件夹时可能出现的异常
            print(f"创建文件夹时出错: {error}")
    else:
        print(f"文件夹 '{path}' 已存在。或正在下载，请等待下载成功！")

# 4、删除文件夹
def delete_dir(menu_path,tool_path):
    # 如果是 链接 或者是 绝对路径
    if "http" in tool_path:
        pass
    else:
        os_path = get_os_path()
        # 获取相对路径的第一个文件夹
        tool_dir = tool_path.split('\\')[0]
        folder_to_delete = os_path + "\\" + menu_path + "\\" + tool_dir

        # 检查是否存在该目录
        if os.path.exists(folder_to_delete):
            # 删除整个文件夹及其内容
            shutil.rmtree(folder_to_delete)
            print(f"已删除文件夹及其所有内容: {folder_to_delete}")
        else:
            print(f"文件夹不存在: {folder_to_delete}")

# 5、判断工具是绝对路径、相对路径还是链接
def is_path(tool):
    def path_check(tool_path):
        if get_menu_path_one(tool["工具分类"]) in tool_path:
            return 1    # 返回绝对路径
        else:
            tool_dir = tool_path.split('\\')[0]
            if os.path.exists(get_os_path() + "\\" + get_menu_path_one(tool["工具分类"]) + "\\" + tool_dir):
                return 2    # 返回相对路径
            else:
                return 1    # 返回绝对路径

    if tool["启动方式"] == "下载链接":
        if len(tool["工具命令"]) == 0:
            return 3    # 返回链接
        else:
            return path_check(tool["工具命令"])
    if tool["启动方式"] == "链接打开":
        return 4

    return path_check(tool["工具路径"])

