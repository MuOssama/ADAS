def arrange_list(lst, order):
    #this function arranges a list quarters
    #the input is like order = "2 1R 4 3"
    #by this input, the list has the 2nd element on first 
    #and the second elemnt is the first but reversly and so on
    quarter_length = len(lst) // 4
    quarters = [
        lst[0:quarter_length],
        lst[quarter_length:2*quarter_length],
        lst[2*quarter_length:3*quarter_length],
        lst[3*quarter_length:]
    ]

    result = []
    #for i in lst:
	#print(i)   
    print("LLLLLLLLLLLLLLLLLLLLLLLLLL") 
    for q in order.split():
        index = int(q[0]) - 1
        if len(q) > 1 and q[1] == 'R':
            result.extend(quarters[index][::-1])
        else:
            result.extend(quarters[index])
   # for i in result:
   #	print(i)
    for itr,data in enumerate(result):
        data[0] = itr
        print(data)
    return result

import math

def filter_readings(readings, car_width_half=0.75):
    i = 0
    readingNumber = len(readings)
    filtered_readings = []

    x=[]  
    for reading in readings:
        i += 1
        index_angle = reading[0]
        L = reading[1]
        lo=L
        angle = float(360.0 * index_angle / 1147.0)


        if index_angle>286:
		angle=180-angle
        

        #replace the lidar reading by Lsin(angle)
        Lsin_angle = L * math.sin(math.radians(angle))
        reading[1] = Lsin_angle

        Lcos_angle = L * math.cos(math.radians(angle))
            


        if L == 'inf':
            filtered_readings.append(reading)
            x.append([reading,angle,lo])
            continue
        



        if Lcos_angle <= car_width_half:
            filtered_readings.append(reading)
            x.append([reading,angle,lo])
	    
        if Lcos_angle > car_width_half:
            print([reading,angle,lo])
	    print("tatatatata")


	if i>573:
            print("Angle exceeded 180")
	    break

    for i in x:
	print(i)
    return filtered_readings



# Filter readings
#filtered_readings = filter_readings(readings)

#print(filtered_readings)


"""
this functions used to edge detection
"""
def group_lists(data, threshold=1):
    #this function used to group relenvant lines
    grouped = []
    current_group = []

    for i, item in enumerate(data):
        if not current_group:
            current_group.append(item)
        else:
            if item[0] - current_group[-1][0] <= threshold:
                current_group.append(item)
            else:
                grouped.append(current_group)
                current_group = [item]
                
    if current_group:
        grouped.append(current_group)
    for f in grouped:
	print(f)
	print("f\nf\nf\nf\nf\nf\n")
    return grouped
    

def find_lowest_average(data):
    #this function calculates the lowest average which is x(t)
    result = []
    averages = []
    if len(data)==0:
	return 0
    for sublist in data:
        if len(sublist)<2:
            continue
        first_elements = [item[0] for item in sublist]
        second_elements = [item[1] for item in sublist]
        
        mean_first = sum(first_elements) / len(first_elements)
        mean_second = sum(second_elements) / len(second_elements)
        
        result.append([mean_first, mean_second])
        averages.append(mean_second)

    # Find the index of the minimum average
    min_avg_index = averages.index(min(averages))
    lowest_avg_list = result[min_avg_index]

    return lowest_avg_list
    
    
def edgeDetecting(readings):
    readings = arrange_list(readings,"4 1 2 3")
    readings = filter_readings(readings, car_width_half=0.75)
    readingsLen = len(readings)
    theshould = 0.2
    for i in range(0, readingsLen):
        try:
            Element1 = float(readings[i][0])
            Element2 = float(readings[i][1])
            readings[i][0] = Element1
            readings[i][1] = Element2
            
        except:
            Element1 = float(readings[i][0])
            Element2 = 0
            readings[i][0] = Element1
            readings[i][1] = Element2

    for f in readings:
        print(f)
    print("ssssssssssssssssssss")

    objects = []
    for i in range(5,readingsLen-5):
        cnt = 0
        for j in range(i-4,i+3):
            if readings[j][1]<readings[i][1]+theshould and readings[j][1]>readings[i][1]-theshould and readings[i][1]>0.001 :
                cnt+=1
                
        if cnt >= 7:
            objects.append([readings[i][0],readings[i][1]])
    
    for i in objects:
          print(i)
    print('hhhhhhhhhhhhhhhh')
    
    #group the relevant lines together
    objects = group_lists(objects, threshold=1)

    for i in objects:
          print(i)
    print('gggggggggggggggg')
    
    xt = find_lowest_average(objects)
    print(xt[0],xt[1])
    return xt
    print("\n\n\n")
