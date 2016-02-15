Database
========

Schema
------

CREATE TABLE RequestSets(SetID INTEGER PRIMARY KEY, Process TEXT, RequesterID INTEGER, ContactID INTEGER, Tag INTEGER, Events INTEGER, Notes TEXT, RequestType INTEGER, GSNew INTEGER, GSValidating INTEGER, GSValidated INTEGER, GSDefined INTEGER, GSSubmitted INTEGER, GSDone INTEGER, FOREIGN KEY(ContactID) REFERENCES Contacts(ContactID), FOREIGN KEY(RequesterID) REFERENCES Requesters(RequesterID), FOREIGN KEY(RequestType) REFERENCES RequestTypes(RequestType));
