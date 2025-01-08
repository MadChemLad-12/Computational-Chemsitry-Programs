#This will be a calculator for gibbs free energy for ORR 
#Note \u0394 is delta
#If you need help with the calculator read the read.me file or if all else fails message Jack. 

#Associative mechanism
import matplotlib.pyplot as plt
from energydiagram import ED
from collections import defaultdict
from numpy import not_equal

#Basic info
print('Hi there welcome to the ORR Gibbs Free Energy Calculator \n Please make sure everything is in eV as I will not work otherwise. \n')
surf = input('What is the surfaces energy? ')
surf = float(surf)
H2O = input('What is the energy of H2O in vaccum? ')
H2O = int(float(H2O))
H2 = input('What is the energy of H2 in vaccum? ')
H2 = int(float(H2))

#Calaculating Gibb energy value
while True:
    deltaG=input('Would you like the \u0394G value (yes or no)? ')
    if deltaG=='yes':
        O2=input('What is the energy of O2 in vaccum? ')
        O2=int(float(O2))
        print('\u0394G value is ', 2*H2+O2-2*H2O)
        deltaG = 2*H2+O2-2*H2O
        break
    if deltaG != 'yes':
        break

#finding delta of each adsorbate
adsOH=input('What was your Surf-OH total energy? ')
adsOH=float(adsOH)
adsO=input('What was your Surf-O total energy? ')
adsO=float(adsO)
adsOOH=input('What was your Surf-OOH total energy? ')
adsOOH=float(adsOOH)

#Deta of each adsorbate
deltaOH=adsOH-surf+H2O+0.5*H2-2*H2O+0.35
deltaO=adsO-surf+H2O+H2-2*H2O+0.05
deltaOOH=adsOOH-surf+1.5*H2-2*H2O+0.4

print('\n\u0394OH   \u0394O   \u0394OOH at U=0V \n',deltaOH, deltaO, deltaOOH)
print('\u0394OH   \u0394O   \u0394OOH at U=1.23V \n',deltaOH-1.23, deltaO-2.46, deltaOOH-3.69)

#The associative overpotential
while True:
    asso=input('\nWould you like the associative ORR and OER overpotential? ')
    if asso=='yes':
        deltaG1 = round(deltaOH, 4)
        deltaG2 = round(deltaO - deltaOH, 4)
        deltaG3 = round(deltaOOH - deltaO, 4)
        deltaG4 = round(4.92-deltaOOH, 4)
        OERover=(max(deltaG1,deltaG2,deltaG3,deltaG4)-1.23)
        ORRover=(1.23-min(deltaG1,deltaG2,deltaG3,deltaG4))
        print('\n\u0394G1   \u0394G2   \u0394G3   \u0394G4 at U=0V \n',deltaG1,deltaG2,deltaG3,deltaG4)
        print('At U=0V OER Overpotential = ', OERover)
        print('At U=0V ORR Overpotential = ', ORRover, '\n \n')
        print('\u0394G1   \u0394G2   \u0394G3   \u0394G4 at U=1.23V \n', deltaOH-1.23, (deltaO-2.46)-(deltaOH-1.23), (deltaOOH-3.69)-(deltaO-2.46), (deltaOOH-3.69-4.92))
        VOERover=(max(deltaOH-1.23, (deltaO-2.46)-(deltaOH-1.23), (deltaOOH-3.69)-(deltaO-2.46), (deltaOOH-3.69-4.92))-1.23)
        VORRover=(1.23-min(deltaOH-1.23, (deltaO-2.46)-(deltaOH-1.23), (deltaOOH-3.69)-(deltaO-2.46), (deltaOOH-3.69-4.92)))
        print('At U=1.23V OER Overpotential = ', VOERover)
        print('At U=1.23V ORR Overpotential = ', VORRover, '\n\n')   
        #Free energy diagrams
        # Note the code for the diagrams can be found here = #https://github.com/giacomomarchioro/PyEnergyDiagrams
        
        while True:
            diagram = input('Would you like the associative free energy diagrams? ')
            if diagram == 'yes':
                
                #This is to convert to int
                while True:
                    O2=input('If you type "defult" we will use 4.92 eV as the \u0394G value \nWhat is the energy of O2 in vaccum? ')
                    if O2 == "defult":
                        deltaG = 4.92
                        break
                    
                    else: 
                        O2=int(float(O2))
                        deltaG = int(float(2*H2+O2-2*H2O))
                        print('\u0394G value is ', deltaG, '. Idealy it should be close to 4.92')
                        break
                
                deltaG = int(float(deltaG))
                deltaOOH = int(float(deltaOOH))
                deltaOH = int(float(deltaOH))
                deltaO = int(float(deltaO))
                
                print('Blue is U=0V and red is for U=1.23V')
                print("Note: These images are of a low quality and should be used to make better figures!!!\n")
                diagram = ED()
                diagram.add_level(deltaG, 'ΔG',color='b')
                diagram.add_level(0, ' ', 'l', color='r')  #second line is for U=1.23V

                diagram.add_level(deltaOOH,'ΔGOOH',color='b')
                diagram.add_level(deltaOOH-3.69,' ','l',color='r')
                
                diagram.add_level(deltaO,'ΔGO',color='b') #Using 'last'  or 'l' it will be together with the previous level
                diagram.add_level(deltaO-2.46,' ','l',color='r')
                
                diagram.add_level(deltaOH,'ΔGOH',color='b')
                diagram.add_level(deltaOH-1.23,' ','l',color='r')
                
                diagram.add_level(0,'Water',color='b')
                diagram.add_level(0,' ','l',color='r')
                                
                diagram.plot(show_IDs=True)
                diagram.add_link(0,2)
                diagram.add_link(2,4)
                diagram.add_link(4,6)
                diagram.add_link(6,8)
                diagram.add_link(1,3)
                diagram.add_link(3,5)
                diagram.add_link(5,7)
                diagram.add_link(7,8)

                diagram.plot(ylabel="Free Energy (eV)") # this is the default ylabel
                plt.show()
                
                break
                
            if diagram != 'yes':
                break
    break

#The dissociative mechanism
while True: 
    disso=input('\n \nWould you like the dissociative ORR and OER overpotentials? ')
    if disso=='yes':
        deltaG1 = round(deltaOH, 4)
        deltaG2 = round(deltaO - deltaOH, 4)
        deltaG3 = round(4.92- 2 * deltaO, 4)
        OERover=(max(deltaG1,deltaG2,deltaG3)-1.23)
        ORRover=(1.23-min(deltaG1,deltaG2,deltaG3))
        print('\u0394G1   \u0394G2   \u0394G3   at U=0V \n',deltaG1,deltaG2,deltaG3)
        print('At U=0V OER Overpotential = ', OERover)
        print('At U=0V ORR Overpotential = ', ORRover, '\n \n')
        print('\u0394G1   \u0394G2   \u0394G3   at U=1.23V \n', deltaOH-1.23, (deltaO-2.46)-(deltaOH-1.23), -4.92 - (2 * (deltaO-2.46)))
        VOERover = (max((deltaOH-1.23), ((deltaO-2.46)-(deltaOH-1.23)), -4.92 + (2 * (deltaO-2.46)))-1.23)
        VORRover = (1.23-min(deltaOH-1.23, ((deltaO-2.46)-(deltaOH-1.23)), -4.92 + (2 * (deltaO-2.46))))
        print('At U=1.23V OER Overpotential = ', VOERover)
        print('At U=1.23V ORR Overpotential = ', VORRover)          
        #Free energy diagrams     
        while True:
            dissoG=input('\n \nWould you like the dissociative free energy diagrams? ')  # Note the code for the diagrams can be found here = #https://github.com/giacomomarchioro/PyEnergyDiagrams
            if dissoG == 'yes':
                while True:
                    
                        O2=input('If you type "defult" we will use 4.92 eV as the \u0394G value \nWhat is the energy of O2 in vaccum? ')
                        if O2 == "defult":
                            deltaG = 4.92
                            break
                        
                        else: 
                            O2=int(float(O2))
                            deltaG = int(float(2*H2+O2-2*H2O))
                            print('\u0394G value is ', deltaG)
                            break
                    
                deltaG = int(float(deltaG))
                deltaOOH = int(float(deltaOOH))
                deltaOH = int(float(deltaOH))
                deltaO = int(float(deltaO))
                    
                print('Blue is U=0V and red is for U=1.23V')
                print("Note: These images are of a low quality and should be used to make better figures!!!\n")
                diagram = ED()
                diagram.add_level(deltaG, 'ΔG',color='b')
                diagram.add_level(0, ' ', 'l', color='r')  #second line is for U=1.23V

                diagram.add_level(deltaO*2,'O+O',color='b')
                diagram.add_level((deltaO*2)-(4*1.23),' ','l',color='r')
                    
                diagram.add_level(deltaO+deltaOH,'O+OH',color='b') #Using 'last'  or 'l' it will be together with the previous level
                diagram.add_level((deltaO+deltaOH)-(2*1.23+1.23),' ','l',color='r')
                    
                diagram.add_level(deltaO,'O+H2O',color='b')
                diagram.add_level(deltaO-(1.23*2),' ','l',color='r')
                
                diagram.add_level(deltaOH*2,'OH+HO', 'l',color='b')
                diagram.add_level((deltaOH*2)-(1.23*2),' ','l',color='r')
                
                diagram.add_level(deltaOH,'OH+H2O',color='b')
                diagram.add_level(deltaOH-1.23,' ','l',color='r')
                    
                diagram.add_level(0,'Water',color='b')
                diagram.add_level(0,' ','l',color='r')
                                    
                diagram.plot(show_IDs=True)
                diagram.add_link(0,2)
                diagram.add_link(2,4)
                diagram.add_link(4,6)
                diagram.add_link(4,8)
                diagram.add_link(6,10)
                diagram.add_link(8,10)
                diagram.add_link(10,12)
                diagram.add_link(1,3)
                diagram.add_link(3,5)
                diagram.add_link(5,7)
                diagram.add_link(5,9)
                diagram.add_link(7,11)
                diagram.add_link(9,11)
                diagram.add_link(11,12)
                
                diagram.plot(ylabel="Free Energy (eV)") # this is the default ylabel
                plt.show()
                    
                break
                    
            if dissoG != 'yes':
                break
        break
    
    if disso != 'yes':
        break
    
    
    break
    
    
print("All done, Make sure to check your working!! :)")    
