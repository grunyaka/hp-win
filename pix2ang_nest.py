import numpy as np
import math

def mk_pix2xy(pix2x,pix2y):
    #pix2x = np.zeros(1024, dtype=int)
    #pix2y = np.zeros(1024, dtype=int)
    for i in range(1024):
        pix2x[i] = 0
    for kpix in range(1024):
        jpix = kpix
        IX = 0
        IY = 0
        IP = 1# // ! bit position( in x and y)
        while (jpix != 0):# ! go through all the bits
            ID = int(math.fmod(jpix, 2))# ! bit value ( in kpix), goes in ix
            jpix = jpix / 2
            IX = ID * IP+IX
            ID = int(math.fmod(jpix, 2))#! bit value ( in kpix), goes in iy
            jpix = jpix / 2
            IY = ID * IP+IY
            IP = 2 * IP# ! next bit ( in x and y)
        pix2x[kpix] = IX# ! in 0, 31
        pix2y[kpix] = IY# ! in 0, 31
def pix2ang_nest(nside,ipix):
    piover2=0.5 * math.pi
    pix2x = np.zeros(1024,dtype=int);pix2y = np.zeros(1024,dtype=int)
    # common / pix2xy / pix2x, pix2y
    jrll = np.array([2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4],dtype=int)
    jpll = np.array([1, 3, 5, 7, 0, 2, 4, 6, 1, 3, 5, 7],dtype=int)
    #npix = 12 * nside * nside;

    #/ * initiates the array for the pixel number -> (x, y) mapping * /
    if ( pix2x[1023] <= 0 ):
        mk_pix2xy(pix2x, pix2y)

    fn = 1. * nside
    fact1 = 1. / (3. * fn * fn)
    fact2 = 2. / (3. * fn)
    nl4   = 4 * nside

    # c     finds the face, and the number in the face
    npface = nside * nside

    face_num = int(ipix / npface)# face number in {0, 11}
    ipf = int(math.fmod(ipix, npface))# pixel number in the face {0, npface-1}

    # c     finds the x, y on the face (starting from the lowest corner)
    # c     from the pixel number
    ip_low = int(math.fmod(ipf, 1024))# ! content of the last 10 bits
    ip_trunc = int(ipf / 1024)# truncation of the last 10 bits
    ip_med = int(math.fmod(ip_trunc, 1024))# content of the next 10 bits
    ip_hi  =  int(ip_trunc / 1024)# content of the high weight 10 bits

    ix = 1024 * pix2x[ip_hi] + 32 * pix2x[ip_med] + pix2x[ip_low]
    iy = 1024 * pix2y[ip_hi] + 32 * pix2y[ip_med] + pix2y[ip_low]

    # c     transforms this in (horizontal, vertical) coordinates
    jrt = ix + iy# 'vertical' in {0, 2 * (nside-1)}
    jpt = ix - iy# 'horizontal' in {-nside+1, nside-1}
    jr =  jrll[face_num] * nside - jrt - 1
    nr = nside# equatorial region (the most frequent)
    z  = (2 * nside-jr) * fact2
    kshift = int(math.fmod(jr - nside, 2))
    if ( jr < nside ):# then     ! north pole region
        nr = jr
        z = 1. - nr * nr * fact1
        kshift = 0
    else:
        if ( jr > 3 * nside ): # then ! south pole region
            nr = nl4 - jr
            z = - 1. + nr * nr * fact1
            kshift = 0
    theta = math.acos(z)

    # c     computes the phi coordinate on the sphere, in[0, 2Pi]
    # jp = (jpll[face_num+1] * nr + jpt + 1 + kshift) / 2; // ! 'phi' number in the ring in {1, 4 * nr}
    jp = (jpll[face_num] * nr + jpt + 1 + kshift) / 2
    if ( jp > nl4 ):
        jp = jp - nl4
    if ( jp < 1 ):
        jp = jp + nl4
    phi = (jp - (kshift+1) * 0.5) * (piover2 / nr)
    return theta, phi

nside=8# min is 1, max is 2^29
ipix=33# min 0, max 12*(nside^2)

(theta,phi)=pix2ang_nest(nside,ipix)
print(ipix)
print(theta,phi)