# Dance and Plant controlled smarthome

My smarthome controlled via sweet dance moves and plants

![Supplies needed for project](https://github.com/burningion/dance-and-plant-controlled-smarthome/raw/master/images/supplies.jpg)

Runs on the NVIDIA Jetson Nano, a C920 webcam, and a Z-Wave USB stick.

It uses [tf-pose-estimation](https://github.com/ildoonet/tf-pose-estimation) for better performance and easier configuration on the Jetson Nano.


Specifically, to get ~4.5FPS on the Jetson Nano, I'm running:

```bash
$ sudo nvpmodel -m 0
$ python3 run_webcam_grab.py --model=mobilenet_thin --resize=368x368 --camera=0 --tensorrt=True
```

The `nvpmodel -m 0` sets the Jetson Nano into it's highest performance, most power drawing mode. I recommend having a 5v power supply to run this, along with a jumper to short the part on the Nano to switch from taking in power from USB.

The `run_webcam_grab.py` takes a while to spin up. Just be patient, and eventually, you'll see the webcam and be able to test it out!



