from bleak import BleakClient, BleakScanner
from dotenv import load_dotenv
import os
from PayloadRepository import PayloadRepository
import asyncio
import threading
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
    
    async def ReadPipe(self):
        print("trying to read pipe")
        try:
            with open(pipe_path, "r") as pipe:
                data = pipe.read()
            print(f"Read data from named pipe: {data}")
            self.pipeData = data 
        except FileNotFoundError:
            return ""

    def ToggleRandom(self):
        self.payloadRepository.SwitchMode("Random")
        
    async def ParsePipeData(self):
        if not self.pipeData:
            self.ReadPipe()
        else:
            print(self.pipeData)
            if pipeData == "Random":
                self.ToggleRandom()
                pipeData = ""
 
    async def RunLoop(self):
        while self.running:
            print("Main loop")
            await self.SendPayload()
            await self.ParsePipeData()
            if self.payloadRepository.Iterating():
                self.payloadRepository.outputColor = self.payloadRepository.payloadList[self.payloadRepository.listIterator]
                self.payloadRepository.IteratePayloadLoop()
            await asyncio.sleep(self.GetSleepTime())
     
    async def SendPayload(self):
        payload = self.payloadRepository.GeneratePayload()
        await self.bleakClient.write_gatt_char(self.GATTHandle, payload, response=False)
        
    def ToggleRunning(self):
        self.running = not self.running 
        