# coding=gbk
import isq
from isq import LocalDevice, QcisDevice
from isq import quantumCor
from ezQpy import *
import copy

pi = 3.1415

a_list = np.array([[0.5, -0.5, -0.5, -0.5], [0.5, 0.5, -0.5, 0.5], [0.5, -0.5, 0.5, 0.5], [0.5, 0.5, 0.5, -0.5]])
a_order = np.array([0,1,2,3])
a_input = np.array([0,0,0,0])
a_cnt = 0

b_list = np.array([[1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],#0000
                   [1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1],#0001
                   [1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1],#0010
                   [1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1],#0011
                   [1, -1, -1, -1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1, 1],#0100
                   [1, 1, -1, 1, 1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, -1],#0101
                   [1, -1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1, 1, -1, -1],#0110
                   [1, 1, 1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, -1, -1, 1],#0111
                   [1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1],#1000
                   [1, 1, -1, 1, -1, 1, -1, 1, 1, -1, 1, -1, 1, -1, 1, -1],#1001
                   [1, -1, 1, 1, -1, -1, 1, 1, 1, 1, -1, -1, 1, 1, -1, -1],#1010
                   [1, 1, 1, -1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1],#1011
                   [1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1],#1100
                   [1, 1, -1, 1, 1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1],#1101
                   [1, -1, 1, 1, 1, 1, -1, -1, 1, 1, -1, -1, -1, -1, 1, 1],#1110
                   [1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1]]) / 4.0#1111
b_order = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
b_input = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
b_cnt = 0

ccz = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1]])

# 实现对于映射关系的存储
# params Matrix: 用于存储映射关系的矩阵
# params order: 用于存储映射关系的顺序
# params m_input: 用于存储映射关系的输入
# params len: 用于存储映射关系的长度
# params ct1: 用于存储映射关系的第一个输入
# params ct2: 用于存储映射关系的第二个输入
def save(ct1, ct2, Matrix, order, m_input, len):
    if m_input[ct2]==1:
        print("save error, please check the input and reuinput!")
        return Matrix
    for i in range(len):
        if ct1 == order[i]:
            ct1_index = i
            # print(i)
    new_Matrix = np.copy(Matrix)
    ct2_list = np.copy(new_Matrix[ct2])
    # print(ct2_list)
    new_Matrix[ct2]=new_Matrix[ct1_index]
    new_Matrix[ct1_index]=ct2_list
    # print(new_Matrix)
    ct2_order = np.copy(order[ct2])
    order[ct2]=order[ct1_index]
    order[ct1_index]=ct2_order
    m_input[ct2]=1
    print('the quantum circuit updated succesfully!')
    return new_Matrix
    # if(num<=cnt):
    #     new_Matrix = np.copy(Matrix)
    #     tmp = np.copy(Matrix[cnt + num])
    #     for i in range(cnt + num, -1, -1):
    #         if i == cnt:
    #             break
    #         new_Matrix[i] = new_Matrix[i - 1]
    #     new_Matrix[cnt] = tmp
    #     # print(new_Matrix)
    #     return new_Matrix
    # else:
    #     new_Matrix = np.copy(Matrix)
    #     tmp = np.copy(Matrix[num])
    #     for i in range(num, -1, -1):
    #         if i == cnt:
    #             break
    #         new_Matrix[i] = new_Matrix[i - 1]
    #     new_Matrix[cnt] = tmp
    #     return new_Matrix

# 实现对于量子电路的构造
# param: bit_len: 量子比特数
# param: bit: 量子比特
# param: matrix: 量子门矩阵
# return: isq_str: 量子电路字符串
def circuit(bit_len, bit: list, matrix):
    # 根据量子比特数，初始化量子比特
    isq_str = '''qbit '''
    for i in range(bit_len):
        if i != bit_len - 1:
            isq_str += ('Q' + str(i + 1) + ', ')
        else:
            isq_str += ('Q' + str(i + 1) + ';\n')

    tmp = """"""
    # 根据量子比特数，初始化量子门
    for i in range(bit_len):
        if bit[i] == '1':
            tmp += ("X(Q" + str(i + 1) + ');\n')

    isq_str += tmp
    # 根据量子比特数，均权叠加
    for i in range(bit_len):
        isq_str += ('H(Q' + str(i + 1) + ');\n')

    # 设置酉矩阵
    quantumCor.addGate("Rs", matrix)
    # 设置CCZ门
    quantumCor.addGate("CCZ", ccz)

    # 根据量子比特数，设置酉矩阵
    isq_str += ('Rs(')
    for i in range(bit_len):
        if i != bit_len - 1:
            isq_str += ('Q' + str(i + 1) + ', ')
        else:
            isq_str += ('Q' + str(i + 1) + ');\n')

            # 设置迭代过程
    for i in range(bit_len):
        isq_str += ('H(Q' + str(i + 1) + ');\n')
    for i in range(bit_len):
        isq_str += ('X(Q' + str(i + 1) + ');\n')

    # 设置CCZ门
    if bit_len == 2:
        isq_str += ('CZ(Q1, Q2);\n')
    else:
        isq_str += ('CCZ(')
        for i in range(bit_len):
            if i != bit_len - 1:
                isq_str += ('Q' + str(i + 1) + ', ')
            else:
                isq_str += ('Q' + str(i + 1) + ');\n')

    # 设置迭代过程
    for i in range(bit_len):
        isq_str += ('X(Q' + str(i + 1) + ');\n')
    for i in range(bit_len):
        isq_str += ('H(Q' + str(i + 1) + ');\n')

    # 测量过程
    for i in range(bit_len):
        isq_str += ('M(Q' + str(i + 1) + ');\n')

    return isq_str


def readBit():
    bit_in = input("please input the 4-bits for searching:")
    return bit_in


# 检测RZ门电路, 传入量子程序, 匹配其中的RZ门和参数
# 例如RZ Q1 3.14156
def check_RZ(isq_qcis: str):
    # 匹配RZ门
    RZ = re.compile(r'RZ\sQ\d*\s\d\.\d+')
    RZ_list = RZ.findall(isq_qcis)
    # 复制RZ_list
    RZ_list_c = copy.deepcopy(RZ_list)

    # print(RZ_list)
    for i in range(len(RZ_list)):
        RZ_list[i] = RZ_list[i].split(' ')
    # 检查列表中的参数是否为大于pi, 如果是, 则进行替换
    for i in range(len(RZ_list)):
        # print(RZ_list[i])
        if (float(RZ_list[i][2]) > pi):
            RZ_list[i][2] = str(float(RZ_list[i][2]) - 2 * pi)
        if (float(RZ_list[i][2]) < -pi):
            RZ_list[i][2] = str(float(RZ_list[i][2]) + 2 * pi)
        RZ_list[i] = ' '.join(RZ_list[i])
    # print(RZ_list)
    # 替换原量子程序中的RZ门
    for i in range(len(RZ_list)):
        isq_qcis = isq_qcis.replace(RZ_list_c[i], RZ_list[i])
    # print(isq_qcis)
    return isq_qcis


def run(bit_in, bit_number, matrix):  # bit_number为处理位数输入2或4
    res = ""
    if bit_number == 2:
        for i in range(0, 1):
            bit_2 = [bit_in[i * 2], bit_in[i * 2 + 1]]
            # isq_str = circuit(bit_in[i * 2], bit_in[i * 2 + 1], calMatrix)
            isq_str = circuit(2, bit_2, matrix)  # isq_str存储字符串

            # =============================================isq跑================================================
            # # 转换为qcis指令
            # print("the first isq gate is displayed as follows")
            # print(isq_str)
            # ld = LocalDevice()
            # ld_res = ld.run(isq_str)
            # ld.draw_circuit(isq_str)
            # # print(ld_res)

            # =============================================isq跑================================================

            # =============================================真机跑================================================
            print(isq_str)
            ld = LocalDevice()
            ir = ld.compile_to_ir(isq_str, target="qcis")
            account = Account(login_key='f719ca98fc5ae6ab03580a039bd0289f', machine_name='ClosedBetaQC')
            print("the quantum circuit launch successfully!")
            print("the login key is:f719ca98fc5ae6ab03580a039bd0289f")
            print("the machine name is: ClosedBetaQC")
        
            # account = Account(login_key='f719ca98fc5ae6ab03580a039bd0289f', machine_name='应答机A')
            
            # 拓扑结构映射
            isq_qcis = account.qcis_mapping_isq(ir)
            isq_qcis = check_RZ(isq_qcis)
            query_id_isQ = account.submit_job(circuit=isq_qcis, version="isQ")
            
            if query_id_isQ:
                ld_res = account.query_experiment(query_id_isQ, max_wait_time=360000)['probability']

            # =============================================真机跑================================================

            m = max(ld_res.values())
            for key, value in ld_res.items():
                if (value == m):
                    res += key
    else:
        for i in range(0, 1):
            bit_2 = [bit_in[i * 4], bit_in[i * 4 + 1], bit_in[i * 4 + 2], bit_in[i * 4 + 3]]
            # isq_str = circuit(bit_in[i * 2], bit_in[i * 2 + 1], calMatrix)
            isq_str = circuit(4, bit_2, matrix)  # isq_str存储字符串

            # =============================================isq跑================================================
            # # 转换为qcis指令
            # print("the first isq gate is displayed as follows")
            # print(isq_str)
            # ld = LocalDevice(2000)
            # ld_res = ld.run(isq_str)
            # # draw the circuit
            # ld.draw_circuit(isq_str)
            # # print(ld_res)

            # =============================================isq跑================================================

            # =============================================真机跑================================================

            print(isq_str)
            ld = LocalDevice()
            ir = ld.compile_to_ir(isq_str, target = "qcis")
            account = Account(login_key='f719ca98fc5ae6ab03580a039bd0289f', machine_name='ClosedBetaQC')
            # account = Account(login_key='f719ca98fc5ae6ab03580a039bd0289f', machine_name='应答机A')
            print("the quantum circuit launch successfully!")
            print("the login key is:f719ca98fc5ae6ab03580a039bd0289f")
            print("the machine name is: ClosedBetaQC")
            
            # 拓扑结构映射
            isq_qcis = account.qcis_mapping_isq(ir)
            isq_qcis = check_RZ(isq_qcis)
            query_id_isQ = account.submit_job(circuit=isq_qcis,version="isQ")
            
            if query_id_isQ:
                ld_res = account.query_experiment(query_id_isQ, max_wait_time=360000)['probability']

            # =============================================真机跑================================================
            m = max(ld_res.values())
            for key, value in ld_res.items():
                if (value == m):
                    res += key
    return res


if __name__ == "__main__":
    # a_new_list = save(2,a_list,0)
    # a_new_list = save(3, a_new_list, 1)

    b_new_list = save(15, 0, b_list, b_order, b_input, 16)
    b_new_list = save(14, 1, b_new_list, b_order, b_input, 16)
    b_new_list = save(13, 2, b_new_list, b_order, b_input, 16)
    b_new_list = save(12, 3, b_new_list, b_order, b_input, 16)
    b_new_list = save(11, 4, b_new_list, b_order, b_input, 16)
    b_new_list = save(10, 5, b_new_list, b_order, b_input, 16)
    b_new_list = save(9, 6, b_new_list, b_order, b_input, 16)
    b_new_list = save(8, 7, b_new_list, b_order, b_input, 16)
    b_new_list = save(7, 8, b_new_list, b_order, b_input, 16)
    b_new_list = save(6, 9, b_new_list, b_order, b_input, 16)
    b_new_list = save(5, 10, b_new_list, b_order, b_input, 16)
    b_new_list = save(4, 11, b_new_list, b_order, b_input, 16)
    b_new_list = save(3, 12, b_new_list, b_order, b_input, 16)
    b_new_list = save(2, 13, b_new_list, b_order, b_input, 16)
    b_new_list = save(1, 14, b_new_list, b_order, b_input, 16)
    b_new_list = save(0, 15, b_new_list, b_order, b_input, 16)

    res = run(readBit(), 4, b_new_list)
    # res = run(readBit(), 2, a_new_list)

    print(res)
