To operate the camera

adc calibration

1 - ensure the odin server is running on the FEM-II modle by logging into 192.168.0.123 and running the script sh /home/yyg19743/qem.sh
2 - run a web browser and browse to the page 192.168.0.123:8888
3 - ensure the clock is set at 10MHz
4 - reload the FPGA using the vivado tools (2015.2) on te7uganda (if this is where it is connected)
5 - use the firmware release_1 \\te9files\ProjectsMED\TEM-QEM\QEM Camera Hardware\Firmware\software\release_1\firmware
6 - load the camera with the loop file required using python load_loop.py <filename> use a file with _ADC_ in the filename
7 - display 10,000 frames using python display_images.py
8 - run the calibration python adc_calibrate.py <name> name = to identify the calibration run 
9 - the data will be stored in /scratch/qem/
10 - Make a folder in /techData/QEMdata/ to represent the run
11 - copy the file from the local disk to the network drive

image capture

