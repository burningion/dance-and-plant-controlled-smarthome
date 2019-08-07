import argparse
import logging
import time

import cv2
import numpy as np

import tensorflow as tf

# make sure tensorflow doesn't take up all the gpu memory
conf = tf.ConfigProto()
conf.gpu_options.allow_growth=True
session = tf.Session(config=conf)

import keras

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

import openzwave
from openzwave.option import ZWaveOption
from openzwave.network import ZWaveNetwork

# make sure these commands get flushed by doing them first, then loading tensorflow...
# tensorflow should take enough time to start for these commands to flush
options = ZWaveOption('/dev/ttyACM0')
options.lock()

network = ZWaveNetwork(options)

logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

tposer = keras.models.load_model('COCO-dab-tpose-other.h5')

fps_time = 0

bounced = time.time()
debounce = 3 # wait 3 seconds before allowing another command
LIGHTS = 0

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--camera', type=int, default=0)

    parser.add_argument('--resize', type=str, default='0x0',
                        help='if provided, resize images before they are processed. default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
    parser.add_argument('--resize-out-ratio', type=float, default=4.0,
                        help='if provided, resize heatmaps before they are post-processed. default=1.0')

    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small')
    parser.add_argument('--show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')
    
    parser.add_argument('--tensorrt', type=str, default="False",
                        help='for tensorrt process.')
    args = parser.parse_args()

    logger.debug('initialization %s : %s' % (args.model, get_graph_path(args.model)))
    w, h = model_wh(args.resize)
    if w > 0 and h > 0:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h), trt_bool=str2bool(args.tensorrt))
    else:
        e = TfPoseEstimator(get_graph_path(args.model), target_size=(432, 368), trt_bool=str2bool(args.tensorrt))
    logger.debug('cam read+')
    cam = cv2.VideoCapture(args.camera)
    ret_val, image = cam.read()
    logger.info('cam image=%dx%d' % (image.shape[1], image.shape[0]))

    while True:
        ret_val, image = cam.read()

        #logger.debug('image process+')
        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=args.resize_out_ratio)
        
        infer = []
        for human in humans:
            hummie = []
            for i in range(18): 
                if i in human.body_parts.keys(): 
                    hummie.append(np.array([human.body_parts[i].x, human.body_parts[i].y], dtype=np.float32)) 
                else: 
                    hummie.append(np.array([0.0, 0.0], dtype=np.float32))
            infer.append(hummie)
        
        if len(infer) > 0:
            #logger.debug("infer greater than zero")
            num = len(infer)
            infer = np.array(infer, dtype=np.float32)
            infer = infer.reshape(num, 36)
            #logger.debug(infer)
            output = tposer.predict_classes(np.array(infer, dtype=np.float32))
            for j in output:
                if j == 1:
                    print("dab detected")
                    if LIGHTS == 0 or (time.time() - bounced) < debounce:
                        continue
                    for node in network.nodes:
                        for val in network.nodes[node].get_switches():
                            network.nodes[node].set_switch(val, False)
                    LIGHTS = 0
                    bounced = time.time()
                elif j == 2:
                    print("tpose detected")
                    if LIGHTS == 1 or (time.time() - bounced) < debounce:
                        continue
                    for node in network.nodes:
                        for val in network.nodes[node].get_switches():
                            network.nodes[node].set_switch(val, True)
                    LIGHTS = 1
                    bounced = time.time()                    
        
        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

        #logger.debug('show+')
        cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.imshow('tf-pose-estimation result', image)
        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
        #logger.debug('finished+')

    cv2.destroyAllWindows()
