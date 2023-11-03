# FOR CONNECTION TO FLASHCAM AND NOTIFATOR - SEE FLASHCAM README.org

from console import fg,bg
import importlib
ROOTimported = False
s9009 = None
histogram_v = None
histogram_h = None
try:
    importlib.import_module( "ROOT" )
    ROOTimported = True
    globals()["ROOT"] = importlib.import_module( "ROOT" )
    print(f"i... {fg.green} ROOT     IMPORTED {fg.default}")
except ImportError:
    print(f"i... {fg.red} ROOT NOT IMPORTED {fg.default}")
# finally:
#     print("I... importing",i) # check if fire is imported
#     globals()[i] = importlib.import_module( importnames[i] )
#     print("I... imported:",i)

#import ROOT

import random
import cv2
from flashcam.base_camera2 import BaseCamera

from flashcam.usbcheck import recommend_video
# import base_camera  #  Switches: slowrate....

import datetime as dt
import time
import socket

import glob

import subprocess as sp
import numpy as np

import flashcam.config as config

from  flashcam.stream_enhancer import Stream_Enhancer


from flashcam import v4lc
from flashcam.v4lc import set_gem, get_gem, tune_histo

from flashcam.mmapwr import mmread_n_clear, mmread

import os
import sys

from notifator import telegram
import threading

# there is a problem with ttf fonts to cv2:
from PIL import ImageFont, ImageDraw, Image

from console import fg,bg


try:
    import pyautogui # take screenshot
except:
    print("X... no DISPLAY, pyautogui cannot be used")
# -----------------------------------------------------------------


def is_int(n):
    try:
        float_n = float(n)
        int_n = int(float_n)
    except ValueError:
        return False
    else:
        return float_n == int_n

def is_float(n):
    try:
        float_n = float(n)
    except ValueError:
        return False
    else:
        return True

def is_bool(n):
    if type(n) is str and n=="False": return True
    if type(n) is str and n=="True": return True
    return False



# -----------------------------------------------------------------

class Camera(BaseCamera):

    video_source = 0
    histomean = 50
    #nfrm = 0 # number frame.... nonono
    capdevice = None # global

    @staticmethod
    def init_cam(  ):
        """
        should return videocapture device
        but also sould set Camerare.video_source
        """
        global s9009, histogram_v, histogram_h
        #  - all is taken from BaseCam
        # res = "640x480"
        res = config.CONFIG["resolution"]
        #print("D... init_cam caleld with res:", res )
        #print("i... init_cam caleld with prod:", res )
        #print("D... init_cam caleld with prod:",  config.CONFIG["product"] )
        print("i... init_cam caleld with prod:",  config.CONFIG["product"] )

        vids = recommend_video( config.CONFIG["product"]  ) # if jpg => give -1

        if len(vids)>0:
            if vids[0]==-1:
                return config.CONFIG["product"] , -1

            vidnum = vids[0]
            cap = cv2.VideoCapture(vidnum,  cv2.CAP_V4L2)

            # config.CONFIG["camera_on"] = True

            # - with C270 - it showed corrupt jpeg
            # - it allowed to use try: except: and not stuck@!!!
            #cap = cv2.VideoCapture(vidnum)
            #   70% stucks even with timeout


            #pixelformat = "MJPG"

            pixelformat = "YUYV" # I use lossless format for camera readout
            pixelformat = config.CONFIG['PIXELFORMAT']

            time.sleep(1)
            fourcc = cv2.VideoWriter_fourcc(*pixelformat) # for capture device
            cap.set(cv2.CAP_PROP_FOURCC, fourcc)
            time.sleep(1)

            w,h =  int(res.split("x")[0]), int(res.split("x")[1])
            print(f"i... {fg.green}   RESOLUTIONwh= {w} x {h}, PIXELFORMAT {pixelformat}  {fg.default}")
            cap.set(cv2.CAP_PROP_FRAME_WIDTH,   w )
            time.sleep(0.5)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT,  h )
            print(f"i... {fg.green}   RESOLUTIONwh= {w} x {h}, PIXELFORMAT {pixelformat}  {fg.default}")

            if ROOTimported and s9009 is None:
                print(f"i... {fg.yellow} ------------------------------ server register {fg.default}")
                histogram_h = ROOT.TH1F("hhtest","hhtest",640,0,640)
                histogram_v = ROOT.TH1F("hvtest","hvtest",480,0,480)
                # serv = ROOT.THttpServer("http:9009?loopback")
                serv = ROOT.THttpServer("http:9009")
                serv.Register("/",histogram_h)
                serv.Register("/",histogram_v)
                serv.SetItemField("/", "_monitoring", "1000")
                serv.SetItemField("/", "_layout", "vert2")
                serv.SetItemField("/", "_drawitem", "[hvtest,hhtest]")


                s9009 = serv
            else:
                serv = None
            return cap,vidnum, serv
        return None, None, None

    @staticmethod
    def acquire_one_frame(cap):
        frame = None
        ret = True #  I change it later
        # capture_time=""
        #print("i...acq_onef: cap==", cap)
        if type(cap) == tuple:
            print("i... TUPLE    cap==", cap, "  --->[0]")
            cap = cap[0] # THIS IS STRANGE FOR newcam20211117
            print("i... TUPLE[0] cap==", cap , " type==",type(cap) )
        if (cap is None):
            print("X... cap is none")
            ret = False
        if cap is not None and not cap.isOpened():
            print("X... 1camera  not Opened(@real_cam aof)")
            time.sleep(0.7)
        if cap is not None and not cap.isOpened():
            print("X... 2camera  not Opened(@real_cam aof)")
            # cap.release() ### NOT TESTED
            ret = False
        if ret:
            #print("OK")
            print(f"i... frame {BaseCamera.nframes:8d}  {BaseCamera.capture_time}   ", end="\r" )
            try: #----this catches errors of libjpeg with cv2.CAP_V4L2
                # ret is frequently false on RPI3.... I give 2 more chances
                ret, frame = cap.read()
                if histogram_v is not None and histogram_h is not None:
                    # print(type(frame), len(frame))

                    framered = np.amax(frame, axis=2)

                    suma480 = np.max( framered, axis = 1)
                    suma640 = np.max( framered, axis = 0)

                    #suma480 = np.sum( frame, axis = 1)
                    #suma640 = np.sum( frame, axis = 0)
                    #suma480 =suma480/len(suma480)/3
                    #suma640 =suma640/len(suma640)/3
                    # print(   len(suma480) ,  suma480[100] , np.sum( suma480[100]  ) ) # ax 1 480
                    for i in range(len(suma480) ): # to 480
                        histogram_v.SetBinContent(i, np.sum( suma480[i] ) )
                    for i in range(len(suma640) ): # to 480
                        histogram_h.SetBinContent(i, np.sum( suma640[i] ) )
                        #histogram_v.SetBinContent(i, np.sum( frame, axis = 0)[i] )
                if not ret:
                    print("X... not good read 1 ()")
                    time.sleep(0.1)
                    ret, frame = cap.read()
                    if not ret:
                        print("X... not good read 2")
                        time.sleep(0.2)
                        ret, frame = cap.read()
                        print(f"X... 3rd read result=={ret}")
                        ## cap.release() ## NOT TESTED

                # SIMULATE A PI3B problem
                # frame = cv2.resize(frame, (640,480) )
                if frame is not None:
                    obtres = f"{frame.shape[1]}x{frame.shape[0]}"
                    sucres = obtres == config.CONFIG['resolution']
                    if not sucres:
                        #w,h = config.CONFIG['resolution'].split("x")
                        #dsize = ( int(w), int(h))
                        #frame = cv2.resize(frame, dsize )
                        frame[0:4,0:4] = [0,0,255]
                        print(f" OBTAIN{fg.red}{obtres}{fg.default} ", end = "" )
                    BaseCamera.nframes+=1
                    BaseCamera.capture_time = dt.datetime.now().strftime("%H:%M:%S.%f")[:-4]

            except Exception as ex:
                print("X... SOME EXCEPTION ON cap.read (@real_cam)...", ex)
                config.CONFIG["camera_on"] = False
        # --- camera probably works ret True
        if not ret:
            time.sleep(0.5)
            config.CONFIG["camera_on"] = False
            print("x...  cap didnt go ok, graying... trying to acquire new cap")
            cap = Camera.init_cam( ) # WHAT IS THIS? the same?<= static?
            print(f"?... {fg.red}  cap 1 return === {cap} {fg.default}")
            nfrm = 0
            height, width = 480, 640
            blank_image = np.zeros((height,width,3), np.uint8)
            # GRAY GREY 255 128 ---- half split image in a case ....happens too frequent..
            blank_image[:,0:width//2] = (90,90,90)      # (B, G, R)
            blank_image[:,width//2:width] = (150,150,150)
            frame = blank_image
            # # create gray + moving lines BUT prev_frame is bad sometimes
            # try:
            #     print("D... trying to gray frame")
            #     frame = cv2.cvtColor(frame_prev, cv2.COLOR_BGR2GRAY)
            #     height, width = frame.shape[0] , frame.shape[1]
            #     skip = 10
            #     startl = 2*(nfrm % skip) # moving lines
            #     for il in range(startl,height,skip):
            #         x1, y1 = 0, il
            #         x2, y2 = width, il
            #         #image = np.ones((height, width)) * 255
            #         line_thickness = 1
            #         cv2.line(frame, (x1, y1), (x2, y2), (111, 111, 111),
            #                  thickness=line_thickness)
            # except:
            #     print("X... prev_frame was bad, no gray image")
        return frame, cap



    @staticmethod
    def camera_or_image( cap, vidnum):
        fullpath_fixed_image = "~/.config/flashcam/monoskop.jpg"
        fullpath_fixed_image = os.path.expanduser( fullpath_fixed_image)
        # debug print( cap, vidnum)
        if not os.path.exists(fullpath_fixed_image):
            print("X... monoskop doesnt exist")
            fullpath_fixed_image = None

        if not (vidnum is None) and (vidnum==-1):
            #
            # No videodevice
            #
            #print("i... image mode", type(cap), cap)
            if (cap.find("screenshot.jpg")==0) and ('pyautogui' in globals()):
                print("i... screenshot mode")
                image = pyautogui.screenshot()
                image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

                scale_percent = 50
                width = int(image.shape[1] * scale_percent / 100)
                height = int(image.shape[0] * scale_percent / 100)
                # dsize
                dsize = (width, height)

                # resize image
                frame = cv2.resize(image, dsize)
                time.sleep(0.3) # from 85%cpu to 20% ??????
                return "image", frame, cap # repeat cap==image

            elif cap.find("clock.jpg")==0:
                #
                # demanded 'living' jpg
                #
                height, width = 480, 640
                blank_image = np.zeros((height,width,3), np.uint8)
                blank_image[:,0:width//2] = (20,20,20)      # (B, G, R)
                blank_image[:,width//2:width] = (25,25,25)
                position = (10,150)

                # FONTS https://www.1001fonts.com/search.html?search=digital
                fontpath = os.path.expanduser("~/.config/flashcam/digital-7.mono.ttf")

                font = ImageFont.truetype(fontpath, 4*32)
                img_pil = Image.fromarray(blank_image)
                draw = ImageDraw.Draw(img_pil)
                drtext = dt.datetime.now().strftime("%H:%M:%S.%f")[:-5]

                #draw.text( position,  "国庆节/中秋节 快乐!", font = font, fill = (b, g, r, a))
                b,g,r,a = 0,255,0,200
                draw.text( position,  drtext, font = font, fill = (b, g, r, a))
                frame = np.array(img_pil)
                time.sleep(0.3) # from 85%cpu to 20% with 0.1;
                # cv2.putText(
                #     blank_image, #numpy array on which text is written
                #     drtext, #text
                #     position, #position at which writing has to start
                #     #cv2.FONT_HERSHEY_SIMPLEX, #font family
                #     font,
                #     4, #font size
                #     (249, 240, 250, 55), #font color
                #     5) #font stroke
                # frame = blank_image
                return "image", frame, cap # repeat cap==image

            elif cap.find(".jpg")>=0:
                #
                # any JPG
                #
                #print("i... static image mode")
                capfull = os.path.expanduser( f"~/.config/flashcam/{cap}" )
                if  os.path.exists(capfull):
                    fullpath_fixed_image =  capfull
                else:
                    print("X... image doesnt exist", cap, "using monoskop")

                time.sleep(0.3) # from 85%cpu to 20% with 0.1
                retimg = cv2.imread( fullpath_fixed_image)
                retimg = cv2.resize(retimg, (640,480) )
                return "image", retimg, cap # repeat cap==image
        else:
            #print("i...  camera mode")
            if cap is None and vidnum is None:
                print("X... camera not accessible")
                time.sleep(0.3)
                frame = cv2.resize(cv2.imread( fullpath_fixed_image), (640,480) )
                return "image_forced",  frame, cap # repeat cap==image
            # if there is a new cap => propagate it upsrtream
            frame, newcap = Camera().acquire_one_frame(cap)
            return "camera", frame, newcap
        print("X... NEVER GET HERE..................")
        return None, None, None




    @staticmethod
    def frames( ):
        """
        product= ... uses the recommend_video to restart the same cam
        """
        # i need these to be in globals() ----evaluate from web.py
        #                                 ---- OR FROM seread
        global substract_background,save_background
        global save_image_decor, save_image_png # save camera_screenshot - web feature - unlike savebg - it saves with all decorations
        global mix_foreground,save_foreground
        global send_telegram, telegramlast

        global speedx, speedy, restart_translate, average
        global gamma_divide, gamma_multiply,gamma_setdef
        global gain_divide,gain_multiply,gain_setdef
        global expo_divide,expo_multiply,expo_setdef,  expovalue, gainvalue
        global timelaps, rotate180
        global fixed_image # show not camera but image
        global zoom
        global pausedMOTION
        global overtext, overtextalpha
        global framekind


        global s9009

        # print("i... staticmethod frames @ real -  enterred; target_frame==", target_frame)
        # ----- I need to inform SENH about the resolution

        senh = Stream_Enhancer( resolution = config.CONFIG["resolution"] ) # i take care inside

        senh.zmqtarget = None # initially
        if 'imagezmq' in config.CONFIG:
            senh.zmqtarget = config.CONFIG['imagezmq']
            if senh.zmqtarget=="None":
                senh.zmqtarget = None
        else:
            print("X... need to update config for imagezmq")
            senh.zmqtarget = None

        if 'jtelegram' in config.CONFIG:
            senh.jtelegram = config.CONFIG['jtelegram']
            if senh.jtelegram=="false":
                senh.jtelegram = False
        else:
            print("X... need to update config for imagezmq")
            senh.jtelegram = False


        # === I must have these GLOBAL and PREDEFINED HERE <= web.py
        # --------------------------------  control
        # -----------get parameters for DetMot, same for web as for all
        #print(config.CONFIG)
        #print( "AVERAGE I AM HAVING ",config.CONFIG['average'] )
        framekind    = config.CONFIG['framekind']
        average      = int(config.CONFIG['average'])
        threshold    = int(config.CONFIG['threshold'])
        blur         = int(config.CONFIG['blur'])
        timelaps     = config.CONFIG['laps']
        histogram    = config.CONFIG['Histogram']
        res          = config.CONFIG['resolution']
        speedx       = float(config.CONFIG['x'])
        speedy       = float(config.CONFIG['y'])
        rotate180    = int(config.CONFIG['otate'])
        zoom         = int(config.CONFIG['zoom'])

        MODE_DMbase = "MODE DM"
        MODE_DM = "MODE DM"

        #imagezmq = None # I use senh.zmqtarget....
        #if 'imagezmq' in config.CONFIG:
        #    imagezmq     = config.CONFIG['imagezmq']

        print( "XY: ", config.CONFIG['x'] ,  config.CONFIG['y']  , speedx, speedy)

        # ------------------    to evaluate commands from web.py
        # ------------------    or searead
        # ------------------    these commands need to be declared here
        #                       AND in globals
        substract_background = False
        save_background = False
        save_image_decor = False # save camera_screenshot
        save_image_png = False # save camera_screenshot
        mix_foreground = False
        save_foreground = False

        send_telegram = None # i hope this is ok too...
        telegramlast = dt.datetime.now()

        restart_translate = False

        gamma_divide = False
        gamma_multiply =False
        gamma_setdef =False

        gain_divide = False
        gain_multiply =False
        gain_setdef =False

        expo_divide = False
        expo_multiply =False
        expo_setdef =False
        exposet = False # not used..
        expovalue = -999. # initial
        gainvalue = -999. # initial

        # rotate180 = False # i define earlier from CONFIG

        fixed_image = None # just camera.

        # --- 433MHz
        pausedMOTION = False
        overtext = None
        overtextalpha = 0


        # ==================== GO TO CAMERA AND IMAGE PROCESSING ==============

        camera = Camera(  )
        vidnum = None # it will be re-asked gain and again

        cap, vidnum, s9009 = camera.init_cam(  ) # can return None,None; of jpg,-1






        # *********  video works,  get capacities and go with EXPO GAIN
        if not( (vidnum is None) or (vidnum == -1) ):

            cc = v4lc.V4L2_CTL("/dev/video"+str(vidnum))
            capa = cc.get_capbilities()


            #--- INITIATION...... collecting???

            exposuredef = True
            gammadefX = True
            gaindefX = True

            cc.autoexpo_on("autoexpo")
            if "gain" in capa:
                gain = cc.get_gain()
                print(f"========={bg.orange}{fg.black} GAIN INIT  {gain}{fg.default}{bg.default} =","="*40)
                gaindef = cc.getdef_gain()
                if gaindef == gain:
                    gaindefX = True
                else:
                    gaindefX = False

            if "gamma" in capa:
                gamma = cc.get_gamma()
                gammadef = cc.getdef_gamma()
                if gammadef == gamma:
                    gammadefX = True
                else:
                    gammadefX = False

            aea,aex,aga,agm = get_gem(cc, capa)
            if aex!=None: ex,exd,mine,maxe,ex10 = aex
            if agm!=None: gm,gmd,minm,maxm,gm10 = agm
            if aga!=None: ga,gad,ming,maxg,ga10 = aga

            # very stupid camera    ZC0303 Webcam
            if "exposure" in capa:
                exposure = cc.get_exposure()
                exposuredef = cc.getdef_exposure()
                #?????
                #auto_exposuredef = cc.getdef_exposure()
                print(f"i... EXPOAUTO (top) == {exposure} vs def={exposuredef}; ")




            nfrm = 0
            if config.CONFIG["product"]:
                wname = "none "
            else:
                wname = config.CONFIG["product"]
        # ___ exposure and gain stuff here... done _____



        # *********************** INFINITE UNCONDITIONAL LOOP  ****
        #  - there is a problem that he searches/restarts the camera all time
        #     and jpg image is not compatible with that
        frame_prev = None
        while True:

            timeoutok = False
            ret = False
            frame = None

            # can change cap to a new one
            ccoi1, frame, cap = camera.camera_or_image(cap, vidnum)
            #print( frame.shape )
            #print( ccoi1 * 30 )
            ret = True # for the next
            if ccoi1 == "camera" and frame is None:
                ret = False
            elif ccoi1 == "image_forced":
                cap, vidnum, s9009 = camera.init_cam()

                # *********  video works,  get capacities and go with EXPO GAIN
                if not( (vidnum is None) or (vidnum == -1) ):
                    cc = v4lc.V4L2_CTL("/dev/video"+str(vidnum))
                    capa = cc.get_capbilities()

                    exposuredef = True
                    gammadefX = True
                    gaindefX = True

            #print("D... ret==", ret)
            if ret: #********************************************************* operations

                # FIXED IMAGE NOT ALLOWED DURING NORMAL CAMERA MODE - ONLY
                # FIXED IMAGE NOT ALLOWED DURING NORMAL CAMERA MODE - ONLY  from 202304027
                # FIXED IMAGE NOT ALLOWED DURING NORMAL CAMERA MODE - ONLY
                #
                # if fixed_image is not None:
                #     fullpath_fixed_image = "~/.config/flashcam/"+fixed_image
                #     fullpath_fixed_image = os.path.expanduser( fullpath_fixed_image )
                #     if os.path.exists(fullpath_fixed_image):
                #         frame = cv2.imread( fullpath_fixed_image)

                frame_prev = frame



                #print(f" (1){fg.cyan}{frame.shape}{fg.default} ", end = "" )
                if senh.add_frame(frame):  # it is a proper image....

                    #=========== BEFORE OTHER === Create final image ====
                    #=========== like ZOOM
                    #=========== THEN CALCULATE HISTO =====
                    #=========== THEN do other stuff


                    # 1. rotate (+translate of the center)
                    # 2. zoom (+translate the center)
                    # 3. histogram !!!here
                    # 4. speed
                    #  others

                    # senh has a frame now
                    if rotate180!=0:   # rotate earlier than zoom
                        senh.rotate180( rotate180 ) #arbitrary int angle

                    if zoom!=1:
                        try:
                            crocfg = os.path.expanduser("~/.config/flashcam/cross.txt")
                            cross_dx, cross_dy  = None, None
                            if os.path.exists(crocfg):
                                with open(crocfg) as f:
                                    cross_dx, cross_dy  = [int(x) for x in next(f).split()]
                                    #senh.zoom( zoom ,0,0 )
                                    senh.zoom( zoom ,cross_dx, cross_dy )
                        except Exception as e:
                            print("!... Problem ar cross.txt file:",e)

                    # ----------  I need to calculate histogram before labels...
                    if histogram: # just calculate a number on plain frame
                        #hmean = senh.histo_mean( ) # hmean STRING NOW
                        hmean = senh.histo_medi( ) # hmean STRING NOW
                        # notwrk #self.histomean = hmean # when called from direct...
                        # print("i... histo value:", hmean)
                        ##tune_histo(cc, hmean )

                    # ---------- before anything - we decode the web command EXECUTE EXECUTION

                    # - compensate for speed of the sky
                    if ((speedx!=0) or (speedy!=0)) \
                    and ((abs(speedx)>1) or (abs(speedy)>1)):
                        senh.translate( speedx, speedy)

                    if restart_translate:
                        senh.reset_camera_start()
                        restart_translate = False


                    # ------------- commands comming from web.py----------------
                    #  expressions     external commands
                    # ------------- COMMANDS COMMING FROM WEB.PY----------------
                    #  expressions
                    # ------------- commands comming from web.py----------------
                    #           -------------- or from seread (fixed_image ...)
                    expression,value = mmread_n_clear( )

                    if expression[:5] != "xxxxx":
                        #print(f"i...  *  EXPR: {expression} == {value}")
                        print(f"i...  *  EXPR: {expression} == {value}")
                        print(f"i...  *  EXPR: {expression} == {value}")

                        # -------------------- conversions without eval inf float bool, string
                        if is_int(value):
                            print("i... ",value, 'can be safely converted to an integer.')
                            value = int(float(value)) # 1.0 => int crashes
                        elif is_float(value):
                            print("i... ",value, 'is a float with non-zero digit(s) in the fractional-part.')
                            value = float(value)
                        elif is_bool(value):
                            #print("i... ",value, 'is true or false.')
                            if value=="True":
                                value = True
                            else:
                                value = False
                        else:
                            print(f"i... /{value}/ is string. It remains a string, without quotes though.")
                            value = str(value) # i dont care anyway
                            value = value.strip('"').strip("'")

                        try:
                            # eval makes float float and int int
                            #print("o... evaluating")
                            globals()[expression] = value  #was  eval(value)
                            print("i...                                   expression evaluated")
                            #  the expression MUST BE decleared   in    globals
                        except:
                            print("X... globals expression FAIL",expression,value)

                        # I need a crosscheck here on terminal screen
                        if expression=="overtext":
                            overtextalpha = 0
                        if expression=="pausedMOTION":
                            if value is True:
                                print("===================== DM RUNNING ====================")
                            if value is False:
                                print("--------------------- DM on standby -----------------")

                        if expression=="telegram":
                            print("i... telegram test******************************* value=",value)
                            senh.telegram_send_image(blocking= False) # it has an internal block (300sec)


                    if save_image_png:  # camera_screenshot PNG Full quality
                        print("D... HERE I SAVE  image camera_screenshot_PNG Full Quality")
                        if config.CONFIG['datapath'][-1] == "/":
                            pngname = dt.datetime.now().strftime("%Y%m%d_%H%M%S.%f")
                            pngname = pngname[:-5].replace(".","_")
                            cv2.imwrite( config.CONFIG['datapath']+f"camera_screenshot_{pngname}.png" , frame ) # nicely saved
                        else:
                            print("X... You need to specify datapath ending with '/' . No screenshot saved")
                        save_image_png = False

                    if save_background:
                        print("D... HERE I SAVE save_background of mask")
                        print("D... HERE I SAVE save_background of mask")
                        print("D... HERE I SAVE save_background of mask")
                        senh.save_background()
                        save_background = False  # ONE SHOT

                    if substract_background:
                        # print("D... HERE I MUST DO subtraction of mask")
                        # print("D... HERE I MUST DO subtraction of mask")
                        # print("D... HERE I MUST DO subtraction of mask",speedx, speedy)
                        senh.subtract()


                    if save_foreground:
                        print("D... HERE I SAVE save_foreground ")
                        print("D... HERE I SAVE save_foreground ")
                        print("D... HERE I SAVE save_foreground ")
                        senh.save_foreground()
                        save_foreground = False  # ONE SHOT


                    if mix_foreground:
                        # print("D... HERE I mix the foreground")
                        senh.mix()


                    # - compensate for speed of the sky
                    if ((speedx!=0) or (speedy!=0)) and ((abs(speedx)<1) and (abs(speedy)<1)):
                        print(f"speed translate {speedx} {speedy}")
                        senh.translate( speedx, speedy)

                    if restart_translate:
                        senh.reset_camera_start()
                        restart_translate = False

                    # average  THIS IS HERE to be changed TOO (ACCUM)
                    # print("i.... average", average)

                    # timelaps  THIS IS HERE to be changed TOO
                    # print("i.... timelaps", timelaps)

                    #print("i... GAMMAS ", gamma, gammadef )

                    if ccoi1 == "camera":
                        if gamma_divide and "gamma" in capa:
                            gamma_divide = False
                            gammadefX = False
                            gamma = cc.gamma_get("gamma")
                            gamma-=0.1
                            cc.gamma(gamma  )
                            gamma = cc.gamma_get("gamma")
                            v4lc.mk_table(cc)

                        if gamma_multiply and "gamma" in capa:
                            gamma_multiply = False
                            gammadefX = False
                            #if "gamma" in capa:
                            gamma = cc.gamma_get("gamma")
                            gamma+=0.1
                            cc.gamma( gamma )
                            gamma = cc.gamma_get("gamma")
                            v4lc.mk_table(cc)
                            # if gamma!=0:
                            #     newgamma =  int(gamma*2)
                            # else:
                            #     newgamma =  int(1)
                            # cc.set_gamma( newgamma )
                            # gamma = newgamma
                        if gamma_setdef and "gamma" in capa:
                            gamma_setdef = False
                            gammadefX = True
                            gamma = gammadef
                            #if "gamma" in capa:
                            cc.setdef_gamma( )
                            #    gamma = gammadef


                        if gain_divide and "gain" in capa:
                            gain_divide = False
                            gaindefX = False
                            gain = cc.gain_get("gain")
                            gain-=0.1
                            cc.gain(gain)
                            gain = cc.gain_get("gain")
                            v4lc.mk_table(cc)


                        if gain_multiply and "gain" in capa:
                            gain_multiply = False
                            gaindefX = False
                            gain = cc.gain_get("gain")
                            gain+=0.1
                            cc.gain(gain)
                            gain = cc.gain_get("gain")
                            v4lc.mk_table(cc)

                        if gain_setdef and "gain" in capa:
                            gain_setdef = False
                            gaindefX = True
                            gain = gaindef
                            print(f"========={bg.orange}{fg.black} GAIN SETDEF {gain} {fg.default}{bg.default} =","="*40)
                            # if "gain" in capa:
                            cc.setdef_gain( )
                            #   gain = gaindef

                        if "exposure_time_absolute" in capa or "exposure_absolute" in capa:
                            if histogram:
                                if hmean<5:
                                    #print(f"i... BOOSTING EXPOSURE TO 100%")
                                    cc.autoexpo_off( "autoexpo")
                                    cc.expo( 1 ,'expo')     # 0-1 log
                                    print("****** -H param => autoex  ************************ OFF")

                                if hmean>240:
                                    #print(f"i... KILLING MAN EXPOSURE ** TO AUTO,  gain too to avoid problem")
                                    cc.autoexpo_on( "autoexpo")
                                    if "gain" in capa:
                                        cc.setdef_gain()
                                    #exposure = -0.1 + exposure
                                    print("****** -H param => autoex  ********************** ON") # e-a-priority problem

                            if expo_divide:
                                expo_divide = False
                                v4lc.mk_table(cc)
                                exposuredef = False

                                cc.autoexpo_off( "autoexpo")

                                exposure = cc.expo_get("expo_get")
                                #print(f"i ... exposure- = {exposure} ")
                                exposure = -0.1 + exposure
                                cc.expo( exposure ,'expo')     # 0-1 log
                                v4lc.mk_table(cc)

                            if expo_multiply:
                                expo_multiply = False
                                v4lc.mk_table(cc)

                                exposuredef = False

                                # ra = random.uniform(0,1)
                                # print("\n\n", round(ra,3) )
                                cc.autoexpo_off( "autoexpo")
                                exposure = cc.expo_get( 'expo_get')     # 0-1 log
                                #print(" I found exposure === ", exposure)
                                cc.expo( exposure + 0.1 ,'expo')     # 0-1 log
                                v4lc.mk_table(cc)

                            if expo_setdef:
                                expo_setdef = False
                                exposuredef = True
                                v4lc.mk_table(cc)
                                exposure = cc.expo_get("expo_get")
                                print(f"i ... AUTO  was;   exposure = {exposure} ")
                                cc.autoexpo_on()
                                exposure = cc.expo_get("expo_get")
                                print(f"i ... AUTO   is;   exposure = {exposure} ")
                                exposure = 0
                                #senh.setbox(f"expo {exposure:.4f}",  senh.expo)
                                v4lc.mk_table(cc)




                            if not exposuredef: senh.setbox(f"exp {exposure:.3f}",  senh.expo)
                            if not gaindefX: senh.setbox(f"gai {gain:.3f}",  senh.gain)
                            if not gammadefX: senh.setbox(f"gam {gamma:.3f}",  senh.gamma)
                            #if  'exposure' in locals() and exposure != exposuredef:
                            #senh.setbox(f"expo {exposure:.4f}",  senh.expo)
                        #-----------exposure in capa
                    # ______________________ section with capa for camera _____________________


                    #--------------- now apply labels ------i cannot get rid in DETM---
                    #--------- all this will be on all rames histo,detect,direct,delta
                    senh.setbox(" ", senh.TIME, kompr=config.CONFIG['kompress'])
                    #senh.setbox(" ", senh.TIME, kompr= frame.shape[1])

                    if framekind in ["detect","delta","histo"]:
                        senh.setbox(f"DISP {framekind}",senh.DISP)
                    if average>0:
                        senh.setbox(f"a {average}",  senh.avg)
                    if blur>0:
                        senh.setbox(f"b  {blur}",  senh.blr)
                    if threshold>0:
                        senh.setbox(f"t  {threshold}",  senh.trh)
                    if timelaps>0:
                        mycodec=config.CONFIG['FOURCC']
                        if mycodec == "DIVX":  #
                            senh.setbox(f"ld {timelaps}",  senh.lap)
                        elif mycodec == "XDIV":  # not  mkv
                            senh.setbox(f"lx {timelaps}",  senh.lap)
                        elif mycodec == "IYUV":
                            senh.setbox(f"lY {timelaps}",  senh.lap)
                        else:
                            senh.setbox(f"l  {timelaps} {mycodec}",  senh.lap)
                    if histogram:
                        senh.setbox(f"h {hmean}",  senh.hist)
                    if speedx!=0:
                        #print(speedx)
                        senh.setbox(f"x {speedx:.3f}",  senh.speedx)
                    if speedy!=0:
                        senh.setbox(f"y {speedy:.3f}",  senh.speedy)
                    if zoom!=1:
                        senh.setbox(f"z {zoom:1d}x", senh.scale)

                    if substract_background and not mix_foreground:
                        senh.setbox("-BCKG",  senh.SUBBG )
                    if not substract_background and mix_foreground:
                        senh.setbox("*MIXFG",  senh.SUBBG )
                    if substract_background and mix_foreground:
                        senh.setbox("-BG*FG",  senh.SUBBG )

                    if rotate180!=0:
                        senh.setbox("ROT",  senh.rot )



                    # # ----------------expo gain gamma
                    # # very stupid camera    ZC0303 Webcam
                    # # print(capa, exposure,exposuredef) # crashes
                    # if "exposure" in capa:
                    #     if exposure!=exposuredef: # manual
                    #         senh.setbox(f"expo {exposure}",  senh.expo)

                    # if "auto_exposure" in capa:
                    #     if expo_auto!=expo_autodef: # manual
                    #         senh.setbox(f"expo {exposure_time_absolute}",  senh.expo)

                    # if ("gain" in capa) and (gain!=gaindef): # gain is not frequently tunable
                    #     senh.setbox(f"g {gain}",  senh.gain)

                    # if ("gamma" in capa):
                    #     if (gamma!=gammadef): # manual
                    #         senh.setbox(f"m {gamma}",  senh.gamma)



                    # delayed telegram - preset in DM ========================

                    if not(type(senh.telegramtrigger))==bool:
                        if dt.datetime.now()>senh.telegramtrigger:
                            print("i... telegram time tripped the  2s wire:", senh.telegramtrigger.strftime("%H:%M:%S"), "NOW=",dt.datetime.now().strftime("%H:%M:%S") )
                            senh.telegramtrigger = False
                            senh.telegram_send_image() # it has an internal block (300sec)


                    # ----  for DetMo ---- work with detect motion----------------
                    #   telegram and imagezmq are active only here
                    if (threshold>0) :
                        # here there was MODE DM.
                        # but with imageZMQ and Telegram ALERT....
                        #
                        if not senh.zmqtarget is None:
                            MODE_DM=MODE_DMbase+"z"
                            if senh.jtelegram:
                                MODE_DM=MODE_DM+"T"
                        elif (senh.jtelegram):
                            MODE_DM=MODE_DMbase+"T"


                        senh.setbox(MODE_DM, senh.MODE, grayed = pausedMOTION) #---push UP to avoid DetMot
                        #print("D... detecting motion")
                        senh.detmo( average, blur)
                        senh.chk_threshold( threshold )
                        #
                        # I need a way to block DETMO ....
                        # ??? BLUETOOTH ------- see later
                        #
                        if senh.motion_detected: # saving avi on mation detect
                            # print("D... sav mot", senh.motion_detected)
                            if not pausedMOTION:
                                senh.save_avi( seconds = -1, name = "dm" )

                    else:
                        senh.setaccum( average  )
                        senh.setblur( blur )
                        #senh.setbox("MODE  ", senh.MODE)

                    # ---draw histogram
                    #print("                               --- ",framekind)
                    if framekind == "histo":
                        senh.histo( )

                    if timelaps>0:
                        mycodec=config.CONFIG['FOURCC']
                        senh.save_avi( seconds = timelaps,
                                       basecamera_string=f"{BaseCamera.nframes:07d} / {BaseCamera.capture_time}",
                                       mycodec = mycodec, frnum= BaseCamera.nframes)

                    if timelaps<0: # NEW...Save Every frame .. timelaps value is different from seconds value
                        mycodec=config.CONFIG['FOURCC']
                        senh.save_avi( seconds = 0.001,
                                       basecamera_string=f"{BaseCamera.nframes:07d} / {BaseCamera.capture_time}",
                                       mycodec = mycodec, frnum= BaseCamera.nframes)



                    #------------yield the resulting frame-----------------------------
                    if framekind in ["detect","delta","histo"]:
                        frame = senh.get_frame(  typ = framekind)
                    else:
                        frame = senh.get_frame(  )

                    # debug info on final resolution
                    #print(f"  FIN{fg.yellow}{frame.shape}{fg.default} ", end = "" )

                    # --- here I can touch frame:
                    if overtext is not None:
                        posx = int(640/2 - len( str(overtext) )*32/2)
                        if posx<0: posx=10
                        position = ( posx ,400)
                        fontpath = os.path.expanduser("~/.config/flashcam/digital-7.mono.ttf")
                        font = ImageFont.truetype(fontpath, 2*32)

                        img_pil = Image.fromarray(frame).convert("RGBA")  # base img
                        txt_img = Image.new("RGBA", img_pil.size, (255,255,255,0))

                        #draw = ImageDraw.Draw(img_pil)
                        draw = ImageDraw.Draw(txt_img)
                        drtext =  f"{overtext}"# {overtextalpha}" # to be sure
                        b,g,r,a = 0,255, 0, 255-int(overtextalpha)
                        draw.text( position,  drtext, font = font, fill = (b, g, r, a))

                        composite = Image.alpha_composite(img_pil, txt_img)
                        #composite.save(output_path)


                        #frame = np.array(img_pil)
                        frame = np.array(composite)
                        if overtextalpha<255:
                            overtextalpha+=0.2
                        else:
                            overtext = None



                    if save_image_decor:  # camera_screenshot with all decor
                        print("D... HERE I SAVE  image camera_screenshot_decor")
                        if config.CONFIG['datapath'][-1] == "/":
                            cv2.imwrite( config.CONFIG['datapath']+"camera_screenshot.jpg" , frame ) # nicely saved
                        else:
                            print("X... You need to specify datapath ending with '/' . No screenshot saved")
                        save_image_decor = False  # ONE SHOT


            yield frame



    # @staticmethod
    # def set_video_source(source):
    #     """
    #     never user whatsoever !
    #     """
    #     print("D... set_video_source: source=", source)
    #     camera = cv2.VideoCapture( source,  cv2.CAP_V4L2)
    #     print("D... ",camera)
    #     print("D... setting MJPG writer....FMP4 works too")
    #     # camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    #     camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('F','M','P','4'))
    #     print("D... first camera read ....")
    #     ok = False
    #     try:
    #         _, img = camera.read()
    #         print(img.size) # this can fail and reset to DEV 0
    #         ok = True
    #     except Exception as ex:
    #         print("X... CAMERA read ... FAILED",ex)

    #     if ok:
    #         return camera
    #     return None
