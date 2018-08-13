import math

def pix2ang_ring(nside,ipix):
    npix = 12 * nside * nside# // ! total number of points
    ipix1 = ipix + 1# in {1, npix}
    nl2 = 2 * nside
    nl4 = 4 * nside
    ncap = 2 * nside * (nside - 1)# ! points in each polar cap, = 0 for nside =1
    fact1 = 1.5 * nside
    fact2 = 3.0 * nside * nside

    if ( ipix1 <= ncap ): #! North Polar cap -------------
        hip   = ipix1 / 2.
        fihip = math.floor(hip)
        iring = int(math.floor(math.sqrt( hip - math.sqrt(fihip) ) )) + 1# ! counted from North pole
        iphi  = ipix1 - 2 * iring * (iring - 1)
        theta = math.acos( 1. - iring * iring / fact2 )
        phi   = (1. * iphi - 0.5) * math.pi / (2. * iring)
    elif ( ipix1 <= nl2 * (5 * nside+1) ):# then ! Equatorial region ------
        ip    = ipix1 - ncap - 1
        iring = int(math.floor( ip / nl4 )) + nside# ! counted from North pole
        iphi  = int(math.fmod(ip, nl4)) + 1

        fodd  = 0.5 * (1 + math.fmod(float(iring+nside), 2))# ! 1 if iring+nside is odd, 1 / 2 otherwise
        theta = math.acos( (nl2 - iring) / fact1 )
        phi   = (1. * iphi - fodd) * math.pi / (2. * nside)
    else:# ! South Polar cap -----------------------------------
        ip    = npix - ipix1 + 1
        hip   = ip / 2.0
        #/ * bug corrige floor instead of 1. * * /
        fihip = math.floor(hip)
        iring = int(math.floor(math.sqrt( hip - math.sqrt(fihip)))) + 1# ! counted from South pole
        iphi  = int((4. * iring + 1 - (ip - 2. * iring * (iring-1))))

        theta = math.acos( -1. + iring * iring / fact2)
        phi   = (1. * iphi - 0.5) * math.pi / (2. * iring)
    return theta, phi

nside=8# min is 1, max is 2^29
ipix=178#min is 0, max is 12*(nside^2)-1

(theta,phi)=pix2ang_ring(nside, ipix)#latitude and longitude in radians
print (theta, phi)