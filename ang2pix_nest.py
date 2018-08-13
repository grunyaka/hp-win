import numpy as np
import math

def mk_xy2pix(x2pix, y2pix):
    for i in range(127):
        x2pix[i] = 0
    for I in range(1,128):
        J  = I-1#!pixel numbers
        K  = 0
        IP = 1
        while(J!=0):
            ID = int(math.fmod(J, 2))
            J = J / 2
            K = IP * ID + K
            IP = IP * 4
        x2pix[I - 1] = K
        y2pix[I - 1] = 2 * K
def ang2pix_nest(nside, theta, phi):
    piover2 = 0.5 * math.pi; twopi = 2.0 * math.pi
    ns_max = 8192
    x2pix = np.zeros(128)
    y2pix = np.zeros(128)
    setup_done = 0

    if ( setup_done==0 ):
        mk_xy2pix(x2pix, y2pix)
        setup_done = 1
    z  = math.cos(theta)
    za = math.fabs(z)
    z0 = 2. / 3.
    if ( phi >= twopi ):
        phi = phi - twopi
    if ( phi < 0. ):
        phi = phi + twopi
    tt = phi / piover2# in[0, 4[* /

    if ( za <= z0 ): # equatorial region * /
        #/ * (the index of edge lines increase when the longitude=phi goes up) * /
        jp = int(math.floor(ns_max * (0.5 + tt - z * 0.75)))# ascending edge line index * /
        jm = int(math.floor(ns_max * (0.5 + tt + z * 0.75)))# descending edge line index * /
        #/ * finds the face * /
        ifp = jp / ns_max# / * in {0, 4} * /
        ifm = jm / ns_max

        if ( ifp == ifm ):
            face_num = int(math.fmod(ifp, 4)) + 4# faces 4 to 7 * /
        elif( ifp < ifm ):
            face_num = int(math.fmod(ifp, 4))# (half-)faces 0 to 3 * /
        else:
            face_num = int(math.fmod(ifm, 4)) + 8# (half-)faces 8 to 11 * /

        ix = int(math.fmod(jm, ns_max))
        iy = ns_max - int(math.fmod(jp, ns_max)) - 1

    else: # * polar region, za > 2 / 3 * /
        ntt = int(math.floor(tt))
        if ( ntt >= 4 ):
            ntt = 3
        tp = tt - ntt
        tmp = math.sqrt( 3. * (1. - za) )# in]0, 1] * /
        jp = int(math.floor( ns_max * tp * tmp ))

        #/ * that one goes away of the closest pole * /
        jm = int(math.floor( ns_max * (1. - tp) * tmp ))
        if(jp < (ns_max-1)):
            jp = int(jp)
        else:
            jp = int(ns_max - 1)

        if(jm < (ns_max - 1)):
            jm = int(jm)
        else:
            jm = int(ns_max - 1)

        if (z >= 0):
            face_num = ntt# / * in {0, 3} * /
            ix = ns_max - jm - 1
            iy = ns_max - jp - 1
        else:
            face_num = ntt + 8# in {8, 11} * /
            ix = jp
            iy = jm
    ix_low = int(math.fmod(ix, 128))
    ix_hi = int(ix / 128)
    iy_low = int(math.fmod(iy, 128))
    iy_hi = int(iy / 128)

    ipf = (x2pix[ix_hi] + y2pix[iy_hi]) * (128 * 128) + (x2pix[ix_low] + y2pix[iy_low])
    ipf = int(ipf /math.pow(ns_max / nside, 2))
    return int(ipf + face_num * math.pow(nside, 2))

nside=8# min is 1, max is 2^29
theta=60#latitude in degree
phi=30#longitude in degree

theta=math.radians(theta)
phi=math.radians(phi)

ipix=ang2pix_nest(nside,theta,phi)#latitude in longitude should be in radians
print(ipix)
print(theta,phi)

