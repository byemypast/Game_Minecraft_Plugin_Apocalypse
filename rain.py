import mcpi.minecraft as minecraft
import mcpi.block as block
import random
import time
TIME_CIRCLE = 0.1
mc = minecraft.Minecraft.create()
frozing = {}
frozing_store = {}
supplement = [block.STONE.id,block.WOOD.id,block.WOOL.id,block.IRON_BLOCK.id,block.GOLD_BLOCK.id,block.COAL_BLOCK.id,block.LAPIS_LAZULI_BLOCK.id,block.SNOW_BLOCK.id]
#FinalSite = (0,0,0)# (xyz).the torch on the bedrock that's surrounded by 4 supplements
#PauseTime = 0 # -1: raining; 0: pause stop; >0: pausing
#PauseScore = 0
MIN_PAUSETIME = 600 # 10 min
SiteRandomX_r = 180
SiteRandomY_MIN = 40
SiteRandomY_MAX = 120
SiteRandomZ_r = 180

def Generate_Site():
	#randomly generate the Site
	RandomEntity = random.choice(mc.getPlayerEntityIds())
	FirstPos = mc.entity.getTilePos(RandomEntity)
	FinalSitex = random.randint(FirstPos.x - SiteRandomX_r,FirstPos.x + SiteRandomX_r)
	FinalSitey = random.randint(SiteRandomY_MIN,SiteRandomY_MAX)
	FinalSitez = FirstPos.z+random.randint(-SiteRandomZ_r,SiteRandomZ_r)
	
	#on the ground/under the ground
	while (mc.getBlock(FinalSitex,FinalSitey,FinalSitez)==0)and(FinalSitey>=-100):
		FinalSitey -= 1
	
	if FinalSitey<=-100:
		FinalSitey = random.randint(SiteRandomY_MIN,SiteRandomY_MAX)
	
	mc.setBlock(FinalSitex,FinalSitey,FinalSitez,block.SNOW_BLOCK.id)
	mc.setBlock(FinalSitex,FinalSitey-1,FinalSitez,block.BEDROCK.id)
	mc.setBlock(FinalSitex-1,FinalSitey-1,FinalSitez,random.choice(supplement))
	mc.setBlock(FinalSitex+1,FinalSitey-1,FinalSitez,random.choice(supplement))
	mc.setBlock(FinalSitex,FinalSitey-1,FinalSitez-1,random.choice(supplement))
	mc.setBlock(FinalSitex,FinalSitey-1,FinalSitez+1,random.choice(supplement))
	FinalSite = (FinalSitex,FinalSitey,FinalSitez)
	print(FinalSite)
	return FinalSite


def Timer_FinalSite(FinalSite,PauseScore,PauseTime):
	if (1):
		if (mc.getBlock(FinalSite)==0)and(mc.getBlock(FinalSite[0],FinalSite[1]-1,FinalSite[2])==block.BEDROCK.id): # The Site is destroied. BEDROCK for detecting the same world
			PauseScore += MIN_PAUSETIME 
			PauseTime += PauseScore
			mc.postToChat("You've successfully destoried the Site ! ")
			mc.postToChat("Peaceful Time: " + str(PauseTime))
			PauseScore = 0
			FinalSite = Generate_Site()
	return FinalSite,PauseScore,PauseTime

def FindAltar(FinalSite,PauseScore,PauseTime):
	entityIDs = mc.getPlayerEntityIds()
	for entity in entityIDs:
		pos = mc.entity.getTilePos(entity)

		a = mc.getBlock(pos.x,pos.y,pos.z-1)
		b = mc.getBlock(pos.x,pos.y,pos.z+1)
		c = mc.getBlock(pos.x-1,pos.y,pos.z)
		d = mc.getBlock(pos.x+1,pos.y,pos.z)
		print(a,b,c,d,block.TORCH.id)
		if (a==b==c==d==block.TORCH.id):
			core = mc.getBlock(pos.x,pos.y-1,pos.z)
			PauseScore += random.randint(-10,min(50,core))
			
			if FinalSite[0]!=pos.x:
				x_direction = (abs(FinalSite[0]-pos.x))/(FinalSite[0]-pos.x)
			else:
				x_direction = 0
				
			if FinalSite[2]!=pos.z:
				z_direction = (abs(FinalSite[2]-pos.z))/(FinalSite[2]-pos.z)
			else:
				z_direction = 0
				
			mc.setBlock(pos.x,pos.y-1,pos.z,block.TNT.id)
			mc.setBlock(pos.x,pos.y-2,pos.z,block.REDSTONE_BLOCK.id)
			mc.setBlock(pos.x+x_direction,pos.y,pos.z+z_direction,block.TNT.id)
	return FinalSite,PauseScore,PauseTime
			
	
def ControlShadow(ReplaceFrom,ReplaceTo,Duration):
	entityIDs = mc.getPlayerEntityIds()
	for entity in entityIDs:
		pos = mc.entity.getTilePos(entity)
		if mc.getBlock(pos.x,pos.y-1,pos.z)==ReplaceFrom:
			frozing[pos] = Duration
			frozing_store[pos] = mc.getBlockWithData(pos.x,pos.y-1,pos.z)
			#mc.setBlock(pos.x,pos.y-1,pos.z,block.OBSIDIAN.id)
			mc.setBlock(pos.x,pos.y-1,pos.z,ReplaceTo)
	
	fn = frozing.copy()
	for fblock in fn:
		frozing[fblock] -= TIME_CIRCLE
		if frozing[fblock] <= 0:
			pos = fblock
			frozing.pop(fblock)
			mc.setBlock(pos.x,pos.y-1,pos.z,frozing_store[fblock].id,frozing_store[fblock].data)
			frozing_store.pop(fblock)
	
	
	
def FUN_rain(x,y,z,FinalSite,PauseScore,PauseTime):
	#times = -1
	x_step = random.randint(-1,1)
	y_step = -1
	z_step = random.randint(-1,1)
	num_tailblock = random.randint(4,10)
	tails = {}
	
	tails[0] = (x,y,z)
	
	while True:
		time.sleep(TIME_CIRCLE)
		try:
			#Watch the Final Site and update the new one
			FinalSite,PauseScore,PauseTime = Timer_FinalSite(FinalSite,PauseScore,PauseTime)
		
			#Watch the Altar the players make
			FinalSite,PauseScore,PauseTime = FindAltar(FinalSite,PauseScore,PauseTime)
		
			#Shadow_Control
			ControlShadow(block.GRASS.id,block.OBSIDIAN.id,min(1+PauseTime/60,20))
		except:
			pass #for single-player death
		
		
		if PauseTime<=0:
			#rain main
			posnow = mc.player.getTilePos()
			#if you're in the end land, the rain will not randomlize the pos
			if mc.getBlock(posnow.x,posnow.y-1,posnow.z)==block.END_STONE.id:
				x_step = 0
				z_step = 0
			
			#times += 1
			
			i = -1
			oldtails = tails.copy()
			for ele_tail in tails:
				i += 1
				tx,ty,tz = tails[i]
				tx += x_step
				ty += y_step
				tz += z_step
				tails[i] = (tx,ty,tz)
	
			#try to extend the tail
			if len(tails) < num_tailblock:
				tx,ty,tz = tails[i]
				tails[i+1] = (tx-x_step,ty-y_step,tz-z_step)
			
			posnow = mc.player.getTilePos()
			
			#if the bomb is going to strike to the land
			if (mc.getBlock(tails[0])!=0)or(abs(ty-posnow.y)>=255): ##bomb
				tx,ty,tz = tails[0]
				#print("*bomb "+str(tx)+" "+str(ty)+" "+str(tz))
				for i in tails:
					mc.setBlock(tails[i],0,0)
				for i in oldtails:
					mc.setBlock(oldtails[i],0,0)
				
				mc.setBlocks(tx-1,ty-3,tz-1,tx+1,ty,tz+1,block.LAVA.id)
				mc.setBlocks(tx+1,ty+1,tz,tx+1,ty+1,tz+1,block.TNT.id)
				mc.setBlocks(tx+1,ty,tz,tx+1,ty,tz+1,block.REDSTONE_BLOCK.id)
				break
			else:
				for i in oldtails:
					mc.setBlock(oldtails[i],0)
				mc.setBlock(tails[0],block.OBSIDIAN.id)
				for tail in tails:
					if tail!=0:
						mc.setBlock(tails[tail],block.REDSTONE_BLOCK.id)
		else:
			PauseTime -= TIME_CIRCLE
			#print(PauseTime)
	return time.time(),FinalSite,PauseScore,PauseTime
	

oldtick = 0
PauseScore = 0
PauseTime = 600
mc.postToChat("You've 600 seconds to prepare for the apocalypse.")
FinalSite = Generate_Site()
while True:
	self_pos = mc.player.getTilePos()	
	y_int = random.randint(40,80)
	newtick,FinalSite,PauseScore,PauseTime = FUN_rain(self_pos.x+random.randint(-15,15),self_pos.y+y_int,self_pos.z+random.randint(-15,15),FinalSite,PauseScore,PauseTime)
	while (newtick-oldtick)<3:
		newtick = time.time()
	oldtick = newtick
	print(FinalSite,mc.player.getTilePos())