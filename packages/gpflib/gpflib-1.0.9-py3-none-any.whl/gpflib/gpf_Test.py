import json
import re
import os,glob
from gpflib import GPF

def PrintRelation(gpf):
    Relations=gpf.GetRelations()
    for R in Relations:
        Relation=gpf.GetWord(R["U1"])+" "+gpf.GetWord(R["U2"])+"("+R["R"]+")"
        KVs=gpf.GetRelationKVs(R["U1"],R["U2"],R["R"])
        Info=""
        for k in KVs:
            Val=" ".join(KVs[k])
            if len(KVs[k]) > 1:
                Info=Info+k+"=["+Val+"] "
            else:
                Info=Info+k+"="+Val+" "
            print("=>"+Relation)
        if Info != "":
	        print("KV:"+Info)


def PrintUnit(gpf,Type=""):
    if Type =="":
        Type="Type=Chunk|Type=Word|Type=Phrase|Type=Char"	
    GridInfo=gpf.GetGrid()
    for Col in GridInfo:
        for Unit in Col:
            if gpf.IsUnit(Unit,Type):
                Info=""
                KVs=gpf.GetUnitKVs(Unit)
                print("=>",gpf.GetWord(Unit))
                for K in KVs:
                    Val=" ".join(KVs[K])
                    print(K,"=",Val)


def DrawGraph(gpf,Name="",DotPath=".\\Graph\\",OutPath="./"):
    Head='''
    digraph g {
        node [fontname="FangSong"]
        rankdir=TD  '''    
    if Name=="":
        DepHeads=gpf.GetGridKVs("URoot")
        Graph="Graph.png"
    else:
        DepHeads=gpf.GetGridKVs("URoot"+Name+"")
        Graph=Name+"Graph.png"
    Graph=OutPath+Graph
    
    Tree="tree.txt"
    OUT = open(Tree ,"w",encoding="utf8")
    print(Head,file=OUT)
    Inserted={}
			
    for i in range(len(DepHeads)):
        print("Root->"+gpf.GetWord(DepHeads[i])+"\n",file=OUT)
        Roles=gpf.GetUnitKVs(DepHeads[i],"RSub"+Name)
        for j in range(len(Roles)):
            Units=gpf.GetUnitKVs(DepHeads[i],"USub"+Name+"-"+Roles[j])
            for k in range(len(Units)):
                Rel=gpf.GetWord(DepHeads[i])+"->"+gpf.GetWord(Units[k])+"[label="+Roles[j]
                if not Inserted.get(Rel):
                    print(Rel+"]\n",file=OUT)
                    Inserted[Rel]=1
                RS=gpf.GetUnitKVs(Units[k],"RSub"+Name)
                for l in range(len(RS)):
                    UnitFs=gpf.GetUnitKVs(Units[k],"USub"+Name+"-"+RS[l])
                    for m in range(len(UnitFs)):
                        Rel=gpf.GetWord(Units[k])+"->"+gpf.GetWord(UnitFs[m])+"[label="+RS[l]
                        if not Inserted.get(Rel):
                            print(Rel+"]\n",file=OUT)
                            Inserted[Rel]=1
    print("}\n",file=OUT)
    OUT.close()
    Cmd=DotPath+"dot -Tpng "+Tree+" -o "+Graph
    os.system(Cmd)
    Cmd="del "+Tree
    os.system(Cmd)


def DrawNode(gpf,OUT,Root,Name=""):
	if Name == "":
		USub="USub-Link"
	else:
		USub="USub"+Name+"-Link"
	
	V=gpf.GetUnitKVs(Root,USub)
	if len(V) == 0:
		return
	for i in range(len(V)):
		POSs=gpf.GetUnitKVs(Root,"POS")
		POS=" ".join(POSs)
		POS1=re.sub("-","",POS)

		POSs=gpf.GetUnitKVs(V[i],"POS")
		POS2=re.sub("-","",POS)
		print(gpf.GetWord(Root)+POS1+" -> "+gpf.GetWord(V[i])+POS2+"\n",file=OUT)
		DrawNode(gpf,OUT,V[i],Name)

def DrawTree(gpf,Name="",DotPath=".\\Graph\\",OutPath="./"):
    Head='''
digraph g {
    node [fontname="FangSong"]
    rankdir=TD  
'''
    if Name == "":
        Root="URoot-Link"
        Graph="tree.png"
    else:
        Root="URoot"+Name+"-Link"
        Graph=Name+"tree.png"
    Graph=OutPath+Graph
    Tree="tree.txt"
    OUT = open(Tree,"w",encoding="utf8")
    print(Head,file=OUT)
    V=gpf.GetGridKVs(Root)
    if len(V) == 0:
        return
    for i in range(len(V)):
        if len(V) >1:
            print("Root->"+gpf.GetWord(V[i])+"\n",file=OUT)
        DrawNode(gpf,OUT,V[i],Name)
    print("}\n",file=OUT)
    OUT.close()
	
    Cmd=DotPath+"dot -Tpng "+Tree+" -o "+Graph
    os.system(Cmd)
    Cmd="del "+Tree
    os.system(Cmd)

def Test_Grid():
    gpf = GPF("config.txt")
    Line='{"Type": "Chunk", "Units": ["瑞士球员塞费罗维奇", "率先", "破门", "，", "沙其理", "梅开二度", "。"], "POS": ["NP", "XP", "VP", "w", "NP", "VP", "w"], "Groups": [{"HeadID": 1, "Group": [{"Role": "sbj", "SubID": 0}]}, {"HeadID": 2, "Group": [{"Role": "sbj", "SubID": 0}]}, {"HeadID": 5, "Group": [{"Role": "sbj", "SubID": 4}]}],"ST":"dep"}'
    gpf.AddStructure(Line)
    Grid = gpf.GetGrid()
    for C in Grid:
        for U in C:
            print(U,gpf.GetWord(U))
            
    KV = gpf.GetGridKVs("")
    for K in KV:
        for V in KV[K]:
            print(K,V)

def Test_JSON():
    Line= """
    {"Words": ["瑞士", "率先", "破门", "，", "沙其理", "梅开二度", "。"], 
    "Tags": ["ns", "d", "v", "w", "nr", "i", "w"], 
    "Relations": [{"U1": 2, "U2":0,"R":"A0","KV":"KV1"},
    {"U1": 2, "U2":1,"R":"Mod","KV":"KV2"},
    {"U1": 5, "U2":4,"R":"A0","KV":"KV3"}]} """
    gpf = GPF("config.txt")
    json_data = json.loads(Line)
    Sentence="".join(json_data["Words"])
    gpf.SetText(Sentence)
    Units=[]
    Col=0
    for i in range(len(json_data["Words"])):
        Col=Col+len(json_data["Words"][i])
        print(json_data["Words"][i],Col-1)
        Unit=gpf.AddUnit(Col-1,json_data["Words"][i])
        gpf.AddUnitKV(Unit,"POS",json_data["Tags"][i])
        Units.append(Unit)
        
    for i in  range(len(json_data["Relations"])):
        U1=Units[json_data["Relations"][i]["U1"]]
        U2=Units[json_data["Relations"][i]["U2"]]
        R=json_data["Relations"][i]["R"]
        KV=json_data["Relations"][i]["KV"]
        gpf.AddRelation(U1,U2,R)
        gpf.AddRelationKV(U1,U2,R,"KV",KV)

    GridInfo=gpf.GetGrid()
    for C in GridInfo:
        for U in  C:
            print("=>",gpf.GetWord(U))
	
    Rs = gpf.GetRelations("")
    for R in Rs:
        print(gpf.GetWord(R["U1"]),gpf.GetWord(R["U2"]),R["R"])
    print(gpf.GetText(0,-1))


def Test_TermInfo():
    gpf = GPF()
    Line="称一种无线通讯技术为蓝牙"
    gpf.SetText(Line)
    gpf.AppTable("Segment_Term")
    gpf.RunFSA("Term")
    Units=gpf.GetUnits("Tag=Term")
    for i in range(len(Units)):
        print(gpf.GetWord(Units[i]))     

def Idx_GPF(Name,Path="./data"):
    for file in glob.glob(Path):
        if os.path.isfile(file):
            os.remove(file)

    gpf = GPF(Path)
    FSA="./Examples/"+Name+"/GPF.fsa"
    if os.path.exists(FSA):
        gpf.IndexFSA(FSA)
    Table="./Examples/"+Name+"/GPF.tab"
    if os.path.exists(Table):
        gpf.IndexTable(Table)
   
def Test_Time():
    Line="星期日下午我去图书馆"
    gpf = GPF()
    gpf.SetText(Line)
    gpf.AppTable("Time_Entry")
    gpf.RunFSA("Time")
    Us=gpf.GetUnits("Tag=Time")
    for U in Us:
        print(gpf.GetWord(U))


def Test_BCC():
    Query="a的n{}Freq"
    # Query="提高{}Context(10)"
    # Query="a的n{}Freq"
    # Query="VP-PRD[]{}Freq"
    # Query="VP-PRD[*发展]NP-OBJ[]{}Freq"
    # Query=".n{}Freq"
    # Query="增强~w{}Freq"
    # Query="是*的w{}Freq"
    # Query="是^的w{}Freq"
    # Query="v了(n){$1=[世界 人类 社会]}Freq" 
    # Query="(v)一(v){$1=$2}Freq" 
    # Query="NP-OBJ[]{end($Q)=[制度]}Freq"
    # Query="VP-PRD[]{beg($Q)=[很 非常]}Freq"
    # Query="吃(n){len($1)=3}Freq" 
    # Query="VP-PRD[d(v)了]{print($1)}Freq" 
    # Query="吃(n){len($1)=1}Freq"
    gpf = GPF()
    json_data={}
    json_data["Func"]="Query"
    json_data["Query"]=Query
    json_data["Value"]=[]
    json_data["Value"].append("")
    json_data["PageNum"]=100
    json_data["PageNo"]=0
    js=json.dumps(json_data,ensure_ascii=False)
    Out=gpf.CallService(js,"hskxw")
    Res=json.loads(Out)
    for i in range(len(Res["res"])):
        print(Res["res"][i])

def Test_DupWord():
    Sent="李明回头看了一看。"
    gpf = GPF()
    Segment=gpf.CallService(Sent,"seg")
    gpf.AddStructure(Segment)
    gpf.RunFSA("DupWord")
    Units=gpf.GetUnits("Tag=DupWord")
    for i in range(len(Units)):
        print(gpf.GetWord(Units[i]))

def Test_Merge():
    Line = "下半场的38分钟，李明攻入第1个球，成功将比分扳平至2-1。"
    gpf = GPF()
    gpf.SetText(Line)
    depseg_struct = gpf.CallService(Line, "depseg")
    gpf.AddStructure(depseg_struct)
    gpf.AppTable("Merge_Dict")
    gpf.RunFSA("Merge")
    phrase_units = gpf.GetUnits("Tag=MatchTime|Tag=Order|Tag=MatchScore")
    for i in range(len(phrase_units)):
        print(gpf.GetWord(phrase_units[i]))

def Test_Mood():
    Sent="李明非常不喜欢他"
    gpf = GPF()
    gpf.SetText(Sent)
    DepStruct=gpf.CallService(gpf.GetText(),"dep")
    gpf.AddStructure(DepStruct)
    Seg=gpf.CallService(gpf.GetText(),"seg")
    gpf.AddStructure(Seg)
    gpf.AppTable("Tab_Mod")
    gpf.RunFSA("Mod2Head")
    gpf.RunFSA("Mod2Prd")
    Logs=gpf.GetLog()
    for log in Logs:
        print(log)
    Units=gpf.GetUnits("Tag=Mood")
    for i in range(len(Units)):
        print(gpf.GetWord(Units[i]))


def Test_WSD():
    gpf=GPF()
    Sentence="这个苹果很甜呀"
    gpf.SetTable("Dict_Info")
    gpf.SetText(Sentence)
    Segment=gpf.CallService(gpf.GetText(),"seg")
    gpf.AddStructure(Segment)
    Units=gpf.GetUnits("Sem=*")
    for i in range(len(Units)):
        Sems=gpf.GetUnitKVs(Units[i],"Sem")
        MaxScore=-10
        WS=""
        for j in range(len(Sems)):
            gpf.RunFSA("WSD","Sem="+Sems[j])
            Score=gpf.GetUnitKVs(Units[i],"Sem_"+Sems[j])
            if len(Score) != 0:
                Score=int(Score[0])
            else:
                Score=0
            if MaxScore < Score:
                MaxScore = Score
                WS=Sems[j]
        if WS != "":
            gpf.AddUnitKV(Units[i],"Sense",WS)
    Units=gpf.GetUnits("Sense=*")
    for i in range(len(Units)):
        WS,=gpf.GetUnitKVs(Units[i],"Sense")
        print(gpf.GetWord(Units[i]),WS)

def Test_SepWord(Type):
    Sent="李明把守的大门被他破了"
    gpf=GPF()
    gpf.SetText(Sent)
    DepStruct=gpf.CallService(gpf.GetText(),"dep")
    gpf.AddStructure(DepStruct)
    Seg=gpf.CallService(gpf.GetText(),"seg")
    gpf.AddStructure(Seg)
    gpf.AppTable("Sep_V")
    if Type == 1:
        gpf.RunFSA("SepV1")
    else:
        gpf.RunFSA("SepV2")
    Units=gpf.GetUnits("Tag=SepWord")
    for  Unit in Units:
        print(gpf.GetWord(Unit))

def Test_CoEvent(Path):
    Sentence="淘气的孩子打碎了一个花瓶。"
    gpf=GPF(Path)
    gpf.SetText(Sentence)
    DepStruct=gpf.CallService(gpf.GetText(),"dep")
    gpf.AddStructure(DepStruct)
    Seg=gpf.CallService(gpf.GetText(),"seg")
    gpf.AddStructure(Seg)
    gpf.AppTable("Co_Event")
    gpf.RunFSA("CoEvent")
    PrintUnit(gpf)
    DrawGraph(gpf)

def Test_DrawTree():
    Line='{"Type":"Tree","Units":["(((王)((阿)(姨)))((((出)(门))((买)(菜)))(了)))"],"ST":"GPF"}'
    gpf=GPF()
    gpf.AddStructure(Line)
    DrawTree(gpf)

def Test_DrawGraph():
    Line='''
    {"Type": "Chunk", "Units": ["瑞士球员塞费罗维奇", "率先", "破门", "，", "沙其理", "梅开二度", "。"], "POS": ["NP", "VP", "VP", "w", "NP", "VP", "w"], "Groups": [{"HeadID": 1, "Group": [{"Role": "sbj", "SubID": 0}]}, {"HeadID": 2, "Group": [{"Role": "sbj", "SubID": 0}]}, {"HeadID": 5, "Group": [{"Role": "sbj", "SubID": 4}]}],"ST":"dep"}'
    '''
    gpf=GPF()
    gpf.AddStructure(Line)
    DrawGraph(gpf)


def Test_Main():
    Idx_GPF("CoEvent","./test1")
    Test_CoEvent("./test1")

def App():
    gpf = GPF("./Test")
    Is=gpf.GetTableItems("Co_Event")
    for i in Is:
        print(i)

App()

