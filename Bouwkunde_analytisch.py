# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 09:11:07 2023

@author: joeri
"""
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def main():
                                #constanten
    #hoeken  
    boven_buitenhoek = 76                             
    boven_binnenhoek = 83

    onder_buitenhoek = 69                          
    onder_binnenhoek = 58
    
    #dimensies pilaar
    breedte_onder = 24
    breedte_midden = 12
    breedte_boven = 6
    hoogte = 96
    
        #matrices
    
    #coordinaten aangrijppunten touwen
    nullenxr = np.zeros(18)
    nullenyr = np.zeros(18)
    nullenxl = np.zeros(18)
    nullenyl = np.zeros(18) 
    
    #hoeken tussen touwen en grond
    hoeken_rechts = np.zeros(9)
    hoeken_links = np.zeros(9)    
    
    
    # aantal kabels - 1 
    aantal = 8
    delta_kabels = 20
    
    # lengte schuine zijden 
    lengte_schuin_rechts = (hoogte/2)/math.cos((90-boven_buitenhoek)*np.pi/180)
    delta_schuin_rechts = lengte_schuin_rechts/aantal
    
    lengte_schuin_links = (hoogte/2)/math.sin(boven_binnenhoek*np.pi/180)
    delta_schuin_links = lengte_schuin_links/aantal
    
    # beslasting
    g = 9.81
    totaal_gewicht = 200#kg
    gewicht_per_kant = totaal_gewicht/2 #kg
    kracht_per_kant = gewicht_per_kant*g #N
    belasting_per_kant = kracht_per_kant/200 #N/cm
    
    #plotten pilaren
    fig, axs = plt.subplots(1, 2, figsize=(30, 12))
    
    pilaar_rechtsx,pilaar_rechtsy = plotten_pilaar_rechts(hoogte, onder_binnenhoek, boven_binnenhoek, breedte_boven, breedte_midden, breedte_onder, axs[0])
    pilaar_linksx,pilaar_linksy = plotten_pilaar_links(hoogte, onder_buitenhoek, boven_binnenhoek,boven_buitenhoek, breedte_boven, onder_binnenhoek, breedte_midden,axs[1],breedte_onder)

    # berekenen lengtes kabels
    sol1,sol2,x1,y1,somR = lengtes_kabels_rechts(nullenxr,nullenyr, hoogte, boven_binnenhoek, boven_buitenhoek, onder_binnenhoek, onder_buitenhoek, breedte_boven, breedte_midden, breedte_onder, aantal,axs[0],delta_schuin_rechts,delta_schuin_links,delta_kabels)
    sol3,sol4,x2,y2,somL = lengtes_kabels_links(nullenxl, nullenyl, hoogte, boven_binnenhoek, boven_buitenhoek, onder_binnenhoek, onder_buitenhoek, breedte_boven, breedte_midden, breedte_onder, aantal, axs[1], delta_schuin_rechts, delta_schuin_links,delta_kabels)
    sol5,sol6 = hoeken(sol2,sol4,sol1,sol3,hoeken_links,hoeken_rechts)
    
    kabelspanning_rechts,vertR,horR = krachtverloop(belasting_per_kant,x1,pilaar_rechtsx,axs[0],sol5,y1,delta_kabels,breedte_onder)
    kabelspanning_links,vertL,horL = krachtverloop(belasting_per_kant,x2,pilaar_linksx,axs[1],sol6,y2,delta_kabels,breedte_onder)
    



    return None

def plotten_pilaar_rechts(hoogte,onder_binnenhoek,boven_binnenhoek,breedte_boven,breedte_midden,breedte_onder,ax):
    
    
    rect1 = patches.Rectangle((breedte_onder, -20), 26, 20, hatch='/', fill=False)
    rect2 = patches.Rectangle((breedte_onder+226,-20),26,20, hatch = '/', fill = False)
    ax.add_patch(rect1)
    ax.add_patch(rect2)

    
    
    x_rechts = np.array([0,(hoogte/2)/math.tan(onder_binnenhoek*np.pi/180),(hoogte/2)/math.tan(onder_binnenhoek*np.pi/180)-(hoogte/2)*math.cos(boven_binnenhoek*np.pi/180),(hoogte/2)/math.tan(onder_binnenhoek*np.pi/180)-(hoogte/2)*math.cos(boven_binnenhoek*np.pi/180)+breedte_boven,(hoogte/2)/math.tan(onder_binnenhoek*np.pi/180)+breedte_midden,breedte_onder])
    y_rechts = np.array([0,hoogte/2,hoogte,hoogte,hoogte/2,0]) 
    for i in range(len(x_rechts)):
        if i <3:
            ax.text(-20, y_rechts[i], f"({x_rechts[i]:.2f}, {y_rechts[i]:.2f})", fontsize=8, verticalalignment='bottom', horizontalalignment='left',color = 'brown')
        else:
            ax.text(-20, y_rechts[i]-10, f"({x_rechts[i]:.2f}, {y_rechts[i]:.2f})", fontsize=8, verticalalignment='bottom', horizontalalignment='left',color = 'brown')
    ax.set_title('pilaar rechts')
    ax.plot(x_rechts,y_rechts,color = 'brown')
    ax.plot([-10,300],[0,0],color = 'orange')
    ax.text(290,5,'wegdek',color = 'orange')
    ax.text(317,100,'afstanden in cm',fontsize = 15)
    return x_rechts,y_rechts
def plotten_pilaar_links(hoogte,onder_buitenhoek,boven_binnenhoek,boven_buitenhoek,breedte_boven,onder_binnenhoek,breedte_midden,ax,breedte_onder):
    
    rect1 = patches.Rectangle((breedte_onder, -20), 26, 20, hatch='/', fill=False)
    rect2 = patches.Rectangle((breedte_onder+226,-20),26,20, hatch = '/', fill = False)
    ax.add_patch(rect1)
    ax.add_patch(rect2)

    x_links = np.array([(hoogte/2)*math.tan((90-onder_buitenhoek)*np.pi/180),0,(hoogte/2)*math.tan((90-boven_buitenhoek)*np.pi/180),(hoogte/2)*math.tan((90-boven_buitenhoek)*np.pi/180)+breedte_boven,breedte_midden,breedte_midden+(hoogte/2)/math.tan(onder_binnenhoek*np.pi/180)])
    y_links = np.array([0,(hoogte/2),(hoogte),(hoogte),(hoogte/2),0])
    for i in range(len(x_links)):
        if i <3:
            ax.text(-30, y_links[i], f"({x_links[i]:.2f}, {y_links[i]:.2f})", fontsize=8, verticalalignment='bottom', horizontalalignment='left',color = 'brown')
        else:
            ax.text(-30, y_links[i]-10, f"({x_links[i]:.2f}, {y_links[i]:.2f})", fontsize=8, verticalalignment='bottom', horizontalalignment='left',color = 'brown')
    ax.plot(x_links,y_links,color = 'brown')
    ax.set_title('pilaar links')
    ax.plot([-10,300],[0,0],color = 'orange')
    ax.text(290,5,'wegdek',color = 'orange')
    return x_links,y_links

def lengtes_kabels_rechts(nullenx,nulleny,hoogte,boven_binnenhoek,boven_buitenhoek,onder_binnenhoek,onder_buitenhoek,breedte_boven,breedte_midden,breedte_onder,aantal,ax,delta_schuin_rechts,delta_schuin_links,delta_kabels):
    lengtes_kabels_rechts = np.zeros(aantal+1)
    delta_horizontaal_rechts = np.zeros(aantal+1)
    
    for i in range(1+aantal):
        x_touwen = (breedte_onder + (hoogte/2)/math.tan(onder_buitenhoek*np.pi/180)) - delta_schuin_rechts*np.tan((90-boven_buitenhoek)*np.pi/180)*(i)
        y_touwen = (hoogte/2) + ((hoogte/2)/aantal)*(i)
        nullenx[i] = x_touwen
        nulleny[i] = y_touwen
    for i in range(1+aantal, len(nullenx)):
        nullenx[i] = (hoogte/2) + delta_kabels*(i-(aantal))
        
    for i in range(0, len(nullenx) - 9):
        x1 = nullenx[i]
        y1 = nulleny[i]
        x2 = nullenx[i + 9]
        y2 = nulleny[i + 9]
        lengtes_kabels_rechts[i] =  math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        ax.plot([x1, x2], [y1, y2], 'red')
        
    for i in range(len(delta_horizontaal_rechts)):
        delta_horizontaal_rechts[i] = nullenx[i+9]-nullenx[i]
    ax.scatter(nullenx,nulleny,color='red')
    for i in range(len(nullenx)):
        if i < 9 :
            ax.text(np.round(nullenx[i])-20, np.round(nulleny[i]), f"({np.round(nullenx[i])})",color = 'blue')
        else:
            ax.text(np.round(nullenx[i]), np.round(nulleny[i])-10, f"({np.round(nullenx[i])})",color = 'blue')
    ax.axis('equal')
    som = np.sum(lengtes_kabels_rechts)

    return delta_horizontaal_rechts,lengtes_kabels_rechts,nullenx,nulleny,som
def lengtes_kabels_links(nullenx,nulleny,hoogte,boven_binnenhoek,boven_buitenhoek,onder_binnenhoek,onder_buitenhoek,breedte_boven,breedte_midden,breedte_onder,aantal,ax,delta_schuin_rechts,delta_schuin_links,delta_kabels):
    lengtes_kabels_links = np.zeros(aantal+1)
    delta_horizontaal_links = np.zeros(aantal+1)
    for i in range(1+aantal):
        x_touwen = breedte_midden + delta_schuin_links/np.tan((boven_binnenhoek)*np.pi/180)*(i)
        y_touwen = (hoogte/2) + ((hoogte/2)/aantal)*(i)
        nullenx[i] = x_touwen
        nulleny[i] = y_touwen
    for i in range(1+aantal, len(nullenx)):
        nullenx[i] = 24+(hoogte/2)*math.tan((90-onder_buitenhoek)*np.pi/180) + delta_kabels*(i-(aantal)) 
    ax.scatter(nullenx,nulleny,color='red')
    for i in range(0, len(nullenx) - 9):
        x1 = nullenx[i]
        y1 = nulleny[i]
        x2 = nullenx[i + 9]
        y2 = nulleny[i + 9]
        lengtes_kabels_links[i] =  math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        ax.plot([x1, x2], [y1, y2], 'r')
    for i in range(len(delta_horizontaal_links)):
        delta_horizontaal_links[i] = nullenx[i+9]-nullenx[i]
    for i in range(len(nullenx)):
        if i < 9:
            ax.text(np.round(nullenx[i])-20, np.round(nulleny[i]), f"({np.round(nullenx[i])})",color = 'blue')
        else:
            ax.text(np.round(nullenx[i]), np.round(nulleny[i])-10, f"({np.round(nullenx[i])})",color = 'blue')
 
    ax.axis('equal')
    som = np.sum(lengtes_kabels_links)
    return delta_horizontaal_links,lengtes_kabels_links,nullenx,nulleny,som

def hoeken(lengtes_rechts, lengtes_links, x_coord_rechts,x_coord_links,hoeken_links,hoeken_rechts):
    for i in range(len(hoeken_rechts)):
        theta1 = math.acos(x_coord_rechts[i] / lengtes_rechts[i])
        theta_degrees1 = math.degrees(theta1)
        hoeken_rechts[i] = theta_degrees1
        
        theta2 = math.acos(x_coord_links[i] / lengtes_links[i])
        theta_degrees2 = math.degrees(theta2)
        hoeken_links[i] = theta_degrees2
    return hoeken_rechts,hoeken_links

    
    
    
    
    return
 
def krachtverloop(belasting_per_kant,nullenx,pilaarx,ax,hoeken,nulleny,delta_kabels,breedte_onder):
    

    hor_kracht = np.zeros(9)
    krachtverloop = np.zeros(11)
    spanning = np.zeros(11)
    kracht = np.copy(krachtverloop)
    krachtverloop[0] = nullenx[9]-delta_kabels
    ax.text(np.round(krachtverloop[0]),-10, f"({np.round(krachtverloop[0])})",color = 'blue')
    
    for i in range(9,len(nullenx)):
        krachtverloop[i-8] = nullenx[i]
    krachtverloop[10] = delta_kabels + krachtverloop[9]
    ax.text(np.round(krachtverloop[10]),-10, f"({np.round(krachtverloop[10])})",color = 'green')
    
    for i in range(len(kracht)-1):
        afstand = krachtverloop[i+1] - krachtverloop[i]  
        force = afstand * belasting_per_kant / 2.  
        kracht[i] +=force
        kracht[i+1]+=force
        
    for x, k in zip(krachtverloop, kracht):
        if x == krachtverloop[-1]:
            ax.arrow(x, k/10+5, 0,-k/10 , head_width=5, head_length=5, color='green')
            ax.text(np.round(x-0.2), -25, f'{np.round(k)} N', color='green')
        else:
            ax.arrow(x, k/10+5, 0,-k/10 , head_width=5, head_length=5, color='blue')
            ax.text(np.round(x-0.2), -25, f'{np.round(k)} N', color='blue')
    
    
    for i in range(len(hor_kracht)):
        hor_kracht[i] = kracht[i+1]/math.tan(hoeken[i]*np.pi/180)
    
    
    
    som = kracht[0]
    for i in range(1,len(krachtverloop)-1):
        spanning[i] = kracht[i]/math.sin(hoeken[i-1]*np.pi/180)
        som+= spanning[i]*math.sin(hoeken[i-1]*np.pi/180)
    
    for i in range(9):
        length = spanning[i+1] / 2.5
        dx = length * math.cos(hoeken[i] * np.pi / 180)  
        dy = length * math.sin(hoeken[i] * np.pi / 180)  
        ax.annotate('', xy=(nullenx[i] + dx, nulleny[i] - dy), xytext=(nullenx[i], nulleny[i]) ,arrowprops=dict(arrowstyle='->', shrinkA=0, shrinkB=0, color = 'black'))  
        ax.text(nullenx[i] + dx / 2, nulleny[i] - dy / 2, f'{np.round(spanning[i+1])} N', color = 'black') 
    ax.arrow(3*breedte_onder/2,som/20+10 , 0,-som/20 -5 , head_width=5, head_length=5,color = 'green')
    ax.text(3*breedte_onder/2 - 20, 10, f'{np.round(som)} N',color = 'green') 
        
    return spanning,kracht,hor_kracht




if __name__ == '__main__':
    main() 
