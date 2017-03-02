n_sample = 1000
txt = open('dummy-data.txt', 'w')
for i in range(n_sample):
    txt.writelines(str(i + 1) + ' 1 0 1 0 ' + 'cat.jpg\n')