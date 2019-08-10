# Dance and Plant controlled smarthome

My smarthome controlled via sweet dance moves and plants

![Supplies needed for project](https://github.com/burningion/dance-and-plant-controlled-smarthome/raw/master/images/supplies.jpg)

Runs on a [Logitech C920](https://amzn.to/2GLdbB6) webcam, along with a [Z-Wave Z-Stick](https://amzn.to/2GJbVyv) in order to control a [Z-Wave switch](https://amzn.to/2yHItnY).

It uses [tf-pose-estimation](https://github.com/ildoonet/tf-pose-estimation) for better performance and easier configuration on the Jetson Nano.

Specifically, to get ~4.5FPS on the Jetson Nano, I'm running:

```bash
$ sudo nvpmodel -m 0
$ python3 run_dab_tpose.py --model=mobilenet_thin --resize=368x368 --camera=0
```

The `nvpmodel -m 0` sets the Jetson Nano into it's highest performance, most power drawing mode. I recommend having a 5v power supply to run this, along with a jumper to short the part on the Nano to switch from taking in power from USB.

## Architecture

![Architecture](https://github.com/burningion/dance-and-plant-controlled-smarthome/raw/master/images/dab-tpose-nano.png)

The main benefit of using Z-Wave is that it's completely separate from your home WiFi system. I didn't want to add devices to my home's WiFi, and still wanted to be able to control my lights from anywhere in my house. 

Using Z-Wave also means my Jetson Nano doesn't need to be connected to WiFi to work at all. I can plug it in anywhere, and it just works. 

No connecting to the cloud required!
