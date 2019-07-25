# Dance and Plant controlled smarthome

My smarthome controlled via sweet dance moves and plants

Runs on the NVIDIA Jetson Nano and a Z-Wave USB stick.

Uses [tf-pose-estimation](https://github.com/ildoonet/tf-pose-estimation) for better performance and easier configuration on the Jetson Nano.


Specifically, to get ~5FPS on the Jetson Nano, I'm running:

```bash
$ python3 run_webcam_grab.py --model=mobilenet_v2_small --resize=368x368 --camera=0 --tensorrt=True
```

It takes _a while_ to spin up. (On the order of minutes.) I haven't yet found the bottleneck, and it's not too much of a worry just yet.

