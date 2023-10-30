from rdkit import Chem
from rdkit.Chem import Draw
import requests
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
import param
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

# Adding descriptors to the dataset

def Add_Wiener_Z1_Z2_to_dataset(file_name, SMILE_row):## Adding descriptors to the dataset and then get csv file with your new adding

  df = pd.read_csv(file_name) # read in the file into a pandas dataframe

  wiener_index = WienerIndex.WienerIndex()               # create descriptor instance for Wiener index
  zagreb_index1 = ZagrebIndex.ZagrebIndex(version = 1)            # create descriptor instance for Zagreb index 1
  zagreb_index2 = ZagrebIndex.ZagrebIndex(version = 2)            # create descriptor instance for Zagreb index 1
  result_Wiener= []
  result_Z1= []
  result_Z2= []

  for index, row in df.iterrows():                # iterate through each row of the CSV data
      SMILE = row[SMILE_row]                       # get SMILES string from row
      mol = Chem.MolFromSmiles(SMILE)             # convert smiles string to mol file
      result_Wiener.append(wiener_index(mol))     # calculate Wiener index descripter value
      result_Z1.append(zagreb_index1(mol))        # calculate zagreb (Z1) descriptor value
      result_Z2.append(zagreb_index2(mol))        # calculate zagreb (Z2) descriptor value

  df['Wiener'] = result_Wiener           # add the results for WienerIndex to dataframe
  df['Z1'] = result_Z1                   # add the results for Zagreb 1 to dataframe
  df['Z2'] = result_Z2                   # add the results for Zagreb 2 to dataframe
  df
  file= df.to_csv('file1.csv')# it will save automatically
  print("You can this file in your device by looking for file1.csv file")
  return display(df)

#m=Add_Wiener_Z1_Z2_to_dataset("BP.CSV",'SMILES')
######################
import statsmodels.api as sm           # import the statsmodels library as sm
def Mulitple_regression_analysis_csv_file_using_statsmodels(file_name,SMILE_row,*d):# Mulitple_regression_analysis_using_statsmodels
  #a=dependent variable
  #*d=independent variables

  df = pd.read_csv(file_name) # read in the file into a pandas dataframe

  wiener_index = WienerIndex.WienerIndex()               # create descriptor instance for Wiener index
  zagreb_index1 = ZagrebIndex.ZagrebIndex(version = 1)            # create descriptor instance for Zagreb index 1
  zagreb_index2 = ZagrebIndex.ZagrebIndex(version = 2)            # create descriptor instance for Zagreb index 1
  result_Wiener= []
  result_Z1= []
  result_Z2= []

  for index, row in df.iterrows():                # iterate through each row of the CSV data
      SMILE = row[SMILE_row]                       # get SMILES string from row
      mol = Chem.MolFromSmiles(SMILE)             # convert smiles string to mol file
      result_Wiener.append(wiener_index(mol))     # calculate Wiener index descripter value
      result_Z1.append(zagreb_index1(mol))        # calculate zagreb (Z1) descriptor value
      result_Z2.append(zagreb_index2(mol))        # calculate zagreb (Z2) descriptor value

  df['Wiener'] = result_Wiener           # add the results for WienerIndex to dataframe
  df['Z1'] = result_Z1                   # add the results for Zagreb 1 to dataframe
  df['Z2'] = result_Z2                   # add the results for Zagreb 2 to dataframe
  #df
  file= df.to_csv('file1.csv')# it will save automatically
  #display(df)
  strrl=[]
  #a=str(a)
  for x in d:
    if type(x) is str:
      print("s")
      x=str(x)
      strrl.append(x)
    elif type(x) is int:
      print("s")
      x=str(x)
      strrl.append(x)

    elif type(x) is list:
      #print("l")
      for m in x:
          x=str(m)
          strrl.append(x)
    else:
      for m in x:
        print(99)
        strrl.append(str(m))
  #print(strrl)
  X = df[strrl]   # select our independent variables
  X = sm.add_constant(X)                 # add an intercept to our model
  y = df[["BP_K"]]                       # select BP as our dependent variable
  model = sm.OLS(y,X).fit()              # set up our model
  predictions = model.predict(X)         # make the predictions
  print(model.summary())                 # print out statistical summary

  return                 # print out statistical summary
#Mulitple_regression_analysis_csv_file_using_statsmodels("BP.CSV",'SMILES', ["MW", "Wiener", "Z1", "Z2"])
#Mulitple_regression_analysis_csv_file_using_statsmodels("BP.CSV",'SMILES', ["MW","BP_C"])#Mulitple_regression_analysis_using_statsmodels("BP.CSV","BP_C", ["MW","BP_C"])

################################
def Delete_Substruct(Substruct,*d):
      IPythonConsole.drawOptions.addAtomIndices = True
      IPythonConsole.drawOptions.addStereoAnnotation = True

      strrl=[]# to save compound name to retrive link date later
      for x in d:
        if type(x) is str:
          #print("s")
          x=str(x)
          strrl.append(x)
        elif type(x) is int:
          #print("s")
          x=str(x)
          strrl.append(x)

        elif type(x) is list:
          #print("l")
          for m in x:
              x=str(m)
              strrl.append(x)
        else:
          for m in x:
            #print(6)
            strrl.append(str(m))
      #print(strrl)
      de=[]
      print("You are going to drop this  ")
      m = Chem.MolFromSmiles(Substruct)
      display(m)

      print("Molecular structure beofre drop substracture ")

      for i in d:
          m = Chem.MolFromSmiles(i)
          display(m)
      print("Molecular structure After drop substracture ")

      if len(strrl)>0:
        for i in strrl:
          m = Chem.MolFromSmiles(i)
          patt = Chem.MolFromSmarts(Substruct)
          rm = AllChem.DeleteSubstructs(m,patt)
          #m= Chem.MolFromSmiles(rm)
          #print(rm)
          #de.append(Chem.MolFromSmiles(rm))
          display(rm)
          #print(Chem.MolToSmiles(rm))
      return de

#Delete_Substruct('C(=O)[OH]','CC(=O)O', 'CC(=O)')

def has_Substruct_or_not(Substruct,*d):
  IPythonConsole.drawOptions.addAtomIndices = True
  IPythonConsole.drawOptions.addStereoAnnotation = True

  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
      #print("s")
      x=str(x)
      strrl.append(x)
    elif type(x) is int:
      #print("s")
      x=str(x)
      strrl.append(x)

    elif type(x) is list:
      #print("l")
      for m in x:
          x=str(m)
          strrl.append(x)
    else:
      for m in x:
        #print(6)
        strrl.append(str(m))
  #print(strrl)
  de=[]
  if len(strrl)>0:
    for i in strrl:
      m = Chem.MolFromSmiles(i)
      patt = Chem.MolFromSmarts(Substruct)
      rm=m.HasSubstructMatch(patt)
      de.append(rm)
      #print(rm)
  return de

#print(has_Substruct_or_not('C(=O)[OH]','CC(=O)O', 'CC(=O)'))

def Maximum_common_substructure(*d):
  IPythonConsole.drawOptions.addAtomIndices = True
  IPythonConsole.drawOptions.addStereoAnnotation = True

  strrl=[]# to save compound name to retrive link date later
  for x in d:
    if type(x) is str:
      #print("s")
      x=str(x)
      strrl.append(x)
    elif type(x) is int:
      #print("s")
      x=str(x)
      strrl.append(x)

    elif type(x) is list:
      #print("l")
      for m in x:
          x=str(m)
          strrl.append(x)
    else:
      for m in x:
        #print(6)
        strrl.append(str(m))
  mols=[]
  for i in strrl:
      mol = Chem.MolFromSmiles(i)
      mols.append(mol)

  if len(mols)>0:
    r = rdFMCS.FindMCS(mols)
    m1 = Chem.MolFromSmarts(r.smartsString)
    m= Draw.MolToImage(m1, legend="MCS1")
  return Draw.MolToImage(m1, legend="MCS1")
#print(Maximum_common_substructure(['C(=O)[OH]','CC(=O)O', 'CC(=O)']))

def chirality_by_smiles(*d):

    IPythonConsole.drawOptions.addAtomIndices = True
    IPythonConsole.drawOptions.addStereoAnnotation = True

    strrl=[]
    for x in d:
        if type(x) is str:
          #print("s")
          x=str(x)
          strrl.append(x)
        elif type(x) is int:
          #print("s")
          x=str(x)
          strrl.append(x)

        elif type(x) is list:
          #print("l")
          for m in x:
              x=str(m)
              strrl.append(x)
        else:
            for m in x:
                x=str(m)
                strrl.append(x)

    for i in strrl:

        m = Chem.MolFromSmiles(i)
        print(Chem.FindMolChiralCenters(m,force=True,includeUnassigned=True,useLegacyImplementation=True))
        display(m)
    return
#chirality_by_smiles("C[C@H]1CCC[C@@H](C)[C@@H]1Cl")

def Identifying_Double_Bond_Stereochemistry(*d):
    strrl=[]
    for x in d:
        if type(x) is str:
          #print("s")
          x=str(x)
          strrl.append(x)
        elif type(x) is int:
          #print("s")
          x=str(x)
          strrl.append(x)

        elif type(x) is list:
          #print("l")
          for m in x:
              x=str(m)
              strrl.append(x)
        else:
            for m in x:
                x=str(m)
                strrl.append(x)

    for i in strrl:

        IPythonConsole.molSize = 250,250
        mol = Chem.MolFromSmiles(i)
        display(mol)
        # Using GetStereo()
        for b in mol.GetBonds():
            print(b.GetBeginAtomIdx(),b.GetEndAtomIdx(),
                  b.GetBondType(),b.GetStereo())
    return
#Identifying_Double_Bond_Stereochemistry(["C\C=C(/F)\C(=C\F)\C=C","C\C=C(/F)\C(=C\F)\C=C"])

def Identify_bond_type_by_smile(*d):
    strrl=[]
    for x in d:
        if type(x) is str:
          #print("s")
          x=str(x)
          strrl.append(x)
        elif type(x) is int:
          #print("s")
          x=str(x)
          strrl.append(x)

        elif type(x) is list:
          #print("l")
          for m in x:
              x=str(m)
              strrl.append(x)
        else:
            for m in x:
                x=str(m)
                strrl.append(x)

    for i in strrl:
        IPythonConsole.molSize = 250,250
        mol = Chem.MolFromSmiles(i)
        mol
        print(mol)

        display(mol)
        # Using GetStereo()
        for b in mol.GetBonds():
            #print(mol.GetBonds)

            #print(b)
            print(b.GetBeginAtomIdx(),b.GetEndAtomIdx(),
                  b.GetBondType(),b.GetStereo())
    return
#Identify_bond_type_by_smile(["CCCO" ,"CCCO"])

def higlight_sepcific_atom_by_smiles(b,*d):
    strrl=[]
    for x in d:
        if type(x) is str:
          #print("s")
          x=str(x)
          strrl.append(x)
        elif type(x) is int:
          #print("s")
          x=str(x)
          strrl.append(x)

        elif type(x) is list:
          #print("l")
          for m in x:
              x=str(m)
              strrl.append(x)
        else:
            for m in x:
                x=str(m)
                strrl.append(x)

    for i in strrl:

        m = Chem.MolFromSmiles(i)
        substructure = Chem.MolFromSmarts(b)
        print(m.GetSubstructMatches(substructure))
        display(m)
    return
#higlight_sepcific_atom_by_smiles('C(=O)O','c1cc(C(=O)O)c(OC(=O)C)cc1','CCCC(=O)O', 'CCCCCCCCCCCCCCCCCCC(=O)O')
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import IPythonConsole
IPythonConsole.molSize = 250,250
IPythonConsole.molSize = 600,600
def find_Gasteiger_Charges(*d):
    strrl=[]
    for x in d:
        if type(x) is str:
          #print("s")
          x=str(x)
          strrl.append(x)
        elif type(x) is int:
          #print("s")
          x=str(x)
          strrl.append(x)

        elif type(x) is list:
          #print("l")
          for m in x:
              x=str(m)
              strrl.append(x)
        else:
            for m in x:
                x=str(m)
                strrl.append(x)

    for i in strrl:

        m = Chem.MolFromSmiles(i)
        AllChem.ComputeGasteigerCharges(m)
        display(m)
        m2 = Chem.Mol(m)
        for at in m2.GetAtoms():
            lbl = '%.2f'%(at.GetDoubleProp("_GasteigerCharge"))
            at.SetProp('atomNote',lbl)
        display(m2)
    return
#find_Gasteiger_Charges('C(=O)O',['c1cc(C(=O)O)c(OC(=O)C)cc1','CCCC(=O)O', 'CCCCCCCCCCCCCCCCCCC(=O)O'])
def draw_list_of_smile(*d):
    strrl=[]
    for x in d:
        if type(x) is str:
          #print("s")
          x=str(x)
          strrl.append(x)

        elif type(x) is int:
          #print("n")
          x=str(x)
          strrl.append(x)
        elif type(x) is list:
          #print("l")
          for m in x:
              x=str(m)
              strrl.append(x)
        else:
          #print("l")
          for m in x:
              x=str(m)
              #print(x)

    mol_list = [Chem.MolFromSmiles(smiles) for smiles in strrl]
    m=Chem.Draw.MolsToGridImage(mol_list)
    #print(m)
    return (m)
#draw_list_of_smile( [ 'C', 'CC', 'CCC', 'CCCC', 'CCCCC', 'C1CCCCC1' ])
def view_difference_by_smiles(mol1, mol2):
    mol1= Chem.MolFromSmiles(mol1)
    mol2= Chem.MolFromSmiles(mol2)
    mcs = rdFMCS.FindMCS([mol1,mol2])
    mcs_mol = Chem.MolFromSmarts(mcs.smartsString)
    match1 = mol1.GetSubstructMatch(mcs_mol)
    target_atm1 = []
    for atom in mol1.GetAtoms():
        if atom.GetIdx() not in match1:
            target_atm1.append(atom.GetIdx())
    match2 = mol2.GetSubstructMatch(mcs_mol)
    target_atm2 = []
    for atom in mol2.GetAtoms():
        if atom.GetIdx() not in match2:
            target_atm2.append(atom.GetIdx())
    return Draw.MolsToGridImage([mol1, mol2],highlightAtomLists=[target_atm1, target_atm2])
#view_difference("CO","CN")

def virtual_screening(file_ism,*colname):
    #colnames = ['smiles','dat', 'id']
    colnames =[]
    for i in colname:
      colnames.append(i)

    df_act = pd.read_csv(file_ism, sep=" ", names=colnames)
    #df_act.head(5)
    smiles_act = df_act.smiles.to_list()

    prolog = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    cids_hit = dict()

    for idx, mysmiles in enumerate(smiles_act) :

        mydata = { 'smiles' : mysmiles }
############################################################################# Similarity Search against PubChem
        url = prolog + "/compound/fastsimilarity_2d/smiles/cids/txt"
        res = requests.post(url, data=mydata)

        if ( res.status_code == 200 ) :
            cids = res.text.split()
            cids = [ int(x) for x in cids ]    # Convert CIDs from string to integer.
        else :
            print("Error at", idx, ":", df_act.loc[idx,'id'], mysmiles )
            print(res.status_code)
            print(res.content)

        for mycid in cids:
            cids_hit[mycid] = cids_hit.get(mycid, 0) + 1
########################################################################### 3. Exclude the query compounds from the hits
        time.sleep(0.2)
    cids_query = dict()
    for idx, mysmiles in enumerate(smiles_act) :
        mydata = { 'smiles' : mysmiles }
        url = prolog + "/compound/fastidentity/smiles/cids/txt?identity_type=same_connectivity"
        res = requests.post(url, data=mydata)
        if ( res.status_code == 200 ) :
            cids = res.text.split()
            cids = [ int(x) for x in cids]
        else :
            print("Error at", idx, ":", df_act.loc[idx,'id'], mysmiles )
            print(res.status_code)
            print(res.content)
        for mycid in cids:
            cids_query[mycid] = cids_query.get(mycid, 0) + 1
        time.sleep(0.2)
    for mycid in cids_query.keys() :

        cids_hit.pop(mycid, None)

################################################################ 4. Filtering out non-drug-like compounds
    chunk_size = 100
    if ( len(cids_hit) % chunk_size == 0 ) :
        num_chunks = len(cids_hit) // chunk_size
    else :
        num_chunks = len(cids_hit) // chunk_size + 1
    cids_list = list(cids_hit.keys())
    #print("# Number of chunks:", num_chunks )

    csv = ""   #sets a variable called csv to save the comma separated output

    for i in range(num_chunks) :
        #print(i, end=" ")
        idx1 = chunk_size * i
        idx2 = chunk_size * (i + 1)
        cids_str = ",".join([ str(x) for x in cids_list[idx1:idx2] ]) # build pug input for chunks of data
        url = prolog + "/compound/cid/" + cids_str + "/property/HBondDonorCount,HBondAcceptorCount,MolecularWeight,XLogP,CanonicalSMILES,IsomericSMILES/csv"
        res = requests.get(url)
        if ( i == 0 ) : # if this is the first request, store result in empty csv variable
            csv = res.text
        else :          # if this is a subsequent request, add the request to the csv variable adding a new line between chunks
            csv = csv + "\n".join(res.text.split()[1:]) + "\n"
        time.sleep(0.2)

    #print(csv)
#########################################################Downloaded data (in CSV) are loaded into a pandas data frame.
    csv_file = StringIO(csv)

    df_raw = pd.read_csv(csv_file, sep=",")

    #df_raw.shape    # Show the shape (dimesnion) of the data frame
    df_freq = pd.DataFrame( cids_hit.items(), columns=['CID','HitFreq'])
    df = df_raw.join(df_freq.set_index('CID'), on='CID')## Create a new data frame called "df" by joining the df and df_freq data frames
    df = df[ ( df['HBondDonorCount'] <= 5) &
             ( df['HBondAcceptorCount'] <= 10 ) &
             ( df['MolecularWeight'] <= 500 ) &
             ( df['XLogP'] < 5 ) ]
################################################################################### Draw the structures of the top 10 compounds
    print("the top 10 unique for those compounds that satisfy all criteria of Lipinski's rule of five")

    cids_top = df.sort_values(by=['HitFreq', 'CID'], ascending=False).head(10).CID.to_list()
    mols = []
    for mycid in cids_top :
        mysmiles = df[ df.CID==mycid ].IsomericSMILES.item()
        mol = Chem.MolFromSmiles( mysmiles )
        Chem.FindPotentialStereoBonds(mol)    # Identify potential stereo bonds!
        mols.append(mol)
    mylegends = [ "CID " + str(x) for x in cids_top ]
    img = Draw.MolsToGridImage(mols, molsPerRow=2, subImgSize=(400,400), legends=mylegends)
    display(img)
################################################################ 6. Extract unique compounds in terms of canonical SMILES
    canonical_smiles = df.CanonicalSMILES.unique()
    idx_to_include = []
    for mysmiles in canonical_smiles :
        myidx = df[ df.CanonicalSMILES == mysmiles ].index.to_list()[0]
        idx_to_include.append( myidx )
    df['Include'] = 0
    #df['Include'].sum()
    df.loc[idx_to_include,'Include'] = 1
    #df['Include'].sum()
    cids_top = df[ df['Include'] == 1].sort_values(by=['HitFreq', 'CID'], ascending=False).head(10).CID.to_list()
    ########################################################### Create a new column 'Include' Now draw the top 10 unique compounds
    print("the top 10 unique compounds in terms of canonical SMILES")
    mols = []
    for mycid in cids_top :
        mysmiles = df[ df.CID==mycid ].IsomericSMILES.item()
        mol = Chem.MolFromSmiles( mysmiles )
        Chem.FindPotentialStereoBonds(mol)    # Identify potential stereo bonds!
        mols.append(mol)

    mylegends = [ "CID " + str(x) for x in cids_top ]
    img = Draw.MolsToGridImage(mols, molsPerRow=2, subImgSize=(400,400), legends=mylegends)
    display(img)
    ############################################################# 7. Saving molecules in files
    for idx, mycid in enumerate( cids_top ) :
        if idx == 3 :
            break
        mysmiles = df[ df['CID'] == mycid ].IsomericSMILES.item()
        mymol = Chem.MolFromSmiles(mysmiles)
        mymol = Chem.AddHs(mymol)
        AllChem.EmbedMolecule(mymol)
        AllChem.MMFFOptimizeMolecule(mymol)

        filename = "pygm_lig" + str(idx) + "_" + str(mycid) + ".mol"
        Chem.MolToMolFile(mymol, filename)
        df.to_csv('Virtual_Screening.csv')
        print("Now, you can Virtual_Screening.csv file in your evice")
    return  df.to_csv('Virtual_Screening.csv')
#virtual_screening("pygm_1c8k_actives.ism","smiles",'dat', 'id')

