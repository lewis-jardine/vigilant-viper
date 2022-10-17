Raspberry Pi Camera Setup

Setup OS on the Pi.
Download the Raspberry Pi imager
Use the imager to load the OS onto the SD card.
Note: You have two options when using the imager. You can download the OS images onto your computer for keeping or download them through the imager when ready to load onto the Pi.

Power up the Pi and go through the installation.
Main Documentation: Raspberry Pi Documentation - Getting Started
Raspberry Pi Imager: Raspberry Pi OS – Raspberry Pi

Install the camera.
Power down the Pi.
Install the camera onto the Pi.
Power up the Pi.
The current Pi OS (Bullseye) automatically detects the camera so there is no longer a need to enable it manually in the Raspberry Pi Configuration.
Execute the command in the next step using the command line.
Test the camera: libcamera-hello
Note: It should show a window displaying the camera feed for five seconds.

Then need to install rtsp simple server
https://github.com/aler9/rtsp-simple-server/releases
check the version of Rpi with: uname-a and take note of the ‘arm’ version as to which bit to install and extract both files
then edit the .yml file to remove everything below paths:, make it 
paths:
    cam:
        source: publish

Now run the rtsp-simple-server file, **OPEN A NEW TERMINAL **and you’re ready to start streaming on rtsp from the camera


Stream from the Pi Camera on the Pi using cvlc.
Stream as RTSP: libcamera-vid -t 0 –-inline –o - | cvlc stream:///dev/stdin –-sout ‘#rtp{sdp=rtsp://:8080/}’ :demux=h264  
Note: This command does several things.
The t flag being set to 0 sets the camera to stream indefinitely. 
The inline flag forces stream header information to be included with every intra frame.
The o flag sets where to send the output.
In this case, the output is piped to cvlc which will send the camera output to an RTSP stream.
Raspberry Pi Documentation - Camera

Stream from the Pi Camera to an RTSP server using ffmpeg.
Stream to RTSP Server: libcamera-vid --width=1024 --height=768 --timeout 0 --vflip=1 --inline -o - | ffmpeg -i /dev/stdin -c copy -f rtsp rtsp://127.0.0.1:8554/cam
Note: Everything before the pipe (|) is configuring the feed from the Pi Camera. Everything after the pipe is ffmpeg.
ffmpeg is reading the video stream from standard input.
ffmpeg is copying the stream directly from input to output without encoding.
ffmpeg  is publishing the stream to the locally hosted RTSP server.
Note: See RTSP server section below for this step.
Annex
Determining the IP address of the Pi.
The command in the next step outputs the IP addresses of the network interfaces on the Pi. wlan0 shows the IP address of the wireless interface. eth0 shows the IP address of the ethernet connection. The IP address is the series of numbers after ‘inet’.
Show IP address: ifconfig
Streaming to multiple outputs with ffmpeg.
https://trac.ffmpeg.org/wiki/Creating%20multiple%20outputs
Setup an RTSP server
Download RTSP Simple server. (An appropriate processor architecture version for the Pi)
Extract it to a desired location.
Retrieve the config file from the Git repository.
Start the RTSP server.
Publish to the RTSP server. (See ffmpeg RTSP section above)

