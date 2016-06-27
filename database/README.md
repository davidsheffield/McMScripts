Database
========

This is a database to track sets of requests in McM.

[View database model](database_model.svg)

Schema
------

```
CREATE TABLE RequestSets(
    SetID INTEGER PRIMARY KEY,
    Process TEXT,
    Tag TEXT,
    Events INTEGER,
    RequestMultiplicity INTEGER,
    Notes TEXT,
    Spreadsheet TEXT,
    Ticket TEXT);
CREATE TABLE Contacts(
    ContactID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Email TEXT,
    DisplayName TEXT NOT NULL,
    UserName TEXT);
CREATE TABLE Requesters(
    RequesterID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Email TEXT);
CREATE TABLE Instances(
    InstanceID INTEGER PRIMARY KEY,
    SetID INTEGER,
    CampaignChainID INTEGER,
    ContactID INTEGER,
    RequesterID INTEGER,
    PriorityBlock INTEGER,
    FOREIGN KEY(SetID) REFERENCES RequestSets(SetID),
    FOREIGN KEY(CampaignChainID) REFERENCES CampaignChains(CampaignChainID),
    FOREIGN KEY(ContactID) REFERENCES Contacts(ContactID),
    FOREIGN KEY(RequesterID) REFERENCES Requesters(RequesterID));
CREATE TABLE Requests(
    RequestsID INTEGER PRIMARY KEY,
    CampaignID INTEGER NOT NULL,
    New INTEGER NOT NULL,
    Validating INTEGER NOT NULL,
    Validated INTEGER NOT NULL,
    Defined INTEGER NOT NULL,
    Approved INTEGER NOT NULL,
    Submitted INTEGER NOT NULL,
    FOREIGN KEY(CampaignID) REFERENCES Campaigns(CampaignID));
CREATE TABLE Instance_Requests(
    InstanceID INTEGER NOT NULL,
    RequestsID INTEGER NOT NULL,
    PRIMARY KEY(InstanceID, RequestsID)
    FOREIGN KEY(InstanceID) REFERENCES Instances(InstanceID),
    FOREIGN KEY(RequestsID) REFERENCES Requests(RequestsID));
CREATE TABLE SuperCampaigns(
    SuperCampaignID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Active INTEGER NOT NULL);
CREATE TABLE CampaignChains(
    CampaignChainID INTEGER PRIMARY KEY,
    Name TEXT,
    SuperCampaignID INTEGER NOT NULL,
    FOREIGN KEY(SuperCampaignID) REFERENCES SuperCampaigns(SuperCampaignID));
CREATE TABLE Campaigns(
    CampaignID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Level INTEGER NOT NULL);
CREATE TABLE CampaignChain_Campaign(
    CampaignChainID INTEGER NOT NULL,
    CampaignID INTEGER NOT NULL,
    OrderInChain INTEGER NOT NULL,
    PRIMARY KEY(CampaignChainID, CampaignID),
    FOREIGN KEY(CampaignChainID) REFERENCES CampaignChains(CampaignChainID),
    FOREIGN KEY(CampaignID) REFERENCES Campaigns(CampaignID));
CREATE TABLE Settings(
    SettingID INTEGER PRIMARY KEY,
    Value TEXT,
    Description TEXT);
```
