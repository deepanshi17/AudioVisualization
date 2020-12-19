import maya.cmds as cmd

file = open("/Users/deepanshisharma/UltralightBeam.txt", "r") # takes mono track input as txt file
samplerate=16000 # samplerate of the audio file in hz
framerate=24 # output framerate
objects=1000 # numbers of poligons or points per line
frames=500 # output frames
header=5 # header lines in the txt file
barwidth=0.1
barlength=10
amplitude=200
zoom=25
value=[0] * objects


 
for index in range(header): # get rid of the txt header
    file.next()
 
try:
    while 1:
        value.append(float(file.next()[0:7]))
except StopIteration: # when it reaches the end of the file this exception occurs
    pass

def line(samplerate, framerate, bars, frames, amplitude, zoom, value):
    pastframe=-1
    indexa=0
    cmd.curve(d=2, p=[(0, 0, 0)], name = "curve" )
    for index in range(bars):
        cmd.curve( "curve", a=True, p=[(index, 0, 0)] )
        cmd.setKeyframe ("curveShape1.cp[" + str(index+1) + "].yv")
    while pastframe<frames:
        indexa+=1
        if (indexa/zoom) != pastframe:
            cmd.currentTime (indexa/zoom)
            pastframe=indexa/zoom
            for indexb in range(bars):
                if (indexa-indexb)>=0:
                    cmd.setAttr (("curveShape1.cp[" + str(indexb) + "].yv"), amplitude*(value[(indexa-indexb)*(samplerate/framerate)/zoom]))
                    cmd.setKeyframe ("curveShape1.cp[" + str(indexb) + "].yv")
                    
def poly(samplerate, framerate, bars, frames, amplitude, zoom, value, barwidth, barlength):
    pastframe=-1
    indexa=0
    for index in range(bars):
        cmd.polyCube (ch=0, o=1, w=barwidth, h=0.1, d=barlength, cuv=4, name="dino"+str(index))
        cmd.move (0, 0.05, 0, "dino" + str(index) + ".scalePivot", "dino" + str(index)+ ".rotatePivot" )
        cmd.move (barwidth*index, 0, 0)
        cmd.setKeyframe ("dino" + str(index) + ".sy")
    
    while pastframe<frames:
        indexa+=1
    
        if (indexa/zoom) != pastframe:
            cmd.currentTime (indexa/zoom)
            pastframe=indexa/zoom
            for indexb in range(bars):
                if (indexa-indexb)>=0:
                    cmd.setAttr (("dino" + str(indexb) + ".scaleY"), amplitude*(value[(indexa-indexb)*(samplerate/framerate)/zoom]))
                    cmd.setKeyframe ("dino" + str(indexb) + ".sy")

                    
line(samplerate, framerate, objects, frames, amplitude, zoom, value) # lines
#poly(samplerate, framerate, objects, frames, amplitude, zoom, value, barwidth, barlength)  # poligons
