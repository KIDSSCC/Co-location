c NPROCS = 16 CLASS = C
c  
c  
c  This file is generated automatically by the setparams utility.
c  It sets the number of processors and the class of the NPB
c  in this directory. Do not modify it by hand.
c  
        integer maxcells, problem_size, niter_default
        parameter (maxcells=4, problem_size=162, niter_default=400)
        double precision dt_default
        parameter (dt_default = 0.00067d0)
        logical  convertdouble
        parameter (convertdouble = .false.)
        character*11 compiletime
        parameter (compiletime='26 Dec 2023')
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
