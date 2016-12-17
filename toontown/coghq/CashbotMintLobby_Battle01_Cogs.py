from SpecImports import *
from toontown.toonbase import ToontownGlobals
import random
a = random.choice([0, 1, 2, 3, 4])
b = random.choice([0, 1, 2, 3, 4])
c = random.choice([0, 1, 2, 3, 4])
d = random.choice([0, 1, 2, 3, 4])
e = random.choice([0, 1, 2, 3, 4])
f = random.choice([0, 1, 2, 3, 4])
g = random.choice([0, 1, 2, 3, 4])
h = random.choice([0, 1, 2, 3, 4])
if a==1:
	b=0
	c=0
	d=0
	e=0
	f=0
	g=0
	h=0
elif b==1:
	a=0
	c=0
	d=0
	e=0
	f=0
	g=0
	h=0
elif c==1:
	a=0
	b=0
	d=0
	e=0
	f=0
	g=0
	h=0
elif d==1:
	a=0
	b=0
	c=0
	e=0
	f=0
	g=0
	h=0
elif e==1:
	a=0
	b=0
	c=0
	d=0
	f=0
	g=0
	h=0
elif f==1:
	a=0
	b=0
	c=0
	d=0
	e=0
	g=0
	h=0
elif g==1:
	a=0
	b=0
	c=0
	d=0
	e=0
	f=0
	h=0
else:
	a=0
	b=0
	c=0
	d=0
	e=0
	f=0
	g=0
	h=1
CogParent = 10000
AParent = 20000
BParent = 20001
CParent = 20002
DParent = 20003
EParent = 20004
FParent = 20005
GParent = 20006
BattleCellId = 0
BattleACellId = 1
BattleBCellId = 2
BattleCCellId = 3
BattleDCellId = 4
BattleECellId = 5
BattleFCellId = 6
BattleGCellId = 7
BattleCells = {BattleCellId: {'parentEntId': CogParent,
                'pos': Point3(0, 0, 0)},
 BattleACellId: {'parentEntId': AParent,
                     'pos': Point3(0, 0, 0)},
 BattleBCellId: {'parentEntId': BParent,
                     'pos': Point3(0, 0, 0)},
 BattleCCellId: {'parentEntId': CParent,
                     'pos': Point3(0, 0, 0)},
 BattleDCellId: {'parentEntId': DParent,
                     'pos': Point3(0, 0, 0)},
 BattleECellId: {'parentEntId': EParent,
                     'pos': Point3(0, 0, 0)},
 BattleFCellId: {'parentEntId': FParent,
                     'pos': Point3(0, 0, 0)},
 BattleGCellId: {'parentEntId': GParent,
                     'pos': Point3(0, 0, 0)}}
CogData = [{'parentEntId': CogParent,
  'boss': a,
  'level': 14,
  'battleCell': BattleCellId,
  'pos': Point3(0, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': AParent,
  'boss': b,
  'level': 14,
  'battleCell': BattleACellId,
  'pos': Point3(0, 0, 0),
  'h': 0,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': BParent,
  'boss': c,
  'level': 14,
  'battleCell': BattleBCellId,
  'pos': Point3(0, 0, 0),
  'h': 0,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': CParent,
  'boss': d,
  'level': 14,
  'battleCell': BattleCCellId,
  'pos': Point3(0, 0, 0),
  'h': 180,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': DParent,
  'boss': e,
  'level': 14,
  'battleCell': BattleDCellId,
  'pos': Point3(0, 0, 0),
  'h': 0,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': EParent,
  'boss': f,
  'level': 14,
  'battleCell': BattleECellId,
  'pos': Point3(0, 0, 0),
  'h': 0,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': FParent,
  'boss': g,
  'level': 14,
  'battleCell': BattleFCellId,
  'pos': Point3(0, 0, 0),
  'h': 0,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1},
 {'parentEntId': GParent,
  'boss': h,
  'level': 14,
  'battleCell': BattleGCellId,
  'pos': Point3(0, 0, 0),
  'h': 0,
  'behavior': 'stand',
  'path': None,
  'skeleton': 1}]
ReserveCogData = []
