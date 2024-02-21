import os
 
def makexml(txtPath):  # 读取txt路径，xml保存路径，数据集图片所在路径
        files = os.listdir(txtPath)
        for i, name in enumerate(files):
            txtname= txtPath + name
            #使用with open，不用close
            with open(txtname) as txtFile:
                txtList = txtFile.readlines()
            with open(txtname, 'w') as f:

              for line in txtList:
                try:
                  print(line)
                  line_split = line.strip().split()
                  if line_split[0] == '4':
                      line_split[0] = '3'
                # #   if line_split[0] == '1':
                # #       line_split[0] = '6'
                #   # if line_split[0] == '2':
                #   #     line_split[0] = '1'
                #   else:
                #       line_split[0] = '3'
                  first_char = line_split[0]
                  if first_char.isdigit() or first_char[1] == '.':
                    # 如果是浮点数，将其转换为整数
                    line_split[0] = str(int(float(line_split[0])))
                  f.write(
                      line_split[0] + ' ' +
                      line_split[1] + " " +
                      line_split[2] + " " +
                      line_split[3] + " " +
                      line_split[4] + '\n')
                except IndexError as e:
                  continue
 
 
if __name__ == "__main__":
    txtPath = r"/1T/liufangtao/datas/glass_changxin/1008/labels/"
    makexml(txtPath)


# 类别 0: 4636 个
# 类别 11: 29 个
# 类别 2: 14 个
# 类别 0.0: 16 个
# 类别 9: 4 个
# 类别 5: 9 个
# 类别 10: 13 个
# 类别 3: 1 个
# 类别 4: 2 个
# 类别 7: 13 个
# 类别 2.0: 1 个
# 类别 7.0: 2 个