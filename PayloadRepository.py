import itertools
import time
import asyncio

class PayloadRepository:
    modes = ["Random", "Flow", "Music", "Color"]
    iteratingModes = ["Random", "Flow"] 
    
    def __init__(self):
        self.outputColor = "000000"
        self.listIterator = 0
        self.payloadList = ["000000"]
        self.mode = "Random"
        self.iterateFrequencyHz = 60
   
    async def RunLoop(self):
        while self.Iterating():
            print('Iterating')
            await asyncio.sleep(self.GetSleepTime()) 
            self.outputColor = self.payloadList[self.listIterator]
            self.IteratePayloadLoop()
            
    def Iterating(self):
        return self.mode in PayloadRepository.iteratingModes
    
    def GeneratePayload(self):
        if self.mode in PayloadRepository.iteratingModes:
            return b"".fromhex(f"7e000503{self.outputColor}00ef")
    
    def IteratePayloadLoop(self):
        if self.listIterator >= len(self.payloadList) -1:
            self.listIterator = 0
        else:
            self.listIterator += 1
   
    def SetIterateFrequency(self, hertz):
        self.iterateFrequencyHz = hertz
        
    def GetSleepTime(self):
        return 1 / self.iterateFrequencyHz
    
    def SwitchMode(self, mode, args=None):
        self.mode = mode
        self.args = args
        if mode == "Random":
            if args == None:
                args = {
                    "stepSize": 1,
                    "size": 100
                }
            self.payloadList = generate_color_grid(args["size"], args["size"], args["stepSize"])

def generate_color_gradient(color1, color2, num_steps):
    # Extract RGB components from color1 and color2
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    
    # Initialize an empty list to store the gradient colors
    gradient = []
    
    # Calculate the step size for each RGB component
    r_step = (r2 - r1) / (num_steps - 1)
    g_step = (g2 - g1) / (num_steps - 1)
    b_step = (b2 - b1) / (num_steps - 1)
    
    # Generate the gradient colors
    for step in range(num_steps):
        r = int(r1 + step * r_step)
        g = int(g1 + step * g_step)
        b = int(b1 + step * b_step)
        gradient.append((r, g, b))
    
    return ['%02x%02x%02x' % color for color in gradient]    

def generate_color_grid(rows, cols, step=32):
    colors = []
    for r, g, b in itertools.product(range(0, 256, step), repeat=3):
        colors.append((r, g, b))
        if len(colors) >= rows * cols:
            break
    return ['%02x%02x%02x' % color for color in colors]