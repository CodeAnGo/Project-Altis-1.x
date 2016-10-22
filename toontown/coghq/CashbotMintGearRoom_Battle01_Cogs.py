from SpecImports import *
from toontown.toonbase import ToontownGlobals
import random
CogParent = 10000
GuardCogParent = 10069
BattleCellId = 0
GuardBattleCellId = 1
BattleCells = {BattleCellId: {'parentEntId': CogParent,
                'pos': Point3(0, 0, 0)},
 GuardBattleCellId: {'parentEntId': GuardCogParent,
                     'pos': Point3(0, 0, 0)}}
CogData = [{'parentEntId': CogParent,
  'boss': 1,
  'level': 12,
  'battleCell': BattleCellId,
  'pos': Point3(-6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': random.choice([10, 11]),
  'battleCell': BattleCellId,
  'pos': Point3(-2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': random.choice([10, 11]),
  'battleCell': BattleCellId,
  'pos': Point3(2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': CogParent,
  'boss': 0,
  'level': random.choice([10, 11]),
  'battleCell': BattleCellId,
  'pos': Point3(6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 0},
 {'parentEntId': GuardCogParent,
  'boss': 0,
  'level': random.choice([7, 8, 9]),
  'battleCell': GuardBattleCellId,
  'pos': Point3(-6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': GuardCogParent,
  'boss': 0,
  'level': random.choice([7, 8, 9]),
  'battleCell': GuardBattleCellId,
  'pos': Point3(-2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': GuardCogParent,
  'boss': 0,
  'level': random.choice([7, 8, 9]),
  'battleCell': GuardBattleCellId,
  'pos': Point3(2, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': GuardCogParent,
  'boss': 0,
  'level': random.choice([7, 8, 9]),
  'battleCell': GuardBattleCellId,
  'pos': Point3(6, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1}]
ReserveCogData = []
