def read_samples(path):
    samples = []                                  # 空列表，准备装记录
    with open(path, encoding="utf-8") as f:       # 打开 path 指定的文件，起名为 f
        lines = f.readlines()                     # 读成"一行一元素"的列表
    for line in lines[1:]:                        # 切片 [1:] = 跳过第 0 行（表头）
        parts = line.strip().split(",")           # 去掉换行，再按逗号切开
        samples.append({                          # 每行做成一个字典，追加进列表
            "name":  parts[0],
            "si_al": float(parts[1]),             # float()：字符串 → 小数
            "temp":  float(parts[2]),
            "conv":  float(parts[3]),
        })
    return lines

samples=read_samples("catalyst_data.csv")
