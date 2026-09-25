# ============================================================
# pandas_try.py —— 门 B（pandas 基础）实验记录
#   数据：data.csv（9 行，自己造的）、dirty_data.csv（10 行，4 行脏）
#   用途：把门 A 手写的每一个动作，用 pandas 重做一遍，并【对上手写结果】
#        （这叫"标尺对照"：新手写、再换工具，工具算对了才敢信它）
#
#   本文件覆盖：B1~B9
#     B1  read_csv + DataFrame       B2  groupby 求平均温度
#     B3  groupby 求成功率           B4  造规则表
#     B5  算准确率（对上 0.67）      B6  布尔索引筛选 + map 边界
#     B7  清洗脏数据（对上 6 收 4 跳）B8  独热编码（文字→数字）
#     B9  严格划分训练/测试（0.67 → 0.33）
#
#   ★ 本阶段的暗线：「跑得通 ≠ 对」——报错会拦住你，跑得通的错不会。
#     已亲手验证 4 次：① map 给 NaN 静默算歪 ② 数据泄漏让分数虚高
#                     ③ read_csv 原样收下 'abc' ④ 列名取错让准确率假成 0.00
# ============================================================
import pandas as pd            # ← 你的第一次 import：把 pandas 工具箱拿进来，起小名叫 pd

df = pd.read_csv('data.csv')   # 一行把 CSV 读成表格
#print(df)                       # 打印看看长啥样
#print(type(df))                 # 看看它是什么类型

#print(df.groupby('topology')['temp'].mean())

#print(df.groupby('topology')['success'].mean()) #我觉得这是直接输出成功率

rates = df.groupby('topology')['success'].mean()
#print(rates)
#print(rates.index)
#print(type(rates))
#print(type(rates.index))
rule = {}
for topo in rates.index:
    if rates[topo] > 0.5:
        rule[topo] = 1
    else:
        rule[topo] = 0
print(rule)


# ============================================================
# ⚠️ 我发现的重大问题：数据泄漏（训练集与测试集重叠） 2026-09-24
#   第 11 行算 rule 用的是 data.csv 全部 9 行；下面这行 test 又是这 9 行里的最后 3 行。
#   两者有重叠 → rule 早就"看过"测试集那 3 行的答案了 → 测出来的 0.67 是虚高的。
#   正确做法：算 rule 时必须把留出集排除掉，再拿留出集去测。
#   （核对：只用前 6 行算 rule，准确率从 0.67 掉到 0.33）
#   ⇒ 这是 B9「划分训练/测试」的正题，也是论文路线用到的第一颗子弹。
# ============================================================
test=df.tail(3)
pred=test['topology'].map(rule)
print(test)
print(pred)
hit=(test['success']==pred)
print(hit)
print(f"正确率为{hit.mean():.2f}")


#B6a测试
rule_jia = {'MFI': 1}                              # 故意只留 MFI
print(df.tail(3)['topology'].map(rule_jia))    # 看它给什么
try:
    print(rule_jia['FAU'])
except KeyError as e:      # as e 把错误对象接住
    print('捕获到:', e)     # 打印它，而不是打印一句没信息量的"报错"

#B6b
#print(df['temp']>170 & df['success']==1)
print((df['temp']>170) & (df['success']==1))   #没有过滤筛选作用
print(df[(df['temp']>170) & (df['success']==1)])     #提示后修改的有修改过滤版本
#[r for r in rows if int(r[2]) > 170 and r[3] == '1']   # 手写：也是那 2 行
#可能错的三点（由ai提供）1.边界问题，等于170度的没有统计可能会导致漏掉很多数据（此边界为人为决定）2.静默失效  success==1  但可能有1.0等导致不被统计 3.空值  数据存在空值导致很多未被统计

# ============================================================
#B7a  pandas 读脏数据 —— 对照门 A 手写的 robust_read.py
#  读进来【完全不报错】，直接得到 10 行。
#  原因：pandas 有一张默认的"空值名单"（N/A / NA / NaN / null / None / 空字段），
#        名单上的自动变 NaN；不在名单上的（比如 'abc'）原样誊抄成文字。
#
#  性格差别（重点）：
#    手写 int(row[2])   = 严格的门卫 —— 转不动就抛 ValueError，程序直接崩
#    pandas read_csv    = 照单全收的书记员 —— 写什么我记什么，不吭声
#  ⇒ 代价：它把"发现问题"的责任全部推给使用者。
#  ⇒ 这就是本阶段那条暗线：「跑得通 ≠ 对」。
# ============================================================
dirty=pd.read_csv('dirty_data.csv')
print(dirty)                 # 能看出 N/A 和空值都变成了 NaN
print(dirty.isna().sum())    # isna() = 哪些格子是空的；.sum() = 数一数 → temp 2 / success 1
print(dirty.dropna())        # dropna() = 丢掉任何含空格子的整行 → 只剩 7 行（丢了 3 行）

# ============================================================
#B7b  把"认不出的错值"也揪出来
#  to_numeric(列, errors='coerce')：把这一列转成数字；
#      转不动的【不要报错，直接给 NaN】（coerce = 硬转/强制转换）
#  左边也写 dirty['temp']，意思是"把结果放回原来那一列"（左边的=往哪儿放，右边的=从哪儿取）
#
#  ⚠️ 关键区别：dropna() 只认"空"，认不出"错"
#     'abc' 不是空值，它是一个【文字】，所以 dropna() 放过它 → 单用它只丢 3 行。
#     加上 to_numeric 之后 'abc' 才变成 NaN → 丢掉 4 行。
#
#  ✅ 最终剩 6 行 —— 与门 A 手写 robust_read.py 的"6 收 4 跳"完全一致，
#     而且两边丢掉的行号都是 [1, 3, 6, 7]。（第三次标尺对照）
# ============================================================
dirty['temp'] = pd.to_numeric(dirty['temp'], errors='coerce')   # 转不动 → NaN
print(dirty.isna().sum())                                       # 数空 → temp 变成 3 个
print(dirty.dropna())                                           # 丢掉含空的行 → 剩 6 行

# ============================================================
#B8  特征工程第一步：把"文字"变成"数字"
#  为什么必须做：模型只会算数字，不会算文字 —— 你没法计算 MFI × 170。
#  dtypes 先看清谁是谁：topology / osda 是文字，temp / success 是数字。
#
#  ⚠️ 陷阱：df['topology'].map({'BEA':0,'FAU':1,'MFI':2})
#     它跑得通、数字也齐全，但【凭空发明了顺序】：模型会以为
#       BEA < FAU < MFI（有了先后）、FAU 夹在中间、MFI 到 BEA 的"距离"是到 FAU 的两倍。
#     这三件事一件都不是真的 —— MFI/FAU/BEA 之间根本没有大小关系。
#     对线性模型后果最严重：它算 w × 编号，编号 2 的权重自动是编号 1 的两倍。
#     通用判据：把 BEA 这个名字换成 CHA（数据一个字不动），编号全变；
#               结论跟着变 → 说明这个编码里掺了假信息。
#
#  ✅ 正解：pd.get_dummies（独热编码 one-hot encoding）
#     dummies = 哑变量 / 虚拟变量。"哑" = 不会说话，只回答"是不是"。
#     columns=['topology'] 里那个方括号是【列表】，所以能一次传多列。
#     结果：4 列 → 6 列（osda, temp, success + topology_BEA / topology_FAU / topology_MFI）
#     新列是 True/False；给模型用的时候 True 和 1 等价。
#     每一行恰好只有 1 个 True —— 所以叫 "one-hot"（只有一个热的）。
# ============================================================
print(df.dtypes)
print(df['topology'].map({'BEA':0, 'FAU':1, 'MFI':2}))
print(pd.get_dummies(df, columns=['topology']))

print(pd.get_dummies(df, columns=['topology', 'osda']))   # 方括号是列表，可以一次处理多列

# ============================================================
#B9  【门 B 自造数据段的最后一步】划分训练/测试 —— 亲手把 0.67 跑成 0.33
#  纪律：用来"算规则"的数据，和用来"测规则"的数据，必须彻底分开。
#  （第 25-32 行已经记过：上面那次 0.67 是泄漏的，训练集和测试集重叠了）
#
#  ⚠️ 踩过的坑 1：KeyError: 0
#     原来写成  for topo in train.index
#     —— train 是【一张表】，它的 .index 是【行号】(0,1,2,3,4,5)，
#        所以 train_rates[0] 找不到 → KeyError。
#     要遍历的是"有哪些拓扑"，必须用 train_rates.index（groupby 结果的【分组名】）。
#     记忆钩子：.index = "这个东西的『名字那一栏』"。
#        表的名字栏 = 行号；groupby 结果的名字栏 = 分组名。
#     下面两行 print 就是当时用来对照的证据。
#
#  ⚠️ 踩过的坑 2：列名取错
#     原来写成  pred2 = test['success'].map(rule2)
#     rule2 的键是【拓扑名】，而 success 里装的是 0/1 → .map 全部给 NaN
#     → 准确率会假成 0.00（一个跑得通、但完全错的数字）
#     正解：test['topology'].map(rule2)
#
#  ✅ 结果：rule2 = {'FAU': 0, 'MFI': 1}  ← 注意【没有 BEA 这一档】！
#         pred2 里两行 BEA 全变 NaN → 全判错 → 准确率 0.33（泄漏版是 0.67）
#  为什么掉这么多：BEA 这个拓扑在训练集（行 0-5）里【一行都没出现过】，
#     规则表里自然没有这一档，测试集里那两行 BEA 就全查不到。
#  ⇒ 《总计划》§4.3 原话："正确切分后分数通常会掉 —— 那个差距是'发现'，不是'失望'。"
# ============================================================
train=df.head(6)                 # head(6) = 取前 6 行当训练集
test=df.tail(3)                  # tail(3) = 取后 3 行当留出集（严格分开！）
rule2={}
train_rates=train.groupby('topology')['success'].mean()   # 注意：用 train，不是 df
for topo in train_rates.index:   # ← 必须用 train_rates.index，不能用 train.index
    if train_rates[topo]>0.5:
        rule2[topo]=1
    else:
        rule2[topo]=0
print(rule2)

print(train.index)               # 表的 .index = 行号 → RangeIndex(0..5)
print(train_rates.index)         # groupby 的 .index = 分组名 → Index(['FAU','MFI'])
pred2 = test['topology'].map(rule2)   # ← 是 topology，不是 success
print(pred2)
hit2 = (pred2 == test['success'])
print(hit2)
print(f'严格切分后的准确率: {hit2.mean():.2f}')