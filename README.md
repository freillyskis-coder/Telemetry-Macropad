# Telemetry-Macropad
This is a place where I store all of my files for my macropad that has an accelerometer, display, and lights that will show telemetry information for racing.

### What It Does
This macropad has a computer, display, accelerometer, a few lights, and 3 keys. The accelerometer is used to measure acceleration in different directions (duh). That information gets used to display which direction it is accelerating in a traction-circle style display, or in plain number format, on the screen. The lights also indicate what direction the board is accelerating, with one pointing in each cardinal direction for the device. The lights each have two functions, requiring a long or short press. They go like this:
- Switch modes on the display (trac circle, current acceleration numbers, etc) (Short) / Set brightness (Long)
- Recalibration (Short) / Switch Units (g’s vs m/s) (Long)
- Freezes max acceleration (Short) / Reset acceleration (size of the traction circle) (Long)
  
### Why I Built This
I have seen traction circles be used in racing simulators to assist the driver. However, I had never seen one in a real car. I thought it would be really cool to try my hand at designing a device that could display information relevant to racing. In the future, I may add new features such as data collection, slip warnings, etc. 

### Challenges
I haven't done that much design work myself, so this was full of new experiences for me. I have used onshape for 3d cad work before, so it was fun learning how to use fusion (they were pretty similar, at least for what I was doing). 
I also enjoyed learning how to use the KiCAD software. I've used Rapidharness before for electrical work, but it was so cool and different designing a PCB. One of the biggest challenges was the coding, as I've only used Java for my compsci class, and figuring out how to use Github (it required a lot of youtube tutorials and headscratching). Overall, I persisted through and I gained a lot of valuable skills and had a good time!

### Designs
Schematic            |  PCB         |   Case    |   
:-------------------------:|:-------------------------:|:-------------------------:|
<img src="Telemetry%20Hackpad/Images/Current%20Designs/KiCAD%20Schematic%20V3.png" width="400">  | <img src="Telemetry%20Hackpad/Images/Current%20Designs/KiCAD%20PCB%20Design%20V4.png" width="400">   | <img src="Telemetry%20Hackpad/Images/Current%20Designs/Case%20Top%20View%204.png" width="400">  

# Overall Hackpad:

<img src="Telemetry%20Hackpad/Images/Current%20Designs/Assembly%20Side%20View%204.png" width="400"> 

### Bill Of Materials
- [1 x SSD1306 OLED](https://www.alibaba.com/product-detail/0-96-128x64-I2C-IIC-Serial_1601221974195.html?spm=a2700.prosearch.normal_offer.d_title.713e67af2h8ats&selectedCarrierCode=SEMI_MANAGED_STANDARD%40%40STANDARD&priceId=9263331f4c5146ce9335b75a9e5a434e) - display, $2.50
- [4 x SK6812MINI-E](https://www.digikey.com/en/products/detail/adafruit-industries-llc/4960/14302512?gclsrc=aw.ds&gad_source=1&gad_campaignid=20228387720&gbraid=0AAAAADrbLlgqid9MNTrAWhJKMXZF-C39b&gclid=CjwKCAiAzZ_NBhAEEiwAMtqKyy2T8yJqQVE5hG_iRolQtgHnV_oXdoksU0azACau9GJ1NhhwS3yk6hoCPRcQAvD_BwE) - lights, $2.95
- [1 x XIAO RP2040 DIP](https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html) - computer, $3.99
- [3 x Cherry MX Switches](https://mechanicalkeyboards.com/products/cherry-mx2a-silent-red-45g-linear?variant=48014625177900) - switches $0.40
- [3 x DSA Black Keycaps](https://thepihut.com/products/black-dsa-keycaps-for-mx-compatible-switches-10-pack) - keycaps (10 pack) $5.80
- [4 x M3x3mm heatset inserts](https://www.adafruit.com/product/4256) - inserts, $5.95 
- [4 x M3x10mm screws](https://www.amazon.com/Screws-Assortment-Machine-Washers-Phillips/dp/B0G9HDWD3K/ref=sr_1_12?crid=15VO2HWVHE0U2&dib=eyJ2IjoiMSJ9.WV9vbUoR7v5KPi58AH83sZsSA7HvHG40hEXMA8HbueS60EWGKL47-TZYQY3TXXlaLUiDxuMThePG_C0DW73KA63eM30HCJDZl3elUEXfaLVWdxwIaKEVdZeLDRrm8IMZwNt0g-c5EK8s48QIQ1roqfLd_2wHsQgpIbIy9LAY3n9HKYXzYhvnC8PRo9urp8rpHIZFLXKtcY7svDHuq47DynBfwkhPvRxjzr1DQoavsg9FY-STt1nrAQnZTKOSEv1by2L08LQVAFx4QCqLNYtsLBaGEWl_z5qazF4EEkFyGn0.bwl7yN3XZuO-iIm4WUgd6dJ_ZpySQU-Q4Z4oi7Gi01I&dib_tag=se&keywords=M3%2Bscrews&qid=1774370715&s=industrial&sprefix=m3%2Bscrew%2Cindustrial%2C140&sr=1-12&th=1)   - screws, $3.99
- My PCB, printed
- My 3D printed case

I have an accelerometer in my designs, but I am not requesting it as I know it is not a part of the kit. I will pay for this myself.
- - [1 x MPU 6050](https://www.alibaba.com/product-detail/TZT-1Set-IIC-I2C-GY-521_1600855862949.html?spm=a2700.prosearch.normal_offer.d_title.444e67afTjlFTW&priceId=fc64e04c517543e99b5e70350475b235) - accelerometer, $1.45

