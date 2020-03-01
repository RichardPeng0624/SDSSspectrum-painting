# SDSSspectrum-painting
Hello guys and 'hello world'!This is my first try on Github.<br>
The script below shows how to read FITS files and paints spectrum from SDSS(Sloan Digital Sky Survey).<br>
If you wanna paint the whole spectrum of a mutliple-obervation source(which means it may be observing several times during different projects) in one picture,you can use this py script.You are expected to prepare something before running it:<br>
1.You need prepare a csv catalog with some basic information of the whole fits files including PLATE,MJD,FiberID,GroupID,GroupSize,Z,specname at least.<br>
*To make this catalog,I recommand you to use `TOPCAT`,a very useful speardsheet software.You can match same sources with RA and DEC by using  'Internal match' in it,then you can get  a matched catalog with columns 'groupid' and 'groupsize' added .Other columns such as S/N,linearea_flux may also be needed.<br>*
2.Download all the needed FITS files at SDSS website.<br>
3.This script use `Astropy`,a python package to read fits file,so please make sure you know the data structure of FITS and some basic functions in astropy.<br>
4.In order to prevent too many files in an folder to open it,the script put 1000 pictures in one file,you can change the number.<br>
5.The disadvantage of this script is your computer must have ample memory if  you wanna process a large number of fits  files at once(more than a thousand).<br>
Another weakness is that if there are fewer fits  than the 'groupsize' shown in one group,some fits files in the next group will be drew in this one inveitably,please pay attention to it though it's a low probability event.<br>
6.Pay attention to the paths in codes and remember to change them.<br>
7.If you improved it, please let me know~<br>
