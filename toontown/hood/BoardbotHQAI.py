#from toontown.building import DistributedChairmanElevatorAI
from toontown.building import FADoorCodes
from toontown.building.DistributedBoardingPartyAI import DistributedBoardingPartyAI
#from toontown.coghq.DistributedBoardOfficeElevatorExtAI import DistributedBoardOfficeElevatorExtAI
from toontown.hood import CogHQAI
#from toontown.suit import DistributedBoardbotBossAI
from toontown.suit import DistributedSuitPlannerAI
from toontown.toonbase import ToontownGlobals
from toontown.betaevent import DistributedBetaEventAI
from toontown.building import DistributedCJElevatorAI
from toontown.suit import DistributedLawbotBossAI

class BoardbotHQAI(CogHQAI.CogHQAI):
    def __init__(self, air):
        CogHQAI.CogHQAI.__init__(
            self, air, ToontownGlobals.BoardbotHQ, ToontownGlobals.LawbotLobby,
            FADoorCodes.LB_DISGUISE_INCOMPLETE,
            DistributedCJElevatorAI.DistributedCJElevatorAI,
            DistributedLawbotBossAI.DistributedLawbotBossAI)

        self.air = air
        self.boardOfficeElevators = []
        self.officeBoardingParty = None
        self.suitPlanners = []
        self.event = None
        self.startup()

    def startup(self):
        CogHQAI.CogHQAI.startup(self)
        self.startEvent()
        pass

    def startEvent(self):
        self.event = DistributedBetaEventAI.DistributedBetaEventAI(self.air)
        self.event.generateWithRequired(self.zoneId)
        self.event.start()