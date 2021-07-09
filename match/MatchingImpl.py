#-*- coding:utf-8 –*- #
import numpy as np

class MatchingImpl:
    def __init__(self):
        '''
        KM匹配算法实现
        '''
        # 声明数据结构
        self.adj_matrix = None  # np array with dimension N*N

        # 初始化顶标
        self.label_left = None  # init label for the left set
        self.label_right = None  # init label for the right set

        # 初始化匹配结果
        self.match_right = None

        # 初始化辅助变量
        self.visit_left = None
        self.visit_right = None
        self.slack_right = None


    def __find_path(self, i):
        '''
        寻找增广路，深度优先
        :param i: 对应的visit_left的编号。
        '''
        i = int(i)
        self.visit_left[i] = 1
        for j, match_weight in enumerate(self.adj_matrix[i]):
            if self.visit_right[j]: continue  # 已被匹配（解决递归中的冲突）
            gap = int(self.label_left[i] + self.label_right[j] - match_weight)
            if gap == 0:
                # 找到可行匹配
                self.visit_right[j] = 1
                if np.isnan(self.match_right[j]) or self.__find_path(self.match_right[j]):  # j未被匹配，或虽然j已被匹配，但是j的已匹配对象有其他可选对象
                    self.match_right[j] = i
                    return True

            # 计算变为可行匹配需要的顶标改变量
            if self.slack_right[j] > gap:
                self.slack_right[j] = gap
        return False


    def __KM(self, N):
        '''
        KM匹配算法实现
        :param N: 节点数量
        '''
        for i in range(N):
            # 重置辅助变量
            self.slack_right = np.ones(N) * np.inf
            while True:
                # 重置辅助变量
                self.visit_left = np.zeros(N)
                self.visit_right = np.zeros(N)

                # 能找到可行匹配
                if self.__find_path(i):    break
                # 不能找到可行匹配，修改顶标
                # (1)将所有在增广路中的X方点的label全部减去一个常数d
                # (2)将所有在增广路中的Y方点的label全部加上一个常数d
                d = np.inf
                for j, slack in enumerate(self.slack_right):
                    if self.visit_right[j] == 0 and slack < d:
                        d = slack
                for k in range(N):
                    if self.visit_left[k] == 1: self.label_left[k] -= d
                for n in range(N):
                    if self.visit_right[n] == 1: self.label_right[n] += d

        # res = 0
        # for j in range(N):
        #     if self.match_right[j] >= 0 and self.match_right[j] < N:
        #         res += adj_matrix[int(self.match_right[j])][j]
        # return res

    def Matching(self, adj_matrix):
        '''
        匹配算法入口
        :param adj_matrix: 匹配矩阵，需要nxn的矩阵
        '''
        self.adj_matrix = adj_matrix
        N = np.array(self.adj_matrix).shape[0]
        # 初始化顶标
        self.label_left = np.max(adj_matrix, axis=1)  # init label for the left set
        self.label_right = np.zeros(N)  # init label for the right set
        # 初始化匹配结果
        self.match_right = np.empty(N) * np.nan

        # 初始化辅助变量
        self.visit_left = np.zeros(N)
        self.visit_right = np.zeros(N)
        self.slack_right = np.ones(N) * np.inf
        self.__KM(N)
        return self.match_right



if __name__ == '__main__':
    a = MatchingImpl()
    adj_matrix = np.array([[3,4,9],
                           [6,8,7],
                           [5,9,2]])
    print (a.Matching(adj_matrix))

