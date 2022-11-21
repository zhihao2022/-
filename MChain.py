import queue
import json
import musicpy as mp
import random

# n阶马尔科夫链 用字典表示
class MCain:
    def __init__(self, n = 1):
        # 链的阶数
        self.n = int(n)

        # 链的主体
        self.MC = {}

        # 上n个音符
        self.old_note = queue.Queue()

        # 已有音符的集合
        self.note_old_in = dict({})
        self.note_in = []

        # 计数
        self.note_old_num = 0
        self.note_num = 0

    # 插入一个音符
    def insert(self, note_name):
        if note_name == '':
            return
        # 若前置要求未满足
        if self.old_note.qsize() < self.n:
            self.old_note.put(note_name)
            return

        # 前置要求满足后
        # 若该note_name元素是新元素
        if note_name not in self.note_in:
            self.note_in.append(note_name)

        # 若已经有该old_note元素
        if str(list(self.old_note.queue)) in self.note_old_in:

            if note_name in self.note_old_in[str(list(self.old_note.queue))]:
                self.note_old_in[str(list(self.old_note.queue))][note_name] += 1
            else:
                self.note_old_in[str(list(self.old_note.queue))][note_name] = 1

        # 若该old_note是新元素
        else:
            self.note_old_in[str(list(self.old_note.queue))] = {}
            self.note_old_in[str(list(self.old_note.queue))][note_name] = 1

        # 更新old_note
        self.old_note.get()
        self.old_note.put(note_name)
        return

    # 归一化并更新MC
    def r_to_1(self):
        # MC赋值
        MC_1 = self.note_old_in
        self.MC = self.note_old_in

        # 归一化
        for note_pre, note_post in MC_1.items():
            sum = 0
            for note_single, num in note_post.items():
                sum += num
            for note_single, num in note_post.items():
                self.MC[note_pre][note_single] = num/sum

    # MC存入.json文件中
    def fout(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.MC, f)

    # 加载.json文件中的MC
    def fin(self, filename):
        with open(filename, 'r') as f:
            self.MC = json.load(f)

# 将.mid文件提取出n阶马尔科夫链
def mid_to_MChain(filename_list, MC_n = 1, track_num = 0, with_time = False):

    MC_name = ''

    # 如果加时值
    note_past_name = ''
    file_past_name = ''
    if with_time:
        file_past_name = '_with_time'

    # 若只输入了一个文件
    if str(type(filename_list)) == "<class 'str'>":
        st = mp.chord([])
        tim = []
        filename = filename_list
        music = mp.read(filename)
        music = music(track_num)

        # 初始化
        MC = MCain(MC_n)

        for i in range(len(music)):
            # 去掉节奏设置

            if str(type(music[i])) == "<class 'musicpy.structures.tempo'>":
                continue
            st.append(music[i])
            if with_time :
                tim.append(music.interval[i])

        # 插入音符
        for i in range(len(st)):
            if with_time:
                note_past_name = '_' + str(tim[i])
            MC.insert(str(st[i]) + note_past_name)

        # 归一化
        MC.r_to_1()

        # 写入.json文件
        filename = filename.split('.')[0]
        MC_name = filename +'_'+str(MC_n) + '_MC' + file_past_name+ '.json'
        MC.fout(MC_name)

    # 若输入了一个列表的文件
    else:
        # 初始化
        MC = MCain(MC_n)

        # 多文件输入，输出时用_连接
        fout_name = ''

        for filename in filename_list:
            fout_name = fout_name + filename.split('.')[0] + '_'
            music = mp.read(filename)
            music = music(track_num)
            st = mp.chord([])
            tim = []
            for i in range(len(music)):
                # 去掉节奏设置
                if str(type(music[i])) != "<class 'musicpy.structures.note'>":
                    continue

                st.append(music[i])
                if with_time:
                    tim.append(music.interval[i])

            # 插入音符
            for i in range(len(st)):
                if with_time:
                    note_past_name = '_' + str(tim[i])
                MC.insert(str(st[i]) + note_past_name)

        # 归一化
        MC.r_to_1()

        # 写入.json文件
        MC_name = fout_name+str(MC_n)+'_' + 'MC' + file_past_name+ '.json'
        MC.fout(MC_name)
    return MC_name

# MChain生成旋律
def MChain_to_chord(MC_name, note_start_name, n = 1, music_len = 500, with_time = False, save_as_mid = True, time_single = 0.25):
    MC = {}
    n = int(n)
    result = mp.chord([])
    # 读出MC
    with open(MC_name, 'r') as f:
        MC = json.load(f)

    # 拆分第一组音符
    note_start_name_list = []
    if note_start_name[0] != '[':
        note_start_name_list = [note_start_name]
        note_start_name = str([note_start_name])
    else:
        note_start_name_list = note_start_name[1,-1].replace("'", '').split(', ')

    # 把第一组音符插入旋律
    for note_start_name_ in note_start_name_list:
        if with_time:
            notel = note_start_name_.split('_')
            if len(notel) == 1:
                notel.append(time_single)
            result.append(mp.to_note(notel[0], float(notel[1])))
        else:
            result.append(mp.to_note(note_start_name_), time_single)

    # 将MC内部倒置并处理频率，使之容易算概率
    MC_re = {}
    max_len = 0
    max_note = ''
    for key, value in MC.items():
        sum = 0
        MC_re[key] = {}
        for k, v in value.items():
            sum += v
            MC_re[key][sum] = k

        if len(value) > max_len:
            max_len = len(value)
            max_note = key

    max_queue = queue.Queue()
    max_note_list = max_note[1: -1].replace("'", '').split(', ')
    for note_max in max_note_list:
        max_queue.put(note_max)

    # 生成乐曲
    note_queue = queue.Queue()
    for note_start_name_ in note_start_name_list:
        note_queue.put(note_start_name_)
    note_name = note_start_name
    music_len -= 1
    for i in range(music_len):
        # 若输入错误的音符，取可能性最多的音符作为代替
        if note_name not in MC_re:
            note_name = max_note
            note_queue = max_queue

        # 随机数
        ran = random.random() % 1

        for key, value in MC_re[note_name].items():
            if key < ran:
                continue

            # 迭代note_name
            if n > 1:
                note_queue.get()
                note_queue.put(value)
                note_name = str(list(note_queue.queue))
            else:
                note_name = str([value])

            # 音符插入旋律中
            if with_time:
                notel = value.split('_')
                if len(notel) == 1:
                    notel.append(time_single)
                result.append(mp.to_note(notel[0], float(notel[1])))
            else:
                result.append(mp.to_note(value), time_single)
            break

    for i in range(len(result)):
        result.interval[i] = result[i].duration

    # 是否保存为.mid文件
    if save_as_mid:
        mid_name = ''
        MC_name_list = MC_name.split('_')
        for i in range(len(MC_name_list)):
            if MC_name_list[i] == 'MC.json' or MC_name_list[i] in ['MC','with','time.json']:
                break
            if i == 0:
                mid_name = MC_name_list[i]
                continue
            mid_name = mid_name + '_' + MC_name_list[i]

        if with_time:
            mid_name = mid_name + '_created_by_MC_with_time.mid'
        else:
            mid_name = mid_name + '_created_by_MC.mid'
        mp.write(result,name = mid_name)
    return result
