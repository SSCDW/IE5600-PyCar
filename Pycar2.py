#Pycar (version one)
#Implement with no Class
import datetime

Reservation_num = 0


#Outlet A
a_o = datetime.time(9,0) #Open Time
a_c = datetime.time(18,0) #Close Time
#Outlet B
b_o = datetime.time(9,0) #Open Time
b_c = datetime.time(18,0) #Close Time
#Outlet C
c_o = datetime.time(8,0) #Open Time
c_c = datetime.time(20,0) #Close Time



# Add Car module
def Add_Car(dic_car):
    #input new car's data
    temp_dict = {}
    license_1,make,model,category,status,outlet = input('please input the new cars license make,model,category.status,outlet and separated by commas：\n Example:SE001A, Toyota, Corolla, Sedan, Available, Outlet A:\n ').split(',')
    
    if dic_car.get(license_1.strip()) == None:#判断牌照号是否已存在 （需要判断）
        
        temp_dict = {license_1.strip():{}}#set a temporary new dict
        
        #check the input data 'category','status' and 'outlet'
        
        if category.strip() not in ["Sedan","SUV","MPV"]:
            print('Input category error!')
        elif status.strip() not in ['Available','Allocated','Pickup','Maintenance']:
            print('Input status error!')
        elif outlet.strip() not in ['Outlet A' ,'Outlet B','Outlet C']:
            print('Input outlet error!')
        else:
            #integrate the info into one dict
            temp_dict[license_1]['make'] = make
            temp_dict[license_1]['model'] = model
            temp_dict[license_1]['category'] = category
            temp_dict[license_1]['status'] = status
            temp_dict[license_1]['outlet'] = outlet
            
            return temp_dict #最后的加入过程在主函数中（还没加）
        
    else: 
        print('the license is already exist!')
        
        


def Reserve_Car(dic_car,Reservation_dict):
    
    global Reservation_num
    name,c_category,pickup_d,return_d,pickup_outlet,return_outlet = input('Please input following info\n Example:Alice, Sedan, 03/10/22 08:00, 05/10/22 06:00, Outlet A, Outlet A:\n').split(',')
    #将两个datetime数据正确储存
    pickup_datetime = datetime.datetime.strptime(pickup_d.strip(),'%d/%m/%y %H:%M')# 正确的储存形式
    return_datetime = datetime.datetime.strptime(return_d.strip(),'%d/%m/%y %H:%M')
    #接下来是判断过程
    #Reservation Check
    temp_dict ={}
    
    # Whether Outside Outlet Operating Hours
    pickup_true = Check_Outlet_isavailable(pickup_datetime,pickup_outlet.strip())
    return_true = Check_Outlet_isavailable(return_datetime,return_outlet.strip())
    
    if pickup_true and return_true:
        #print('input time avaliable')
        available_carinfo = {}
        license_temp = 0
        available_carinfo,license_temp = Dict_AvailableCar(c_category.strip(),pickup_datetime,return_datetime,pickup_outlet.strip(),return_outlet.strip(),dic_car)
        
        if available_carinfo == None:
            print('Not Available\n')
            
        elif available_carinfo['outlet'] == pickup_outlet.strip():
            
            
            #更新所有信息到主dict
            available_carinfo['status'] = 'Allocated' #改变当前car的状态
            available_carinfo['pickuptime'] = pickup_datetime
            available_carinfo['returntime'] = return_datetime
            available_carinfo['pickoutlet'] = pickup_outlet.strip()
            available_carinfo['returnoutlet'] = return_outlet.strip()
            dic_car.update(available_carinfo)
            
            #更新所有信息到订单dict
            Reservation_num += 1
            temp_key = '#{}'.format(Reservation_num)
            temp_dict= {temp_key.strip():{}}
            temp_dict[temp_key]['outlet'] = pickup_outlet.strip()
            temp_dict[temp_key]['license'] = available_carinfo.keys()
            
            Reservation_dict.update(temp_dict)
            #计算总成本
            sum_cost = cost_cal(pickup_datetime,return_datetime,c_category.strip())
            print('Avaliable,${} and Reserved with #{}'.format(sum_cost,Reservation_num))
            
        elif available_carinfo['outlet'] != pickup_outlet.strip():
            #更新所有信息到主dict
            available_carinfo['outlet'] = return_outlet.strip()
            available_carinfo['status'] = 'Allocated' #改变当前car的状态
            available_carinfo['pickuptime'] = pickup_datetime
            available_carinfo['returntime'] = return_datetime
            available_carinfo['pickoutlet'] = pickup_outlet.strip()
            available_carinfo['returnoutlet'] = return_outlet.strip()
            dic_car.update(available_carinfo)
            
            #更新所有信息到订单dict
            Reservation_num += 1
            temp_key = '#{}'.format(Reservation_num)
            temp_dict= {temp_key.strip():{}}
            temp_dict[temp_key]['outlet'] = pickup_outlet.strip()
            temp_dict[temp_key]['license'] = available_carinfo.keys()
            
            Reservation_dict.update(temp_dict)
            #计算总成本
            sum_cost = cost_cal(pickup_datetime,return_datetime,c_category.strip())
            print('Available(Sufficient Transit Time),')
            #print('${} and Reserved with #{}'.format(args, kwargs))
            
        #elif available_carinfo[]
    
    else:
        print('Not Available (Outside Outlet Operating Hours)\n')
        
        
def cost_cal(a,b,c):
    day = (b-a).days
    if (b-a).seconds != 0:
        day += 1
    if c == "Sedan": return day*100
    elif c == "SUV": return day*150
    elif c =="MPV": return day*200
        
        
  
         
    # reserve 的过程只需要返回是否可订和原因就行了
#找到可用的汽车并返回
def Dict_AvailableCar(c_category,pickup_datetime,return_datetime,pickup_outlet,return_outlet,dic_car):
    
    for  license_R in list(dic_car.keys()):
        if dic_car[license_R]['status'] != 'Maintenance':#
            if dic_car[license_R]['status'] == 'Available':
                if dic_car[license_R]['outlet'] == pickup_outlet:
                    #dic_car[license_R]['status'] = 'Allocated' #Change status
                    return dic_car[license_R],license_R
                else: #判断是否有足够时间运送
                    if dic_car[license_R]['outlet'] == 'Outlet C' and pickup_datetime.time().hour >= 10: #判断是否能有足够时间取到车（不够完善，只考虑了与取货当天提前2h，没考虑能否前一天提前开车到预约点）
                        #dic_car[license_R]['status'] = 'Allocated' # Remember change Outlet location
                        return dic_car[license_R],license_R
                    elif dic_car[license_R]['outlet'] == 'Outlet A' and pickup_datetime.time().hour >= 11:
                        #dic_car[license_R]['status'] = 'Allocated' # Remember change Outlet location
                        return dic_car[license_R],license_R
                    elif dic_car[license_R]['outlet'] == 'Outlet B' and pickup_datetime.time().hour >= 11:
                        #dic_car[license_R]['status'] = 'Allocated' # Remember change Outlet location
                        return dic_car[license_R],license_R
            else: 
                #判断被预定或者取走的车能不能继续使用
                judge_pickuptime = pickup_datetime - datetime.timedelta(hours=2)
                if dic_car[license_R]['returnoutlet'] !=pickup_outlet:#归还地址和取货地址不一样
                    if judge_pickuptime.__ge__(dic_car[license_R]['returntime']):
                        return dic_car[license_R],license_R
                    else: 
                        return None
                else:#归还地址和取货地址一样
                    if pickup_datetime.__ge__(dic_car[license_R]['returntime']):
                        return dic_car[license_R],license_R
                    else: 
                        return None
                
    
    
    
    #查询已预定或使用的车是否可满足订单
    #for license_RP in list(dic_RPCar.keys()):
        #if dic_RPCar[license_RP]['outlet'] = pickup_outlet:
           # if dic_RPCar[license_RP]['pickup_datetime'] = pickup_datetime:
                
                
                
                
        
        
        
                
#检查输入的取货或者归还时间是否在营业时间
def Check_Outlet_isavailable(x,y):
    
    if y == 'Outlet A':
        
        if x.time().__ge__(a_o) and x.time().__le__(a_c):
            return True
        else:
            return False
    
    elif y == 'Outlet B':
        
        if x.time().__ge__(b_o) and x.time().__le__(b_c):
            return True
        else:
            return False
    
    elif y == 'Outlet C':
        
        if x.time().__ge__(c_o) and x.time().__le__(c_c):
            return True
        else:
            return False
        
    else: print('Outlet Input Error !')
    


#def Allocate_Car():

    




 #def Pickup_Car():

    


 #def Return_Car():
    

def main():
    
    # Initial data
    dic_init ={'SE001A': {'make': 'Toyota','model': 'Corolla','category': 'Sedan','status': 'Available','outlet': 'Outlet A'},
               'SE002A': {'make': 'Toyota','model': 'Corolla','category': 'Sedan','status': 'Available','outlet': 'Outlet A'},
               'SE003A': {'make': 'Toyota','model': 'Corolla','category': 'Sedan','status': 'Maintenance','outlet': 'Outlet A'},
               'SE001B': {'make': 'Honda','model': 'Civic','category': 'Sedan','status': 'Available','outlet': 'Outlet B'},
               'SE002B': {'make': 'Honda','model': 'Civic','category': 'Sedan','status': 'Available','outlet': 'Outlet B'},
               'SE003B': {'make': 'Honda','model': 'Civic','category': 'Sedan','status': 'Maintenance','outlet': 'Outlet B'},
               'SE001C': {'make': 'Kia','model': 'Cerato','category': 'Sedan','status': 'Available','outlet': 'Outlet C'},
               'SU002C': {'make': 'Subaru','model': 'Forrester','category': 'SUV','status': 'Available','outlet': 'Outlet C'},
               'MP003C': {'make': 'Honda','model': 'Odyssey','category': 'MPV','status': 'Available','outlet': 'Outlet C'}}
    
    
    dic_car = {} # Dict of all the cars
    Reservation_dict = {} #Dict of all the revervation list
    
    
    
    
                          
    # Load Initaial Data
    dic_car.update(dic_init)
    
    
    #Add_Car()
    for i in range(6):
        Reserve_Car(dic_car,Reservation_dict)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    
    main()