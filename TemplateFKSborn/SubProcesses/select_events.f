      program select_events
c Keeps selected events out of those originally stored in the event file.
c Compile with
c g77 -o select_events select_events.f mcatnlo_str.f handling_lhe_events.f
      implicit none
      integer maxevt,ifile,ofile,i,npart,nevmin,nevmax
      integer IDBMUP(2),PDFGUP(2),PDFSUP(2),IDWTUP,NPRUP,LPRUP
      double precision EBMUP(2),XSECUP,XERRUP,XMAXUP
      INTEGER MAXNUP
      PARAMETER (MAXNUP=500)
      INTEGER NUP,IDPRUP,IDUP(MAXNUP),ISTUP(MAXNUP),
     # MOTHUP(2,MAXNUP),ICOLUP(2,MAXNUP)
      DOUBLE PRECISION XWGTUP,SCALUP,AQEDUP,AQCDUP,
     # PUP(5,MAXNUP),VTIMUP(MAXNUP),SPINUP(MAXNUP)
      double precision sum_wgt
      integer isorh_lhe,ifks_lhe,jfks_lhe,fksfather_lhe,ipartner_lhe
      double precision scale1_lhe,scale2_lhe,percentage
      integer jwgtinfo,mexternal,iwgtnumpartn
      double precision wgtcentral,wgtmumin,wgtmumax,wgtpdfmin,wgtpdfmax
      character*80 event_file,fname2
      character*140 buff
      character*10 MonteCarlo,string
      character*1 ch1
      logical AddInfoLHE

      include "genps.inc"
      integer j,k,itype,istep,ievts_ok
      real*8 ecm,xmass(nexternal),xmasstmp(nexternal),
     &xmom(0:3,nexternal)
c
      write(*,*)'Enter event file name'
      read(*,*)event_file
      write(*,*)'Type 1 to keep S events'
      write(*,*)'     2 to keep H events'
      write(*,*)'     3 to keep a subset of events'
      read(*,*)itype
      if(itype.eq.1)then
         call fk88strcat(event_file,'.S',fname2)
      elseif(itype.eq.2)then
         call fk88strcat(event_file,'.H',fname2)
      elseif(itype.eq.3)then
         call fk88strcat(event_file,'.RED',fname2)
         write(*,*)'Enter first and last event to keep'
         read(*,*)nevmin,nevmax
         ifile=34
         open(unit=ifile,file=event_file,status='old')
         call read_lhef_header(ifile,maxevt,MonteCarlo)
         if(nevmin.gt.maxevt.and.nevmax.gt.maxevt)then
            write(*,*)'Invalid inputs',nevmin,nevmax,maxevt
            stop
         endif
         close(34)
      else 
         write(*,*)'Invalid itype',itype
         stop
      endif

      ifile=34
      ofile=35
      open(unit=ifile,file=event_file,status='old')
      open(unit=ofile,file=fname2,status='unknown')
      open(unit=36,file='select_events.out')
      AddInfoLHE=.false.

      call read_lhef_header(ifile,maxevt,MonteCarlo)
      call read_lhef_init(ifile,
     &     IDBMUP,EBMUP,PDFGUP,PDFSUP,IDWTUP,NPRUP,
     &     XSECUP,XERRUP,XMAXUP,LPRUP)
      string='abcdeABCDE'
      call write_lhef_header_string(ofile,string,MonteCarlo)
      call write_lhef_init(ofile,
     &     IDBMUP,EBMUP,PDFGUP,PDFSUP,IDWTUP,NPRUP,
     &     XSECUP,XERRUP,XMAXUP,LPRUP)
      
      i=1
      ievts_ok=0
      sum_wgt=0d0

      if(itype.le.2)then
        do while(i.le.maxevt)
          call read_lhef_event(ifile,
     &        NUP,IDPRUP,XWGTUP,SCALUP,AQEDUP,AQCDUP,
     &        IDUP,ISTUP,MOTHUP,ICOLUP,PUP,VTIMUP,SPINUP,buff)
          sum_wgt=sum_wgt+XWGTUP

          if(i.eq.1.and.buff(1:1).eq.'#')AddInfoLHE=.true.
          if(AddInfoLHE)then
            if(buff(1:1).ne.'#')then
              write(*,*)'Inconsistency in event file',i,' ',buff
              stop
            endif
            read(buff,200)ch1,iSorH_lhe,ifks_lhe,jfks_lhe,
     #                        fksfather_lhe,ipartner_lhe,
     #                        scale1_lhe,scale2_lhe,
     #                        jwgtinfo,mexternal,iwgtnumpartn,
     #             wgtcentral,wgtmumin,wgtmumax,wgtpdfmin,wgtpdfmax
          endif

          npart=0
          do k=1,nup
            if(abs(ISTUP(k)).eq.1)then
              npart=npart+1
              xmasstmp(npart)=pup(5,k)
              xmass(npart)=0d0
              xmass(npart)=xmasstmp(npart)
              do j=1,4
                xmom(mod(j,4),npart)=pup(j,k)
              enddo
            endif
          enddo
          call phspncheck_nocms2(i,npart,xmass,xmom)

          if(itype.eq.iSorH_lhe)then
            ievts_ok=ievts_ok+1
            call write_lhef_event(ofile,
     &         NUP,IDPRUP,XWGTUP,SCALUP,AQEDUP,AQCDUP,
     &         IDUP,ISTUP,MOTHUP,ICOLUP,PUP,VTIMUP,SPINUP,buff)
          endif

          istep=maxevt/10
          if(istep.eq.0)istep=1
          percentage=i*100.d0/maxevt
          if(mod(i,istep).eq.0.or.i.eq.maxevt)
     &      write(*,*)'Read',int(percentage),'% of event file'

          i=i+1
        enddo
      else
        do while(i.le.min(maxevt,nevmax))
          call read_lhef_event(ifile,
     &        NUP,IDPRUP,XWGTUP,SCALUP,AQEDUP,AQCDUP,
     &        IDUP,ISTUP,MOTHUP,ICOLUP,PUP,VTIMUP,SPINUP,buff)
          sum_wgt=sum_wgt+XWGTUP

          if(i.eq.1.and.buff(1:1).eq.'#')AddInfoLHE=.true.
          if(AddInfoLHE)then
            if(buff(1:1).ne.'#')then
              write(*,*)'Inconsistency in event file',i,' ',buff
              stop
            endif
            read(buff,200)ch1,iSorH_lhe,ifks_lhe,jfks_lhe,
     #                        fksfather_lhe,ipartner_lhe,
     #                        scale1_lhe,scale2_lhe,
     #                        jwgtinfo,mexternal,iwgtnumpartn,
     #             wgtcentral,wgtmumin,wgtmumax,wgtpdfmin,wgtpdfmax
          endif

          npart=0
          do k=1,nup
            if(abs(ISTUP(k)).eq.1)then
              npart=npart+1
              do j=1,4
                xmom(mod(j,4),npart)=pup(j,k)
              enddo
              xmasstmp(npart)=pup(5,k)
              xmass(npart)=0d0
              xmass(npart)=xmasstmp(npart)
            endif
          enddo
          call phspncheck_nocms2(i,npart,xmass,xmom)

          if(i.ge.nevmin.and.i.le.nevmax)then
            ievts_ok=ievts_ok+1
            call write_lhef_event(ofile,
     &         NUP,IDPRUP,XWGTUP,SCALUP,AQEDUP,AQCDUP,
     &         IDUP,ISTUP,MOTHUP,ICOLUP,PUP,VTIMUP,SPINUP,buff)
         endif
         i=i+1
        enddo
      endif

      write(ofile,*)'</LesHouchesEvents>'

      write(36,*)event_file
      write(36,*)itype
      write(36,*)ievts_ok

      if(ievts_ok.eq.0)then
         write(*,*)' '
         write(*,*)'No events of desired type found in file !'
         write(*,*)' '
         stop
      endif

      if(itype.eq.3)write(*,*)'The sum of the weights is:',sum_wgt

 200  format(1a,1x,i1,4(1x,i2),2(1x,d14.8),1x,i1,2(1x,i2),5(1x,d14.8))

      close(34)
      close(35)
      close(36)

      end



      subroutine phspncheck_nocms2(nev,npart,xmass,xmom)
c Checks four-momentum conservation. Derived from phspncheck;
c works in any frame
      implicit none
      integer nev,npart,maxmom
      include "genps.inc"
      real*8 xmass(nexternal),xmom(0:3,nexternal)
      real*8 tiny,vtiny,xm,xlen4,den,xsum(0:3),xsuma(0:3),
     # xrat(0:3),ptmp(0:3)
      parameter (tiny=5.d-3)
      parameter (vtiny=1.d-6)
      integer jflag,i,j,jj
      double precision dot
      external dot
c
      jflag=0
      do i=0,3
        xsum(i)=-xmom(i,1)-xmom(i,2)
        xsuma(i)=abs(xmom(i,1))+abs(xmom(i,2))
        do j=3,npart
          xsum(i)=xsum(i)+xmom(i,j)
          xsuma(i)=xsuma(i)+abs(xmom(i,j))
        enddo
        if(xsuma(i).lt.1.d0)then
          xrat(i)=abs(xsum(i))
        else
          xrat(i)=abs(xsum(i))/xsuma(i)
        endif
        if(xrat(i).gt.tiny.and.jflag.eq.0)then
          write(*,*)'Momentum is not conserved [nocms]'
          write(*,*)'i=',i
          do j=1,npart
            write(*,'(4(d14.8,1x))') (xmom(jj,j),jj=0,3)
          enddo
          jflag=1
        endif
      enddo
      if(jflag.eq.1)then
        write(*,'(4(d14.8,1x))') (xsum(jj),jj=0,3)
        write(*,'(4(d14.8,1x))') (xrat(jj),jj=0,3)
        write(*,*)'event #',nev
      endif
c
      do j=1,npart
        do i=0,3
          ptmp(i)=xmom(i,j)
        enddo
        xm=xlen4(ptmp)
        if(ptmp(0).ge.1.d0)then
          den=ptmp(0)
        else
          den=1.d0
        endif
        if(abs(xm-xmass(j))/den.gt.tiny .and.
     &       abs(xm-xmass(j)).gt.tiny)then
          write(*,*)'Mass shell violation [nocms]'
          write(*,*)'j=',j
          write(*,*)'mass=',xmass(j)
          write(*,*)'mass computed=',xm
          write(*,'(4(d14.8,1x))') (xmom(jj,j),jj=0,3)
          write(*,*)'event #',nev
        endif
      enddo

      return
      end


      double precision function dot(p1,p2)
C****************************************************************************
C     4-Vector Dot product
C****************************************************************************
      implicit none
      double precision p1(0:3),p2(0:3)
      dot=p1(0)*p2(0)-p1(1)*p2(1)-p1(2)*p2(2)-p1(3)*p2(3)

      if(dabs(dot).lt.1d-6)then ! solve numerical problem 
         dot=0d0
      endif

      end


      function xlen4(v)
      implicit none
      real*8 xlen4,tmp,v(0:3)
c
      tmp=v(0)**2-v(1)**2-v(2)**2-v(3)**2
      xlen4=sign(1.d0,tmp)*sqrt(abs(tmp))
      return
      end
