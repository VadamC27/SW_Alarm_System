CREATE TABLE uzytkownicy (login TEXT PRIMARY KEY NOT NULL, 
                        haslo TEXT NOT NULL);

CREATE TABLE kody(login TEXT NOT NULL,
                  kod TEXT PRIMARY KEY NOT NULL,
                  typ TEXT,
                  FOREIGN KEY (login) REFERENCES uzytkownicy(login));

CREATE TABLE czujniki(id_czujnika INTEGER NOT NULL,
                      nazwa TEXT NULL);       

CREATE TABLE obserwowane_czujniki(login TEXT NOT NULL,
                                  id_czujnika INTEGER NOT NULL,
                                  FOREIGN KEY (login) REFERENCES uzytkownicy(login),
                                  FOREIGN KEY (id_czujnika) REFERENCES czujniki(id_czujnika));   

CREATE TABLE zarejestrowan_ruch (data TEXT NOT NULL, 
                                id_czujnika TEXT NOT NULL,
                                FOREIGN KEY (id_czujnika) REFERENCES czujniki(id_czujnika));

