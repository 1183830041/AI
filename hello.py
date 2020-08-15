#用户名和密码写入文档
def WriteToFile(usrname,usrpwd,filename):
    f1 = open(filename,'a+')
    f1.writelines(usrname + '\t' + usrpwd + '\n')
    f1.close()

#删除用户名和密码          
def DeleteUsrData(usrname, filename):
    flag = False
    f2 = open(filename, 'r')
    l1 = []
    for e in f2.readlines():
        a,b = e.split('\t')
        if a == usrname:
            flag = True
            pass
        else:
            l1.append(e)
    f2.close()
    f1 = open(filename, 'w+')
    f1.writelines(l1)
    f1.close()
    return flag

#通过搜索用户名找到相对于的密码并输出密码，在此之前先删除换行符再解密。
def Queryuserpassword(usrname, filename):
    f2 = open(filename, 'r')
    for e in f2.readlines():
        a, b = e.split('\t')
        if a == usrname:
            print(Decryption(Removethenewlinecharacter(b)))
            return True    
    return False 

#删除用户输入时的空格和分割符等等。
def Invalidcharacterprocessing(usrname):
    return usrname.replace(" ", "").replace("\t", "")

#给用户名和密码加密
def Convertascllcode(usrname):
    str = ''
    for i in usrname:
        str += chr(ord(i) + 4)
    return str

#给用户名和密码解密
def Decryption(usrpwd):
    str = ''
    for i in usrpwd:
        str += chr(ord(i) - 4)
    return str 

#删除查询时密码后面的换行符。
def Removethenewlinecharacter(usrpwd):
    str = ''
    for i in usrpwd:
        if i != '\n':
          str += i
    return str

#利用冒泡法进行排序
def Sorting(filename):
    f2 = open(filename, 'r')
    l1 = []
    l2 = []
    for e in f2.readlines():
        a,b = e.split('\t')
        l1.append(a)
        l2.append(b) 
    for i in range(len(l1)):
        for j in range(0,len(l1)-i-1):
            if i < len(l1)-1:
                l = PartialOrder(l1[j],l1[j+1])
                if l > 0:
                    l1[j],l1[j+1] = l1[j+1],l1[j]
                    l2[j],l2[j+1] = l2[j+1],l2[j]
    f1 = open(filename, 'w')
    for usrname in range(len(l1)):
        for usrpwd in range(len(l2)):
            if usrname == usrpwd:
                f1.write(l1[usrname] + '\t' + l2[usrpwd])            
    f1.close()
    f2.close()

#比较来个字符串大小算出值   
def PartialOrder(str1, str2):
    l = min(len(str1), len(str2))
    a = 0
    for i in range(0,l):
        if str1[i] != str2[i]:
            a = ord(str1[i]) - ord(str2[i])
            return a
    return len(str1) -len(str2)

#利用二分法进行查询        
def binarySearch (l1, l, r, usrname):
    if r >= l:
        mid = int(l + (r - l)/2)
        if l1[mid] == usrname: 
            return mid
        elif l1[mid] > usrname: 
            return binarySearch(l1, l, mid-1, usrname)
        else: 
            return binarySearch(l1, mid+1, r, usrname)
    else:
        return -1


if __name__ == "__main__":
    opt = input('1：增加\t2：删除\t3: 改变\t4: 查询\t5：退出')
    if opt == "1":
        usrname = Convertascllcode(Invalidcharacterprocessing(input("输入用户名：")))
        usrpwd = Convertascllcode(input("输入密码："))
        WriteToFile(usrname,usrpwd,"filename.txt")
        Sorting("filename.txt")
    if opt == "2":
        usrname = Convertascllcode(Invalidcharacterprocessing(input("输入用户名：")))
        tag = DeleteUsrData(usrname, "filename.txt")
        if tag:
            print('该用户已删除')
        else:
            print('用户不存在')
            
    if opt == "3":
        usrname = Convertascllcode(Invalidcharacterprocessing(input("输入用户名：")))
        tag = Queryuserpassword(usrname, "filename.txt")
        tag = DeleteUsrData(usrname, "filename.txt")
        usrname = Convertascllcode(Invalidcharacterprocessing(input("输入用户名：")))
        usrpwd = Convertascllcode(input("输入密码："))
        WriteToFile(usrname,usrpwd,"filename.txt")
        Sorting("filename.txt")

    if opt == "4":
        f = open("filename.txt",'r')
        l1 = []
        l2 = []
        for e in f.readlines():
            a,b = e.split('\t')
            l1.append(a)
            l2.append(b)
        usrname = Convertascllcode(Invalidcharacterprocessing(input("输入用户名：")))
        result = binarySearch(l1, 0, len(l1)-1,usrname) 
        if result != -1: 
            print (l2[result])
        else: 
            print ('用户不存在')    
        
        
