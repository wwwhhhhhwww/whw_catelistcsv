d = {"a": 1, "b": 2}           d = {"x": 1}
print(d.get("c", 0))  #0        d["y"] = d["x"] + 1
print("a" in d)     #True        print(len(d))    #2
                               print(d["y"])   #2




d = {"p": 1, "q": 2}                          def f(x, k=3):
for k, v in d.items():                        return x ** k
    print(k, v * 10)  #'p':10 /n 'q':20       print(f(2))      #8
                                              print(f(2, 2))   #4





def s(nums):
    return min(nums), max(nums), sum(nums)/len(nums)
a, b, c = s([2, 4, 6])
print(a, b, c)        #2,6,4



line = "ZSM5-1,50,170\n"                         nums = [1, 2, 3, 4]                          name, conv = "ZSM5-1", 85.234
print(line.strip().split(","))   #[ZSM5-1,50,170]  print([n ** 2 for n in nums])  #1,4,9,16   print(f"{name} 转化率 {conv:.1f}%")     # ZSM5-1 转化率 85.2%
