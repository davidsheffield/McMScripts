Database
========

Schema
------

CREATE TABLE RequestSets(SetID INTEGER PRIMARY KEY, Process TEXT, RequesterID INTEGER, ContactID INTEGER, Tag INTEGER, Events INTEGER, Notes TEXT, Spreadsheet TEXT, RequestType INTEGER, RequestMultiplicity INTEGER, LHE_New INTEGER, LHE_Validating INTEGER, LHE_Validated INTEGER, LHE_Defined INTEGER, LHE_Approved INTEGER, LHE_Submitted INTEGER, LHE_Done INTEGER, GS_New INTEGER, GS_Validating INTEGER, GS_Validated INTEGER, GS_Defined INTEGER, GS_Approved INTEGER, GS_Submitted INTEGER, GS_Done INTEGER, DR_New INTEGER, DR_Validating INTEGER, DR_Validated INTEGER, DR_Defined INTEGER, DR_Approved INTEGER, DR_Submitted INTEGER, DR_Done INTEGER, MiniAOD_New INTEGER, MiniAOD_Validating INTEGER, MiniAOD_Validated INTEGER, MiniAOD_Defined INTEGER, MiniAOD_Approved INTEGER, MiniAOD_Submitted INTEGER, MiniAOD_Done INTEGER, MiniAODv2_New INTEGER, MiniAODv2_Validating INTEGER, MiniAODv2_Validated INTEGER, MiniAODv2_Defined INTEGER, MiniAODv2_Approved INTEGER, MiniAODv2_Submitted INTEGER, MiniAODv2_Done INTEGER, FOREIGN KEY(ContactID) REFERENCES Contacts(ContactID), FOREIGN KEY(RequesterID) REFERENCES Requesters(RequesterID), FOREIGN KEY(RequestType) REFERENCES RequestTypes(RequestType));
CREATE TABLE Contacts(ContactID INTEGER PRIMARY KEY, Name TEXT, Email TEXT, DisplayName TEXT, UserName TEXT);
CREATE TABLE Requesters(RequesterID INTEGER PRIMARY KEY, Name TEXT, Email TEXT);
