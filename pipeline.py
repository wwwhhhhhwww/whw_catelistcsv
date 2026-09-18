# pipeline.py —— 读数据 → 算指标 → 打印

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
    return samples                                # 交回"列表里装了一堆字典"


def summarize(samples):
    convs = [s["conv"] for s in samples]          # 列表推导式：把每条的 conv 抽成一个新列表
    total = sum(convs)                            # sum() 求和
    best_conv = samples[0]["conv"]                # 先假设第 0 条是最好的
    best_name = samples[0]["name"]
    for s in samples:                             # 每轮 s 是"一个字典"
        if s["conv"] > best_conv:                 # 发现更高的就替换
            best_conv = s["conv"]
            best_name = s["name"]
    return len(samples), best_conv, total / len(convs), best_name   # 一次交回四个值


data = read_samples("catalyst_data.csv")          # 读文件 → 一堆字典
n, hi, avg, best = summarize(data)                # 四个返回值拆给四个变量
print(f"样品数：{n}")                              # f-string：花括号里放变量
print(f"最高转化率：{hi}（样品 {best}）")
print(f"平均转化率：{avg:.1f}")                     # :.1f = 保留 1 位小数

