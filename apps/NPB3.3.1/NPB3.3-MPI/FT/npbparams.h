c NPROCS = 4 CLASS = C
c  
c  
c  This file is generated automatically by the setparams utility.
c  It sets the number of processors and the class of the NPB
c  in this directory. Do not modify it by hand.
c  
        integer nx, ny, nz, maxdim, niter_default, ntdivnp, np_min
        parameter (nx=512, ny=512, nz=512, maxdim=512)
        parameter (niter_default=20)
        parameter (np_min = 4)
        parameter (ntdivnp=((nx*ny)/np_min)*nz)
        double precision ntotal_f
        parameter (ntotal_f=1.d0*nx*ny*nz)
        logical  convertdouble
        parameter (convertdouble = .false.)
        character*11 compiletime
        parameter (compiletime='05 Jan 2024')
        character*5 npbversion
        parameter (npbversion='3.3.1')
        character*6 cs1
        parameter (cs1='mpif77')
        character*9 cs2
        parameter (cs2='$(MPIF77)')
        character*6 cs3
        parameter (cs3='(none)')
        character*20 cs4
        parameter (cs4='-I/usr/local/include')
        character*17 cs5
        parameter (cs5='-O -mcmodel=large')
        character*17 cs6
        parameter (cs6='-O -mcmodel=large')
        character*6 cs7
        parameter (cs7='randi8')
