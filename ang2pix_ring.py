import math

def ang2pix_ring(nside,theta, phi):
    piover2 = 0.5 * math.pi
    twopi = 2.0 * math.pi
    z0 = 2.0 / 3.0
    z = math.cos(theta)
    za =math.fabs(z)
    if (phi >= twopi):
        phi = phi - twopi
    if (phi < 0.):
        phi = phi + twopi
    tt = phi / piover2# ! in [0, 4)
    nl2 = 2 * nside
    nl4 = 4 * nside
    ncap = nl2 * (nside - 1)# ! number of pixels in the north polar cap
    npix = 12 * nside * nside
    if (za <= z0):
        jp = int(math.floor(nside * (0.5 + tt - z * 0.75)))#index of ascending edge line
        jm = int(math.floor(nside * (0.5 + tt + z * 0.75)))#index of descending edge line
        ir = nside + 1 + jp - jm# in {1, 2n + 1}(ring number counted from z=2 / 3)
        kshift = 0
        if (math.fmod(ir, 2) == 0.):
            kshift = 1# kshift = 1 if ir even, 0 otherwise
        ip = int(math.floor((jp + jm - nside + kshift + 1) / 2)) + 1# ! in {1, 4n}
        if (ip > nl4):
            ip = ip - nl4
        ipix1 = ncap + nl4 * (ir - 1) + ip
    else:
        tp = tt - math.floor(tt)#MOD(tt, 1.d0)
        tmp = math.sqrt(3. * (1. - za))
        jp = int(math.floor(nside * tp * tmp))# ! increasing edge line index
        jm = int(math.floor(nside * (1. - tp) * tmp))# ! decreasing edge line index
        ir = jp + jm + 1# ! ring number counted from the closest pole
        ip = int(math.floor(tt * ir)) + 1 #! in {1, 4 * ir}
        if (ip > 4 * ir):
            ip = ip - 4 * ir
        ipix1 = 2 * ir * (ir - 1) + ip
        if (z <= 0.):
            ipix1 = npix - 2 * ir * (ir + 1) + ip
    return ipix1 - 1 #! in {0, npix - 1}

nside=8# min is 1, max is 2^29
theta=60#latitude in degree
phi=30#longitude in degree


theta=math.radians(theta)
phi=math.radians(phi)
ipix=ang2pix_ring(nside, theta, phi)# latitude and longitude should be in radians
print(ipix)