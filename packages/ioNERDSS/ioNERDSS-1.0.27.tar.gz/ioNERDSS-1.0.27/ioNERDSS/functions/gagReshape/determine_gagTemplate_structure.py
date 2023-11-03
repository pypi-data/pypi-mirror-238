import numpy as np


def determine_gagTemplate_structure(numGag, positionsVec):
    """
    Determine the template structure of the gags, which is the average structure of the first gag.
    The template structure is used to determine the internal basis system of each gag, and the internal
    coordinates of each interface in the internal basis system.

    Parameters:
        numGag (int): number of gags
        positionsVec (np.array): positions of all atoms in the system, rowvec
    
    Returns:
        template (np.array): the template structure of the gags, rowvec
    """

    internalBasis = np.zeros([3,3,numGag]) # 18 gags, each gag has 3 vectors of internal basises, rowvec
    coefficients = np.zeros([5,3,numGag])  # internal coords of interfaces in the internal basis system
    # set up the internal coord system for each gag: basis vec1, vec2, vec3 
    # and then calculate the coords of each interface in this internal system: internal coords
    # then the mean value of the internal coords gives the template structure 
    for i in range (0,numGag):
        center = positionsVec[6*i,:]
        interfaces = positionsVec[1+6*i:5+1+6*i,:]
        # determine the three internal basis: vec1, vec2, vec3
        vec1 = center
        vec1 = vec1/np.linalg.norm(vec1) 
        vec2 = interfaces[0,:] - center
        vec3 = np.cross(vec1,vec2)
        vec3 = vec3/np.linalg.norm(vec3)
        vec2 = np.cross(vec3,vec1)
        vec2 = vec2/np.linalg.norm(vec2)
        internalBasis[0,:,i] = vec1
        internalBasis[1,:,i] = vec2
        internalBasis[2,:,i] = vec3
        # calculate the interal coords for the 5 interfaces
        for j in range (0,5):
            p = interfaces[j,:] - center
            A = np.array([vec1, vec2, vec3])
            coeff = np.dot(p, np.linalg.inv(A))
            if (np.linalg.norm(np.dot(coeff,A)-p) > 1e-12) : # check whether correctly calculated!
                print('Wrong calculation of coefficients\n',np.linalg.norm(np.dot(coeff,A)-p))
            coefficients[j,:,i] = coeff
    
    # regularize the gags internal coords
    coeffReg = np.zeros([5,3]) # five sites, each site has 3 coefficients of internal coords
    for i in range(0,5) :
        coeffReg[i,0] = np.mean(coefficients[i,0,:])
        coeffReg[i,1] = np.mean(coefficients[i,1,:])
        coeffReg[i,2] = np.mean(coefficients[i,2,:])

    # using the mean coefficients to calculate the structure of the first gag, and take it as the template
    chosenGagIndex = 0
    vec1 = internalBasis[0,:,chosenGagIndex]
    vec2 = internalBasis[1,:,chosenGagIndex]
    vec3 = internalBasis[2,:,chosenGagIndex]
    center1 = positionsVec[0+6*chosenGagIndex,:]
    template = np.zeros([6,3])
    template[0,:] = center1
    for i in range(0,5):
        template[i+1,:] = coeffReg[i,0] * vec1 + coeffReg[i,1] * vec2 + coeffReg[i,2] * vec3 + center1
    
    return template

