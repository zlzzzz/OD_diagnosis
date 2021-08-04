import numpy as np
import pandas as pd

'''
diag_and_disa 函数共有四个输入变量：
1.纯音测听矩阵 6*6矩阵
2.年龄 数值型 
3.性别 数值型 0：女 or 1：男 
4.工龄 数值型 0:工龄<三年  1:工龄>=3年
'''


def diag_and_disa(pta_table, age, gender, work_age):

    diagnosis = "不能诊断噪声聋"
    disability = "不能进行伤残鉴定"
    adjust_now = None
    BHFTA = None

    adjust_male_row = [[0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [1, 1, 1, 2, 2, 3],
                       [2, 2, 3, 6, 8, 9],
                       [4, 4, 7, 12, 16, 18],
                       [6, 7, 12, 20, 28, 32],
                       [10, 11, 19, 31, 43, 49]]
    adjust_male = pd.DataFrame(adjust_male_row, columns=['male500', 'male1000', 'male2000', 'male3000', 'male4000',
                                                         'male6000'])
    adjust_female_row = [[0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [1, 1, 1, 1, 1, 2],
                       [2, 2, 3, 4, 4, 6],
                       [4, 4, 6, 8, 9, 12],
                       [6, 7, 11, 13, 16, 21],
                       [10, 11, 16, 20, 24, 32]]
    adjust_female = pd.DataFrame(adjust_female_row, columns=['female500', 'female1000', 'female2000', 'female3000',
                                                             'female4000', 'female6000'])

    if work_age == 1:
        adjust_now = [0, 0, 0, 0, 0, 0]
        if gender == 0:
            adjust_now = adjust_female.iloc[int(age/10)]  # int()取整数  .iloc 位置函数
        elif gender == 1:
            adjust_now = adjust_male.iloc[int(age/10)]
        else:
            print('性别输入有误！')
            adjust_now = 0
        print(adjust_now)

        pta_table = np.array(pta_table)
        print('输入的听力结果', pta_table)
        print('校正值：', adjust_now)
        # 校正
        list = [0, 1, 2, 3, 4, 5]
        for i in list:
            pta_table[i] = pta_table[i]-adjust_now
        print('校正的听力结果', pta_table)

        r500 = min(pta_table[0][0], pta_table[2][0], pta_table[4][0])
        r1000 = min(pta_table[0][1], pta_table[2][1], pta_table[4][1])
        r2000 = min(pta_table[0][2], pta_table[2][2], pta_table[4][2])
        l500 = min(pta_table[1][0], pta_table[3][0], pta_table[5][0])
        l1000 = min(pta_table[1][1], pta_table[3][1], pta_table[5][1])
        l2000 = min(pta_table[1][2], pta_table[3][2], pta_table[5][2])

        rm500 = np.mean([pta_table[0][0], pta_table[2][0], pta_table[4][0]])
        rm1000 = np.mean([pta_table[0][1], pta_table[2][1], pta_table[4][1]])
        rm2000 = np.mean([pta_table[0][2], pta_table[2][2], pta_table[4][2]])
        lm500 = np.mean([pta_table[1][0], pta_table[3][0], pta_table[5][0]])
        lm1000 = np.mean([pta_table[1][1], pta_table[3][1], pta_table[5][1]])
        lm2000 = np.mean([pta_table[1][2], pta_table[3][2], pta_table[5][2]])

        r3000 = min(pta_table[0][3], pta_table[2][3], pta_table[4][3])
        r4000 = min(pta_table[0][4], pta_table[2][4], pta_table[4][4])
        r6000 = min(pta_table[0][5], pta_table[2][5], pta_table[4][5])
        l3000 = min(pta_table[1][3], pta_table[3][3], pta_table[5][3])
        l4000 = min(pta_table[1][4], pta_table[3][4], pta_table[5][4])
        l6000 = min(pta_table[1][5], pta_table[3][5], pta_table[5][5])

        hight = np.array([[r3000, r4000, r6000, l3000, l4000, l6000]])
        # print(hight)
        BHFTA = round(np.mean(hight))
        # print(round(np.mean(hight)))
        print('BHFTA=', BHFTA)

        if BHFTA >=40:  # BHFTA >=40 继续
            # MTMV left and right
            MTMV_right = round(np.mean([r500, r1000, r2000])*0.9 + r4000*0.1)  # 是否需要四舍五入取整
            print('mtmv_right =', MTMV_right)
            MTMV_left = round(np.mean([l500, l1000, l2000])*0.9 + l4000*0.1)
            print('mtmv_left =', MTMV_left)

            # output diagnosis and disability
            if BHFTA < 40:
                diagnosis = "无噪声聋"
            elif min(MTMV_right, MTMV_left) >= 56:
                diagnosis = "重度噪声聋"
            elif min(MTMV_right, MTMV_left) >= 41:
                diagnosis = "中度噪声聋"
            elif min(MTMV_right, MTMV_left) >= 26:
                diagnosis = "轻度噪声聋"
            else:
                diagnosis = "无噪声聋"
            print('参考诊断结果为：', diagnosis)

            # disability 听力障碍伤残鉴定
            hearing_right = np.mean([rm500, rm1000, rm2000])  # 是否需要取整
            hearing_left = np.mean([lm500, lm1000, lm2000])
            hearing_both_mean = (min(hearing_right, hearing_left)*4 + max(hearing_right, hearing_left))/5
            print('双耳平均听阈:', hearing_both_mean, '右耳听力:', hearing_right, '左耳听力:',  hearing_left)

            if hearing_both_mean >= 91:
                disability = "四级伤残"
            elif hearing_both_mean >= 81:
                disability = "五级伤残"
            elif hearing_both_mean >= 71:
                disability = "六级伤残"
            elif hearing_both_mean >= 56:
                disability = "七级伤残"
            elif hearing_both_mean >= 41 or max(hearing_right, hearing_left) >= 91:
                disability = "八级伤残"
            elif hearing_both_mean >= 31 or max(hearing_right, hearing_left) >= 71:
                disability = "九级伤残"
            elif hearing_both_mean >= 26 or max(hearing_right, hearing_left) >= 56:
                disability = "十级伤残"
            else:
                disability = "无伤残"
            print('参考伤残鉴定：', disability)
        else:
            pass
    else:
        pass
    dd_result = {'pta_after_adj': pta_table, 'adjust_now': adjust_now, 'BHFTA': BHFTA,
          'diagnosis': diagnosis, 'disability': disability}
    return dd_result

# save the data

