import pandas as pd
import re
import hashlib

#This handle and read the files that we gonna use
def files():
    fileMain= open("main.bundle.js","r",encoding="utf8")
    f=fileMain.read()
    fileData= open("SaveData.sav","r")
    fd=fileData.read()
    x=""
    return fileMain,f,fileData,fd,x

#Change stats function
def change_stats(f):
    dit={}
    ChampionStats=re.findall(r"(?:\'completedStages\':\[\])(.{800})",f) #fetching for the stats
    ChampionNames=re.findall(r"\'charName\':\'([A-Za-z]*\s*[A-Za-z]*|O\\'Sole)(?:.{990})",f) #searching for names    
    print(ChampionNames)
    #print(f"we have {len(ChampionStats)} Champions Stats")
    #print(ChampionStats)
    #print(f"we have {len(ChampionNames)} Champions Names")
    #print(ChampionNames)
    
    # we clean a bit the dirty data we had.
    for n,champ in enumerate(ChampionStats):
        ChampionStats[n]=ChampionStats[n][ChampionStats[n].index("maxHp"):ChampionStats[n].index("'banish'")+12]
   
    # We introduce the data to the dict using zip and a loop.
    for name,champs in zip(ChampionNames,ChampionStats):
        dit[name]=champs
    
    name= input("introduce the name of the champion: ").capitalize()
    
    print("I got program a more powerfull version of the character do you want go with that or introduce your own modification")
    mstats=input("Choose betwen Basic or Own: ").capitalize()
    if mstats=="Basic":
        Super_Hero={"hero":"maxHp':0x299,'armor':0x10,'regen':0x0,'moveSpeed':0x3,'power':0x1,'cooldown':0x1,'area':0x5,'speed':0x1,'duration':0x1,'amount':0x0,'luck':0x10,'growth':0x5,'greed':0x1,'curse':0x1,'magnet':0x5,'revivals':0x0,'rerolls':0x0,'skips':0x0,'banish':0x0"}
    else:
        print("this are the stats for the selected character: ",dit[name])
        print("remember all this numbers are hex if you wanna write big numbers on it")
        hp=input("hp: ")
        armor=input("armor: ")
        regen=input("regen: ")
        mspeed=input("mspeed: ")
        power=input("power: ")
        cooldown=input("cooldown(0 is the minimun of coldown): ")
        area=input("area: ")
        speed=input("speed: ")
        duration=input("duration: ")
        luck=input("luck: ")
        growth=input("growth: ")
        greed=input("greed: ")
        curse=input("curse: ")
        magnet=input("magnet: ")
        revivals=input("revivals: ")
        rerolls=input("rerolls: ")
        skips=input("skips: ")
        banish=input("banish: ")
        
        stats=f"maxHp':0x{hp},'armor':0x{armor},'regen':0x{regen},'moveSpeed':0x{mspeed},'power':0x{power},'cooldown':0x{cooldown},'area':0x{area},'speed':0x{speed},'duration':0x{duration},'amount':0x0,'luck':0x{luck},'growth':0x{growth},'greed':0x{greed},'curse':0x{curse},'magnet':{magnet},'revivals':0x{revivals},'rerolls':0x{rerolls},'skips':0x{skips},'banish':0x{banish}"
        Super_Hero={"hero": stats}
    

    #you can change the values manual here to add to the hero that you like
    
    f=f.replace(dit[name], Super_Hero["hero"])
    print("Do you want to apply this change also to all the characters? ")
    if input("Y/N ").capitalize() == "Y":
        for n in ChampionNames:
            f=f.replace(dit[n],Super_Hero["hero"])
            dit.update({n:Super_Hero["hero"]})
    dit.update({name:Super_Hero["hero"]})
    
    
    
    return f

#For unlock all the characters
def Unlock_all_Characters(f):
    nlist=[]
    text=re.findall(r"................................\]\]:\[\{\'hidden\':.....",f)
    for n in text:
        b=n.replace("!","")
        nlist.append(b)

    for n,v in enumerate(text):
        f=f.replace(text[n],nlist[n])
    print(f"You have unlock all the {len(text)} characters")
    return f

def Unlock_all_Achivements(f):
    alist=[]
    text=re.findall(r"'achieved':!0x1",f)
    for n in text:
        b=n.replace("!","")
        alist.append(b)

    for n,v in enumerate(text):
        f=f.replace(text[n],alist[n])
    print(f"You have unlock all the {len(text)} Achivements")
    return f    

def Unlock_all_Arcanas(f):
    alist=[]
    text=re.findall(r"enabled':!0x1,'unlocked':!0x1",f)
    for n in text:
        b=n.replace("!","")
        alist.append(b)

    for n,v in enumerate(text):
        f=f.replace(text[n],alist[n])
    print(f"You have unlock all the {len(text)} arcanas")
    return f

def Unlock_all_stuff(f):
    alist=[]
    text=re.findall(r"'hidden':!0x1",f)
    for n in text:
        b=n.replace("!","")
        alist.append(b)
    for n,v in enumerate(text):
        f=f.replace(text[n],alist[n])
    
    blist=[]
    text1=re.findall(r"'hidden':!0x0",f)
    for n in text1:
        b=n.replace("!","")
        blist.append(b)
    for n,v in enumerate(text1):
        f=f.replace(text1[n],blist[n])

    print(f"You have Unhide {len(text1)+len(text)} objects")
    return f
#Add gold
def add_gold(fd):
    print("Your actuall gold is: ",re.findall('\"Coin..:(\d*)\.*\d*',fd)[0])
    newgold= input("introduce the amount of gold you want to add: ")

    #this section find the amounts in the file
    Coins=re.findall("\"Coin..:(\d*)\.*\d*",fd)[0] 
    LifeTimeCoins=re.findall("LifetimeCoins\":(\d*)",fd)[0]
    TotalCoins=re.findall("TotalCoins\":(\d*)",fd)[0]

    #This section add the ammount to your actual values
    CoinsGold=str(int(Coins)+int(newgold)) # for calculate the new gold
    LifeGold=str(int(LifeTimeCoins)+int(newgold))
    TotalGold=str(int(TotalCoins)+int(newgold))

    #This section replace the old values for the new ones
    fd=fd.replace(Coins,CoinsGold)
    fd=fd.replace(LifeTimeCoins,LifeGold)
    fd=fd.replace(TotalCoins,TotalGold)

    #This last section its to double check everything was allright
    if re.findall("LifetimeCoins\":(\d*)",fd)[0]==LifeGold and re.findall("TotalCoins\":(\d*)",fd)[0]==TotalGold and re.findall("\"Coin..:(\d*)\.*\d*",fd)[0]==CoinsGold: 
        print("New expend gold: {}\nNew Life Time Gold: {}\nNew Total Gold: {}".format(re.findall("\"Coin..:(\d*)\.*\d*",fd)[0],re.findall("LifetimeCoins\":(\d*)",fd)[0],re.findall("TotalCoins\":(\d*)",fd)[0]))

    # coding back the check sum for the .sav

    fd=fd.replace(re.findall("checksum\":\"([a-z0-9]*)",fd)[0],"")
    #print("* Checksum now empty")
    code=hashlib.sha256(fd.encode("utf-8")).hexdigest()
    #print("* New code hex created")
    Sum=re.findall("checksum\":\"[a-z0-9]*",fd)
    #print("* Finded the placement for the new data")
    fd=fd.replace(re.findall("checksum\":\"[a-z0-9]*",fd)[0],Sum[0]+code)
    #print("* Replaced the empty space with the new hex code")
    if re.findall("checksum\":\"([a-z0-9]*)",fd)[0]==code:
        print("Security test passed")
    return fd

#Main Bundle
def save_main(x,fileMain):
    fileMain.close()
    text_file = open("main.bundle.js", "w",encoding="utf8")
    #print(re.findall(r"\'charName\':\'(Poe)(.{990})", x))
    text_file.write(x)
    text_file.close()
    
    print("Main File Saved to main1.bundle")

#Save Data
def save_sav(g,fileData):
    text_file.close()
    text_file = open("SaveData.sav", "w",encoding="utf8")
    text_file.write(g)

    fileData.close()
    print("Sav file modify and save to SaveData1")

#Main Function
def main():

    run=True
    
    while run:
        
        print("""
If you are running this file you need to know few things

    * This folder come with my SaveData.sav and main.bundle.js also come with an extra copy on the folder for if u mess
      things up, you can always use them.
    * If you wanna use your own files, copy them from the respective folders from your pc and pastle them here, i recomend you also
      to use the CleansCopy folder and pastle there also your back up, nothing bad gonna happends but is always good to have a Backup.
    * This program get an input of your file and reescribe on it all the modifications that you want, after finish you just need to copy
      the resultant file and pastle it in the directory where you pick it up at first.
    * If you have any problems just report it, and i will try to fix it. 
    * If you wanna exit to get your own folders you can just write Close.

          """)

        print(" Do you want change Stats, get more gold or Unlock stuff?:")
        answer=input("Introduce Stats, Gold, Unlock or Close: ").capitalize()
        fileMain,f,fileData,fd,x=files()
        if answer == "Stats":

            x=change_stats(f)
            save_main(x,fileMain)

        elif answer== "Gold":

            g=add_gold(fd)
            save_sav(g,fileData)

        elif answer == "Unlock":
            x=f
            if input("Do you want unlock all the characters? Y/N ").capitalize() == "Y": x=Unlock_all_Characters(x)
            
            if input("Do you want to unlock all the achivement items: Y/N ").capitalize() =="Y":x=Unlock_all_Achivements(x)
            
            if input("Do you want to unlock also the arcanas: Y/N ").capitalize() =="Y": x=Unlock_all_Arcanas(x)

            if input("Do you want to unhide some objects that normally you would not find in the pulls?: Y/N ").capitalize() =="Y":x=Unlock_all_stuff(x)

            

            save_main(x,fileMain)

        elif answer=="Close":
            run=False

        else: print("Command not found, try again")
        

if __name__ == "__main__":
    main()