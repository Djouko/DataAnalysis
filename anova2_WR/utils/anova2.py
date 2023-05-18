import numpy as np
from scipy import stats

class ANOVA2WR:
    def __init__(self, data, r, c, n, facteur1, facteur2, alpha) -> object:
        # Initialisation des variables
        self.r, self.c, self.n = r, c, n  # Nombre de niveaux du facteur 1, facteur 2 et des répétitions
        self.facteur1 = facteur1  # Nom du facteur 1
        self.facteur2 = facteur2  # Nom du facteur 2
        self.data = data  # Données
        self.alpha = alpha  # Niveau de signification
        self.tppp = self.calc_T(data, r, c, n)  # Somme des carrés des valeurs
        self.cf = self.calculate_cf(data, r, c, n)  # Correction de la factorisation
        self.SST = self.calculate_SST(data, r, c, n)  # Somme des carrés totale
        self.SSC = self.calculate_SSC(data, r, c, n)  # Somme des carrés du facteur 1
        self.SSR = self.calculate_SSR(data, r, c, n)  # Somme des carrés du facteur 2
        self.SSRC = self.calculate_SSRC(data, r, c, n)  # Somme des carrés de l'interaction des facteurs 1 et 2
        self.SSE = self.calculate_SSE(self.SST, self.SSC, self.SSR, self.SSRC)  # Somme des carrés de l'erreur
        self.MSC = int((self.SSC) / (self.c - 1) * 1000) / 1000  # Moyenne des carrés du facteur 1
        self.MSR = int((self.SSR) / (self.r - 1) * 1000) / 1000  # Moyenne des carrés du facteur 2
        self.MSRC = int(((self.SSRC) / ((self.r - 1) * (self.c - 1))) * 1000) / 1000  # Moyenne des carrés de l'interaction des facteurs 1 et 2
        self.MSE = int(((self.SSE) / ((self.r) * (self.c) * (self.n - 1))) * 1000) / 1000  # Moyenne des carrés de l'erreur
        self.FC = int((self.MSC) / (self.MSE) * 1000) / 1000  # Statistique F pour le facteur 1
        self.FR = int((self.MSR) / (self.MSE) * 1000) / 1000  # Statistique F pour le facteur 2
        self.FRC = int((self.MSRC) / (self.MSE) * 1000) / 1000  # Statistique F pour l'interaction des facteurs 1 et 2
        
        # Calcul des valeurs critiques pour chaque statistique F
        self.crit_val_FR = stats.f.ppf(1 - self.alpha, self.r - 1, self.r * self.c * (self.n - 1))
        self.crit_val_FC = stats.f.ppf(1 - self.alpha, self.c - 1, self.r * self.c * (self.n - 1))
        self.crit_val_FRC = stats.f.ppf(1-self.alpha, (self.r-1)*(self.c-1), self.r*self.c*(self.n-1))
        #
        self.crit_val_FR = int(self.crit_val_FR*1000)/1000
        self.crit_val_FC = int(self.crit_val_FC*1000)/1000
        self.crit_val_FRC = int(self.crit_val_FRC*1000)/1000
        
        """_summary_
        cette condition compare la valeur calculée de FR avec la valeur critique de FR.
        Si la valeur calculée est supérieure à la valeur critique, 
        cela signifie que l'hypothèse nulle pour le facteur 2 est rejetée et l'hypothèse alternative est acceptée.
        Le message "Rejected" est imprimé pour indiquer que l'hypothèse nulle est rejetée.
        Sinon, le message "Accepted" est imprimé et l'hypothèse nulle est acceptée.
        """
        if self.FR > self.crit_val_FR :

            self.accepted_FR_message = f"H0' du facteur {self.facteur2} est refuser et donc H1' accepter"
            print("Rejected ")
        else:
            self.accepted_FR_message = f"H0' du facteur {self.facteur2} est accepter"
            print("Accepted ")
        
        """
        cette condition compare la valeur calculée de FC avec la valeur critique de FC. 
        Si la valeur calculée est supérieure à la valeur critique, 
        cela signifie que l'hypothèse nulle pour le facteur 1 est rejetée et l'hypothèse alternative est acceptée. 
        Le message "Rejected" est imprimé pour indiquer que l'hypothèse nulle est rejetée. 
        Sinon, le message "Accepted" est imprimé et l'hypothèse nulle est acceptée.
        """
        
        if self.FC > self.crit_val_FC :
            
            self.accepted_FC_message = f"H0'' du facteur {self.facteur1} est refuser et donc H1'' accepter"
            print("Rejected ")
        else:
            self.accepted_FC_message = f"H0'' du facteur {self.facteur1} est accepter"
            print("Accepted ")
        
        """
        cette condition compare la valeur calculée de FRC avec la valeur critique de FRC. 
        Si la valeur calculée est supérieure à la valeur critique, 
        cela signifie que l'hypothèse nulle pour l'interaction entre les facteurs 1 et 2 est rejetée et l'hypothèse alternative est acceptée. 
        Le message "Rejected" est imprimé pour indiquer que l'hypothèse nulle est rejetée. 
        Sinon, le message "Accepted" est imprimé et l'hypothèse nulle est acceptée.
        """
        
        if (self.FRC > self.crit_val_FRC) :
            
            self.accepted_FRC_message = f"H0''' de l'interaction entre les facteurs {self.facteur1} et {self.facteur2} est refuser et donc H1''' accepter"
            print("Rejected ")
        else:
            self.accepted_FRC_message = f"H0''' de l'interaction entre les facteurs {self.facteur1} et {self.facteur2} est accepter"
            print("Accepted ")
        
    #Fonction de la class ANOVA2WR

    def calc_T(self, data, r, c, n, p=1):
        """
        Calculer la somme des carrés des erreurs
        
        Args:
        data : tableau 3D : Données pour l'analyse
        r : int : Nombre de niveaux pour le Facteur 1
        c : int : Nombre de niveaux pour le Facteur 2
        n : int : Nombre de répétitions
        p : int : Puissance à laquelle élever chaque élément
        """
        sum = 0 
        for i in range(0, r):
            for j in range(0, c):
                for k in range(0, n):
                    sum += data[i][j][k]**p
        return sum


    def calculate_cf(self, data, r, c, n):
        """
        Calculer le facteur de correction

        Args:
        data : tableau 3D : Données pour l'analyse
        r : int : Nombre de niveaux pour le Facteur 1
        c : int : Nombre de niveaux pour le Facteur 2
        n : int : Nombre de répétitions
        
        Returns:
        cf : float : facteur de correction
        """
        tpp = self.calc_T(data, r, c, n, 1)
        cf = tpp ** 2 / (r * c * n)
        return int(cf * 1000) / 1000
        

    def calculate_SST(self, data, r, c, n):
        """
        Calculer la somme des carrés totaux

        Args:
        data : tableau 3D : Données pour l'analyse
        r : int : Nombre de niveaux pour le Facteur 1
        c : int : Nombre de niveaux pour le Facteur 2
        n : int : Nombre de répétitions
        
        Returns:
        sst : float : somme des carrés totaux
        """
        sum = self.calc_T(data, r, c, n, p=2)
        cf = self.calculate_cf(data, r, c, n)
        sst = sum - cf
        return int(sst * 1000) / 1000


    def calculate_SSC(self, data, r, c, n):
        """
        Calculer la somme des carrés des colonnes

        Args:
        data : tableau 3D : Données pour l'analyse
        r : int : Nombre de niveaux pour le Facteur 1
        c : int : Nombre de niveaux pour le Facteur 2
        n : int : Nombre de répétitions
        
        Returns:
        ssc : float : somme des carrés des colonnes
        """
        tpjp = 0
        for j in range(0, c):
            sum = 0
            for i in range(0, r):
                for k in range(0, n):
                    sum += data[i][j][k]
            tpjp += sum ** 2
        ssc = tpjp / (r * n) - self.calculate_cf(data, r, c, n)
        return int(ssc * 1000) / 1000


    def calculate_SSR(self, data, r, c, n):
        """
        Calculer la somme des carrés des lignes

        Args:
        data : tableau 3D : Données pour l'analyse
        r : int : Nombre de niveaux pour le Facteur 1
        c : int : Nombre de niveaux pour le Facteur 2
        n : int : Nombre de répétitions
        
        Returns:
        ssr : float : somme des carrés des lignes
        """
        tipp = 0
        for i in range(0, r):
            sum = 0
            for j in range(0, c):
                for k in range(0, n):
                    sum += data[i][j][k]
            tipp += sum ** 2
        ssr = tipp / (c * n) - self.calculate_cf(data, r, c, n)
        return int(ssr * 1000) / 1000


    def calculate_SSRC(self, data, r, c, n):
        """
        Calculer la somme des carrés des interactions entre les facteurs 1 et 2

        Args:
        data : tableau 3D : Données pour l'analyse
        r : int : Nombre de niveaux pour le Facteur 1
        c : int : Nombre de niveaux pour le Facteur 2
        n : int : Nombre de répétitions
        
        Returns:
        ssrc : float : somme des carrés des interactions entre les facteurs 1 et 2
        """
        tijp = 0
        for i in range(0, r):
            for j in range(0, c):
                sum = 0
                for k in range(0, n):
                    sum += data[i][j][k]
                tijp += sum**2

        ssr = self.calculate_SSR(data, r, c, n)
        ssc = self.calculate_SSC(data, r, c, n)
        cf = self.calculate_cf(data, r, c, n)

        ssrc = tijp/n - ssr - ssc - cf

        return int(ssrc * 1000) / 1000


    def calculate_SSE(self, sst, ssc, ssr, ss_RC):
        """
        Calculer la somme des carrés des erreurs

        Args:
        sst : float : Somme des carrés totale
        ssc : float : Somme des carrés du Facteur 1
        ssr : float : Somme des carrés du Facteur 2
        ss_RC : float : Somme des carrés des interactions entre les répétitions et les Facteurs 1 et 2
        
        Returns:
        SSE : float : somme des carrés des erreurs
        """
        SSE = sst - ssc - ssr - ss_RC
        return int(SSE * 1000) / 1000


    def calculate_MSR(self, data, ssr, ddlr, r, c, n):
        """
        Calculer la moyenne des carrés des lignes

        Args:
        data : tableau 3D : Données pour l'analyse
        ssr : float : Somme des carrés du Facteur 2
        ddlr : float : Degrés de liberté pour le Facteur 2
        r : int : Nombre de niveaux pour le Facteur 1
        c : int : Nombre de niveaux pour le Facteur 2
        n : int : Nombre de répétitions
        
        Returns:
        MSR : float : moyenne des carrés des lignes
        """
        SSR = self.calculate_SSR(data, r, c, n)
        ddlr = r - 1
        MSR = SSR / ddlr
        return int(MSR * 1000) / 1000


    def calculate_MSC(self, data, ssrce, ddlc, r, c, n):
        """
        Calculer la moyenne des carrés des colonnes

        Args:
        data : tableau 3D : Données pour l'analyse
        ssrce : float : Somme des carrés de l'erreur
        ddlc : float : Degrés de liberté pour le Facteur 1
        r : int : Nombre de niveaux pour le Facteur 1
        c : int : Nombre de niveaux pour le Facteur 2
        n : int : Nombre de répétitions

        Returns:
        MSC : float : moyenne des carrés des colonnes
        """
        SSC =self.calculate_SSC(data,r,c,n)
        ddlc=c-1
        MSC = SSC/ddlc
        return int(MSC * 1000) / 1000
    
    
    def calculate_MSRC(self,data,ssrc,ddlrc,r,c,n):
        """
        Calculer la moyenne des interactions
        
        Args:
        data : tableau 3D : Données pour l'analyse
        ssrce : float : Somme des carrés de l'interaction
        ddlrc : float : Degrés de liberté pour le Facteur 1
        r : int : Nombre de niveaux pour le Facteur 1
        c : int : Nombre de niveaux pour le Facteur 2
        n : int : Nombre de répétitions
        
        Returns:
        MSRC : float : moyenne des carrés des interactions
        """
        SSRC =self. calculate_SSRC (self,data,r,c,n)
        ddlc=(c-1)*(r-1)
        MSRC = SSRC/ddlc
        return int(MSRC * 1000) / 1000
    
    
    


""" 








data = np.array([[[7, 3],
                  [6, 2],
                  [5, 4]],
            [[ 2, 1],
             [9, 8],
             [3, 7]],

            [[5, 2],
             [8, 4],
             [3, 6]]])

r,c,n = 3,3,2
tppp =calc_T(data,3,3,2)
cf =calculate_cf(data,r,c,n)
SST =  calculate_SST(data,r,c,n)
SSC =calculate_SSC(data,r,c,n )
SSR =calculate_SSR(data,r,c,n)
SSRC=calculate_SSRC (data,r,c,n)
SSE=calculate_SSE( SST,SSC,SSR,SSRC)
print(" T... = ",tppp, "\n CF = ",cf,"\n SST = ",SST,"\n SSC = " ,SSC,
      "\n SSR = ",SSR ,"\nSSRC =" ,SSRC , "\nSSE = ",SSE) """