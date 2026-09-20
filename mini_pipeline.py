with open('data.csv','r')as f:
    lines=f.readlines()
rows=[line.strip().split(',') for line in lines[1:]]

#print(rows)

groups={}
for row in rows:
    topo=row[0]
    if topo not in groups:
        groups[topo]=[]
    groups[topo].append(row)

#print(groups)
print(type(groups))

rule={}
for topo in groups:
    ok=0
    fail=0
    for row in groups[topo]:
        if row[3]=='1':
            ok+=1
        else:
            fail+=1
    if ok>=fail:
        rule[topo]='1'
    else:
        rule[topo]='0'

print(rule)


test = rows[-3:]
print('测试集:', test)


correct = 0
for row in test:
    pred = rule[row[0]]
    real = row[3]
    if pred == real:
        correct += 1
        print(f'拓扑={row[0]}  预测={pred}  真实={real}  → 对')
    else:
        print(f'拓扑={row[0]}  预测={pred}  真实={real}  → 错')

print('猜对', correct, '行')

acc = correct / len(test)
print(f'准确率: {acc:.2f}')

with open('result.txt', 'w', encoding='utf-8') as f:
    for topo in groups:
        n = len(groups[topo])
        ok = len([x for x in groups[topo] if x[3] == '1'])
        rate = ok / n
        f.write(f"{topo} | {n} | {rate:.2f} | {rule[topo]}\n")

    f.write(f"ACC | {len(test)} | {correct} | {acc:.2f}\n")


print('已写出 result.txt')

with open('data_1.csv', 'r', encoding='utf-8') as f:
    lines_1 = f.readlines()

rows_1 = [line.strip().split(',') for line in lines_1[1:]]

print('新实验建议：')
for row in rows_1:
    pred = rule[row[0]]
    row.append(pred)
    print(f'{row[0]}  温度 {row[2]}  → 预测 {row[3]}   (1=成功, 0=失败)')

























