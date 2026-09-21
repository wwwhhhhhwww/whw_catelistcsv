# robust_read.py —— 读脏数据：好的收下、坏的跳过、最后报告

ok_rows = []
bad_lines = []

with open('dirty_data.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for line in lines[1:]:
    row = line.strip().split(',')
    try:
        temp = int(row[2])                 # 温度：N/A / 空 / abc 会在这儿炸
        success = row[3]                   # 缺列会 IndexError
        if success not in ('0', '1'):      # ★ 新增：主动检查 success 合不合法
            bad_lines.append(line.strip())
        else:
            ok_rows.append(row)            # 全部合格 → 收下
    except (ValueError, IndexError):
        bad_lines.append(line.strip())

print('成功读入:', len(ok_rows), '行')
print('跳过:', len(bad_lines), '行')
print('--- 跳过的行 ---')
for b in bad_lines:
    print(b)
