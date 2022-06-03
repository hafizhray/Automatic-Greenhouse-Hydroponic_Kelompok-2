class EnDecode():
    def enc(self, x, t, n):
        x = 10**t*x
        x = int(round(x, 0))
        if x > 10**n:
            return "9"*n
        for i in range(n + 1):
            if int(x/(10**i)) == 0:
                if i == 0:
                    return "0"*(n-i)
                return "0"*(n-i) + str(x)
    
    def enc_data(self, data):
        data_str = ""
        for i in range(int(len(data)/3)):
            data_str += self.enc(data[3*i], data[3*i+1], data[3*i+2])
        return data_str
    
    def dec_data(self, data, key = "0213130106011301"):
        key_list = []
        for i in key:
            key_list.append(int(i))
        
        data_list = []
        count = 0
        for i in range(int(len(key_list)/2)):
            if key_list[2*i] != 0:
                data_list.append(int(data[count:count+key_list[2*i+1]])/10**key_list[2*i])
            else:
                data_list.append(int(data[count:count+key_list[2*i+1]]))
            count += key_list[2*i+1]
        
        return data_list
        

