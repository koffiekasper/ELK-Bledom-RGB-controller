from bleak import BleakClient, BleakScanner
from dotenv import load_dotenv
import os
from PayloadRepository import PayloadRepository
import asyncio
from concurrent.futures import ThreadPoolExecutor
global pipe_path

pipe_path = "./.pipe"

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
        self.executor = ThreadPoolExecutor()
        self.futureFile = self.executor.submit(self.ReadPipe)
        
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

    def ToggleRandom(self):
        self.payloadRepository.SwitchMode("Random")
        
    async def ParsePipeData(self):
        if self.pipeData:
            if self.pipeData == "mode_random":
                print("Switching to Random mode")
                self.ToggleRandom()
                self.pipeData = ""
 
    async def RunLoop(self):
        while self.running:
            if self.futureFile.done():
                await self.ParsePipeData()
                self.futureFile = self.executor.submit(self.ReadPipe) 
            await self.SendPayload()
            if self.payloadRepository.Iterating():
                self.payloadRepository.outputColor = self.payloadRepository.payloadList[self.payloadRepository.listIterator]
                self.payloadRepository.IteratePayloadLoop()
            await asyncio.sleep(self.GetSleepTime())
     
    async def SendPayload(self):
        payload = self.payloadRepository.GeneratePayload()
        await self.bleakClient.write_gatt_char(self.GATTHandle, payload, response=False)
        
    def ToggleRunning(self):
        self.running = not self.running 
        