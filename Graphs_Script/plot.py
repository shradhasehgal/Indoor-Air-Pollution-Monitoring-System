import csv
import numpy as np
import matplotlib.pyplot as plt

sensors = ["NovaPM.txt","Grove_eCO2.txt","Grove_Multichannel.txt","DHT22.txt"]
locations = ["SPCRC","KRB","Workspaces","SH2","CIE","Nilgiri","Paarijat"]
readings = [["PM2.5","PM10"],["VOC","eCO2"],["NH3","CO","NO2"],["Temperature","Humidity"]]
units = [[" (μg/m3)"," (μg/m3)"],[" (ppb)"," (ppm)"],[" (ppm)"," (ppm)"," (ppm)"],[" (Celsius)"," (%RH)"]]
timings = [ [[26,21,20],[27,21,15],[28,21,30]],
            [[26,21,45],[27,21,40],[28,21,55]],
            [[26,22,20],[27,22,5] ,[28,22,20]],
            [[26,22,45],[27,22,30],[28,23,8 ]],
            [[26,23,15],[27,22,55],[28,23,45]],
            [[26,23,48],[27,23,22],[29,0,12 ]],
            [[27,0,20], [27,23,50],[29,0,42 ]] ]
danger_x = [[[0,20],[0,20]],[[0,20],[0,20]],[[0,20],[0,20],[0,20]],[[0,20],[0,20]]]
danger_y = [[[60,60],[100,100]],[[500,500],[5000,5000]],[[35,35],[35,35],[100,100]],[[60,60],[50,50]]]

average = [0,0,0]
number = [0,0,0]

xx = [0]


def flag_update(l,flag,day,hour,minute):
    if day == timings[l][flag][0] and hour == timings[l][flag][1] and minute >= timings[l][flag][2]:
        flag += 1
    return flag

def axis_update(l,index,day,hour,minute,second,x_axis,y_axis,value,quantity):
    
    index -= 1
    con_minute = minute
    
    if minute < timings[l][index][2]:
        con_minute += 60
    
    con_minute -= timings[l][index][2]
    

    if timings[l][index][2] < 40:
        
        if day == timings[l][index][0] and hour == timings[l][index][1] and minute >= timings[l][index][2] and minute <= timings[l][index][2] + 20:
            print('\tOn ', day,'At ', hour, ":",  minute , ', ' , quantity,' was measured to be ', value)
            x_axis[index].append(float(value))
            y_axis[index].append(float(con_minute + (second/60)))  
            average[index] += float(value)
            number[index] += 1

    else:
        if day == timings[l][index][0] and hour == timings[l][index][1] and minute <= 59:
            print('\tOn ', day,'At ', hour, ":",  minute , ', ' , quantity,' was measured to be ', value)
            x_axis[index].append(float(value))
            y_axis[index].append(float(con_minute + (second/60)))
            average[index] += float(value)
            number[index] += 1   

        if timings[l][index][1] == 23:
            if day == timings[l][index][0]+1 and hour == 0 and minute <= 20 - (60 - timings[l][index][2]):
                print('\tOn ', day,'At ', hour, ":",  minute , ', ' , quantity,' was measured to be ', value)
                x_axis[index].append(float(value))
                y_axis[index].append(float(con_minute + (second/60))) 
                average[index] += float(value)
                number[index] += 1  

        else:
            if day == timings[l][index][0] and hour == timings[l][index][1]+1 and minute <= 20 - (60 - timings[l][index][2]):
                print('\tOn ', day,'At ', hour, ":",  minute , ', ' , quantity,' was measured to be ', value)
                x_axis[index].append(float(value))
                y_axis[index].append(float(con_minute + (second/60))) 
                average[index] += float(value)
                number[index] += 1  


for l in range(len(locations)):
    
    for m in range(len(sensors)):


        for n in range(len(readings[m])):
            x_axis = [[],[],[]]
            y_axis = [[],[],[]]
            
            with open(sensors[m]) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                flag = 0
                for row in csv_reader:
                    
                    day = row[0].split()
                    day = day[0].split('-')
                    day = int(day[2])
                    
                    time = row[0].split()
                    time = time[1].split(':')
                    for x in range(len(time)):
                        time[x] = int(time[x])

                    hour = int(time[0])
                    minute = int(time[1])
                    second = int(time[2])

                    if flag < 3:
                        flag = flag_update(l,flag,day,hour,minute)

                    if flag > 0:
                        axis_update(l,flag,day,hour,minute,second,x_axis,y_axis,row[n+2],readings[m][n])

            


            plt.plot(y_axis[0],x_axis[0],'r',label='Pre-Diwali')
            plt.plot(y_axis[1],x_axis[1],'b',label='During Diwali')
            plt.plot(y_axis[2],x_axis[2],'y',label='Post-Diwali')
            plt.plot(danger_x[m][n],danger_y[m][n],'k',label='Danger',linestyle='dashed')

            plt.subplots_adjust(left=None, bottom=0.23, right=None, top=None, wspace=None, hspace=None)
            plt.xlabel('Time (Minutes)', fontsize='medium')
            plt.ylabel(readings[m][n] + units[m][n], fontsize='medium')
            plt.title(locations[l])
            
            print(average[0]," ",number[0])
            print(average[1]," ",number[1])
            print(average[2]," ",number[2])

            if number[0] > 0:
                plt.text(0.10, 0.025, "Average = " + str(int(average[0]/number[0])),transform=plt.gcf().transFigure)
            if number[1] > 0:
                plt.text(0.33, 0.025, "Average = " + str(int(average[1]/number[1])),transform=plt.gcf().transFigure)
            if number[2] > 0:
                plt.text(0.57, 0.025, "Average = " + str(int(average[2]/number[2])),transform=plt.gcf().transFigure)
            
            plt.text(0.78, 0.025, "Danger = " + str(danger_y[m][n][0]),transform=plt.gcf().transFigure)

            plt.legend(loc=9, bbox_to_anchor=(0.5, -0.15), ncol=4)
            string = "Quantity/" + readings[m][n] + "/" + locations[l] + "_" + readings[m][n] + ".png"
            plt.savefig(string)
            string = "Locations/" + locations[l] + "/" + locations[l] + "_" + readings[m][n] + ".png"
            plt.savefig(string)
            plt.show()

            average = [0,0,0]
            number = [0,0,0]