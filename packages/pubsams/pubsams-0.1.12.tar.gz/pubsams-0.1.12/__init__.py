from rdkit import Chem
from rdkit.Chem import Draw
import c
from rdkit.Chem import MACCSkeys
from rdkit.Chem import AllChem
from rdkit.Chem import rdmolops
from base64 import b64decode
from rdkit import DataStructs
from rdkit.Chem import Draw
from PIL import Image
from IPython.display import display
from rdkit.Chem.AtomPairs import Pairs
from rdkit.Chem.Fingerprints import FingerprintMols
#from rdkit.Chem import MCS
from rdkit.Chem import rdFMCS
from rdkit.Chem.Draw import IPythonConsole
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import rdFMCS
from rdkit.Chem.Draw import rdDepictor
rdDepictor.SetPreferCoordGen(True)
IPythonConsole.drawOptions.minFontSize=20
import time
from io import StringIO
from mordred import WienerIndex
from mordred import ZagrebIndex
import pandas as pd
#from rdkit import MCS
import statsmodels as sm
from mordred import Calculator, descriptors
import matplotlib.pyplot as plt
from rdkit.Chem import rdFMCS

def PCFP_BitString(pcfp_base64) :

    pcfp_bitstring = "".join( ["{:08b}".format(x) for x in b64decode( pcfp_base64 )] )[32:913]
    return pcfp_bitstring

from rdkit import Chem


def help():
    print("This library help user to look for specific chemical features ncluding find smailarity, chirality, bond, type, double bond sterochmsitry, and common substcure and chirality for more information look for this link word documantry on google drive")
    print("")
    print("https://docs.google.com/document/d/1AqRdpTBIaBZEBkiAnuuzMNLSqoenK4yL/edit?usp=sharing&ouid=118019681680310111518&rtpof=true&sd=true")
    print("")
    print("This is github link if you link to see code file for this project")
    print("https://github.com/Ahmed212517329/pubcem.git")
    return

help()
def assay_aid_to_active_cid__inactive_cid_smliarity(e):
    IPythonConsole.drawOptions.addAtomIndices = True
    IPythonConsole.drawOptions.addStereoAnnotation = True

    ########################################find description link sids #####################################################
    sc=[]
    print("This code find active and inactive substance for given assay they it measure the smilarity between these inactive and active substance")

    description= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(e)+"/description/xml"
    print("Here is link descript your entery assay ")
    print("")
    print(description)
    print("")
    #print("Here is list of substances are active in your assay ")
    print("")
    ########################################find active sids #####################################################

    active= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(e)+ "/cids/txt?cids_type=active"
    url=requests.get(active)
    cidactive= (url.text.split())
    #print(cids)
    ########################################find inactive sids #####################################################
    inactive= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(e)+ "/cids/txt?cids_type=inactive"
    url=requests.get(inactive)
    cidinactive= (url.text.split())
    ########################################find active Fingerprint2D #####################################################
    prolog = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    str_cid = ",".join([ str(x) for x in cidactive])
    url = prolog + "/compound/cid/" + str_cid + "/property/Fingerprint2D/txt"
    res = requests.get(url)
    Fingerprint2Dactive = res.text.split()
    ########################################find inactive Fingerprint2D #####################################################
    prolog = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    str_cid = ",".join([ str(x) for x in cidinactive])
    url = prolog + "/compound/cid/" + str_cid + "/property/Fingerprint2D/txt"
    res = requests.get(url)
    Fingerprint2Dinactive = res.text.split()
    ########################################find inactive & active snilarity score #####################################################

    for i in range(len(Fingerprint2Dactive)):
            IPythonConsole.drawOptions.addAtomIndices = True
            IPythonConsole.drawOptions.addStereoAnnotation = True

            for j in range(len(Fingerprint2Dinactive)) :
                fps1=(DataStructs.CreateFromBitString(PCFP_BitString(Fingerprint2Dactive[i])))
                fps2=(DataStructs.CreateFromBitString(PCFP_BitString(Fingerprint2Dinactive[j])))
                score = DataStructs.FingerprintSimilarity(fps1, fps2)
                print("active cid", cidactive[i], "vs.", "inactive", cidinactive[j], ":", round(score,3), end='')
                sc.append(str(score))
                    ########################################draw active structure #####################################################
                print("")

                print("Active molecule structure")
                print("")
                w1="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"+ cidactive[i] +"/property/isomericsmiles/txt"
                res1 = requests.get(w1)
                img1 = Chem.Draw.MolToImage( Chem.MolFromSmiles( res1.text.rstrip() ), size=(200, 100))
                display(img1)

    ########################################draw inactive structure #####################################################
                print("Inactive molecule structure")
                print("")
                w2="https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"+ cidinactive[j] +"/property/isomericsmiles/txt"
                res2 = requests.get(w2)

                img2 = Chem.Draw.MolToImage( Chem.MolFromSmiles( res2.text.rstrip() ), size=(200, 100) )
                display(img2)
    ########################################print inactive & active snilarity score #####################################################

                if ( score >= 0.85 ):
                    print(" ****")
                elif ( score >= 0.75 ):
                    print(" ***")
                elif ( score >= 0.65 ):
                    print(" **")
                elif ( score >= 0.55 ):
                    print(" *")
                else:
                    print(" ")
    return
#assay_aid_to_active_cid__inactive_cid_smliarity(1000)

    ########################################find description link sids #####################################################
def assay_aid_to_active_cid_common_substracture(e):
    IPythonConsole.drawOptions.addAtomIndices = True
    IPythonConsole.drawOptions.addStereoAnnotation = True

    study= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(1000)+ "/cids/txt?cids_type=active"
    url=requests.get(study)
    cids= (url.text.split())
        #print(cidactive)
    str_cid = ",".join([ str(x) for x in cids])
    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/" + str_cid + "/property/IsomericSMILES/txt"
    prolog = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    res = requests.get(url)
        #print(smiles)
        ########################################find active sids #####################################################
    ms = res.text.split()
    ms = list(map(Chem.MolFromSmiles, ms))
    i = Chem.Draw.MolsToGridImage(ms, subImgSize=(400,400))
    r = MCS.FindMCS(ms, threshold=0.7)
    display(i)
    #rdkit.Chem.Draw.MolToImage(r.queryMol, size=(400,400))
    res = rdFMCS.FindMCS(ms, threshold=0.7)
    ii= Chem.MolFromSmarts( res.smartsString)
    #ii= Chem.MolFromSmarts(res.smarts)
    #Chem.MolFromSmarts(res.smarts)
    print("The common substructure for these cids")
    display(ii)
    return url
#assay_aid_to_active_cid(180)
import rdkit.Chem
import rdkit.Chem
from rdkit.Chem import MCS

    ########################################find description link sids #####################################################
def assay_aid_to_inactive_cid_common_substracture(e):
    IPythonConsole.drawOptions.addAtomIndices = True
    IPythonConsole.drawOptions.addStereoAnnotation = True

    study= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(1000)+ "/cids/txt?cids_type=inactive"
    url=requests.get(study)
    cids= (url.text.split())
        #print(cidactive)
    str_cid = ",".join([ str(x) for x in cids])
    url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/" + str_cid + "/property/IsomericSMILES/txt"
    res = requests.get(url)
        #print(smiles)
        ########################################find active sids #####################################################

    ms = res.text.split()
    ms = list(map(rdkit.Chem.MolFromSmiles, ms))
    i = Chem.Draw.MolsToGridImage(ms, subImgSize=(400,400))
    r = MCS.FindMCS(ms, threshold=0.5)
    display(i)
    #rdkit.Chem.Draw.MolToImage(r.queryMol, size=(400,400))
    #rdkit.Chem.Draw.MolToImage(r.queryMol, size=(400,400))
    res = rdFMCS.FindMCS(ms, threshold=0.7)
    ii= Chem.MolFromSmarts( res.smartsString)
    #ii= Chem.MolFromSmarts(res.smarts)
    #Chem.MolFromSmarts(res.smarts)
    print("The common substructure for these cids")
    display(ii)
    return url
#find_active_sids_for_aid(180)#find_active_sids_for_aid(100)
def assay_aid_to_active_cid(e):
    IPythonConsole.drawOptions.addAtomIndices = True
    IPythonConsole.drawOptions.addStereoAnnotation = True

    e=str(e)
    active= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(e)+ "/cids/txt?cids_type=active"
    url=requests.get(active)
    cidactive= (url.text.split())

    print("These substance sids are \n \n", cidactive)
    return active
#assay_aid_sid_active_common_substracture(1000)

def assay_aid_to_inactive_cid(e):
    rdDepictor.SetPreferCoordGen(True)
    IPythonConsole.drawOptions.minFontSize=20

    e=str(e)
    inactive= "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/"+str(e)+ "/cids/txt?cids_type=inactive"
    url=requests.get(inactive)
    cidinactive= (url.text.split())

    print("These compound cids are \n \n", cidinactive)
        ########################################find active sids #####################################################
    return inactive
#assay_aid_to_inactive_cid(1000)

def compound_smile_to_morgan_atom_topological(a,b):
    ms = [Chem.MolFromSmiles(a), Chem.MolFromSmiles(b)]
    fig=Draw.MolsToGridImage(ms[:],molsPerRow=2,subImgSize=(400,200))
    display(fig)
    from rdkit.Chem.AtomPairs import Pairs
    from rdkit.Chem import AllChem
    from rdkit.Chem.Fingerprints import FingerprintMols
    from rdkit import DataStructs

    radius = 2

    fpatom = [Pairs.GetAtomPairFingerprintAsBitVect(x) for x in ms]
    fpatom = [Pairs.GetAtomPairFingerprintAsBitVect(x) for x in ms]

    print("atom pair score: {:8.4f}".format(DataStructs.TanimotoSimilarity(fpatom[0], fpatom[1])))
    fpmorg = [AllChem.GetMorganFingerprint(ms[0],radius,useFeatures=True),
              AllChem.GetMorganFingerprint(ms[1],radius,useFeatures=True)]
    fptopo = [FingerprintMols.FingerprintMol(x) for x in ms]
    print("morgan score: {:11.4f}".format(DataStructs.TanimotoSimilarity(fpmorg[0], fpmorg[1])))
    print("topological score: {:3.4f}".format(DataStructs.TanimotoSimilarity(fptopo[0], fptopo[1])))
    return
#compound_smile_to_morgan_atom_topological("CCO","CNCN")
def show_csv_file(a):# show csv file
    df = pd.read_csv(a) # read in the file into a pandas dataframe
    df
    return display(df)
#m=sho_csv_file("BP.CSV")#show_csv_file("ahmed.csv")
def plot_from_csv_file(file_name, xscat,yscat,xla,yla):#plot from csv file
    df = pd.read_csv(file_name) # read in the file into a pandas dataframe
    df = df
    df
    plt.scatter(xscat, yscat)     # plot of boiling point (in K) vs molecular weight
    plt.xlabel(xla)
    plt.ylabel(yla)
    plt.show()
    return
#plot_from_csv_file("BP.CSV",df.BP_C,df.MW, 'Wiener Index', 'Boiling Point in Kelvin')
#plot_from_csv_file("ahmed.csv",df.MolecularWeight,df.XLogP, 'Wiener Index', 'Boiling Point in Kelvin')

