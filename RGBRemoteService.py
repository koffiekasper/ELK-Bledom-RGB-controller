from bleak import BleakClient, BleakScanner
from dotenv import load_dotenv
import os
from PayloadRepository import PayloadRepository
import asyncio
from concurrent.futures import ThreadPoolExecutor
global pipe_path

pipe_path = "./.pipe"
pipe_path_osc = "./.pipe_osc"

class OscSettings:
    def __init__(self):
        self.beat = False
        self.volume = False
        self.prog1 = False
        self.prog2 = False
        self.prog3 = False
        self.prog4 = False
        self.prog5 = False
        self.prog6 = False
        self.prog7 = False
        self.prog8 = False

class RGBRemoteService:
    def __init__(self):
        load_dotenv()
        self.UUID = os.getenv('ADDRESS')
        self.mode = "Random"
        self.args = ""
        self.running = True 
        self.pollingFrequencyHz = 60
        self.payloadRepository = PayloadRepository()
        self.pipeData = None
        self.pipeDataOsc = None
        self.executor = ThreadPoolExecutor()
        self.executorOsc = ThreadPoolExecutor()
        self.futureFile = self.executor.submit(self.ReadPipe)
        self.futureFileOsc = self.executorOsc.submit(self.ReadPipeOsc)
        
    async def InitAsync(self):
        device = await BleakScanner.find_device_by_address(
            self.UUID,cb=dict(use_bdaddr=False)
        )
       
        async with BleakClient(
            device,
            services=None
        ) as client:
            print("Connected")
            self.running = True
            self.bleakClient = client  
            for service in self.bleakClient.services:
                for char in service.characteristics:
                    if char.handle == 13:
                        self.GATTHandle = char
            await self.RunLoop()
        return True
        
    def SetPollingFrequency(self, updateFrequencyInHz):
        self.pollingFrequencyHz = updateFrequencyInHz
   
    def GetSleepTime(self):
        return 1 / self.pollingFrequencyHz
    
    def ReadPipe(self):
        with open(pipe_path, 'r') as pipe:
            try:
                data = pipe.read()
                print(f"Read data from named pipe: {data}")
                self.pipeData = data 
                return
            except FileNotFoundError:
                return 

    def ReadPipeOsc(self):
        with open(pipe_path_osc, 'r') as pipe:
            try:
                data = pipe.read()
                self.pipeDataOsc = data 
                return
            except FileNotFoundError:
                return 
            
    async def ParseOscPipeData(self):
        if self.pipeDataOsc:
            print(self.pipeDataOsc)
            data = self.pipeDataOsc.split(',')
            if "/beat" in data and self.payloadRepository.IsBeatControlled():
                self.payloadRepository.IteratePayloadLoop()
            
    def ToggleRandom(self):
        self.payloadRepository.SwitchMode("Random")
        
    def ToggleBeatControlled(self):
        self.payloadRepository.SwitchMode("BeatControlled")
        
    async def ParsePipeData(self):
        if self.pipeData:
            data = self.pipeData.split(',')
            if data[0] == "mode_random":
                print("Switching to Random mode")
                self.ToggleRandom()
                self.pipeData = ""
            if data[0] == "cmd_colorName":
                if not self.payloadRepository.SetCS4Color(data[1]):
                    print(f"CSS4 color {data[1]} not found.")
                else:
                    self.payloadRepository.ToggleColorMode()
                    print(f"CSS4 color {[data[1]]} set")
            if data[0] == "cmd_colorHex":
                if self.payloadRepository.SetHexColor(data[1]) :
                    self.payloadRepository.ToggleColorMode()
                    print(f'Set custom hex color {data[1]}')
                else:
                    print(f'Custom hex color {data[1]} not found.')
            if data[0] == "cmd_setIterateList":
                colors = data[1:]
                colorHexList = [self.payloadRepository.GetCS4ColorFromName(color) for color in colors]
                if False in colorHexList:
                    print("One or more of the colors are not found")
                else:
                    self.payloadRepository.SetPayloadList(colorHexList)
                    print("Set iterate list to: " + str(colors))
            if data[0] == "cmd_setIterateListRainbow":
                self.payloadRepository.SetPayloadListRainbow()
            if data[0] == "cmd_setSpeedHz":
                self.SetPollingFrequency(int(data[1]))
            if data[0] == "mode_beatcontrolled":
                print("Switching to beat controlled mode")
                self.ToggleBeatControlled()
 
    async def RunLoop(self):
        while self.running:
            if self.futureFile.done():
                await self.ParsePipeData()
                self.futureFile = self.executor.submit(self.ReadPipe) 
            if self.futureFileOsc.done():
                await self.ParseOscPipeData()
                self.futureFileOsc = self.executorOsc.submit(self.ReadPipeOsc)
            await self.SendPayload()
            if self.payloadRepository.Iterating():
                self.payloadRepository.IteratePayloadLoop()
                self.payloadRepository.outputColor = self.payloadRepository.payloadList[self.payloadRepository.listIterator]
            if self.payloadRepository.IsBeatControlled():
                self.payloadRepository.outputColor = self.payloadRepository.payloadList[self.payloadRepository.listIterator]
            await asyncio.sleep(self.GetSleepTime())
     
    async def SendPayload(self):
        payload = self.payloadRepository.GeneratePayload()
        await self.bleakClient.write_gatt_char(self.GATTHandle, payload, response=False)
        
    def ToggleRunning(self):
        self.running = not self.running 
        