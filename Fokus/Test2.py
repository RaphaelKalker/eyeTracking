from multiprocessing import Process, Lock
import time
from random import randint


# imageLock = Lock()image = 'initial'

imageLeft = []
imageRight = []

imageLock = Lock()

def getLeftImage():

    with imageLock:
        global imageLeft
    # with lock:
    #     print image
        return imageLeft

def setLeftImage(value):
    with imageLock:
        global imageLeft
        # with lock:
        print value
        imageLeft = value

def getRightImage():

    with imageLock:
        global imageRight
    # with lock:
    #     print image
        return imageRight

def setRightImage(value):
    with imageLock:
        global imageRight
        # with lock:
        print value
        imageRight = value

def f(l, processNum, delay):

    if  processNum is '1':
        tabs = ''
    else:
        tabs = '\t\t\t\t\t\t\t'

    imageNr = 0

    while imageNr < 10:

        imageNr += 1

        setLeftImage('{} Camera {} \t downloading {}'.format(tabs, processNum, imageNr))
        time.sleep(delay)
        setLeftImage('{} Camera {} \t done {}'.format(tabs, processNum, imageNr))
        # getImage()






    # # with l:
    # #     l.acquire()
    #     for imageNr in range(10):
    #
    #         with l:
    #             print msgDownloading
    #         time.sleep(1) #download image
    #         setImage(msgdone)
    #         with l:
    #             print getImage()
        # l.release()



    #
    # with l:
    # # l.acquire()
    #     time.sleep(randint(0,2))
    #     msg = 'Camera {} \t END'.format(processNum)
    # # print msg
    #     setImage(msg, l)
    #     print getImage(l)
    # l.release()

if __name__ == '__main__':
    lock1 = Lock()
    lock2 = Lock()


    p1 = Process(target=f, args=(lock1, '1', 1))
    p2 = Process(target=f, args=(lock2, '2', 2))

    p1.start()
    p2.start()


    p1.join()
    p2.join()




    # for num in range(2):
    #     # Process(target=f, args=(lock1, lock2, num, '2')).start()


