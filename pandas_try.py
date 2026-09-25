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

#B7a  pandas清洗
dirty=pd.read_csv('dirty_data.csv')
print(dirty)
print(dirty.isna().sum())
print(dirty.dropna())

#B7b
dirty['temp'] = pd.to_numeric(dirty['temp'], errors='coerce')   # 转不动 → NaN
print(dirty.isna().sum())                                       # 数空
print(dirty.dropna())                                           # 丢掉含空的行


#B8
print(df.dtypes)
print(df['topology'].map({'BEA':0, 'FAU':1, 'MFI':2}))
print(pd.get_dummies(df, columns=['topology']))


