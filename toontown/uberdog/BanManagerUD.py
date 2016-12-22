import os
import json

class BanManagerUD:

    def __init__(self, air):
        self.air = air
        
        self.bansFilename = 'bannedPlayers.json'
        self.bansFileData = {}
    
    def setup(self):
        if not os.path.exists(self.bansFilename):
            with open(self.bansFilename, 'w') as file:
                file.write(json.dumps({})); file.close()

        # update the ban information from the file
        self.update()

    def update(self):
        with open(self.bansFilename, 'rb') as file:
            self.bansFileData = json.loads(file.read()); file.close()
    
    def banToon(self, cookie, reason):
        if cookie in self.bansFileData.keys():
            # uh wtf just happened?
            return
        
        self.bansFileData[cookie] = reason
        
        # update the storage file data
        with open(self.bansFilename, 'r+') as file:
            file.write(json.dumps(self.bansFileData)); file.close()
    
    def getToonBanned(self, cookie):
        # update the ban information from the file
        self.update()
        
        if cookie in self.bansFileData.keys():
            return True
        
        return False
    
    def getToonBanReason(self, cookie):
        return self.bansFileData[cookie]
