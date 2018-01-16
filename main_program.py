from lcd_display import lcd 
import subprocess
import time
import RPi.GPIO as GPIO

import sys
sys.path.append("/home/pi/raspi-gpio/lib/")

import tool 

GPIO.setmode(GPIO.BOARD)

KEYPAD = [
        [1,2,3,"A"],
        [4,5,6,"B"],
        [7,8,9,"C"],
        [".",0,"#","D"]
]

ROW = [7,11,13,15] # BCM numbering
COL = [12,16,18,22] # BCM numbering
my_lcd=lcd()

def chooseRouter(ROW,COL,KEYPAD,my_lcd):
   scri4="  wc -l 1.txt | awk '{ print $1 }'" 
   count=int(subprocess.check_output(scri4,shell=True))-1 
   print (count)
   my_lcd.display_string("MAX:"+str(count)+" Quit:A",1) 
   for i in range (count): 
     scri5=" sed -n "+str(i+2)+"p 1.txt "
     outd=subprocess.check_output(scri5,shell=True)
     print (outd[0:-1])
   while (True):
     temp=""
     scri5="sed -n "+str(i)+"p 1.txt "
     outd=subprocess.check_output(scri5,shell=True)
     no_of_host=""
     ipcount=0
     while(True):
       for j in range (4):
         GPIO.output(COL[j],0)
         for i in range(4):
             if GPIO.input(ROW[i])==0:
                temp=KEYPAD[i][j]
                if ipcount==3:
                  break
                elif temp=='#':
                  ipcount=3
                  break
                elif temp=='D':
                  ipcount=0
                  no_of_host=""
                else:
                  no_of_host=str(no_of_host)+str(temp)
                  print (no_of_host)
                  my_lcd.display_string("Max:"+str(count)+" Show:"+no_of_host,1)
                  time.sleep(0.2)
                  ipcount=ipcount+1
                while (GPIO.input(ROW[i])==0):
                  pass
         GPIO.output(COL[j],1)
         if ipcount == 3 :
           break
       if ipcount ==3:
         break
     if no_of_host=='':
       break  
     
     scri5="sed -n "+str(no_of_host)+"p 1.txt "

     outd=subprocess.check_output(scri5,shell=True)
     my_lcd.display_string("Max:"+str(count)+" Show:"+no_of_host,1)
     print("---")
     outd = str(outd) 
     outd = outd[2:-3]
     if (outd.find("b")>=0):
         print("the position is ",outd.find("b")) 
     else:
         print("it is not b")
     print("axi "+outd)
     my_lcd.display_string(outd,2) 
     time.sleep(5)

def main():
   subprocess.call('rm 1.txt 2.txt',shell=True)
#keypad input ip
   my_lcd.display_string("Input the IP",1)
   for j in range(4):
     GPIO.setup(COL[j],GPIO.OUT)
     GPIO.output(COL[j],1)
   for i in range(4):
     GPIO.setup(ROW[i],GPIO.IN,pull_up_down = GPIO.PUD_UP)
   ipstr=""
   ipcount=0
   ipstr,ipcount = tool.checkInput(ROW,COL,KEYPAD,my_lcd)
#   run ping script and get the keyword
   tool.pingScript(ipstr,my_lcd) 
   tool.traceRouteScript(ipstr,ROW,COL,KEYPAD,my_lcd)
   scri4="  wc -l 1.txt | awk '{ print $1 }'" 
   count=int(subprocess.check_output(scri4,shell=True))-1 
   print (count)
   my_lcd.display_string("MAX:"+str(count)+" Quit:A",1) 
   for i in range (count): 
     scri5=" sed -n "+str(i+2)+"p 1.txt "
     outd=subprocess.check_output(scri5,shell=True)
     print (outd[0:-1])
   while (True):
     temp=""
     scri5="sed -n "+str(i)+"p 1.txt "
     outd=subprocess.check_output(scri5,shell=True)
     no_of_host=""
     ipcount=0
     while(True):
       for j in range (4):
         GPIO.output(COL[j],0)
         for i in range(4):
             if GPIO.input(ROW[i])==0:
                temp=KEYPAD[i][j]
                if ipcount==3:
                  break
                elif temp=='#':
                  ipcount=3
                  break
                elif temp=='D':
                  ipcount=0
                  no_of_host=""
                else:
                  no_of_host=str(no_of_host)+str(temp)
                  print (no_of_host)
                  my_lcd.display_string("Max:"+str(count)+" Show:"+no_of_host,1)
                  time.sleep(0.2)
                  ipcount=ipcount+1
                while (GPIO.input(ROW[i])==0):
                  pass
         GPIO.output(COL[j],1)
         if ipcount == 3 :
           break
       if ipcount ==3:
         break
     if no_of_host=='':
       break  
     
     scri5="sed -n "+str(no_of_host)+"p 1.txt "

     outd=subprocess.check_output(scri5,shell=True)
     my_lcd.display_string("Max:"+str(count)+" Show:"+no_of_host,1)
     print("---")
     outd = str(outd) 
     outd = outd[2:-3]
     if (outd.find("b")>=0):
         print("the position is ",outd.find("b")) 
     else:
         print("it is not b")
     print("axi "+outd)
     my_lcd.display_string(outd,2) 
     
     time.sleep(5)
main()
