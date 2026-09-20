# 目标：造 9 行 CSV(topology,osda,temp,success) → 读回 → 按拓扑统计 → 打印


with open('data_1.csv','w',encoding='utf-8')as f:
    f.write('topology,osda,temp,success\n')
    f.write('MFI,TPAOH,170,1\n')
    f.write('MFI,TPAOH,165,1\n')
    f.write('MFI,TPAOH,160,0\n')
    f.write('MFI,TPAOH,175,1\n')
    f.write('FAU,TMOAH,150,0\n')
    f.write('FAU,TMOAH,155,1\n')
    f.write('FAU,TMOAH,145,0\n')
    f.write('BEA,TEAOH,180,1\n')
    f.write('BEA,TEAOH,185,0\n')


groups={}
with open('data.csv','r',encoding='utf-8')as f:
    lines=f.readlines()
for line in lines[1:]:
    row=line.strip().split(',')
    topo=row[0]

    if topo not in groups:
        groups[topo]=[]
    groups[topo].append(row)

print(groups)
print(type(groups['MFI']))
print(groups['MFI'])
def states(rows):
    sum_n=len(rows)
    success_n=0
    sum_temp=0
    for row in rows:
        sum_temp+=int(row[2])
        if row[3]=='1':
            success_n+=1
    aver_temp=sum_temp/sum_n
    success_rate=success_n/sum_n
    return sum_n,success_n,success_rate,aver_temp

for topo in groups:
    n,success_n,rate,aver = states(groups[topo])
    #print(topo)
    #print(type(topo))
    #print(groups[topo])
    print(f"  {topo} : 总次数为{n}，成功次数为{success_n}，成功率为{rate:.2f}，平均温度为{aver:.1f}")


















