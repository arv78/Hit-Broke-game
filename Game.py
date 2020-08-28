from tkinter import *
import tkinter.messagebox
import random
import array

#most important function of project
#computes number of loses and wins for a specific movement of computer
def play(distance,win,lose,level,p_moves,c_moves):
    #levels that can be checked are limited
    if(level<=0):
        return win,lose
    #all possible movements that user can do
    for i in p_moves:
        #user win
        if(max(p_moves)>distance):
            lose+=1
            break
        #all possible movements that computer can do
        for j in c_moves:
            #computer win
            if(max(c_moves)>distance-i):
                win+=1
                break
            #continue the tree
            win,lose=play(distance-i-j,win,lose,level-1,p_moves,c_moves)
    return win,lose


class Game:
    def __init__(self,player_num,computer_num,distance2,distance,p_moves,c_moves,best_move,flag,flag2,distance_rect1,distance_rect2):
        self.window = Tk()
        # middle window
        window_height = 435
        window_width = 800
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        
        self.window.title("Hit & broke")
        self.distance = distance
        self.best_move = best_move
        self.distance2 = distance2
        self.distance_rec1 = distance_rect1
        self.distance_rec2 = distance_rect2
        self.flag = flag
        self.flag2 = flag2

        self.canvas = Canvas(self.window, width = 800,height = 400,bg = "khaki3")
        self.canvas.grid(row=1,column=1,columnspan=3)
        
        # the moves
        frame1 = Frame(self.window)
        frame2 = Frame(self.window)
        frame1.grid(row=2,column=1)
        frame2.grid(row=2,column=3)
        label1 = Label(frame1,text = "Which move: ")
        label1.grid(row=1,column=1)
        
        self.val = IntVar()
        last = -1
        for i in range (0,player_num):
            globals()['rb_move_%s'%(i+1)] = Radiobutton(frame1,text = p_moves[i],variable = self.val,value = p_moves[i]).grid(row=1,column=(i+2))
            last = i
        
        label2 = Label(frame2,text = "computer moves: ")
        label2.grid(row=1,column=1)
        for j in range (0,computer_num):
            globals()['lb_move_%s'%(j+1)] = Label(frame2,text = c_moves[j]).grid(row=1,column=(j+2))
            
        # the canvas shapes
        self.off_set = (eval(self.canvas["width"]) - self.distance2)//2
        self.canvas.create_line(self.off_set,(eval(self.canvas["height"])//2)+100,(eval(self.canvas["width"]) - self.off_set),(eval(self.canvas["height"])//2)+100,width = 5,fill = "blue",tags = "line")

        if self.flag ==0:
            self.canvas.create_rectangle(self.off_set,(eval(self.canvas["height"])//2)+85,self.off_set+5,(eval(self.canvas["height"])//2)+90,fill = "black",tags = "rect1")
            self.canvas.create_rectangle((eval(self.canvas["width"]) - self.off_set),(eval(self.canvas["height"])//2)+85,(eval(self.canvas["width"]) - self.off_set)-5,(eval(self.canvas["height"])//2)+90,fill = "red",tags = "rect2")
        elif self.flag ==1:
            if self.flag2 ==1:
                self.canvas.create_rectangle(self.distance_rec1,(eval(self.canvas["height"])//2)+85,self.distance_rec1+5,(eval(self.canvas["height"])//2)+90,fill = "black",tags = "rect1")
                self.canvas.create_rectangle(self.distance_rec2,(eval(self.canvas["height"])//2)+85,(self.distance_rec2)-5,(eval(self.canvas["height"])//2)+90,fill = "red",tags = "rect2")        
            elif self.flag2 ==0:
                self.canvas.create_rectangle(self.distance_rec1,(eval(self.canvas["height"])//2)+85,self.distance_rec1+5,(eval(self.canvas["height"])//2)+90,fill = "black",tags = "rect1")
                self.canvas.create_rectangle((eval(self.canvas["width"]) - self.off_set),(eval(self.canvas["height"])//2)+85,(eval(self.canvas["width"]) - self.off_set)-5,(eval(self.canvas["height"])//2)+90,fill = "red",tags = "rect2")

        self.canvas.create_text(eval(self.canvas["width"])-40,10,text="Player : black",font = "Times 10 bold underline",tags = "text1")
        self.canvas.create_text(eval(self.canvas["width"])-30,30,text="CPU : red",fill = "red",font = "Times 10 bold underline",tags = "text2")
        self.canvas.create_text(eval(self.canvas["width"])-70,50,text="Computer's last move: %i"%best_move,fill = "green",font = "Times 10 bold",tags = "text4")
        self.canvas.create_text(eval(self.canvas["width"])-55,70,text="Total distance: %i"%self.distance2,fill = "purple",font = "Times 10 bold",tags = "text5")
        self.Dist = self.canvas.create_text((self.off_set+(self.distance//2)),(eval(self.canvas["height"])//2)+120,text = "distance : %i"%self.distance,font = "Times 10 bold",tags = "text3")
        
        if self.best_move>0:
            self.move_computer()
            bt_choose = Button(frame1,text = "Choose",command = self.move_forward).grid(row=1,column=last+3)
            self.window.mainloop()
        elif self.best_move<=0:
            bt_choose = Button(frame1,text = "Choose",command = self.move_forward).grid(row=1,column=last+3)
            self.window.mainloop()
        
    def move_forward(self):
        #move forward
        self.canvas.move("rect1",self.val.get(),0)  
        if self.flag==0:
            #print("1",self.distance_rec1)
            self.distance_rec1 = self.off_set+self.val.get()
        elif self.flag==1:
            #print("2",self.distance_rec1)
            self.distance_rec1 = self.distance_rec1+self.val.get()
        self.distance = self.distance - self.val.get()
        print("updated distance: ",self.distance)
        self.canvas.delete("text3")
        off_set2 = (eval(self.canvas["width"]) - self.distance)//2
        self.Dist = self.canvas.create_text((off_set2+(self.distance//2)),(eval(self.canvas["height"])//2)+120,text = "distance : %i"%self.distance,font = "Times 10 bold",tags = "text3")
        self.window.destroy()
        
    def move_computer(self):
        self.canvas.move("rect2",-(self.best_move),0)
        if self.flag==0:
            self.distance_rec2 = eval(self.canvas["width"]) - self.off_set - self.best_move
        elif self.flag==1:
            if self.flag2==1:
                self.distance_rec2 = self.distance_rec2 - self.best_move
            elif self.flag2==0:
                self.distance_rec2 = eval(self.canvas["width"]) - self.off_set - self.best_move
        self.distance = self.distance - self.best_move
        print("updated distance: ",self.distance)
        self.canvas.delete("text3")
        off_set2 = (eval(self.canvas["width"]) - self.distance)//2
        self.Dist = self.canvas.create_text((off_set2+(self.distance//2)),(eval(self.canvas["height"])//2)+120,text = "distance : %i"%self.distance,font = "Times 10 bold",tags = "text3")
        
def main():
    flag =0
    flag2 = 0
    distance_rect1 = 0
    distance_rect2 = 0
    S = input("How do you want to enter the inputs?!( random(r), consol(c), text file(f) ) \n")
    if S=="c":      
        # normal input
        p_moves = []
        c_moves = []
        distance = eval(input("What is the total distance?! \n"))
        player_num = eval(input("how many moves does the player have?! \n"))
        computer_num = eval(input("how many moves does the computer have?! \n"))
        print("what are the player moves?! \n")
        for i in range (0,player_num):
            p_moves.append(eval(input()))
        print("what are the computer moves?! \n")
        for i in range (0,computer_num):
            c_moves.append(eval(input()))
        print(p_moves)
        print(c_moves)
          
    elif S=="f":
        # file input
        p_moves = []
        c_moves = []
        p_moves2 = []
        c_moves2 = []
        file1 = open("input.txt","r")
        temp = file1.readline().split()
        distance = eval(temp[0])
        player_num = eval(temp[1])
        computer_num = eval(temp[2])
        for i in range(0,player_num):
            p_moves.append(eval(file1.readline()))
        for i in range(0,computer_num):
            c_moves.append(eval(file1.readline()))
##        distance = eval(file1.readline().strip())
##        nums = []
##        # check with appending method
##        nums = file1.readline().strip()
##        player_num = eval(nums[0])
##        computer_num = eval(nums[2])
        print(distance,player_num,computer_num)
##        p_moves2 = file1.readline().split()
##        c_moves2 = file1.readline().split()
##        for i in range(0,player_num):
##            p_moves.append(eval(p_moves2[i]))
##        for j in range(computer_num):
##            c_moves.append(eval(c_moves2[j]))
        print(p_moves)
        print(c_moves)
        file1.close()

    elif S=="r":        
        # random input
        p_moves = []
        c_moves = []
        distance = random.randint(50,100)
        player_num = random.randint(2,7)
        computer_num = random.randint(2,7)
        last_random = -1
        last_random2 = -1
        for i in range (0,player_num):
            last_random = random.randint(1,25)
            while last_random in p_moves:
                last_random = random.randint(1,25)
            p_moves.append(last_random)
        for j in range (0,computer_num):
            last_random2 = random.randint(1,25)
            while last_random2 in c_moves:
                last_random2 = random.randint(1,25)
            c_moves.append(last_random2)
        print(distance)
        print(p_moves)
        print(c_moves)

    max_user=max(p_moves)
    max_computer=max(c_moves)
    max_total=max(max_user,max_computer)
    # choose the starter of the game
    starter = input("Who's going to start the Game?!(computer(c) or player(p))\n")

    distance2 = distance
    best_move = 0
    if starter == "c" :
        #play the game until someone win
        while(distance>=0):
            #if distance is so big, play maximum number possible
            while(distance>2*(max_computer+max_user)):
                max_play=max_computer
                G1 = Game(player_num,computer_num,distance2,distance,p_moves,c_moves,max_play,flag,flag2,distance_rect1,distance_rect2)
                flag = 1
                flag2 = 1
                distance_rect1 = G1.distance_rec1
                distance_rect2 = G1.distance_rec2
                distance=distance - G1.val.get() - max_play     
            best_win=-2
            best_move=0
            #check all moves that computer can play
            for i in c_moves:
                if(i>distance):
                    best_move=i
                    break 
                #set level
                if((distance>3*((sum(c_moves)/len(c_moves))+(sum(p_moves)/len(p_moves)))) and (len(c_moves)+len(p_moves)>8)):#compare with average
                    level=3
                else:
                    level=7
                print("level=",level)    
                num_win,num_lose=play(distance-i,0,0,level,p_moves,c_moves)
                print(num_win/(num_lose+num_win))
                #select the best movement possible
                if(num_win/(num_lose+num_win)>best_win):
                    best_win=num_win/(num_lose+num_win)
                    best_move=i
                #play best_move
            print("computer's move: ",best_move)
            #computer won
            if(best_move>distance):
                print("computer won")
                tkinter.messagebox.showinfo("Result","Computer Won!!")
                return
            #user's turn
            G1 = Game(player_num,computer_num,distance2,distance,p_moves,c_moves,best_move,flag,flag2,distance_rect1,distance_rect2)
            flag = 1
            flag2 = 1
            distance_rect1 = G1.distance_rec1
            distance_rect2 = G1.distance_rec2
            #computer lost
            if(G1.val.get()>distance - best_move):
                print("user won")
                tkinter.messagebox.showinfo("Result","You Won!!")
                return
            #update the distance
            distance=distance - G1.val.get() - best_move
    elif starter == "p" :
        G1 = Game(player_num,computer_num,distance2,distance,p_moves,c_moves,best_move,flag,flag2,distance_rect1,distance_rect2)
        distance = distance - G1.val.get()
        distance_rect1 = G1.distance_rec1
        distance_rect2 = G1.distance_rec2
        flag = 1
        #play until someone win
        while(distance>=0):
            #if distance is so big, play maximum nuber possible
            while(distance>2*(max_computer+max_user)):
                max_play=max_computer
                G1 = Game(player_num,computer_num,distance2,distance,p_moves,c_moves,max_play,flag,flag2,distance_rect1,distance_rect2)
                flag = 1
                flag2 = 1
                distance_rect1 = G1.distance_rec1
                distance_rect2 = G1.distance_rec2
                distance=distance - G1.val.get() - max_play  
            best_win=-2
            best_move=0
            #check all moves that computer can play
            for i in c_moves:
                if(i>distance):
                    best_move=i
                    break
                #set level
                if((distance>3*((sum(c_moves)/len(c_moves))+(sum(p_moves)/len(p_moves)))) and (len(c_moves)+len(p_moves)>8)):#compare with average
                    level=3
                else:
                    level=7
                print("level=",level)
                num_win,num_lose=play(distance-i,0,1,level,p_moves,c_moves)
                print(num_win/(num_lose+num_win))
                if(num_win/(num_lose+num_win)>best_win):
                    best_win=num_win/(num_lose+num_win)
                    best_move=i
                #play best_move
            print("computer's move: ",best_move)
            #computer won
            if(best_move>distance):
                print("computer won")
                tkinter.messagebox.showinfo("Result","Computer Won!!")
                return
            #user's turn
            
            G1 = Game(player_num,computer_num,distance2,distance,p_moves,c_moves,best_move,flag,flag2,distance_rect1,distance_rect2)
            distance_rect1 = G1.distance_rec1
            distance_rect2 = G1.distance_rec2
            flag = 1
            flag2 = 1
             #computer lost
            if(G1.val.get()>distance - best_move):
                print("user won")
                tkinter.messagebox.showinfo("Result","You Won!!")
                return
            #update the distance
            distance=distance - G1.val.get() - best_move
        
        
main()


