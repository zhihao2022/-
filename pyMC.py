import MChain as mn
import musicpy as mp
import sys
import getopt

if __name__ == '__main__':

    argv = sys.argv[1:]
    try:
        """
            options, args = getopt.getopt(args, shortopts, longopts=[])

            参数args：一般是sys.argv[1:]。过滤掉sys.argv[0]，它是执行脚本的名字，不算做命令行参数。
            参数shortopts：短格式分析串。例如："hp:i:"，h后面没有冒号，表示后面不带参数；p和i后面带有冒号，表示后面带参数。
            参数longopts：长格式分析串列表。例如：["help", "ip=", "port="]，help后面没有等号，表示后面不带参数；ip和port后面带冒号，表示后面带参数。

            返回值options是以元组为元素的列表，每个元组的形式为：(选项串, 附加参数)，如：('-i', '192.168.0.1')
            返回值args是个列表，其中的元素是那些不含'-'或'--'的参数。
        """
        opts, args = getopt.getopt(argv, "hNFPm:n:s:ta:i:T:")
    except getopt.GetoptError:
        print('输入 -h 获取帮助')
        sys.exit(2)

    if ('-h','') in opts:
        print("帮助页面:")
        print("-h: 帮助信息")
        print("-n <num>: 生成num阶马尔可夫链, 默认为1")
        print("-N: 不生成随机音乐.mid文件, 默认生成")
        print("-F: 只生成马尔科夫链，不生成随机音乐")
        print("-P: 播放生成的随机音乐")
        print("-m <MChain>: 直接由输入的马尔科夫链文件生成随机音乐")
        print("-t: 生成带时值的马尔可夫链")
        print("-a <num>: 由不带时值的马尔科夫链生成的单个音符的时值，默认为0.0625")
        print("-i <num>: 音色选择，1~127，默认为1")
        print("-T <num>: 选择第几条音轨，默认为0")
        print("-s <note>: 输入生成的随即音乐的头音符，默认为B3,带时值为B3_0.0625")
        print("note可选: 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', ")
        print("       'B', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'c', 'c#', 'd', 'd#', 'e', ")
        print("       'f', 'f#', 'g', 'g#', 'a', 'a#', 'b', 'bb', 'eb', 'ab', 'db', 'gb'")
        print("最后输入用来生成马尔科夫链的.mid文件名")

    num = 1
    inst = 1
    mid_create = True
    MC_not_only = True
    if_play = False
    MC_name = ''
    fin_MC = False
    note_start = 'B3'
    if_time = False
    time_single = 0.0625
    mid_name_in = list(args)
    track_num = 0
    for ele in opts:
        if ele[0] == '-n':
            num = int(ele[1])
        elif ele[0] == '-N':
            mid_create = False
        elif ele[0] == '-F':
            MC_not_only = False
        elif ele[0] == '-P':
            if_play = True
        elif ele[0] == '-m':
            MC_name = ele[1]
            fin_MC = True
        elif ele[0] == '-s':
            note_start = ele[1]
        elif ele[0] == '-t':
            if_time = True
        elif ele[0] == '-a':
            time_single = int(ele[1])
        elif ele[0] == '-i':
            inst = int(ele[1])
        elif ele[0] == '-T':
            track_num = int(ele[1])
        else:
            continue

    if args == []:
        MC_name = 'butterfly_MC.json'
        mid_name_in = 'butterfly.mid'

    if not fin_MC:
        MC_name = mn.mid_to_MChain(mid_name_in, track_num = track_num, MC_n = num, with_time = if_time)

    if MC_not_only:
        a = mn.MChain_to_chord(MC_name, note_start_name = note_start,
                               with_time = if_time,save_as_mid = mid_create, time_single = time_single, n = num)

        if if_play:
            mp.play(a, instrument = inst, wait = True,save_as_file = False)
