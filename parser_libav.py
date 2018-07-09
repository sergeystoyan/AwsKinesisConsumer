#by Sergey Stoyan: sergey.stoyan@gmail.com
from logger import LOG
import settings
import os
import sys
#import imp
import boto3
#import json
#from datetime import datetime
import time
import cv2#, platform
import io
import numpy as np
#import Image
import subprocess as sp
import signal
import threading
from ebml import EbmlReader
import ebml
import copy


cimport cython
import numpy as np
cimport numpy as np

DTYPE = np.float
ctypedef np.float_t DTYPE_t

# This file shows 4 examples:
#   - Wrapping an external c function into python, "c_hello"
#   - Making a wrapped c function on python types w/ cython syntax, "factorial"
#   - A c function that takes an ndarray array and returns a scalar, "array_sum"
#   - A c function that takes an ndarray and returns an ndarray "tesselation"

cdef extern from "lib/cfunc.h":
    # Imports definitions from a c header file
    # Corresponding source file (cfunc.c) must be added to
    # the extension definition in setup.py for proper compiling & linking

    void hello()


def c_hello():
    # Exposes a c function to python

    hello()







class Parser:
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.dispose()

    def __del__(self):
        self.dispose()

    def dispose(self):
        if self.disposed:
            return
        with self.lock:
            self.disposed = True
            LOG.info('Shutting down Parser...')        
            self.run_kinesis_stream_reader = False
        
    def __init__(self,
        stream_name,
        time_span_between_frames_in_secs = -1,
        frame_queue_max_length = 10,
        save_frames2disk = True,
        catch_frames = True,
        ):
        self.lock = threading.Lock()
        self.disposed = False
        self.FrameQueueMaxLength = 10
        self.TimeSpanBetweenFramesInSecs = -1
        self.SaveFrames2Disk = True
        self.run_kinesis_stream_reader = True
        self.ffmpeg_process = None
        self.run_frame_parser = True
        self.Frames = []
        self.catch_frames = catch_frames
        
        try:
            LOG.info('STARTED')
            LOG.info('stream_name: ' + stream_name)

            self.FrameQueueMaxLength = frame_queue_max_length
            self.TimeSpanBetweenFramesInSecs = time_span_between_frames_in_secs
            self.SaveFrames2Disk = save_frames2disk
        
        # client = boto3.client(
               # service_name = 'kinesisvideo',
               # region_name = settings.REGION_NAME
        # )
        # LOG.info(
               # client.list_streams(
               # )
        # )

            LOG.info('requesting kinesis get_data_endpoint')
            client = boto3.client(
                service_name = 'kinesisvideo',
                region_name = settings.REGION_NAME
            )
            response = client.get_data_endpoint(
                StreamName = stream_name,
                APIName = 'GET_MEDIA'
            )
            LOG.info('response: ' + format(response))
            endpoint_url = response['DataEndpoint']
        
            LOG.info('requesting kinesis get_media')
            client = boto3.client(
                service_name = 'kinesis-video-media',
                endpoint_url = endpoint_url,
                region_name = settings.REGION_NAME,
            )
            response = client.get_media(
                StreamName = stream_name,
                StartSelector = {
                    'StartSelectorType': 'NOW',
                }
            )
            LOG.info('response: ' + format(response))
            kinesis_stream = response['Payload']
            
            frame_dir = '_frames'
            if os.path.exists(frame_dir):
                import shutil
                shutil.rmtree(frame_dir)
                os.makedirs(frame_dir)
             















            exit()




            self.pipe = r'/tmp/testFifo'
            try:                                
                os.remove(self.pipe)
            except:
                pass
            os.mkfifo(self.pipe)
            
                
            print('@@@@')
            #pipeW = open(self.pipe, 'w')
            fd = os.open(self.pipe, os.O_RDWR) #non-blocking
            pipeW = os.fdopen(fd, 'w') #also non-blocking
            print('+++')
                        
            READ_BUFFER_SIZE = 1000000
            total_bytes = 0
            while True:
                #data = kinesis_stream.read(amt=READ_BUFFER_SIZE)
                f = open('test.mkv', 'rb')
                data = f.read()
                if not data:
                    print('^^^^^^')
                    break
                total_bytes += len(data)
                print('Kinesis: ' + format(total_bytes))
                pipeW.write(data)
                pipeW.flush()

                
                import av
                #video = open(kinesis_stream)
                video = av.open(self.pipe)
                print('====')

                print('container:', video)
                print('\tformat:', video.format)
                print('\tduration:', float(video.duration) / time_base)
                print('\tmetadata:')
                for k, v in sorted(video.metadata.iteritems()):
                    print('\t\t%s: %r' % (k, v))
                print()
  

                stream = next(s for s in video.streams if s.type == 'video')
                i = 0
                for packet in video.demux(stream):
                    print('$$$$$$$$$')
                    for frame in packet.decode():
                        print('&&&&&&&&&&&')
                    # some other formats gray16be, bgr24, rgb24
                        img = frame.to_nd_array(format='bgr24')
                        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        i += 1
                        if i > 10:
                            exit()

                #time.sleep(5)

                                    
            exit()





            LOG.info('starting kinesis_stream_reader')
            from threading import Thread
            kinesis_stream_reader_thread = Thread(target = self.kinesis_stream_reader, args = (kinesis_stream, ))

            self.run_kinesis_stream_reader = True
            kinesis_stream_reader_thread.start()  

            
            print('#####')
            import av
            #video = open(kinesis_stream)
            video = open(self.pipe)
            print('====')
            

            stream = next(s for s in video.streams if s.type == 'video')
            i = 0
            for packet in video.demux(stream):
                for frame in packet.decode():
                # some other formats gray16be, bgr24, rgb24
                    img = frame.to_nd_array(format='bgr24')
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    i += 1
                    if i > 10:
                        exit()

        except:
            LOG.exception(sys.exc_info()[0])
        finally:
            pass
            
    
    def kinesis_stream_reader(self,
        kinesis_stream
    ):
        try:  
            
            print('@@@@')
            #pipeW = open(self.pipe, 'w')
            fd = os.open(self.pipe, os.O_RDWR) #non-blocking
            pipeW = open(fd, 'w')
            print('+++')
                        
            READ_BUFFER_SIZE = 1000000
            total_bytes = 0
            while self.run_kinesis_stream_reader:
                data = kinesis_stream.read(amt=READ_BUFFER_SIZE)
                if not data:
                    break
                total_bytes += len(data)
                print('Kinesis: ' + format(total_bytes))
                pipeW.write(data)
                pipeW.flush()

                
                import av
                #video = open(kinesis_stream)
                video = open(self.pipe)
                print('====')
            

                stream = next(s for s in video.streams if s.type == 'video')
                i = 0
                for packet in video.demux(stream):
                    for frame in packet.decode():
                    # some other formats gray16be, bgr24, rgb24
                        img = frame.to_nd_array(format='bgr24')
                        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        i += 1
                        if i > 10:
                            exit()

                #time.sleep(5)

                                    
            exit()

        except:
            LOG.exception(sys.exc_info()[0])
        finally:
            LOG.info('exiting kinesis_stream_reader')
            self.dispose()




    def print_ebml_element_head(self, ebmlParser, size,  id, name, type_):
        LOG.info('position: %d, size:%d, id:%s, name:%s, type_:%s' % (ebmlParser.position, size, hex(id), name, type_))
            
    def print_ebml_element(self, size, id, name, type_, value):
        #if type_ != ebml.BINARY:
        #    LOG.info('value: %s' % (value))
        #else:
        #    LOG.info('value: %s' % ('<BINARY>')) 
        if type_ != ebml.BINARY:
            LOG.info('name:%s, size:%d, id:%s, type_:%s, value: %s' % (name, size, hex(id), type_, value))
        else:
            LOG.info('name:%s, size:%d, id:%s, type_:%s, value: %s' % (name, size, hex(id), type_, '<BINARY>'))             

    def catch_frame(self,
        tags,
        frame,
    ):
        try:         
            self.frame_count += 1
            
            if self.TimeSpanBetweenFramesInSecs <= 0 or self.next_frame_time <= time.time():
                next_frame_time = time.time() + self.TimeSpanBetweenFramesInSecs

            if self.SaveFrames2Disk:
                frame_file = frame_dir + "/frame%d.png" % frame_count
                LOG.info('frame ' + str(frame_count) + ': ' + frame_file)
            else:
                LOG.info('frame ' + str(frame_count))

            image = np.fromstring(frame, np.uint8)
            image = image.reshape((1080,1920,3))
            #image2 = cv2.imdecode(image, cv2.CV_LOAD_IMAGE_COLOR)                                

            with self.lock:
                self.Frames.append({'image':image, 'time':time.time(), 'tags':tags, 'file':frame_file})

                if len(self.Frames) > self.FrameQueueMaxLength:
                    i = self.Frames[0]
                    try:# file can be in use or deleted
                        os.remove(i['file'])
                    except:
                        pass
                    del self.Frames[0]

                if self.SaveFrames2Disk:
                    cv2.imwrite(frame_file, image)
                    #image.save("frame_%d.jpg" % frame_count, image)                                       
        except:
            LOG.exception(sys.exc_info()[0])
        finally:
            LOG.info('exiting frame_parser')
            self.dispose()

                            
    def GetFrame(self,
                 index = -1  #last one
                 ):
        with self.lock:
            try:
                l = len(self.Frames)
                if index >= l or l < 1:
                    return
                if index < 0:
                    index = l - 1
                    return self.Frames[index]
            except:
                LOG.exception(sys.exc_info()[0])


    def Suspend(self,
                ):
        self.catch_frames = False
               
    def Resume(self,
               ):
        self.catch_frames = True

    

if __name__ == '__main__':#not to run when this module is being imported
    import sys
    if len(sys.argv) > 1:
        stream_name = sys.argv[1]
    with Parser(
        stream_name = 'test8',
        time_span_between_frames_in_secs = 0.3,
        frame_queue_max_length = 20,
        save_frames2disk = True,
        catch_frames = True,
        ) as p:
                
        time.sleep(3)
        f = p.GetFrame(0)#thread safe method
        if f is not None:
            print("First frame: (%d), %s\r\n" % (f['time'], f['file']))

        time.sleep(3)
        f = p.GetFrame()#last frame
        if f is not None:
            print("Last frame: (%d), %s\r\n" % (f['time'], f['file']))

        p.Suspend()
        #p.Frames must be accessed only after Suspend() to avoid concurrency!!!
        for f in p.Frames:
            print("Frame: (%d), %s\r\n" % (f['time'], f['file']))                
            
        p.Resume()
        time.sleep(10)
        f = p.GetFrame()#last frame
        if f is not None:
            print("Last frame: (%d), %s\r\n" % (f['time'], f['file']))
    exit()
