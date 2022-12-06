import os
from PIL import Image, ExifTags

#declaration calsse
class prepImg():

    #declaration variable de la classe
    def __init__(self, path, ecranX, ecranY):
        self.path = path
        self.ecranX = ecranX
        self.ecranY = ecranY

    #methode pour formatter les fichiers photo selon les besoin d'affichage
    def set(self):
        #declaration des variables de path dossiers
        dossiers = os.listdir(self.path)
        nbDossiers = len(dossiers)
        numeroDossiers = range(nbDossiers)
        print(dossiers)
        print(nbDossiers)
        print(numeroDossiers)
        for n in numeroDossiers:
            #declaration des variables de path fichiers
            dossierPath = self.path+dossiers[n]+"/"
            fichiers = os.listdir(dossierPath)
            nbFichiers = len(fichiers)
            numeroFichiers = range(nbFichiers)
            print(fichiers)
            print(nbFichiers)
            print(numeroFichiers)
            for n in numeroFichiers:
                    #declarartion des variables fichiers
                    fichier = fichiers[n]
                    fichierPath = dossierPath+fichier
                    taille = (self.ecranX, self.ecranY)
                    img = Image.open(fichierPath)
                    print(fichier)
                    print(fichierPath)
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation] == 'Orientation':
                            break
                    print("Orientation (Indice) : ", orientation)
                    #test sur l'extraction des valeur EXIF
                    try:
                        z = 0
                        while z < 2:
                            img = Image.open(fichierPath)
                            exifData = img._getexif()
                            z = z+1
                        print("Orientation (Valeur) : ", exifData[orientation])
                    except:
                        print("Incapable d'extraire de donnée EXIF")
                    try:
                        # reorientation des images selon leurs tag
                        img = Image.open(fichierPath)
                        exifData = img._getexif()
                        if exifData[orientation] == 3:
                            rgbImg = img.rotate(180)
                            rgbImg.save(fichierPath)
                        elif exifData[orientation] == 6:
                            rgbImg = img.rotate(270)
                            rgbImg.save(fichierPath)
                        elif exifData[orientation] == 8:
                            rgbImg = img.rotate(90)
                            rgbImg.save(fichierPath)
                        print("Orientation (Valeur) : ", exifData[orientation])
                    except:
                        print("Incapable de faire de rotation")
                    try:
                        #recalibrage de l'image selon les variables d'affichages
                        w=0
                        while w < 2 :
                            rgbImg = img.convert('RGB')
                            rgbImg.thumbnail(taille)  # version miniature
                            rgbImg.save(fichierPath)
                            w = w+1
                        print("convert " + fichier)
                        print(img.size)
                    except:
                        print("impossible de convertir "+fichier)
                        print(img.size)
                    try:
                        #reconfiguration des fichiers en fichiers images compatibles
                        nomFichier, extensionFichier = os.path.splitext(fichier)
                        #print(extensionFichier)
                        if extensionFichier != '.jpg' and extensionFichier != '.jpeg' and extensionFichier != '.JPG' and extensionFichier != ".JPEG":
                            img = Image.open(fichierPath)
                            rgbImg = img.convert('RGB')
                            rgbImg.save(dossierPath+nomFichier + ".jpg")
                            os.remove(fichierPath)
                            print("converti jpg"+extensionFichier+nomFichier)
                    except OSError:
                        print("Impossible de convertir en jpeg ", fichier)
                    





