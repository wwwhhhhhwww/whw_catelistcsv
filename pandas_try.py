import pandas as pd            # ← 你的第一次 import：把 pandas 工具箱拿进来，起小名叫 pd

df = pd.read_csv('data.csv')   # 一行把 CSV 读成表格
print(df)                       # 打印看看长啥样
print(type(df))                 # 看看它是什么类型

print(df.groupby('topology')['temp'].mean())

print(df.groupby('topology')['success'].mean()) #我觉得这是直接输出成功率

rates = df.groupby('topology')['success'].mean()
print(rates)
print(rates.index)
print(type(rates))
print(type(rates.index))
rule = {}
for topo in rates.index:
    if rates[topo] > 0.5:
        rule[topo] = 1
    else:
        rule[topo] = 0
print(rule)


test=df.tail(3)
pred=test['topology'].map(rule)
print(test)
print(pred)
hit=(test['success']==pred)
print(hit)
print(f"正确率为{hit.mean():.2f}")

rule_jia = {'MFI': 1}                              # 故意只留 MFI
print(df.tail(3)['topology'].map(rule_jia))    # 看它给什么
try:
    print(rule_jia['FAU'])
except KeyError as e:      # as e 把错误对象接住
    print('捕获到:', e)     # 打印它，而不是打印一句没信息量的"报错"






