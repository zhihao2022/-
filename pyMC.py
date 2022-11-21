import MChain as mn
import musicpy as mp

if __name__ == '__main__':
    mid_name_in = ['butterfly.mid','onlymyrailgun.mid',"Naruto - Naruto No Theme (Better verison).mid"]
    # i = 0
    # mid_name_in = []
    # while 1:
    #     print("输入第%d个文件名,输入end结束"%i)
    #     name_in = input()
    #     if name_in == 'end':
    #         break
    #     mid_name_in.append(name_in)
    #     i+=1
    for i in range(8):
        num = i+1
        mid_create = True
        MC_not_only = True
        if_play = False
        MC_name = ''
        fin_MC = False
        note_start = 'B3'
        if_time = True
        time_single = 0.0625
        track_num = 0
        MC_name = mn.mid_to_MChain(mid_name_in, track_num = track_num, MC_n = num, with_time = if_time)
        a = mn.MChain_to_chord(MC_name, note_start_name = note_start,
                               with_time = if_time,save_as_mid = mid_create, time_single = time_single, n = num)
