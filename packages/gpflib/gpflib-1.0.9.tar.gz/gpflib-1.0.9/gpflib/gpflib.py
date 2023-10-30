import json
from ctypes import *
import platform
import os
import re
import struct


OS = platform.system()
if OS == "Windows":
    import win32api

class GPF:
    def __init__(self, dataPath="./data"):
        dll_name = ''

        if OS == "Windows":
            dll_name = 'gpflib.dll'
        else:
            dll_name = 'libgpflib.so'

        dll_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), dll_name)
        cfg_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.txt')
        self.library = cdll.LoadLibrary(dll_file)
        self.buf_max_size = 2048*10
        self.Config= cfg_file
        self.dataPath= dataPath
        self.library.GPF_Init.argtypes = [c_char_p]
        self.library.GPF_Init.restype  = c_void_p  
        self.hHandle = self.library.GPF_Init(cfg_file.encode(), dataPath.encode())
        # https://stackoom.com/question/1VWM
        if OS == "Windows":
            self.dll_close = win32api.FreeLibrary
        elif OS == "Linux":
            try:
                stdlib = CDLL("")
            except OSError:
                stdlib = CDLL("libc.so")
            self.dll_close = stdlib.dlclose
            self.dll_close.argtypes = [c_void_p]

    def __del__(self):
        self.library.GPF_Term(c_void_p(self.hHandle))
        self.dll_close(self.library._handle)
    
    def SetText(self, text):
        self.library.GPF_SetText.argtypes = [c_void_p, c_char_p]
        self.library.GPF_SetText.restype  = c_int
        ret = self.library.GPF_SetText(self.hHandle, text.encode())
        return ret


    def AddStructure(self, json_str):
        self.library.GPF_AddStructure.argtypes = [c_void_p, c_char_p]
        self.library.GPF_AddStructure.restype  = c_int
        ret = self.library.GPF_AddStructure(self.hHandle, json_str.encode())
        return ret

    def RunService(self, sentence, name):
        return self.CallService(sentence, name)

    def CallService(self, sentence, name):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_CallService.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library.GPF_CallService.restype  = c_int
        str_len = self.library.GPF_CallService(self.hHandle, name.encode(), sentence.encode(), return_value, self.buf_max_size)
        ret = string_at(return_value, str_len)
        return ret.decode()


    def SetTable(self, tableName):
        self.library.GPF_SetLexicon.argtypes = [c_void_p, c_char_p]
        self.library.GPF_SetLexicon.restype  = c_int
        ret = self.library.GPF_SetLexicon(self.hHandle, tableName.encode())
        return ret

    def RunTable(self, tableName):
        return self.AppTable(tableName)

    def AppTable(self, tableName):
        self.library.GPF_AppLexicon.argtypes = [c_void_p, c_char_p]
        self.library.GPF_AppLexicon.restype  = c_int
        self.library.GPF_AppLexicon(self.hHandle, tableName.encode())
        return 0

    def GetSuffix(self, tableName, sentence):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_GetSuffix.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library.GPF_GetSuffix.restype  = c_int
        str_len = self.library.GPF_GetSuffix(self.hHandle, tableName.encode(), sentence.encode(), return_value, self.buf_max_size)
        ret = string_at(return_value, str_len)
        return ret.decode()
    
    def GetPrefix(self, tableName, sentence):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_GetPrefix.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library.GPF_GetPrefix.restype  = c_int
        str_len = self.library.GPF_GetPrefix(self.hHandle, tableName.encode(), sentence.encode(), return_value, self.buf_max_size)
        ret = string_at(return_value, str_len)
        return ret.decode()

    def GetWord(self, UnitNo):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_GetWord.argtypes = [c_void_p, c_char_p, c_char_p, c_int]
        self.library.GPF_GetWord.restype  = c_int
        str_len = self.library.GPF_GetWord(self.hHandle, UnitNo.encode(), return_value, self.buf_max_size)
        ret = string_at(return_value, str_len)
        return ret.decode()


    def RunFSA(self, fsaName, param=""):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_RunFSA.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library.GPF_RunFSA.restype  = c_int

        self.library.GPF_SetFSAPath.argtypes = [c_void_p, c_char_p, c_int]
        self.library.GPF_SetFSAPath.restype  = c_int

        len = self.library.GPF_RunFSA(self.hHandle, fsaName.encode(), param.encode(),return_value,self.buf_max_size)

        TotalNum=struct.unpack("i",return_value[0:4])
        offset=4
        for i in range(TotalNum[0]):
            OperationLen=struct.unpack("i",return_value[offset:offset+4])
            offset+=4
            code=return_value[offset:offset+OperationLen[0]]
            offset+=OperationLen[0]
            MatchPathLen=struct.unpack("i",return_value[offset:offset+4])
            offset+=4
            self.library.GPF_SetFSAPath(self.hHandle, return_value[offset:offset+MatchPathLen[0]],MatchPathLen[0])
            offset+=MatchPathLen[0]
            exec(code.decode())

        return len

    def GetParam(self, key):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_GetParam.argtypes = [c_void_p, c_char_p, c_char_p, c_int]
        self.library.GPF_GetParam.restype  = c_int
        str_len = self.library.GPF_GetParam(self.hHandle, key.encode(), return_value, self.buf_max_size)
        ret = string_at(return_value, str_len)
        return ret.decode()
    
        
    def GetGrid(self):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_GetGrid.argtypes = [c_void_p, c_char_p, c_int]
        self.library.GPF_GetGrid.restype  = c_int
        str_len = self.library.GPF_GetGrid(self.hHandle, return_value, self.buf_max_size)
        if str_len != 0:
            str_ret = string_at(return_value, str_len)
            json_data = json.loads(str_ret.decode())
            return json_data
        return ""
        
    def GetText(self, begin=0, end=-1):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_GetTextByRange.argtypes = [c_void_p, c_int, c_int, c_char_p, c_int]
        self.library.GPF_GetTextByRange.restype  = c_int
        str_len = self.library.GPF_GetTextByRange(self.hHandle, begin, end, return_value, self.buf_max_size)
        ret = string_at(return_value, str_len)
        return ret.decode()

    def GetGridKVs(self, key=""):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_GetGridKVs.argtypes = [c_void_p, c_char_p, c_char_p, c_int]
        self.library.GPF_GetGridKVs.restype  = c_int
        str_len = self.library.GPF_GetGridKVs(self.hHandle, key.encode(), return_value, self.buf_max_size)
        if str_len != 0:
            ret = string_at(return_value, str_len)
            json_data = json.loads(ret.decode())
            return json_data
        return ""
    
    def GetUnit(self, pathNo):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_GetUnitByInt.argtypes = [c_void_p, c_int, c_char_p, c_int]
        self.library.GPF_GetUnitByInt.restype  = c_int
        str_len = self.library.GPF_GetUnitByInt(self.hHandle, pathNo, return_value, self.buf_max_size)
        ret = string_at(return_value, str_len)
        return ret.decode()

    def GetUnits(self, kv,UnitNo="",UExpress=""):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_GetUnitsByKV.argtypes = [c_void_p, c_char_p, c_char_p, c_int]
        self.library.GPF_GetUnitsByKV.restype  = c_int

        self.library.GPF_GetUnitsByNo.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library.GPF_GetUnitsByNo.restype  = c_int

        if UnitNo == "":
            str_len = self.library.GPF_GetUnitsByKV(self.hHandle, kv.encode(), return_value, self.buf_max_size)
        else:
            str_len = self.library.GPF_GetUnitsByNo(self.hHandle, UnitNo.encode(),UExpress.encode(),kv.encode(), return_value, self.buf_max_size)

        if str_len != 0:
            ret = string_at(return_value, str_len)
            json_data = json.loads(ret.decode())
            return json_data
        return 0
   
    def GetUnitKVs(self, unitNo, key=""):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_GetUnitKVs.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library.GPF_GetUnitKVs.restype  = c_int
        str_len = self.library.GPF_GetUnitKVs(self.hHandle, unitNo.encode(), key.encode(), return_value, self.buf_max_size)
        if str_len != 0:
            ret = string_at(return_value, str_len)
            json_data = json.loads(ret.decode())
            return json_data
        return ""

    def GetRelations(self, kv=""):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_GetRelations.argtypes = [c_void_p, c_char_p, c_char_p, c_int]
        self.library.GPF_GetRelations.restype  = c_int
        str_len = self.library.GPF_GetRelations(self.hHandle, kv.encode(), return_value, self.buf_max_size)
        if str_len != 0:
            ret = string_at(return_value, str_len)
            json_data = json.loads(ret.decode())
            return json_data
        return ""

    def GetRelationKVs(self, unitNo1, unitNo2, role, key=""):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_GetRelationKVs.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library.GPF_GetRelationKVs.restype  = c_int
        str_len = self.library.GPF_GetRelationKVs(self.hHandle, unitNo1.encode(), unitNo2.encode(), role.encode(), key.encode(), return_value, self.buf_max_size)
        if str_len != 0:
            ret = string_at(return_value, str_len)
            json_data = json.loads(ret.decode())
            return json_data
        return ""
        
    def GetTableItems(self, tableName, kv=""):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_GetTableItems.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library.GPF_GetTableItems.restype  = c_int
        str_len = self.library.GPF_GetTableItems(self.hHandle, tableName.encode(), kv.encode(), return_value, self.buf_max_size)
        if str_len != 0:
            ret = string_at(return_value, str_len)
            json_data = json.loads(ret.decode())
            return json_data
        return ""

    def GetTableItemKVs(self, tableName, item="", key=""):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_GetTableItemKVs.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library.GPF_GetTableItemKVs.restype  = c_int
        str_len = self.library.GPF_GetTableItemKVs(self.hHandle, tableName.encode(), item.encode(), key.encode(), return_value, self.buf_max_size)
        if str_len != 0:
            ret = string_at(return_value, str_len)
            json_data = json.loads(ret.decode())
            return json_data
        return ""

    def GetFSANode(self, tag="-1"):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_GetFSANodeByTag.argtypes = [c_void_p, c_char_p, c_char_p, c_int]
        self.library.GPF_GetFSANodeByTag.restype  = c_int
        PathNo = self.library.GPF_GetFSANodeByTag(self.hHandle, tag.encode(), return_value, self.buf_max_size)
        return PathNo

    def AddUnit(self, colNo,text):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_AddUnit.argtypes = [c_void_p, c_int, c_char_p, c_char_p, c_int]
        self.library.GPF_AddUnit.restype  = c_int
        str_len = self.library.GPF_AddUnit(self.hHandle, colNo, text.encode(), return_value, self.buf_max_size)
        ret = string_at(return_value, str_len)
        return ret.decode()

    def AddUnitKV(self, unitNo, key,val):
        self.library.GPF_AddUnitKV.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
        self.library.GPF_AddUnitKV.restype  = c_int
        str_len = self.library.GPF_AddUnitKV(self.hHandle, unitNo.encode(), key.encode(), val.encode())
        return 1

    def AddGridKV(self, key,val):
        self.library.GPF_AddGridKV.argtypes = [c_void_p, c_char_p, c_char_p]
        self.library.GPF_AddGridKV.restype  = c_int
        self.library.GPF_AddGridKV(self.hHandle, key.encode(),val.encode())
        return 0
    
    def AddRelation(self, unitNo1, unitNo2, role):
        self.library.GPF_AddRelation.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
        self.library.GPF_AddRelation.restype  = c_int
        self.library.GPF_AddRelation(self.hHandle, unitNo1.encode(), unitNo2.encode(), role.encode())
        return 1

    def AddRelationKV(self, unitNo1, unitNo2, role, key, val):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_AddRelationKV.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, c_int]
        self.library.GPF_AddRelationKV.restype  = c_int
        str_len = self.library.GPF_AddRelationKV(self.hHandle, unitNo1.encode(), unitNo2.encode(), role.encode(), key.encode(), val.encode(), return_value, self.buf_max_size)
        ret = string_at(return_value, str_len)
        return ret.decode()

    def IsUnit(self, unitNo, kv):
        self.library.GPF_IsUnit.argtypes = [c_void_p, c_char_p, c_char_p]
        self.library.GPF_IsUnit.restype  = c_int
        ret = self.library.GPF_IsUnit(self.hHandle, unitNo.encode(), kv.encode())
        return ret

    def IsRelation(self, unitNo1, unitNo2, role, kv=""):
        self.library.GPF_IsRelation.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p, c_char_p]
        self.library.GPF_IsRelation.restype  = c_int
        ret = self.library.GPF_IsRelation(self.hHandle, unitNo1.encode(), unitNo2.encode(), role.encode(), kv.encode())
        return ret

    def IsTable(self, tableName, item="", kv=""):
        self.library.GPF_IsTable.argtypes = [c_void_p, c_char_p, c_char_p, c_char_p]
        self.library.GPF_IsTable.restype  = c_int
        ret = self.library.GPF_IsTable(self.hHandle, tableName.encode(), item.encode(), kv.encode())
        return ret

   
    def IndexFSA(self, rule_filename):
        self.library.GPF_MakeRule.argtypes = [c_char_p]
        self.library.GPF_MakeRule.restype  = c_int
        ret = self.library.GPF_MakeRule(rule_filename.encode())
        self.library.GPF_ReLoad.argtypes = [c_char_p]
        self.library.GPF_ReLoad.restype  = c_int
        self.library.GPF_ReLoad(self.Config.encode())
        return ret
    
    def Write2File(self, json_data,Idx2):
        RetInf=0
        Out=open(Idx2,"w",encoding="utf8")
        for Table in json_data:
            Items=self.GetTableItems(Table,"")
            for Item in Items:
                Colls=self.GetTableItemKVs(Table,Item,"Coll")
                for Coll in Colls:
                    CollItems=self.GetTableItemKVs(Table,Item,Coll)
                    if len(CollItems)>0:
                        self.WriteColl2File(Item,Coll,CollItems,Out)
                        RetInf=1
        Out.close()
        return RetInf

    def WriteColl2File(self, Item,Coll,CollItems,Out):
        Line="Table "+Coll+"_"+Item
        print(Line,file=Out)
        for Item in CollItems:
            print(Item,file=Out)
        
    def IndexTable(self, table_filename):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_MakeTable.argtypes = [c_char_p, c_char_p, c_int]
        self.library.GPF_MakeTable.restype  = c_int
        str_len = self.library.GPF_MakeTable(table_filename.encode(),return_value,self.buf_max_size)

        self.library.GPF_ReLoad.argtypes = [c_char_p]
        self.library.GPF_ReLoad.restype  = c_int
        self.library.GPF_ReLoad(self.Config.encode())
        if str_len != 0:
            str_ret = string_at(return_value, str_len)
            json_data = json.loads(str_ret.decode())
            Idx2=os.path.dirname(table_filename)+"/Coll_"+os.path.basename(table_filename)
            if self.Write2File(json_data,Idx2):
                self.IndexTable(Idx2)
            os.remove(Idx2)
            self.library.GPF_ReLoad.argtypes = [c_char_p]
            self.library.GPF_ReLoad.restype  = c_int
            self.library.GPF_ReLoad(self.Config.encode())
            return json_data
        return 0

    def GetLog(self):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_GetLog.argtypes = [c_void_p, c_char_p, c_int]
        self.library.GPF_GetLog.restype  = c_int
        str_len=self.library.GPF_GetLog(self.hHandle,return_value,self.buf_max_size)
        if str_len != 0:
            str_ret = string_at(return_value, str_len)
            json_data = json.loads(str_ret.decode())
            return json_data
        return ""

    def Reduce(self,From=0,To=-1,Head=-1):
        return_value = create_string_buffer(''.encode(), self.buf_max_size)
        self.library.GPF_Reduce.argtypes = [c_void_p, c_int,c_int,c_char_p, c_int]
        self.library.GPF_Reduce.restype  = c_int
        str_len=self.library.GPF_Reduce(self.hHandle,From,To,return_value,self.buf_max_size)
        HeadUnit=self.GetUnit(Head)
        self.library.GPF_SetHead.argtypes = [c_void_p, c_char_p, c_char_p]
        self.library.GPF_SetHead.restype  = c_int
        self.library.GPF_SetHead(self.hHandle,return_value,HeadUnit)
        ret = string_at(return_value, str_len)
        return ret.decode()
