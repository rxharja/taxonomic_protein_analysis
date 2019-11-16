#!/usr/bin/env
import subprocess,sys,time,threading

#Just a fun UI element to show that a process is running. Gives visual feedback to user in form of a spinning wheel
class Spinner:
    busy = False
    delay = 0.1

    #this makes the animation
    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

   
    def __init__(self, out, delay=None):
	#set description of task to out
        self.out = out
        #initialize spinning cursor
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay


    def spinner_task(self):
	#While busy is true, write to same line with a delay of 0.1 so it looks like 
	#an animation of a spinning wheel next to some descriptive text of the task
	#--stty -echo turns off user input to screen, but inputs still happen, it just
	#makes the animation not get messed up by user input
        subprocess.Popen("stty -echo",shell=True)
        while self.busy:
	    #write to screen message next to spinnig wheel, flush to have it display
	    #automatically, otherwise it may wait until while loop finishes running
            sys.stdout.write(self.out + next(self.spinner_generator))
            sys.stdout.flush()
	    #slows writing down to give animation effect
            time.sleep(self.delay)
	    #clear line and return to start
            sys.stdout.write("\r")
            sys.stdout.write("\033[K")
            sys.stdout.flush()
	#turn inputs back on
        subprocess.Popen("stty echo",shell=True)


    #turns busy to true, begins spinner process on seperate thread
    #so program does not stop to display the spinning
    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()


    #exit parameters 
    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False
