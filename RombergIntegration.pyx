# cython: language_level=3, boundscheck=False, wraparound=True, cdivision=True
from libc.math cimport pow as c_pow, fabs as c_fabs
from cpython.pycapsule cimport PyCapsule_New, PyCapsule_GetPointer
from cpython.ref cimport PyObject
from cython.operator cimport dereference as deref
from libcpp.functional cimport function as cpp_function
from libcpp.string cimport string
from libcpp.unordered_map cimport unordered_map
from libcpp.vector cimport vector

ctypedef long double LDFLOAT

# 定义 C++ 函数指针类型
ctypedef LDFLOAT (*func_ptr)(LDFLOAT)

cdef class RombergIntegration:
    """
    Romberg 积分算法实现（Cython 版本）
    
    提供两种积分方法：
    1. recursive(): 使用递归方法和哈希表缓存
    2. dynamic_programming(maximum_step=20): 使用动态规划方法
    """
    
    cdef:
        # 被积函数 - Python 可调用对象
        object _integrand
        LDFLOAT _lower_bound
        LDFLOAT _upper_bound
        LDFLOAT _precision
        dict _romberg_map
        list _romberg_table
        list _precision_table
    
    def __cinit__(self, LDFLOAT a, LDFLOAT b, LDFLOAT precision, object integrand):
        """
        初始化 RombergIntegration 对象。
        
        Parameters
        ----------
        a : float
            积分的下界
        b : float
            积分的上界
        precision : float
            积分结果的精度要求
        integrand : callable
            被积函数，接受一个浮点数参数，返回一个浮点数值
        """
        self._lower_bound = a
        self._upper_bound = b
        self._precision = precision
        self._integrand = integrand
        self._romberg_map = {}
        self._romberg_table = []
        self._precision_table = []
    
    cdef str _generate_key(self, int m, int k):
        """
        生成 Romberg 表中 (m, k) 位置的键。
        
        Parameters
        ----------
        m : int
            Romberg 表的行索引
        k : int
            Romberg 表的列索引
        
        Returns
        -------
        str
            格式为 "m-k" 的键字符串
        """
        return f"{m}-{k}"
    
    cdef LDFLOAT _T(self, int m, int k):
        """
        计算 Romberg 表中 (m, k) 位置的值。
        
        递归计算，使用哈希表缓存中间结果。
        
        Parameters
        ----------
        m : int
            Romberg 表的行索引
        k : int
            Romberg 表的列索引
        
        Returns
        -------
        long double
            Romberg 表中 (m, k) 位置的值
        """
        cdef:
            str key = self._generate_key(m, k)
            int n
            LDFLOAT h
            LDFLOAT sum_val
            int i
            LDFLOAT Tmk1
            LDFLOAT Tm1k
        
        if key in self._romberg_map:
            return self._romberg_map[key]
        
        if m == 0:
            # 梯形公式的初始值
            n = 1 << k  # 2^k
            h = (self._upper_bound - self._lower_bound) / n
            sum_val = 0.5 * (self._integrand(self._lower_bound) + 
                            self._integrand(self._upper_bound))
            for i in range(1, n):
                sum_val += self._integrand(self._lower_bound + i * h)
            self._romberg_map[key] = h * sum_val
        else:
            Tmk1 = self._T(m - 1, k + 1)
            Tm1k = self._T(m - 1, k)
            self._romberg_map[key] = (c_pow(4, m) * Tmk1 - Tm1k) / (c_pow(4, m) - 1)
        
        return self._romberg_map[key]
    
    def recursive(self):
        """
        执行 Romberg 积分算法（递归方法）。
        
        使用递归方法和哈希表缓存中间结果，逐步提高精度直到满足精度要求。
        
        Returns
        -------
        float
            计算得到的积分结果
        """
        cdef:
            int m = 0
            LDFLOAT Tm0
            LDFLOAT Tm1_0
            LDFLOAT diff
        
        Tm0 = self._T(m, 0)
        Tm1_0 = 0
        diff = 0
        
        while True:
            Tm1_0 = self._T(m + 1, 0)
            diff = c_fabs(Tm1_0 - Tm0)
            if diff < self._precision:
                return float(Tm1_0)
            Tm0 = Tm1_0
            m += 1
    
    cdef void _sub_problem(self, list lst_pre, LDFLOAT first_current, list lst_current):
        """
        辅助函数：计算动态规划中当前行的值。
        
        根据前一行的值和当前梯形值，使用 Romberg 加速计算当前行。
        
        Parameters
        ----------
        lst_pre : list
            前一行的 Romberg 表值
        first_current : long double
            当前行的第一个值（梯形法则）
        lst_current : list
            当前行的结果列表（输出参数）
        """
        cdef:
            int m
            LDFLOAT down = first_current
            LDFLOAT elem
        
        lst_current.append(first_current)
        m = 1
        for up in lst_pre:
            elem = (c_pow(4, m) * down - up) / (c_pow(4, m) - 1)
            down = elem
            lst_current.append(elem)
            m += 1
    
    def dynamic_programming(self, int maximum_step=20):
        """
        执行 Romberg 积分算法（动态规划方法）。
        
        使用迭代动态规划方法，构建 Romberg 表，逐步提高精度。
        
        Parameters
        ----------
        maximum_step : int, optional
            最大迭代步数，默认为 20
        
        Returns
        -------
        float
            计算得到的积分结果
        """
        cdef:
            int m = 0
            int n
            LDFLOAT h
            LDFLOAT trapezoid
            int i, j
            list lst_m
            LDFLOAT precision_diff
        
        # 初始化：m=0，n=1
        n = 1 << m  # 2^0 = 1
        h = (self._upper_bound - self._lower_bound) / n
        trapezoid = 0.5 * (self._integrand(self._lower_bound) + 
                          self._integrand(self._upper_bound))
        lst_m = [trapezoid]
        self._romberg_table.append(lst_m)
        
        # 迭代计算
        for i in range(1, maximum_step):
            m = i
            n = 1 << m  # 2^m
            h = (self._upper_bound - self._lower_bound) / n
            trapezoid = 0.5 * (self._integrand(self._lower_bound) + 
                              self._integrand(self._upper_bound))
            for j in range(1, n):
                trapezoid += self._integrand(self._lower_bound + j * h)
            trapezoid *= h
            
            lst_m = []
            self._sub_problem(self._romberg_table[-1], trapezoid, lst_m)
            self._romberg_table.append(lst_m)
            
            # 检查精度是否达标
            precision_diff = c_fabs(self._romberg_table[m][-1] - self._romberg_table[m - 1][-1])
            self._precision_table.append(precision_diff)
            
            if precision_diff < self._precision:
                return float(self._romberg_table[m][-1])
            
            # 检查精度是否在增加（说明已经最优）
            if len(self._precision_table) > 1 and self._precision_table[-1] > self._precision_table[-2]:
                return float(self._romberg_table[m - 1][-1])
        
        return float(self._romberg_table[m][-1])
    
    @property
    def romberg_map(self):
        """返回 Romberg 哈希表（递归方法使用）"""
        return self._romberg_map
    
    @property
    def romberg_table(self):
        """返回 Romberg 动态规划表"""
        return self._romberg_table
    
    @property
    def precision_table(self):
        """返回精度变化表"""
        return self._precision_table
