################################
#
# requestClass.py
#
#  author: David G. Sheffield (Rutgers)
#
################################

class Request:
    """Class to store request information"""
    def __init__(self):
        """Initialize request with all fields set to false"""
        self.useDataSetName_        = False
        self.useMCDBID_             = False
        self.useCS_                 = False
        self.useEvts_               = False
        self.useFrag_               = False
        self.useMcMFrag_            = False
        self.useTime_               = False
        self.useSize_               = False
        self.useTag_                = False
        self.useGen_                = False
        self.useFiltEff_            = False
        self.useFiltEffErr_         = False
        self.useMatchEff_           = False
        self.useMatchEffErr_        = False
        self.usePWG_                = False
        self.useCamp_               = False
        self.usePrepId_             = False
        self.useSequencesCustomise_ = False
        self.useProcessString_      = False
        self.useJobID_              = False
        self.useNotes_              = False
        self.useMcMTag_             = False

    def setDataSetName(self,x):
        self.DataSetName_ = x
        self.useDataSetName_ = True
    def setMCDBID(self,x):
        self.MCDBID_ = x
        self.useMCDBID_ = True
    def setCS(self,x):
        self.CS_ = float(x)
        self.useCS_ = True
    def setEvts(self,x):
        self.Evts_ = int(x)
        self.useEvts_ = True
    def setFrag(self,x):
        self.Frag_ = x
        self.useFrag_ = True
    def setMcMFrag(self,x):
        self.McMFrag_ = x
        self.useMcMFrag_ = True
    def setTime(self,x):
        self.Time_ = float(x)
        self.useTime_ = True
    def setSize(self,x):
        self.Size_ = float(x)
        self.useSize_ = True
    def setTag(self,x):
        self.Tag_ = x
        self.useTag_ = True
    def setGen(self,x):
        self.Gen_ = x
        self.useGen_ = True
    def setFiltEff(self,x):
        self.FiltEff_ = float(x)
        self.useFiltEff_ = True
    def setFiltEffErr(self,x):
        self.FiltEffErr_ = float(x)
        self.useFiltEffErr_ = True
    def setMatchEff(self,x):
        self.MatchEff_ = float(x)
        self.useMatchEff_ = True
    def setMatchEffErr(self,x):
        self.MatchEffErr_ = float(x)
        self.useMatchEffErr_ = True
    def setPWG(self,x):
        self.PWG_ = x
        self.usePWG_ = True
    def setCamp(self,x):
        self.Camp_ = x
        self.useCamp_ = True
    def setPrepId(self,x):
        self.PrepId_ = x
        self.usePrepId_ = True
    def setSequencesCustomise(self,x):
        self.SequencesCustomise_ = x
        self.useSequencesCustomise_ = True
    def setProcessString(self,x):
        self.ProcessString_ = x
        self.useProcessString_ = True
    def setJobID(self,x):
        self.JobID_ = x
        self.useJobID_ = True
    def setNotes(self, x):
        self.Notes_ = x
        self.useNotes_ = True
    def setMcMTag(self, x):
        self.McMTag_ = x
        self.useMcMTag_ = True

    def getDataSetName(self):
        return self.DataSetName_
    def getMCDBID(self):
        return self.MCDBID_
    def getCS(self):
        return self.CS_
    def getEvts(self):
        return self.Evts_
    def getFrag(self):
        return self.Frag_
    def getMcMFrag(self):
        return self.McMFrag_
    def getTime(self):
        return self.Time_
    def getSize(self):
        return self.Size_
    def getTag(self):
        return self.Tag_
    def getGen(self):
        return self.Gen_
    def getFiltEff(self):
        return self.FiltEff_
    def getFiltEffErr(self):
        return self.FiltEffErr_
    def getMatchEff(self):
        return self.MatchEff_
    def getMatchEffErr(self):
        return self.MatchEffErr_
    def getPWG(self):
        return self.PWG_
    def getCamp(self):
        return self.Camp_
    def getPrepId(self):
        return self.PrepId_
    def getSequencesCustomise(self):
        return self.SequencesCustomise_
    def getProcessString(self):
        return self.ProcessString_
    def getJobID(self):
        return self.JobID_
    def getNotes(self):
        return self.Notes_
    def getMcMTag(self):
        return self.McMTag_

    def useDataSetName(self):
        return self.useDataSetName_
    def useMCDBID(self):
        return self.useMCDBID_
    def useCS(self):
        return self.useCS_
    def useEvts(self):
        return self.useEvts_
    def useFrag(self):
        return self.useFrag_
    def useMcMFrag(self):
        return self.useMcMFrag_
    def useTime(self):
        return self.useTime_
    def useSize(self):
        return self.useSize_
    def useTag(self):
        return self.useTag_
    def useGen(self):
        return self.useGen_
    def useFiltEff(self):
        return self.useFiltEff_
    def useFiltEffErr(self):
        return self.useFiltEffErr_
    def useMatchEff(self):
        return self.useMatchEff_
    def useMatchEffErr(self):
        return self.useMatchEffErr_
    def usePWG(self):
        return self.usePWG_
    def useCamp(self):
        return self.useCamp_
    def usePrepId(self):
        return self.usePrepId_
    def useSequencesCustomise(self):
        return self.useSequencesCustomise_
    def useProcessString(self):
        return self.useProcessString_
    def useJobID(self):
        return self.useJobID_
    def useNotes(self):
        return self.useNotes_
    def useMcMTag(self):
        return self.useMcMTag_
