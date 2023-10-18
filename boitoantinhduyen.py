def boitoantinhduyen(ten_nam,ten_nu):
    ten_nam=ten_nam.lower()
    ten_nu=ten_nu.lower()
    dem=0
    for chu_cai in range(ord("a"),ord("z")+1):
        if(chr(chu_cai) in ten_nam) and (chr(chu_cai) in ten_nu):
            dem=dem+1
        if dem==0:
            ket_qua= "Người dưng nước lã, 1 quật 500k"
        elif dem<3:
            ket_qua= "Bạn tình qua đêm"
        else:
            ket_qua= "Khít lỗ đít"
        return ket_qua

print("Nhap ten ban nam")
nam=input()
print("Nhap ten ban nu")
nu=input()
print("Kết quả tình duyên cua 2 ban: "+ nam+ " và "+ nu + " là " + boitoantinhduyen(nam,nu))

