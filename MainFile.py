import csv
import os
import sys
from datetime import datetime
from PyQt6.QtCore import Qt, QDate, QUrl, QTimer
from PyQt6.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem, QApplication, QWidget, QDialog, QVBoxLayout
from PyQt6.QtGui import QPixmap, QAction
from PyQt6 import QtWidgets, uic, QtCore, QtGui

#Controle de saisie numero d'inscription
def saisirNumInscrip(ch):
    return ((len(ch)==8) and (ch.isdigit()))
#Controle de saisie nom
def saisirNom(ch):
    for i in ch:
        if (not(i.upper() in ["A","Z"])) or (i!=" "):
            return True
    return False
#Controle de saisie deux dates
def saisirDate(ch1,ch2):
    D1 = datetime.strptime(ch1, "%d/%m/%Y")
    D2 = datetime.strptime(ch2, "%d/%m/%Y")
    if D1<D2:
        return True
    else:
        return False
#Controle de saisie mail
def saisirMail(ch):
    return (ch.count("@")==1 and ch.find(".")!=-1)
    
#Controle de saisie numero de telephone
def saisirTel(ch):
    return ((len(ch)==8) and (ch.isdigit()) and (ch[0] in ["2","4","5","7","9"]))
#Controle de saisie référence
def saisirRef(ch):
    return (ch.isalnum())
#Controle de saisie année
def saisirAnnee(ch):
    return (len(ch)==4 and ch.isdigit() and (ch[0] in ["1","2"]))
#Controle de saisie du nombre d'exemplaires
def saisirNb(ch):
    return(ch.isdigit() and eval(ch)>0)
def existe(d,x):
    for k in d.keys():
        if k==x:
            return True
    return False
#Emprunt existe ou non, x est le NumInscrip et y la Ref du livre
def existemp(d,x,y):
    for cle,val in d.items():
        if cle==x and val[0]==y:
            return True 
    return False
#Enregistrement
def enregistrementEtud():
    etudiant=Etudiant
    f=open('Etudiants.csv', 'w',newline='')
    writer = csv.writer(f, delimiter=';')
    writer.writerow(["NumInscrip","Nom","Prenom","DateNiss","Adresse","Mail","Tel","Section","Niveau"])
    for cle,val in etudiant.items():
        ch=[cle]+val
        writer.writerow(ch)
        
def enregistrementLivre():
    f=open('Livres.csv', 'w',newline='')
    writer = csv.writer(f, delimiter=';')
    writer.writerow(["Ref","Titre","Auteur","Annee","NbExp"])
    for cle,val in Livre.items():
        ch=[cle]+val
        writer.writerow(ch)
        
def enregistrementEmprunt():
    f=open('Emprunts.csv', 'w',newline='')
    writer = csv.writer(f, delimiter=';')
    writer.writerow(["NumInscrip","Ref","DateEmprunt","DateRetour","Retourné"])
    for cle,val in Emprunt.items():
        ch=[cle]+val
        writer.writerow(ch)
#Recuperation des étudiants
def recupEtud():
    global Etudiant
    dic={}
    with open('Etudiants.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        next (csv_reader)
        for row in csv_reader:
            dic[row[0]]=row[1:]
    Etudiant=dic
#Recuperation des livres
def recupLivres():
    global Livre
    dic={}
    with open('Livres.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        next (csv_reader)
        for row in csv_reader:
            dic[row[0]]=row[1:]
    Livre=dic
#Recuperation des emprunts
def recupEmprunts():
    global Emprunt
    dic={}
    with open('Emprunts.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        next (csv_reader)
        for row in csv_reader:
            dic[row[0]]=row[1:]
    Emprunt=dic
#DialogEnreg
def open_dialog_enreg(wind):
    dialogE = DialogEnreg(wind)
    dialogE.exec()
#DialogRecup
def open_dialog_recup():
    dialogR = DialogRecup()
    dialogR.exec()
#Info
def open_Info():
    Inf = Info()
    Inf.exec()

class Info(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        uic.loadUi('Info.ui', self)
        self.setWindowOpacity(1.0)
class DialogRecup(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        uic.loadUi('DialogRecup.ui', self)
        self.Recuperer = self.findChild(QtWidgets.QPushButton, 'Recuperer')
        self.Recuperer.clicked.connect(self.Recuper)
        self.Ignorer  = self.findChild(QtWidgets.QPushButton, 'Ignorer')
        self.Ignorer.clicked.connect(self.close)
        self.setWindowOpacity(1.0)
    def Recuper(self):
        recupEtud()
        recupLivres()
        recupEmprunts()
        self.close()
        QMessageBox.information(None, "Succés", "Fichiers récupérés avec succés")
    def closeEvent(self,event):
        window1.setEnabled(True)
    
class DialogEnreg(QtWidgets.QDialog):
    def __init__(self, wind):
        global window1
        super().__init__()
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        uic.loadUi('DialogEnreg.ui', self)
        self.setWindowOpacity(1.0)
        self.Enregistrer = self.findChild(QtWidgets.QPushButton, 'Enregistrer')
        self.Enregistrer.clicked.connect(lambda: self.Enreg(wind))
        self.Quitter = self.findChild(QtWidgets.QPushButton, 'Quitter')
        self.Quitter.clicked.connect(lambda: self.Quitt(wind))
    def Quitt(self,wind):
        global window1
        self.accept()
        if wind!=window1:
            window1.close()
        wind.close()
    def Enreg(self,wind):
        global window1
        enregistrementEtud()
        enregistrementLivre()
        enregistrementEmprunt()
        QMessageBox.information(None, "Succés", "Modfications enregistrées avec succés.\nA bientôt!")
        if wind!=window1:
            window1.close()
        wind.close()
        self.accept()
        
class Accueil(QtWidgets.QMainWindow):
    def __init__(self):
        global Modification
        super().__init__()
        uic.loadUi('Accueil.ui', self)
        
        self.AjoutEtudBut = self.findChild(QtWidgets.QPushButton, 'AjoutEtudBut')
        self.AjoutEtudBut.clicked.connect(self.open_AjouterEtudiant)
        
        self.AjoutLivreBut = self.findChild(QtWidgets.QPushButton, 'AjoutLivreBut')
        self.AjoutLivreBut.clicked.connect(self.open_AjouterLivre)
        
        self.AjoutEmpruntBut = self.findChild(QtWidgets.QPushButton, 'AjoutEmpruntBut')
        self.AjoutEmpruntBut.clicked.connect(self.open_AjouterEmprunt)
        
        self.ModifEtudBut = self.findChild(QtWidgets.QPushButton, 'ModifierEtudBut')
        self.ModifEtudBut.clicked.connect(self.open_ModifierEtudiant)
        
        self.ModifLivreBut = self.findChild(QtWidgets.QPushButton, 'ModifLivreBut')
        self.ModifLivreBut.clicked.connect(self.open_ModifierLivre)

        self.RetourEmpruntBut = self.findChild(QtWidgets.QPushButton, 'RetourEmpruntBut')
        self.RetourEmpruntBut.clicked.connect(self.open_RetourEmprunt)
        
        self.SuppEtudBut = self.findChild(QtWidgets.QPushButton, 'SuppEtudBut')
        self.SuppEtudBut.clicked.connect(self.open_SupprimerEtudiant)

        self.SuppLivreBut = self.findChild(QtWidgets.QPushButton, 'SuppLivreBut')
        self.SuppLivreBut.clicked.connect(self.open_SupprimerLivre)
        
        self.ModifEmpruntBut = self.findChild(QtWidgets.QPushButton, 'ModifEmpruntBut')
        self.ModifEmpruntBut.clicked.connect(self.open_ModifierEmprunt)
        
        self.RechEtudBut = self.findChild(QtWidgets.QPushButton, 'RechEtudBut')
        self.RechEtudBut.clicked.connect(self.open_RechercherEtudiant)
        
        self.RechLivreBut = self.findChild(QtWidgets.QPushButton, 'RechLivreBut')
        self.RechLivreBut.clicked.connect(self.open_RechercherLivre)
        
        self.RechEmpruntBut = self.findChild(QtWidgets.QPushButton, 'RechEmpruntBut')
        self.RechEmpruntBut.clicked.connect(self.open_RechercherEmprunt)
        
        self.Enregistrer = self.findChild(QtWidgets.QPushButton, 'Enregistrer')
        self.Enregistrer.clicked.connect(self.Eng)
        
        self.Recuperer = self.findChild(QtWidgets.QPushButton, 'Recuperer')
        self.Recuperer.clicked.connect(self.Recuper)
        
        self.Fermer = self.findChild(QtWidgets.QPushButton, 'Fermer')
        self.Fermer.clicked.connect(lambda: open_dialog_enreg(self))
        
        self.Info = self.findChild(QtWidgets.QPushButton, 'Info')
        self.Info.clicked.connect(open_Info)
        
    def Recuper(self):
        recupEmprunts()
        recupLivres()
        recupEtud()
        QMessageBox.information(None,"Success","Données récupérés avec succés")
    def Eng(self):
        global Modification,Etudiant,Livre,Emprunt
        if Modification==1:
            self.Enregistrer.clicked.connect(enregistrementEtud)
            self.Enregistrer.clicked.connect(enregistrementEmprunt)
            self.Enregistrer.clicked.connect(enregistrementLivre)
            QMessageBox.information(None,"Success","Modifications enregistrées avec succés")
        if Etudiant=={} and Emprunt=={} and Livre=={}:
            QMessageBox.critical(None,"Attention","Attention! les fichiers ne sont pas récupérés.\nL'enregistrement n'est pas autorisé pour ne pas perdre les données.\nVeuillez cliquer sur le bouton Récupérer.")            

    def open_AjouterEtudiant(self):
        self.AjouterEtudiant = AjouterEtudiant()
        self.AjouterEtudiant.showFullScreen()
        
    def open_AjouterLivre(self):
        self.AjouterLivre = AjouterLivre()
        self.AjouterLivre.showFullScreen()
        
    def open_AjouterEmprunt(self):
        self.AjouterEmprunt = AjouterEmprunt()
        self.AjouterEmprunt.showFullScreen()
        
    def open_ModifierEtudiant(self):
        self.ModifierEtudiant = ModifierEtudiant()
        self.ModifierEtudiant.showFullScreen()
        
    def open_ModifierLivre(self):
        self.ModifierLivre = ModifierLivre()
        self.ModifierLivre.showFullScreen()
        
    def open_RetourEmprunt(self):
        self.RetourEmprunt = RetourEmprunt()
        self.RetourEmprunt.showFullScreen()
        
    def open_SupprimerEtudiant(self):
        self.SupprimerEtudiant = SupprimerEtudiant()
        self.SupprimerEtudiant.showFullScreen()
        
    def open_SupprimerLivre(self):
        self.SupprimerLivre = SupprimerLivre()
        self.SupprimerLivre.showFullScreen()
        
    def open_ModifierEmprunt(self):
        self.ModifierEmprunt = ModifierEmprunt()
        self.ModifierEmprunt.showFullScreen()
        
    def open_RechercherEtudiant(self):
        self.RechercherEtudiant = RechercherEtudiant()
        self.RechercherEtudiant.showFullScreen()
        
    def open_RechercherLivre(self):
        self.RechercherLivre = RechercherLivre()
        self.RechercherLivre.showFullScreen()
        
    def open_RechercherEmprunt(self):
        self.RechercherEmprunt = RechercherEmprunt()
        self.RechercherEmprunt.showFullScreen()
        
        
class AjouterEtudiant(QtWidgets.QMainWindow):
    def __init__(self):
        global window1
        global Modification
        super().__init__()
        uic.loadUi('AjouterEtudiant.ui', self)
        
        self.Ajouter = self.findChild(QtWidgets.QPushButton, 'Ajouter')
        self.Ajouter.clicked.connect(self.ajouterEtudAction)
        
        self.Return = self.findChild(QtWidgets.QPushButton, 'Return')
        self.Return.clicked.connect(self.close)
        
        self.Fermer = self.findChild(QtWidgets.QPushButton, 'Fermer')
        self.Fermer.clicked.connect(lambda: open_dialog_enreg(self))
        
    #Fonction Ajouter Etudiant
    def ajouterEtudAction(self):
        global Modification
        global window1
        global Etudiant
        while True:
            err=0
            #Numéro d'inscription
            NumInscrip=self.EdNumInscrip.text()
            self.ErrNumInscrip.setText("")
            if not (saisirNumInscrip(NumInscrip)):
                self.ErrNumInscrip.setText("Numéro d'inscription invalide, doit être composé de 8 chiffres.")
                err=1
            elif (existe(Etudiant,NumInscrip)):
                QMessageBox.critical(None, "Erreur d'ajout", "Cet étudiant existe déja")
                err=1
    
            #Nom étudiant
            Nom=self.EdNomEtud.text()
            self.ErrNomEtud.setText("")
            if not (saisirNom(Nom)):
                #self.EdNomEtud.setText("")
                self.ErrNomEtud.setText("Nom invalide.")
                err=1
        
            #Prenom étudiant
            Prenom=self.EdPrenomEtud.text()
            self.ErrPrenomEtud.setText("")
            if not (saisirNom(Prenom)):
                #self.EdPrenomEtud.setText("")
                self.ErrPrenomEtud.setText("Prenom invalide.")
                err=1

            DateNiss=self.EdDateNiss.text()
            Adresse=self.EdAdresse.text()

            #Mail
            Mail=self.EdMail.text()
            self.ErrMail.setText("")
            if not (saisirMail(Mail)):
                #self.EdMail.setText("")
                self.ErrMail.setText("Mail invalide.")
                err=1
    
            #Numero de téléphone
            Tel=self.EdTel.text()
            self.ErrTel.setText("")
            if not (saisirTel(Tel)):
                #self.EdTel.setText("")
                self.ErrTel.setText("Numéro invalide.")
                err=1
            #Section
            Section=self.EdSection.currentText()
            Niveau=self.EdNiveau.currentText()
            self.ErrSection.setText("")
            if (Section=="--Choisir Section--")and(Niveau=="--Choisir Niveau--"):
                self.ErrSection.setText("Verifier la section et le niveau.")
                err=1
            elif (Section=="--Choisir Section--"):
                self.ErrSection.setText("Verifier la section.")
                err=1
            elif (Niveau=="--Choisir Niveau--"):
                self.ErrSection.setText("Verifier le niveau.")
                err=1
                
            if err==0:
                self.Success.setText("Etudiant ajouté avec succés")
                self.EdNumInscrip.setText("")
                self.EdNomEtud.setText("")
                self.EdPrenomEtud.setText("")
                self.EdMail.setText("")
                self.EdNiveau.setCurrentIndex(0)
                self.EdAdresse.setText("")
                self.EdDateNiss.setDate(QDate(2000,1,1))
                self.EdSection.setCurrentIndex(0)
                self.EdTel.setText("")
                Etudiant[NumInscrip]=[Nom,Prenom,DateNiss,Adresse,Mail,Tel,Section,Niveau]
                Modification=1
            break
        
class AjouterLivre(QtWidgets.QMainWindow):
    def __init__(self):
        global window1
        global Modification
        super().__init__()
        uic.loadUi('AjouterLivre.ui', self)
        
        self.Ajouter = self.findChild(QtWidgets.QPushButton, 'Ajouter')
        self.Ajouter.clicked.connect(self.ajouterLivreAction)
        
        self.Return = self.findChild(QtWidgets.QPushButton, 'Return')
        self.Return.clicked.connect(self.close)
        
        self.Fermer = self.findChild(QtWidgets.QPushButton, 'Fermer')
        self.Fermer.clicked.connect(lambda: open_dialog_enreg(self))
        
    #Fonction Ajouter Livre
    def ajouterLivreAction(self):
        global Modification
        global Livre
        while True:
            err=0
            #Référence
            Ref=self.EdRef.text()
            self.ErrRef.setText("")
            if not (saisirRef(Ref)):
                self.ErrRef.setText("Référence invalide.")
                err=1
            elif (existe(Livre,Ref)):
                QMessageBox.critical(None, "Erreur d'ajout", "Ce Livre existe déja")
                err=1
    
            #Titre
            Titre=self.EdTitre.text()        
            #Auteur
            Auteur=self.EdAuteur.text()
            self.ErrAuteur.setText("")
            if not (saisirNom(Auteur)):
                self.ErrAuteur.setText("Nom auteur invalide.")
                err=1

            #Année d'édition
            Annee=self.EdAnneeEdit.text()
            self.ErrAnneeEdit.setText("")
            if not (saisirAnnee(Annee)):
                self.ErrAnneeEdit.setText("Année invalide.")
                err=1
    
            #Nombre d'exemplaires
            NbExp=self.EdNbExp.text()
            self.ErrNbExp.setText("")
            if not (saisirNb(NbExp)):
                self.ErrNbExp.setText("Nombre d'examplaires invalide.")
                err=1
    
            if err==0:
                Livre[Ref]=[Titre,Auteur,Annee,NbExp]
                self.Success.setText("Livre ajouté avec succés")
                self.EdAnneeEdit.setText("")
                self.EdAuteur.setText("")
                self.EdNbExp.setText("")
                self.EdRef.setText("")
                self.EdTitre.setText("")
                Modification=1
            break

class AjouterEmprunt(QtWidgets.QMainWindow):
    def __init__(self):
        global window1
        global Modification
        super().__init__()
        uic.loadUi('AjouterEmprunt.ui', self)
        
        self.Ajouter = self.findChild(QtWidgets.QPushButton, 'Ajouter')
        self.Ajouter.clicked.connect(self.ajouterEmpruntAction)
        
        self.Return = self.findChild(QtWidgets.QPushButton, 'Return')
        self.Return.clicked.connect(self.close)
        
        self.Fermer = self.findChild(QtWidgets.QPushButton, 'Fermer')
        self.Fermer.clicked.connect(lambda: open_dialog_enreg(self))
        
    def ajouterEmpruntAction(self):
        global Modification
        global Emprunt
        while True:
            Retourne="Non"
            msg=""
            err=0
            #Numéro d'inscription
            NumInscrip=self.EdNumInscrip.text()
            self.ErrNumInscrip.setText("")
            if not (saisirNumInscrip(NumInscrip)):
                self.ErrNumInscrip.setText("Numéro d'inscription invalide, doit être composé de 8 chiffres.")
                err=1
            if not existe(Etudiant,NumInscrip):
                msg+="Etudiant n'existe pas. \n"
                
            #Référence
            Ref=self.EdRef.text()
            self.ErrRef.setText("")
            if not (saisirRef(Ref)):
                self.ErrRef.setText("Référence invalide.")
                err=1
            if not existe(Livre,Ref):
                msg+="Livre n'existe pas. \n"
            if (existemp(Emprunt,NumInscrip,Ref)):
                msg="Emprunt existe déja"
            #Dates emprunt et retour
            DateEmprunt=self.EdDateEmprunt.text()
            DateRetour=self.EdDateRetour.text()
            self.ErrDate.setText("")
            if not (saisirDate(DateEmprunt,DateRetour)):
                self.ErrDate.setText("Vérifiez les dates.")
                err=1
    
            if err==0:
                if msg!="":
                    QMessageBox.critical(None,"Erreur",msg)
                else:
                    Emprunt[NumInscrip]=[Ref,DateEmprunt,DateRetour,Retourne]
                    self.Success.setText("Emprunt ajouté avec succés")
                    self.EdNumInscrip.setText("")
                    self.EdRef.setText("")
                    self.EdDateEmprunt.setDate(QDate(2023,1,1))
                    self.EdDateRetour.setDate(QDate(2023,1,1))
                    Modification=1
            break
        
class ModifierLivre(QtWidgets.QMainWindow):
    def __init__(self):
        global window1
        global Modification
        super().__init__()
        uic.loadUi('ModifierLivre.ui', self)
        
        self.Return = self.findChild(QtWidgets.QPushButton, 'Return')
        self.Return.clicked.connect(self.close)
        
        self.Fermer = self.findChild(QtWidgets.QPushButton, 'Fermer')
        self.Fermer.clicked.connect(lambda: open_dialog_enreg(self))
        
        self.Modifier = self.findChild(QtWidgets.QPushButton, 'Modifier')
        self.Modifier.clicked.connect(self.modifLivreAction)
        
    def modifLivreAction(self):
        global Modification
        global Livre
        while True:
            err,modif=0,0
            Ref=self.EdRef.text()
            self.ErrRef.setText("")
            if not (saisirRef(Ref)):
                self.ErrRef.setText("Référence invalide.")
                err=1
            elif not (existe(Livre,Ref)):
                QMessageBox.critical(None, "Erreur", "Ce livre n'existe pas.")
                err=1
            for cle,val in Livre.items():
                if cle==Ref:
                    Titre=val[0]
                    Auteur=val[1]
                    NbExp=val[3]
            NbExpN=self.EdNbExp.text()
            self.ErrNbExp.setText("")
            if NbExpN!="" and not (saisirNb(NbExpN)):
                self.ErrNbExp.setText("Nombre d'exemplaires invalide.")
                err=1
            elif NbExpN!="":
                NbExp=NbExpN
                modif=1
            if err==0:
                Livre[Ref][3]=NbExp
                self.Affichage.setText(" "+Titre+" \n "+Auteur+" \n "+NbExp)
                if modif:
                    self.Success.setText("Nombre d'exemplaires modifié avec succés.")
                    Modification=1
            break
        
class RetourEmprunt(QtWidgets.QMainWindow):
    def __init__(self):
        global window1
        global Modification
        super().__init__()
        uic.loadUi('RetourEmprunt.ui', self)
        
        self.Return = self.findChild(QtWidgets.QPushButton, 'Return')
        self.Return.clicked.connect(self.close)
        
        self.Fermer = self.findChild(QtWidgets.QPushButton, 'Fermer')
        self.Fermer.clicked.connect(lambda: open_dialog_enreg(self))
        
        self.Supprimer = self.findChild(QtWidgets.QPushButton, 'Supprimer')
        self.Supprimer.clicked.connect(self.suppEmpruntAction)
        
        self.Retourner = self.findChild(QtWidgets.QPushButton, 'Retourner')
        self.Retourner.clicked.connect(self.retourEmpruntAction)
        
    #Fonction retourner Emprunt:
    def retourEmpruntAction(self):
        global Modification
        global Emprunt
        while True:
            msg=""
            err=0
            #Numéro d'inscription
            NumInscrip=self.EdNumInscrip.text()
            self.ErrNumInscrip.setText("")
            if not (saisirNumInscrip(NumInscrip)):
                self.ErrNumInscrip.setText("Numéro d'inscription invalide, doit être composé de 8 chiffres.")
                err=1
            elif not existe(Etudiant,NumInscrip):
                msg+="Etudiant n'existe pas. \n"
                
            #Référence
            Ref=self.EdRef.text()
            self.ErrRef.setText("")
            if not (saisirRef(Ref)):
                self.ErrRef.setText("Référence invalide.")
                err=1
            elif not existe(Livre,Ref):
                msg+="Livre n'existe pas. \n"
            if msg=="" and not(existemp(Emprunt,NumInscrip,Ref)):
                msg="Emprunt n'existe pas"
    
            if err==0:
                if msg!="":
                    QMessageBox.critical(None,"Erreur",msg)
                else:
                    for key,val in Emprunt.items():
                        if key==NumInscrip and val[0]==Ref:
                            message="Emprunt du livre "+Livre[val[0]][0]+" de l'étudiant "+Etudiant[key][0]+" "+Etudiant[key][1]+" retourné avec succés\n"
                            val[3]="Oui"
                    QMessageBox.information(None,"Succés",message)
                    self.EdNumInscrip.setText("")
                    self.EdRef.setText("")
                    Modification=1
            break
    #Fonction Supprimer Emprunt
    def suppEmpruntAction(self):
        global Emprunt
        global Livre
        global Etudiant
        global Modification
        while True:
            msg=""
            err=0
            #Numéro d'inscription
            NumInscrip=self.EdNumInscrip.text()
            self.ErrNumInscrip.setText("")
            if not (saisirNumInscrip(NumInscrip)):
                self.ErrNumInscrip.setText("Numéro d'inscription invalide, doit être composé de 8 chiffres.")
                err=1
            elif not existe(Etudiant,NumInscrip):
                msg+="Etudiant n'existe pas. \n"
                
            #Référence
            Ref=self.EdRef.text()
            self.ErrRef.setText("")
            if not (saisirRef(Ref)):
                self.ErrRef.setText("Référence invalide.")
                err=1
            elif not existe(Livre,Ref):
                msg+="Livre n'existe pas. \n"
            if msg=="" and not(existemp(Emprunt,NumInscrip,Ref)):
                msg="Emprunt n'existe pas"
    
            if err==0:
                if msg!="":
                    QMessageBox.critical(None,"Erreur",msg)
                else:
                    emp={}
                    for key,val in Emprunt.items():
                        if key==NumInscrip and val[0]==Ref:
                            message="Emprunt du livre "+Livre[val[0]][0]+" de l'étudiant "+Etudiant[key][0]+" "+Etudiant[key][1]+" supprimé avec succés\n"
                            continue
                        emp[key]=val
                    Emprunt=emp
                    QMessageBox.information(None,"Succés",message)
                    self.EdNumInscrip.setText("")
                    self.EdRef.setText("")
                    Modification=1
            break
        
class ModifierEtudiant(QtWidgets.QMainWindow):
    def __init__(self):
        global window1
        global Modification
        super().__init__()
        uic.loadUi('ModifierEtudiant.ui', self)
        
        self.Return = self.findChild(QtWidgets.QPushButton, 'Return')
        self.Return.clicked.connect(self.close)
        
        self.Fermer = self.findChild(QtWidgets.QPushButton, 'Fermer')
        self.Fermer.clicked.connect(lambda: open_dialog_enreg(self))
        
        self.Modifier = self.findChild(QtWidgets.QPushButton, 'Modifier')
        self.Modifier.clicked.connect(self.modifEtudAction)
        
    def modifEtudAction(self):
        global Modification
        global Etudiant
        while True:
            msg=""
            err,nb,nberr=0,0,0
            NumInscrip=self.EdNumInscrip.text()
            self.ErrNumInscrip.setText("")
            if not (saisirNumInscrip(NumInscrip)):
                self.ErrNumInscrip.setText("Numéro d'inscription invalide, doit être composé de 8 chiffres.")
                err=1
            elif not (existe(Etudiant,NumInscrip)):
                QMessageBox.critical(None, "Erreur", "Cet étudiant n'existe pas.")
                err=1
            for cle,val in Etudiant.items():
                    if cle==NumInscrip:
                        Nom=val[0]
                        Prenom=val[1]
                        Section=val[6]
                        Niveau=val[7]
                        Adresse=val[3]
                        Mail=val[4]
                        Tel=val[5]
            NAdresse=self.EdAdresse.text()
            NMail=self.EdMail.text()
            NTel=self.EdTel.text()
            if NAdresse!="":
                Adresse=NAdresse
                nb+=1
            if NMail!="":
                if not saisirMail(NMail):
                    msg="Mail invalide."
                    nberr+=1
                else:
                    Mail=NMail
                    nb+=1
            if NTel!="":
                if not saisirTel(NTel):
                    msg="Numéro de téléphone invalide."
                    nberr+=1
                else:
                    Tel=NTel
                    nb+=1
            if nberr==2:
                msg="Mail et numéro de téléphone invalides."
            self.Err.setText(msg)
            if err==0:
                Etudiant[NumInscrip][3]=Adresse
                Etudiant[NumInscrip][4]=Mail
                Etudiant[NumInscrip][5]=Tel
                self.Affichage.setText(Nom+"\n"+Prenom+"\n"+Section+"\n"+Niveau+"\n"+Adresse+"\n"+Mail+"\n"+Tel)
                if nb!=0:
                    self.Success.setText("Etudiant Modifié avec succés")
                    self.EdAdresse.setText("")
                    self.EdMail.setText("")
                    self.EdTel.setText("")
                    Modification=1
            break
        
class SupprimerEtudiant(QtWidgets.QMainWindow):
    def __init__(self):
        global window1
        global Modification
        super().__init__()
        uic.loadUi('SupprimerEtudiant.ui', self)
        
        self.Return = self.findChild(QtWidgets.QPushButton, 'Return')
        self.Return.clicked.connect(self.close)
        
        self.Fermer = self.findChild(QtWidgets.QPushButton, 'Fermer')
        if Modification==1:
            self.self.Fermer.clicked.connect(lambda: open_dialog_enreg(self)).clicked.connect(lambda: open_dialog_enreg(self))
        else:
            self.Fermer.clicked.connect(self.close)
            self.Fermer.clicked.connect(window1.close)
        
        self.Supprimer = self.findChild(QtWidgets.QPushButton, 'Supprimer')
        self.Supprimer.clicked.connect(self.suppEtudAction)
        
    #Fonction Supprimer Etudiant
    def suppEtudAction(self):
        global Modification
        global Etudiant
        NumInscrip,Section,Niveau="","",""
        while True:
            etudiant=Etudiant
            err,nb=0,0
            a,b,c=0,0,0 #Des variables octales représantant les indices des champs
            #Numéro d'inscription
            NumInscrip=self.EdNumInscrip.text()
            Section=self.EdSection.currentText()
            Niveau=self.EdNiveau.currentText()
            if NumInscrip!="":
                nb+=1
                a=4 
            if Section!="--Choisir Section--":
                nb+=1
                b=2
            if Niveau!="--Choisir Niveau--":
                nb+=1
                c=1
            if nb==0:
                QMessageBox.critical(None, "Erreur", "Veuillez remplir au moins un champ.")
                err=1
            self.ErrNumInscrip.setText("")
            if NumInscrip!="" and not (saisirNumInscrip(NumInscrip)):
                self.ErrNumInscrip.setText("Numéro d'inscription invalide, doit être composé de 8 chiffres.")
                err=1
            elif NumInscrip!="" and not (existe(Etudiant,NumInscrip)):
                QMessageBox.critical(None, "Erreur", "Cet étudiant n'existe pas.")
                err=1
                
            if err==0:
                message=""
                msg=0
                s=a+b+c
                if nb==1:
                    if s==4:
                        message+=etudiant[NumInscrip][0]+" "+etudiant[NumInscrip][1]+"\n"
                        etudiant.pop(NumInscrip)
                    if s==2:
                        etud={}
                        for key,val in etudiant.items():
                            if val[6]==Section:
                                message+=etudiant[key][0]+" "+etudiant[key][1]+"\n"
                                continue
                            etud[key]=val
                        etudiant=etud
                    if s==1:
                        etud={}
                        for key,val in etudiant.items():
                            if val[7]==Niveau:
                                message+=etudiant[key][0]+" "+etudiant[key][1]+"\n"
                                continue
                            etud[key]=val
                        etudiant=etud
                if nb==2:
                    if s==6: #s=6 si a=4 et b=2: càd lorsque les champs numInscrip et Section sont non vides
                        if etudiant[NumInscrip][6]!=Section:
                            msg=1
                        else:
                            message+=etudiant[NumInscrip][0]+" "+etudiant[NumInscrip][1]+"\n"
                            etudiant.pop(NumInscrip)
                    if s==5:
                        if etudiant[NumInscrip][7]!=Niveau:
                            msg=1
                        else:
                            message+=etudiant[NumInscrip][0]+" "+etudiant[NumInscrip][1]+"\n"
                            etudiant.pop(NumInscrip)
                    if s==3:
                        test=0
                        for key,val in etudiant.items():
                            if val[7]==Niveau and val[6]==Section:
                                message+=etudiant[key][0]+" "+etudiant[key][1]+"\n"
                                test+=1
                                continue
                            etud[key]=val
                        if test==0:
                            msg=1
                        else:
                            etudiant=etud
                if nb==3:
                    if etudiant[NumInscrip][7]!=Niveau or etudiant[NumInscrip][6]!=Section:
                        msg=1
                    else:
                        message+=etudiant[NumInscrip][0]+" "+etudiant[NumInscrip][1]+"\n"
                        etudiant.pop(NumInscrip)
                if msg==1:
                    QMessageBox.critical(None,"Coordonnées ne correspondent pas","Verifier les coordonnées.")
                else:
                    if message=="":
                        QMessageBox.critical(None,"Erreur","N'existe pas")
                    else:
                        Etudiant=etudiant
                        self.Success.setText("Etudiants supprimés avec succés")
                        QMessageBox.information(None,"Etudiants supprimés",message)
                        self.EdNumInscrip.setText("")
                        self.EdSection.setCurrentIndex(0)
                        self.EdNiveau.setCurrentIndex(0)
                        Modification=1
            break
        
class SupprimerLivre(QtWidgets.QMainWindow):
    def __init__(self):
        global window1
        global Modification
        super().__init__()
        uic.loadUi('SupprimerLivre.ui', self)
        
        self.Return = self.findChild(QtWidgets.QPushButton, 'Return')
        self.Return.clicked.connect(self.close)
        
        self.Fermer = self.findChild(QtWidgets.QPushButton, 'Fermer')
        self.Fermer.clicked.connect(lambda: open_dialog_enreg(self))
        
        self.Supprimer = self.findChild(QtWidgets.QPushButton, 'Supprimer')
        self.Supprimer.clicked.connect(self.suppLivreAction)
        
    #Fonction Supprimer Livre
    def suppLivreAction(self):
        global Modification
        global Livre
        Ref,Auteur,Annee="","",""
        while True:
            livre=Livre
            err,nb=0,0
            a,b,c=0,0,0 #Des variables octales représantant les indices des champs
            #Reference
            Ref=self.EdRef.text()
            Auteur=self.EdAuteur.text()
            Annee=self.EdAnnee.text()
            if Ref!="":
                nb+=1
                a=4 
            if Auteur!="":
                nb+=1
                b=2
            if Annee!="":
                nb+=1
                c=1
            if nb==0:
                QMessageBox.critical(None, "Erreur", "Veuillez remplir au moins un champ.")
                err=1
            self.ErrRef.setText("")
            if Ref!="" and not (saisirRef(Ref)):
                self.ErrRef.setText("Référence invalide.")
                err=1
            elif Ref!="" and not (existe(Livre,Ref)):
                QMessageBox.critical(None, "Erreur", "Ce livre n'existe pas.")
                err=1
            #Auteur
            self.ErrAuteur.setText("")
            if Auteur!="" and not saisirNom(Auteur):
                self.ErrAuteur.setText("Verifier l'auteur.")
                err=1
            #Niveau
            self.ErrAnnee.setText("")
            if Annee!="" and not saisirAnnee(Annee):
                self.ErrAnnee.setText("Verifier l'année d'édition.")
                err=1
                
            if err==0:
                message=""
                msg=0
                s=a+b+c
                if nb==1:
                    if s==4:
                        message+=livre[Ref][0]+" de l'auteur "+livre[Ref][1]+"\n"
                        livre.pop(Ref)
                    if s==2:
                        liv={}
                        for key,val in livre.items():
                            if val[1]==Auteur:
                                message+=livre[key][0]+" de l'auteur "+livre[key][1]+"\n"
                                continue
                            liv[key]=val
                        livre=liv
                    if s==1:
                        liv={}
                        for key,val in livre.items():
                            if val[2]==Annee:
                                message+=livre[key][0]+" de l'auteur "+livre[key][1]+"\n"
                                continue
                            liv[key]=val
                        livre=liv
                if nb==2:
                    if s==6: #s=6 si a=4 et b=2: càd lorsque les champs numInscrip et Section sont non vides
                        if livre[Ref][1]!=Auteur:
                            msg=1
                        else:
                            message+=livre[Ref][0]+" de l'auteur "+livre[Ref][1]+"\n"
                            livre.pop(Ref)
                    if s==5:
                        if livre[Ref][2]!=Annee:
                            msg=1
                        else:
                            message+=livre[Ref][0]+" de l'auteur "+livre[Ref][1]+"\n"
                            livre.pop(Ref)
                    if s==3:
                        liv={}
                        test=0
                        for key,val in livre.items():
                            if val[2]==Annee and val[1]==Auteur:
                                message+=livre[key][0]+" de l'auteur "+livre[key][1]+"\n"
                                test+=1
                                continue
                            liv[key]=val
                        if test==0:
                            msg=1
                        else:
                            livre=liv
                if nb==3:
                    if livre[Ref][2]!=Annee or livre[Ref][1]!=Auteur:
                        msg=1
                    else:
                        message+=livre[Ref][0]+" de l'auteur "+livre[Ref][1]+"\n"
                        livre.pop(Ref)
                if msg==1:
                    QMessageBox.critical(None,"Coordonnées ne correspondent pas","Verifier les coordonnées.")
                else:
                    if message=="":
                        QMessageBox.critical(None,"Erreur","N'existe pas")
                    else:
                        Livre=livre
                        self.Success.setText("Livres supprimés avec succés")
                        QMessageBox.information(None,"Livres supprimés",message)
                        self.EdRef.setText("")
                        self.EdAuteur.setText("")
                        self.EdAnnee.setText("")
                        Modification=1
            break
        
class ModifierEmprunt(QtWidgets.QMainWindow):
    def __init__(self):
        global window1
        global Modification
        super().__init__()
        uic.loadUi('ModifierEmprunt.ui', self)
        
        self.Return = self.findChild(QtWidgets.QPushButton, 'Return')
        self.Return.clicked.connect(self.close)
        
        self.Fermer = self.findChild(QtWidgets.QPushButton, 'Fermer')
        self.Fermer.clicked.connect(lambda: open_dialog_enreg(self))
        
        self.Modifier = self.findChild(QtWidgets.QPushButton, 'Modifier')
        self.Modifier.clicked.connect(self.modifEmpruntAction)
        
    #Fonction modifier Emprunt:
    def modifEmpruntAction(self):
        global Modification
        global Emprunt
        while True:
            msg=""
            err=0
            #Numéro d'inscription
            NumInscrip=self.EdNumInscrip.text()
            self.ErrNumInscrip.setText("")
            if not (saisirNumInscrip(NumInscrip)):
                self.ErrNumInscrip.setText("Numéro d'inscription invalide, doit être composé de 8 chiffres.")
                err=1
            elif not existe(Etudiant,NumInscrip):
                msg+="Etudiant n'existe pas. \n"
                
            #Référence
            Ref=self.EdRef.text()
            self.ErrRef.setText("")
            if not (saisirRef(Ref)):
                self.ErrRef.setText("Référence invalide.")
                err=1
            elif not existe(Livre,Ref):
                msg+="Livre n'existe pas. \n"
            if msg=="" and not(existemp(Emprunt,NumInscrip,Ref)):
                msg="Emprunt n'existe pas"
            #Dates
            DateEmprunt=self.EdDateEmprunt.text()
            DateRetour=self.EdDateRetour.text()
            self.ErrDate.setText("")
            if not (saisirDate(DateEmprunt,DateRetour)):
                self.ErrDate.setText("Vérifiez les dates.")
                err=1
            if err==0:
                if msg!="":
                    QMessageBox.critical(None,"Erreur",msg)
                else:
                    for key,val in Emprunt.items():
                        if key==NumInscrip and val[0]==Ref:
                            message="Emprunt du livre "+Livre[val[0]][0]+" de l'étudiant "+Etudiant[key][0]+" "+Etudiant[key][1]+" modifié avec succés\n"
                            val[1]=DateEmprunt
                            val[2]=DateRetour
                        break
                    QMessageBox.information(None,"Succés",message)
                    self.EdNumInscrip.setText("")
                    self.EdRef.setText("")
                    self.EdDateEmprunt.setDate(QDate(2023,1,1))
                    self.EdDateRetour.setDate(QDate(2023,1,1))
                    Modification=1
            break
        
class RechercherEtudiant(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('RechercherEtudiant.ui', self)
        global window1
        global Modification
        global Etudiant
        self.Return = self.findChild(QtWidgets.QPushButton, 'Return')
        self.Return.clicked.connect(self.close)
        
        self.Fermer = self.findChild(QtWidgets.QPushButton, 'Fermer')
        self.Fermer.clicked.connect(lambda: open_dialog_enreg(self))
        
        self.Afficher = self.findChild(QtWidgets.QPushButton, 'Afficher')
        self.Afficher.clicked.connect(lambda: self.open_afficherResultEtud(Etudiant))
        
        self.Rechercher = self.findChild(QtWidgets.QPushButton, 'Rechercher')
        self.Rechercher.clicked.connect(self.rechEtud)
    def open_afficherResultEtud(self,E):
        self.afficherResEtud = afficherResultEtud(E)
        self.afficherResEtud.showFullScreen()
    def rechEtud(self):
        while True:
            global Etudiant
            Etu={}
            err,nb,msg=0,0,0
            a,b,c=0,0,0 #Des variables octales représantant les indices des champs
            #Numéro d'inscription
            NumInscrip=self.EdNumInscrip.text()
            Section=self.EdSection.currentText()
            Niveau=self.EdNiveau.currentText()
            if NumInscrip!="":
                nb+=1
                a=4 
            if Section!="--Choisir Section--":
                nb+=1
                b=2
            if Niveau!="--Choisir Niveau--":
                nb+=1
                c=1
            if nb==0:
                QMessageBox.critical(None, "Erreur", "Veuillez remplir au moins un champ.")
                err=1
            self.ErrNumInscrip.setText("")
            if NumInscrip!="" and not (saisirNumInscrip(NumInscrip)):
                self.ErrNumInscrip.setText("Numéro d'inscription invalide, doit être composé de 8 chiffres.")
                err=1
            elif NumInscrip!="" and not (existe(Etudiant,NumInscrip)):
                QMessageBox.critical(None, "Erreur", "Cet étudiant n'existe pas.")
                err=1
            if err==0:
                s=a+b+c
                if nb==1:
                    if s==4:
                        Etu[NumInscrip]=Etudiant[NumInscrip]
                    if s==2:
                        for cle,val in Etudiant.items():
                            if val[6]==Section:
                                Etu[cle]=val
                    if s==1:
                        for cle,val in Etudiant.items():
                            if val[7]==Niveau:
                                Etu[cle]=val
                #Niveau et section
                if s==3:
                    for cle,val in Etudiant.items():
                        if val[6]==Section and val[7]==Niveau:
                            Etu[cle]=val
                #Num inscription + un autre champ
                if s==5 and Etudiant[NumInscrip][7]!=Niveau:
                    msg=1
                elif s==6 and Etudiant[NumInscrip][6]!=Section:
                    msg=1
                elif s==7 and (Etudiant[NumInscrip][6]!=Section or Etudiant[NumInscrip][7]!=Niveau):
                    msg=1
                elif s in [5,6,7]:
                    Etu[NumInscrip]=Etudiant[NumInscrip]
                if msg==1:
                    QMessageBox.critical(None,"Erreur","Vérifiez vos coordonnées ou entrez le numéro d'inscription seulement")
                elif Etu=={}:
                    QMessageBox.critical(None,"Erreur","N'existe pas")
                else:
                    self.open_afficherResultEtud(Etu)
            break
        
class afficherResultEtud(QtWidgets.QMainWindow):
    def __init__(self,E):
        super().__init__()
        uic.loadUi('AfficherEtudiant.ui', self)
        #self.afficher()
    #def afficher(self):
        #global Etudiant
        #E=Etudiant
        self.TableEtud = self.findChild(QtWidgets.QTableWidget, 'TableEtud')
        #self.TableEtud = self.findChild(QtWidgets.QTableWidget, 'TableEtud')
        self.TableEtud.setRowCount(len(E))
        self.TableEtud.setColumnCount(9)
        self.TableEtud.setHorizontalHeaderLabels(["NumInscrip", "Nom","Prenom","DatNiss","Adresse","Mail","Tel","Section", "Niveau"])
        i=0
        for cle, value in E.items():
            tab_NumInscrip=QtWidgets.QTableWidgetItem(str(cle))
            tab_Nom=QtWidgets.QTableWidgetItem(str(value[0]))
            tab_Prenom=QtWidgets.QTableWidgetItem(str(value[1]))
            tab_DateNiss=QtWidgets.QTableWidgetItem(str(value[2]))
            tab_Adresse=QtWidgets.QTableWidgetItem(str(value[3]))
            tab_Mail=QtWidgets.QTableWidgetItem(str(value[4]))
            tab_Tel=QtWidgets.QTableWidgetItem(str(value[5]))
            tab_Section=QtWidgets.QTableWidgetItem(str(value[6]))
            tab_Niveau=QtWidgets.QTableWidgetItem(str(value[7]))
            self.TableEtud.setItem(i, 0, tab_NumInscrip)
            self.TableEtud.setItem(i, 1, tab_Nom)
            self.TableEtud.setItem(i, 2, tab_Prenom)
            self.TableEtud.setItem(i, 3, tab_DateNiss)
            self.TableEtud.setItem(i, 4, tab_Adresse)
            self.TableEtud.setItem(i, 5, tab_Mail)
            self.TableEtud.setItem(i, 6, tab_Tel)
            self.TableEtud.setItem(i, 7, tab_Section)
            self.TableEtud.setItem(i, 8, tab_Niveau)
            i+=1
        self.TableEtud.setColumnWidth(0, 120)
        self.TableEtud.setColumnWidth(1, 120)
        self.TableEtud.setColumnWidth(2, 120)
        self.TableEtud.setColumnWidth(4, 150)
        self.TableEtud.setColumnWidth(5, 230)
        self.TableEtud.setColumnWidth(6, 90)
        self.TableEtud.setColumnWidth(7, 150)
        self.TableEtud.setColumnWidth(8, 70)
        
class RechercherLivre(QtWidgets.QMainWindow):
    def __init__(self):
        global window1
        global Modification
        super().__init__()
        uic.loadUi('RechercherLivre.ui', self)
        
        self.Return = self.findChild(QtWidgets.QPushButton, 'Return')
        self.Return.clicked.connect(self.close)
        
        self.Fermer = self.findChild(QtWidgets.QPushButton, 'Fermer')
        self.Fermer.clicked.connect(lambda: open_dialog_enreg(self))
        
        self.Afficher = self.findChild(QtWidgets.QPushButton, 'Afficher')
        self.Afficher.clicked.connect(lambda: self.open_afficherResultLivre(Livre))
        
        self.AfficherAlpha = self.findChild(QtWidgets.QPushButton, 'AfficherAlpha')
        self.AfficherAlpha.clicked.connect(self.alphab)
        
        self.Rechercher = self.findChild(QtWidgets.QPushButton, 'Rechercher')
        self.Rechercher.clicked.connect(self.rechLiv)
    def open_afficherResultLivre(self,L):
        self.afficherResultLivre = afficherResultLivre(L)
        self.afficherResultLivre.showFullScreen()
    def alphab(self):
        global livre
        liv={}
        for key,val in sorted(Livre.items(), key=lambda x: x[1]):
            liv[key]=Livre[key]
        self.open_afficherResultLivre(liv)
    def rechLiv(self):  
        while True:
            global Livre
            Ref,Titre,Auteur,Annee="","","",""
            Liv={}
            err,nb=0,0
            a,b,c,d=0,0,0,0 #Des variables octales représantant les indices des champs
            Ref=self.EdRef.text()
            Titre=self.EdTitre.text()
            Auteur=self.EdAuteur.text()
            Annee=self.EdAnnee.text()
            if Ref!="":
                nb+=1
                a=8
            if Titre!="":
                nb+=1
                b=4
            if Auteur!="":
                nb+=1
                c=2
            if Annee!="":
                nb+=1
                d=1
            if nb==0:
                QMessageBox.critical(None, "Erreur", "Veuillez remplir au moins un champ.")
                err=1
            self.ErrRef.setText("")
            if Ref!="" and not (saisirRef(Ref)):
                self.ErrRef.setText("Référence invalide.")
                err=1
            elif Ref!="" and not (existe(Livre,Ref)):
                QMessageBox.critical(None, "Erreur", "Ce livre n'existe pas.")
                err=1
            #Titre
            self.ErrTitre.setText("")
            if Titre!="" and not saisirNom(Titre):
                self.ErrTitre.setText("Titre invalide.")
                err=1
            #Auteur
            self.ErrAuteur.setText("")
            if Auteur!="" and not saisirNom(Auteur):
                self.ErrAuteur.setText("Nom d'auteur invalide.")
                err=1
            #Niveau
            self.ErrAnnee.setText("")
            if Annee!="" and not saisirAnnee(Annee):
                self.ErrAnnee.setText("Année d'édition invalide.")
                err=1
                
            if err==0:
                msg,msg2=0,0
                s=a+b+c+d
                if nb==1:
                    if s==8:
                        Liv[Ref]=Livre[Ref]
                    if s==4:
                        for key,val in Livre.items():
                            if val[0]==Titre:
                                Liv[key]=Livre[key]
                    if s==2:
                        for key,val in Livre.items():
                            if val[1]==Auteur:
                                Liv[key]=Livre[key]
                    if s==1:
                        for key,val in Livre.items():
                            if val[2]==Annee:
                                Liv[key]=Livre[key]
                #Ref + un autre champ(ou plusieurs)
                if s in [9,10,11,12,13,14,15]:
                    if s in [9,11,13,15] and Livre[Ref][2]!=Annee:
                        msg=1
                    if s in [10,11,14,15] and Livre[Ref][1]!=Auteur:
                        msg=1
                    if s in [12,13,14,15] and Livre[Ref][0]!=Titre:
                        msg=1
                    elif s in [9,10,11,12,13,14,15]:
                        Liv[Ref]=Liv[Ref]
                    #Champs remplis autre que celui de la référence
                    #Deux champs:
                elif nb==2:
                    if s==6:
                        test=0
                        for key,val in Livre.items():
                            if val[0]==Titre and val[1]==Auteur:
                                Liv[key]=Livre[key]
                                test=1
                        if test==0:
                            msg2=1
                    if s==5:
                        test=0
                        for key,val in Livre.items():
                            if val[0]==Titre and val[2]==Annee:
                                Liv[key]=Livre[key]
                                test=1
                        if test==0:
                            msg2=1
                    if s==3:
                        test=0
                        for key,val in Livre.items():
                            if val[1]==Auteur and val[2]==Annee:
                                Liv[key]=Livre[key]
                                test=1
                        if test==0:
                            msg2=1
                #Trois champs
                elif nb==3:
                    test=0
                    for key,val in Livre.items():
                        if val[0]==Titre and val[1]==Auteur and val[2]==Annee:
                            Liv[key]=Livre[key]
                            test=1
                    if test==0:
                        msg2=1
                if msg==1:
                    QMessageBox.critical(None,"Coordonnées ne correspondent pas","Verifier les coordonnées ou entrez seulement la référence.")
                elif msg2==1:
                    QMessageBox.critical(None,"Coordonnées ne correspondent pas","Verifier les coordonnées.")
                elif Liv=={}:
                    QMessageBox.critical(None,"Erreur","N'existe pas")
                else:
                    self.open_afficherResultLivre(Liv)
            break
        
class afficherResultLivre(QtWidgets.QMainWindow):
    def __init__(self,L):
        super().__init__()
        uic.loadUi('AfficherLivre.ui', self)
        self.TableLivre = self.findChild(QtWidgets.QTableWidget, 'TableLivre')
        self.TableLivre.setRowCount(len(L))
        self.TableLivre.setColumnCount(5)
        self.TableLivre.setHorizontalHeaderLabels(["Référence", "Titre","Auteur","Année Edition","Nbre d'Exemp"])
        i=0
        for cle, value in L.items():
            tab_Ref=QtWidgets.QTableWidgetItem(str(cle))
            tab_Titre=QtWidgets.QTableWidgetItem(str(value[0]))
            tab_Auteur=QtWidgets.QTableWidgetItem(str(value[1]))
            tab_Annee=QtWidgets.QTableWidgetItem(str(value[2]))
            tab_NbExp=QtWidgets.QTableWidgetItem(str(value[3]))
            self.TableLivre.setItem(i, 0, tab_Ref)
            self.TableLivre.setItem(i, 1, tab_Titre)
            self.TableLivre.setItem(i, 2, tab_Auteur)
            self.TableLivre.setItem(i, 3, tab_Annee)
            self.TableLivre.setItem(i, 4, tab_NbExp)
            i+=1
        self.TableLivre.setColumnWidth(0, 160)
        self.TableLivre.setColumnWidth(1, 280)
        self.TableLivre.setColumnWidth(2, 280)
        self.TableLivre.setColumnWidth(3, 210)
        self.TableLivre.setColumnWidth(4, 220)
        
class RechercherEmprunt(QtWidgets.QMainWindow):
    def __init__(self):
        global Emprunt
        global window1
        global Modification
        super().__init__()
        uic.loadUi('RechercherEmprunt.ui', self)
        
        self.Return = self.findChild(QtWidgets.QPushButton, 'Return')
        self.Return.clicked.connect(self.close)
        
        self.Fermer = self.findChild(QtWidgets.QPushButton, 'Fermer')
        self.Fermer.clicked.connect(lambda: open_dialog_enreg(self))
        
        self.Afficher = self.findChild(QtWidgets.QPushButton, 'Afficher')
        self.Afficher.clicked.connect(lambda: self.open_afficherResultEmp(Emprunt))
        
        self.Rechercher = self.findChild(QtWidgets.QPushButton, 'Rechercher')
        self.Rechercher.clicked.connect(self.rechEmp)
    def open_afficherResultEmp(self,Emp):
        self.afficherResEmp = afficherResultEmp(Emp)
        self.afficherResEmp.showFullScreen()
        
    def rechEmp(self):
        while True:
            global Emprunt
            global Livre
            global Etudiant
            Ref,NumInscrip="",""
            Emp={}
            err,nb,a,b=0,0,0,0
            msg,msg2="","Il n'existe pas d'emprunt."
            if self.RefInscrip.isChecked():
                Ref=self.EdRef.text()
                NumInscrip=self.EdNumInscrip.text()
                self.ErrRef.setText("")
                if Ref!="" and not (saisirRef(Ref)):
                    self.ErrRef.setText("Référence invalide.")
                    err=1
                elif Ref!="" and not (existe(Livre,Ref)):
                    msg+="Ce livre n'existe pas.\n"
                    err=1
                #NumInscrip
                self.ErrNumInscrip.setText("")
                if NumInscrip!="" and not saisirNumInscrip(NumInscrip):
                    self.ErrNumInscrip.setText("Numéro d'inscription invalide, doit être composé de 8 chiffres.")
                    err=1
                elif NumInscrip!="" and not (existe(Etudiant,NumInscrip)):
                    msg+="Cet étudiant n'existe pas."
                    err=1
            elif self.DateEmpBut.isChecked():
                D=self.EdDateEmp.text()
                for key,val in Emprunt.items():
                    if val[1]==D:
                        Emp[key]=Emprunt[key]
                D=self.EdDateRetour.text()
                for key,val in Emprunt.items():
                    if val[2]==D:
                        Emp[key]=Emprunt[key]
            elif self.EmpDBut.isChecked():
                date1=self.EdEmpDEmp.text()
                date2=self.EdEmpDRet.text()
                self.ErrDate.setText("")
                if not (saisirDate(date1,date2)):
                    self.ErrDate.setText("Vérifiez les dates.")
                    err=1
                else:
                    D1 = datetime.strptime(date1, "%d/%m/%Y")
                    D2 = datetime.strptime(date2, "%d/%m/%Y")
                    for key,val in Emprunt.items():
                        date=datetime.strptime(val[1], "%d/%m/%Y")
                        if D1<=date<=D2:
                            Emp[key]=Emprunt[key]
            elif self.RetDBut.isChecked():
                date1=self.EdEmpDEmp.text()
                date2=self.EdRetDRet.text()
                self.ErrDate.setText("")
                if not (saisirDate(date1,date2)):
                    self.ErrDate.setText("Vérifiez les dates.")
                    err=1
                else:
                    D1 = datetime.strptime(date1, "%d/%m/%Y")
                    D2 = datetime.strptime(date2, "%d/%m/%Y")
                    for key,val in Emprunt.items():
                        date=datetime.strptime(val[2], "%d/%m/%Y")
                        if D1<=date<=D2:
                            Emp[key]=Emprunt[key]
            else:
                msg2="Veuiller sélectionner la méthode de recherche."
            if err==0:
                if NumInscrip!="" and Ref!="":
                    for key,val in Emprunt.items():
                        if key==NumInscrip and val[0]==Ref:
                                Emp[key]=Emprunt[key]
                elif NumInscrip!="":
                    Emp[NumInscrip]=Emprunt[NumInscrip]
                elif Ref!="":
                    for key,val in Emprunt.items():
                        if val[0]==Ref:
                            Emp[key]=Emprunt[key]
                if msg!="":
                    QMessageBox.critical(None,"Erreur",msg)
                elif Emp=={}:
                    QMessageBox.critical(None,"Erreur",msg2)
                else:
                    self.open_afficherResultEmp(Emp)
            break
        
class afficherResultEmp(QtWidgets.QMainWindow):
    def __init__(self,Empr):
        super().__init__()
        uic.loadUi('AfficherEmprunt.ui', self)
        global Emprunt
        global Etudiant
        global Livre
        self.TableEmp = self.findChild(QtWidgets.QTableWidget, 'TableEmp')
        self.TableEmp.setRowCount(len(Empr))
        self.TableEmp.setColumnCount(7)
        self.TableEmp.setHorizontalHeaderLabels(["Num Inscription","Etudiant", "Référence", "Titre","Date Emprunt","Date Retour","Retourné"])
        i=0
        for cle, value in Empr.items():
            tab_NumInscrip=QtWidgets.QTableWidgetItem(str(cle))
            tab_Etudiant=QtWidgets.QTableWidgetItem(str(Etudiant[cle][1]+" "+Etudiant[cle][0]))
            tab_Ref=QtWidgets.QTableWidgetItem(str(value[0]))
            tab_Titre=QtWidgets.QTableWidgetItem(str(Livre[value[0]][0]))
            tab_DateEmp=QtWidgets.QTableWidgetItem(str(value[1]))
            tab_DateRetour=QtWidgets.QTableWidgetItem(str(value[2]))
            tab_Retourne=QtWidgets.QTableWidgetItem(str(value[3]))
            self.TableEmp.setItem(i, 0, tab_NumInscrip)
            self.TableEmp.setItem(i, 1, tab_Etudiant)
            self.TableEmp.setItem(i, 2, tab_Ref)
            self.TableEmp.setItem(i, 3, tab_Titre)
            self.TableEmp.setItem(i, 4, tab_DateEmp)
            self.TableEmp.setItem(i, 5, tab_DateRetour)
            self.TableEmp.setItem(i, 6, tab_Retourne)
            i+=1
        self.TableEmp.setColumnWidth(0, 160)
        self.TableEmp.setColumnWidth(1, 270)
        self.TableEmp.setColumnWidth(2, 100)
        self.TableEmp.setColumnWidth(3, 260)
        self.TableEmp.setColumnWidth(4, 130)
        self.TableEmp.setColumnWidth(5, 120)

#main
if __name__ == '__main__':
    global Etudiant
    Etudiant={}
    global Livre
    Livre={}
    global Emprunt
    Emprunt={}
    global Recup
    global Modification
    global window1
    Modification=0
    app = QtWidgets.QApplication([])
    window1 = Accueil()
    window1.showFullScreen()
    window1.setEnabled(False)
    open_dialog_recup()
    app.exec()