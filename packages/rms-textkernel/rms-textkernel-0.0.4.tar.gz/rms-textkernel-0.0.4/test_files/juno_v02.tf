KPL/FK

Juno Frames Kernel
===============================================================================

   This frame kernel contains complete set of frame definitions for the
   Juno (JUNO) spacecraft, its structures and science instruments. This
   frame kernel also contains name - to - NAIF ID mappings for JUNO
   science instruments and s/c structures (see the last section of the
   file.)


Version and Date
-------------------------------------------------------------------------------

   Version 0.2 -- July 13, 2009 -- Boris Semenov, NAIF

      Re-defined JUNO_FGM_IB and JUNO_FGM_IB frames based on 
      the input from Jack Connerney.

   Version 0.1 -- June 12, 2009 -- Boris Semenov, NAIF

      Defined preliminary frames for all structures and instruments
      based on CDR materials and draft MICDs.

   Version 0.0 -- February 3, 2009 -- Boris Semenov, NAIF

      Initial Release: bare-bones version with just two frames needed
      to access JUNO nominal attitude CK file.


References
-------------------------------------------------------------------------------

   1. ``Frames Required Reading''

   2. ``Kernel Pool Required Reading''

   3. ``C-Kernel Required Reading''


Contact Information
-------------------------------------------------------------------------------

   Boris V. Semenov, NAIF/JPL, (818)-354-8136, bsemenov@spice.jpl.nasa.gov


Implementation Notes
-------------------------------------------------------------------------------

   This file is used by the SPICE system as follows: programs that make
   use of this frame kernel must ``load'' the kernel, normally during
   program initialization. The SPICE routine FURNSH loads a kernel file
   into the pool as shown below.

      CALL FURNSH ( 'frame_kernel_name; )    -- FORTRAN
      furnsh_c ( "frame_kernel_name" );      -- C
      cspice_furnsh, frame_kernel_name       -- IDL
      cspice_furnsh( 'frame_kernel_name' )   -- MATLAB

   This file was created and may be updated with a text editor or word
   processor.


JUNO Frames
-------------------------------------------------------------------------------

   The following JUNO frames are defined in this kernel file:

           Name                  Relative to           Type       NAIF ID
      ======================  =====================  ============   =======

   Spacecraft frame:
   -----------------
      JUNO_SPACECRAFT         varies                 CK             -61000
      JUNO_SPIN_AXIS          J2000                  CK             -61900

   Magnetometer and ASC frames:
   ----------------------------
      JUNO_ASC1               J2000, SPACECRAFT      CK             -61111
      JUNO_ASC2               J2000, SPACECRAFT      CK             -61112
      JUNO_MOB_IB             ASC1, ASC2             CK             -61113
      JUNO_FGM_IB             JUNO_MOB_IB            FIXED          -61114

      JUNO_ASC3               J2000, SPACECRAFT      CK             -61121
      JUNO_ASC4               J2000, SPACECRAFT      CK             -61122
      JUNO_MOB_OB             ASC3, ASC4             CK             -61123
      JUNO_FGM_OB             JUNO_MOB_OB            FIXED          -61124

   JADE Frames:
   ------------
      JUNO_JADE_E060          SPACECRAFT             FIXED          -61201
      JUNO_JADE_E180          SPACECRAFT             FIXED          -61202
      JUNO_JADE_E300          SPACECRAFT             FIXED          -61203
      JUNO_JADE_I             SPACECRAFT             FIXED          -61204

   JEDI Frames:
   ------------
      JUNO_JEDI_090           SPACECRAFT             FIXED          -61301
      JUNO_JEDI_A180          SPACECRAFT             FIXED          -61302
      JUNO_JEDI_270           SPACECRAFT             FIXED          -61303

   JIRAM Frames:
   -------------
      JUNO_JIRAM_URF          SPACECRAFT             FIXED          -61401
      JUNO_JIRAM_I            JIRAM_URF              FIXED          -61410
      JUNO_JIRAM_I_LBAND      JIRAM_IMAGER           FIXED          -61411
      JUNO_JIRAM_I_MBAND      JIRAM_IMAGER           FIXED          -61412
      JUNO_JIRAM_S            JIRAM_IMAGER           FIXED          -61420

   JUNOCAM Frames:
   ---------------
      JUNO_JUNOCAM            SPACECRAFT             FIXED          -61500

   MWR Frames:
   -----------
      JUNO_MWR_A1             SPACECRAFT             FIXED          -61601
      JUNO_MWR_A2             SPACECRAFT             FIXED          -61602
      JUNO_MWR_A3             SPACECRAFT             FIXED          -61603
      JUNO_MWR_A4             SPACECRAFT             FIXED          -61604
      JUNO_MWR_A5             SPACECRAFT             FIXED          -61605
      JUNO_MWR_A6             SPACECRAFT             FIXED          -61606

   UVS Frames:
   -----------
      JUNO_UVS_BASE           SPACECRAFT             FIXED          -61700
      JUNO_UVS                UVS_BASE               CK             -61701

   WAVES Frames:
   -----------
      JUNO_WAVES_MSC          SPACECRAFT             FIXED          -61810
      JUNO_WAVES_ANTENNA      SPACECRAFT             FIXED          -61820

   Solar Array frames:
   -------------------
      JUNO_SA1_HINGE          SPACECRAFT             FIXED          -61010
      JUNO_SA1                SA1_HINGE              CK             -61011
      JUNO_SA2_HINGE          SPACECRAFT             FIXED          -61020
      JUNO_SA2                SA2_HINGE              CK             -61021
      JUNO_SA3_HINGE          SPACECRAFT             FIXED          -61030
      JUNO_SA3                SA3_HINGE              CK             -61031

   Antenna frames:
   ---------------
      JUNO_HGA                SPACECRAFT             FIXED          -61040
      JUNO_MGA                SPACECRAFT             FIXED          -61050
      JUNO_LGA_FORWARD        SPACECRAFT             FIXED          -61061
      JUNO_LGA_AFT            SPACECRAFT             FIXED          -61062
      JUNO_LGA_TOROID         SPACECRAFT             FIXED          -61063

   ACS Sensor frames:
   ------------------
      JUNO_SRU1               SPACECRAFT             FIXED          -61071
      JUNO_SRU2               SPACECRAFT             FIXED          -61072
      JUNO_SSS1               SPACECRAFT             FIXED          -61073
      JUNO_SSS2               SPACECRAFT             FIXED          -61074

   Truster frames:
   ---------------
      JUNO_REM_FL1            SPACECRAFT             FIXED          -61081
      JUNO_REM_FL2            SPACECRAFT             FIXED          -61082
      JUNO_REM_FL3            SPACECRAFT             FIXED          -61083
      JUNO_REM_FL4            SPACECRAFT             FIXED          -61084
      JUNO_REM_FA1            SPACECRAFT             FIXED          -61085
      JUNO_REM_FA2            SPACECRAFT             FIXED          -61086

      JUNO_REM_RL1            SPACECRAFT             FIXED          -61091
      JUNO_REM_RL2            SPACECRAFT             FIXED          -61092
      JUNO_REM_RL3            SPACECRAFT             FIXED          -61093
      JUNO_REM_RL4            SPACECRAFT             FIXED          -61094
      JUNO_REM_RA1            SPACECRAFT             FIXED          -61095
      JUNO_REM_RA2            SPACECRAFT             FIXED          -61096


JUNO Frames Hierarchy
-------------------------------------------------------------------------------

   The diagram below shows the JUNO frames hierarchy:


                                 "J2000" INERTIAL
        +----------------------------------------------------------------+
        |          |   |          |            |          |   |          |
        | <--pck   |   |          |<--ck       |          |   |          |
        |          |   |          |            |          |   |    pck-> |
        V          |   |          V            |          |   |          V
    "IAU_JUPITER"  |   |   "JUNO_SPIN_AXIS"    |          |   |    "IAU_EARTH"
    -------------- |   |   ----------------    |          |   |   ------------
                   |   |          |            |          |   |
              ck-->|   |<--ck     |            |     ck-->|   |<--ck
                   |   |          |            |          |   |
                   V   V          |            |          V   V
          "JUNO_ASC1" "JUNO_ASC2" |            | "JUNO_ASC3" "JUNO_ASC4"
          ----------- ----------- |            | ----------- -----------
            ^      |   |      ^   |            |   ^      |   |      ^
            |      |   |      |   |            |   |      |   |      |
            | ck-->|   |<--ck |   |            |   | ck-->|   |<--ck |
            |      |   |      |   |            |   |      |   |      |
            |      V   V      |   |            |   |      V   V      |
            |  "JUNO_MOB_IB"  |   |            |   |  "JUNO_MOB_OB"  |
            |  -------------  |   |            |   |  -------------  |
            |        |        |   |            |   |        |        |
            |        |<-fixed |   |            |   |        |<-fixed |
            |        |        |   |            |   |        |        |
            |        V        |   |            |   |        V        |
            |  "JUNO_FGM_IB"  |   |            |   |  "JUNO_FGM_OB"  |
            |  -------------  |   |            |   |  -------------  |
            |                 |   |            |   |                 |
            |<--ck       ck-->|   |<--ck  ck-->|   |<--ck            |<--ck
            |                 |   |            |   |                 |
            V                 V   V            V   V                 V
                                "JUNO_SPACECRAFT"
            +------------------------------------------------------------+
            |    |    |    |    |    |    |            |  |  |  |  |  |  |
     fixed->|    |    |    |    |    |    |     fixed->|  |  |  |  |  |  |
            |    |    |    |    |    |    |            |  |  |  |  |  |  |
            V    |    |    |    |    |    |            V  |  |  |  |  |  |
   "JUNO_JADE_*" |    |    |    |    |    |    "JUNO_HGA" |  |  |  |  |  |
   ------------- |    |    |    |    |    |    ---------- |  |  |  |  |  |
                 |    |    |    |    |    |               |  |  |  |  |  |
          fixed->|    |    |    |    |    |        fixed->|  |  |  |  |  |
                 |    |    |    |    |    |               |  |  |  |  |  |
                 V    |    |    |    |    |               V  |  |  |  |  |
      "JUNO_JEDI_*"   |    |    |    |    |       "JUNO_MGA" |  |  |  |  |
      -------------   |    |    |    |    |       ---------- |  |  |  |  |
                      |    |    |    |    |                  |  |  |  |  |
               fixed->|    |    |    |    |           fixed->|  |  |  |  |
                      |    |    |    |    |                  |  |  |  |  |
                      V    |    |    |    |                  V  |  |  |  |
        "JUNO_JIRAM_URF"   |    |    |    |        "JUNO_LGA_*" |  |  |  |
        ----------------   |    |    |    |        ------------ |  |  |  |
                 |         |    |    |    |                     |  |  |  |
          fixed->|         |    |    |    |              fixed->|  |  |  |
                 |         |    |    |    |                     |  |  |  |
                 V         |    |    |    |                     V  |  |  |
          "JUNO_JIRAM_S"   |    |    |    |           "JUNO_REM_*" |  |  |
          --------------   |    |    |    |           ------------ |  |  |
                 |         |    |    |    |                        |  |  |
          fixed->|         |    |    |    |<-fixed          fixed->|  |  |
                 |         |    |    |    |                        |  |  |
                 V         |    |    |    V                        V  |  |
          "JUNO_JIRAM_I"   |    |    |   "JUNO_WAVES_*"   "JUNO_SRU*" |  |
          --------------   |    |    |   --------------   ----------- |  |
                 |         |    |    |                                |  |
          fixed->|         |    |    |<-fixed                  fixed->|  |
                 |         |    |    |                                |  |
                 V         |    |    V                                V  |
    "JUNO_JIRAM_I_*BAND"   |    |   "JUNO_UVS_BASE"          "JUNO_SSS*" |
    --------------------   |    |   ---------------          ----------- |
                           |    |    |                                   |
                    fixed->|    |    |<-ck                        fixed->|
                           |    |    |                                   |
                           V    |    V                                   V
               "JUNO_JUNOCAM"   |   "JUNO_UVS"             "JUNO_SA*_HINGE"
               --------------   |   ----------             ----------------
                                |                                        |
                         fixed->|                                    ck->|
                                |                                        |
                                V                                        V
                     "JUNO_MWR_A*"                                "JUNO_SA*"
                     -------------                                ----------


Spacecraft Orientation Frame Chains

   Possible "J2000" -> "JUNO_SPACECRAFT" frame chains are:

      -- using data from a nominal spacecraft CK:

            "J2000" -> "JUNO_SPIN_AXIS" -> "JUNO_SPACECRAFT"

      -- using data from a reconstructed spacecraft CK:

            "J2000" -> "JUNO_SPACECRAFT"

      -- using data from a reconstructed ASC CK and an ASC "alignment" CK:

            "J2000" -> "JUNO_ASC#" -> "JUNO_SPACECRAFT"


Magnetometer Sensor Frame Chains

   Possible "J2000" -> "JUNO_FGM_IB" (same for OB) frame chains are:

      -- using data from a nominal spacecraft CK, an ASC "alignment" CK,
         and a MOB "alignment" CK:

            "J2000" -> "JUNO_SPIN_AXIS" -> "JUNO_SPACECRAFT" ->
                    -> "JUNO_ASC#" -> "JUNO_MOB_IB" -> "JUNO_FGM_IB"

      -- using data from a reconstructed spacecraft CK, an ASC
         "alignment" CK, and a MOB "alignment" CK:

            "J2000" -> "JUNO_SPACECRAFT" ->
                    -> "JUNO_ASC#" -> "JUNO_MOB_IB" -> "JUNO_FGM_IB"

      -- using data from a reconstructed ASC CK, an ASC "alignment" CK,
         and a MOB "alignment" CK:

            "J2000" -> "JUNO_ASC#" -> "JUNO_MOB_IB" -> "JUNO_FGM_IB"


Spacecraft Bus Frame
-------------------------------------------------------------------------------

   The spacecraft frame (or AACS control frame) is defined by the s/c design
   as follows [from TBD]:

      -  +Z axis is along the nominal spin axis and points in the
         direction of the nominal HGA boresight

      -  +X axis is along the solar array 1 symmetry axis and points
         towards the magnetometer boom

      -  +Y axis completes the right-handed frame

      -  the origin of the frame is centered on the launch vehicle
         separation plane.

   These diagrams illustrates the s/c frame:

      Spacecraft +Z side view:
      ------------------------

                .-\
             .-'   \
          .-'       \ Solar Array 3
       .-'           \
       \           .-'\
        \       .-'    \
         \   ,-'        \
          \-'         .-'\
           \       .-'    \
            \   .-'        \
             \-'         .-'\             <-. Spin Direction
              \       .-'    \               `.
               \   .-'        \.
                \-'         .-' `-.
                 \       .-'       `-.
                  \   .-'    ----- .  `-.      Solar Array 1
                   .-'    +Ysc ^    `.   `-.--------------------.
                   |    /      |      \    |      |      |      |
                   |   /       |       \   |      |      |      |``--..
                   |  '        |    +Xsc   |      |      |      |      `--..
                   |  |        o------> |  |      |      |      |           |
                   |  .      +Zsc       ,  |      |      |      |     ..--''
                   |   \               /   |      |      |      |..--'
                   |    \ HGA         /    |      |      |      | Magnetometer
                   `-.   `.         .'   .-'--------------------'     Boom
                  /   `-.  ` ----- '  .-'
                 /       `-.       .-'
                /           `-. .-'
               /`-.           /'
              /    `-.       /
             /        `-.   /
            /`-.         `-/
           /    `-.       /
          /        `-.   /
         /`-.         `-/
        /    `-.       /
       /        `-.   /
      /.           `-/
        `-.         / Solar Array 2                  +Zsc is out of
           `-.     /                                    the page.
              `-. /
                 `


      Spacecraft -Y side view:
      ------------------------
                               o
                              / \
                      .-----------------, HGA
                       \               /
                        `.           .'
                           `-------'
                           |       |                            Magnetometer
                           |       |                                Boom
      ================o==o==o==o-----------o======o======o======o===========*
          Solar    |           |           |   Solar Array 1
         Array 2   |           |           |
                   |                       |
                   |                       |
                   |      +Zsc ^           |
                   |           |           |
                   |           |           |
                   |           |           |            +Ysc is into
                   `----- +Ysc x------>   -'              the page.
                            /_____\  +Xsc


   Since the S/C bus attitude with respect to an inertial frame is provided
   by a C kernel (see [3] for more information), this frame is defined as
   a CK-based frame.

   \begindata

      FRAME_JUNO_SPACECRAFT        = -61000
      FRAME_-61000_NAME            = 'JUNO_SPACECRAFT'
      FRAME_-61000_CLASS           = 3
      FRAME_-61000_CLASS_ID        = -61000
      FRAME_-61000_CENTER          = -61
      CK_-61000_SCLK               = -61
      CK_-61000_SPK                = -61

   \begintext


Spin Axis Frame
-------------------------------------------------------------------------------


   The JUNO_SPIN_AXIS frame is a special frame used in the nominal
   orientation CK files. In these files the JUNO_SPACECRAFT frame
   orientation is not stored relative to the J2000 frame. Instead it is
   "decomposed" into two orientations: the nominal spin axis
   orientation captured in the segments providing the orientation of
   the JUNO_SPIN_AXIS frame relative to the J2000 frame and the nominal
   rotation about the spin axis captured in the segments providing the
   orientation of the JUNO_SPACECRAFT frame relative to the
   JUNO_SPIN_AXIS frame.

   JUNO_SPIN_AXIS is defined as a CK-based frame.

   \begindata

      FRAME_JUNO_SPIN_AXIS         = -61900
      FRAME_-61900_NAME            = 'JUNO_SPIN_AXIS'
      FRAME_-61900_CLASS           = 3
      FRAME_-61900_CLASS_ID        = -61900
      FRAME_-61900_CENTER          = -61
      CK_-61900_SCLK               = -61
      CK_-61900_SPK                = -61

   \begintext


Magnetometer Frames
-------------------------------------------------------------------------------

   The set of frames for the Magnetometer experiment includes two
   Magnetometer optical bench frames -- JUNO_MOB_IB and JUNO_MOB_OB, --
   two FGM frames -- JUNO_FGM_IB and JUNO_FGM_OB, -- and four ASC
   frames -- JUNO_ASC1, JUNO_ASC2, JUNO_ASC3, and JUNO_ASC4.

   The optical bench frames -- JUNO_MOB_IB and JUNO_MOB_OB -- are defined
   as follows:

      -  +Z axis is normal to the optical bench plane on the FGM side

      -  +X axis is in the optical bench plane and points from the
         midpoint between ASCs towards FGM

      -  +Y axis completes the right-handed frame

      -  the origin of the frame is in the center of the outer mounting
         hole on the ASC side bracket

   The optical bench frames are defined as CK-based frames because
   their orientation can be provided with respect to either of ASCs
   mounted on the bench.

   The FGM frames -- JUNO_FGM_IB and JUNO_FGM_OB -- are defined as
   fixed-offset frames rotated by 180 degrees about +X with respect to
   the corresponding optical bench frames. The FGM frame centers are in
   the geometric center of sensor assemblies. (Of note: The FGM/OB
   frame is nominally co-aligned with the spacecraft frame; the FGM/IB
   frame is nominally rotated from the spacecraft frame by 180 degrees
   about +Z.)

   These diagrams illustrate the optical bench and FGM frames:

      Spacecraft -Z side view:
      ------------------------


                         Magnetometer Boom
                 /```---...          ___
                 |         ```---.+Yfgm_ib      +Ymob_ob
                 |                        ^ .           ^
                 |                        |  ```---...  |
                 |                        | ASC1      ``|- ASC3
    +Zsc    +Xsc |               +Zmob_ib-|-@-.         |-@---.|    +Xfgm_ob
      x------>   |                 <---<--x---o         o---x-->--->
      |          |          +Xfgm_ib    `---@-|         `-@-|-'+Zmob_ob
      |          |                       ASC2 |       .ASC4'|
      |          |                           .|.---'''      |
      v          |                       /''' v             v
       +Ysc      |         ...---'''\   /     +Ymob_ib       +Yfgm_ob
                 \...---'''          ---

                                        +Zmob_ib and +Zmob_ob are out 
                                                  of the page.

                                        +Zsc, +Zfgm_ib, and +Zfgm_ob 
                                               is into the page.

   The keywords below define the optical bench and FGM frames.

   \begindata

      FRAME_JUNO_MOB_IB            = -61113
      FRAME_-61113_NAME            = 'JUNO_MOB_IB'
      FRAME_-61113_CLASS           = 3
      FRAME_-61113_CLASS_ID        = -61113
      FRAME_-61113_CENTER          = -61
      CK_-61113_SCLK               = -61
      CK_-61113_SPK                = -61

      FRAME_JUNO_FGM_IB            = -61114
      FRAME_-61114_NAME            = 'JUNO_FGM_IB'
      FRAME_-61114_CLASS           = 4
      FRAME_-61114_CLASS_ID        = -61114
      FRAME_-61114_CENTER          = -61
      TKFRAME_-61114_SPEC          = 'ANGLES'
      TKFRAME_-61114_RELATIVE      = 'JUNO_MOB_IB'
      TKFRAME_-61114_ANGLES        = ( 180.0, 0.0, 0.0 )
      TKFRAME_-61114_AXES          = ( 1,   2,   3   )
      TKFRAME_-61114_UNITS         = 'DEGREES'

      FRAME_JUNO_MOB_OB            = -61123
      FRAME_-61123_NAME            = 'JUNO_MOB_OB'
      FRAME_-61123_CLASS           = 3
      FRAME_-61123_CLASS_ID        = -61123
      FRAME_-61123_CENTER          = -61
      CK_-61123_SCLK               = -61
      CK_-61123_SPK                = -61

      FRAME_JUNO_FGM_OB            = -61124
      FRAME_-61124_NAME            = 'JUNO_FGM_OB'
      FRAME_-61124_CLASS           = 4
      FRAME_-61124_CLASS_ID        = -61124
      FRAME_-61124_CENTER          = -61
      TKFRAME_-61124_SPEC          = 'ANGLES'
      TKFRAME_-61124_RELATIVE      = 'JUNO_MOB_OB'
      TKFRAME_-61124_ANGLES        = ( 180.0, 0.0, 0.0 )
      TKFRAME_-61124_AXES          = ( 1,   2,   3   )
      TKFRAME_-61124_UNITS         = 'DEGREES'

   \begintext

   The ASC frames -- JUNO_ASC1, JUNO_ASC2, JUNO_ASC3, and JUNO_ASC4 --
   are defined as follows:

      -  +Z axis is along the boresight

      -  +X axis is along the sensor side roughly aligned with the cable
         direction, pointing away from the cable side.

      -  +Y axis completes the right-handed frame

      -  the origin of the frame is at the ASC's focal point

   The ASC frames are defined as CK-based frames because their
   orientation can be provided in one of three ways:

      -  with respect to the J2000 frame, based on the ASC's attitude
         solution

      -  with respect to the spacecraft frame, based on the in-flight
         relative alignment calibration

      -  with respect to the corresponding optical bench, based on
         the ground calibrations.

   These diagrams illustrate the ASC frames:

      Spacecraft -Z side view:
      ------------------------


                         Magnetometer Boom
                 /```---...          ___
                 |         ```---.../   \                 ^ +Yasc3
                 |                       \...             |
                 |                           ```---...    ^ +Yasc4
                 |             +Xasc1        ASC1    ASC3-|--..  +Xasc3
    +Zsc    +Xsc |                   <------o-.         .-o------>
      x------>   |                 FGM_IB @ | |         | | @ FGM_OB
      |          |                   <------o-'         `-o------>
      |          |             +Xasc2       |ASC2    ASC4--'''   +Xasc4
      |          |                          v +Yasc1''
      v          |                       /''|
       +Ysc      |         ...---'''\   /   v +Yasc2
                 \...---'''          ---

                                        +Zasc1, +Zasc2, +Zasc3, and +Zasc4
                                         are out of the page, inclined at
                                                   13 degrees.

                                               +Zsc is into the page.

      Spacecraft +X side view:
      ------------------------


          In-bound MOB                    Out-bound MOB
          ------------                    -------------

                    +Ymob_ib       +Ymob_ob
      +Xmob_ib x------>                 <------o +Xmob_ob
               |                               |
               |                               |
               |                               |
      +Zmob_ib V                               V +Zmob_ob

                       +Yasc2    +Yasc3
                       .>             <.
                    .-'                 `-.
     +Xasc1 x     x'+Xasc2           +Xasc3`o     o +Xasc4
           / `-.   \                       /   .-' \
          /     `>  \                     /  <'     \
         /    +Yasc1 \                   / +Yasc4    \
        v             v                 v             v
    +Zasc1          +Zasc2          +Zasc3          +Zasc4

      /<-------|------->\             /<-------|------->\
        13 deg | 13 deg                 13 deg | 13 deg


                               ^ +Zsc               +Xsc, +Xmob_ob, +Xasc3,
                               |                        and +Xasc4 are
                               |                       out of the page.
                               |
                               o------> +Ysc        +Xmob_ib, +Xasc1, and
                             +Xsc                  +Xasc2 are into the page.

   The keywords below define the optical bench and FGM frames.

   \begindata

      FRAME_JUNO_ASC1              = -61111
      FRAME_-61111_NAME            = 'JUNO_ASC1'
      FRAME_-61111_CLASS           = 3
      FRAME_-61111_CLASS_ID        = -61111
      FRAME_-61111_CENTER          = -61
      CK_-61111_SCLK               = -61
      CK_-61111_SPK                = -61

      FRAME_JUNO_ASC2              = -61112
      FRAME_-61112_NAME            = 'JUNO_ASC2'
      FRAME_-61112_CLASS           = 3
      FRAME_-61112_CLASS_ID        = -61112
      FRAME_-61112_CENTER          = -61
      CK_-61112_SCLK               = -61
      CK_-61112_SPK                = -61

      FRAME_JUNO_ASC3              = -61121
      FRAME_-61121_NAME            = 'JUNO_ASC3'
      FRAME_-61121_CLASS           = 3
      FRAME_-61121_CLASS_ID        = -61121
      FRAME_-61121_CENTER          = -61
      CK_-61121_SCLK               = -61
      CK_-61121_SPK                = -61

      FRAME_JUNO_ASC4              = -61122
      FRAME_-61122_NAME            = 'JUNO_ASC4'
      FRAME_-61122_CLASS           = 3
      FRAME_-61122_CLASS_ID        = -61122
      FRAME_-61122_CENTER          = -61
      CK_-61122_SCLK               = -61
      CK_-61122_SPK                = -61

   \begintext


JADE Frames
-------------------------------------------------------------------------------

   The set of frames for the JADE experiment includes three Electron
   Sensor frames -- JUNO_JADE_E060, JUNO_JADE_E180, and JUNO_JADE_E300
   -- and one Ion Sensor frame -- JUNO_JADE_I.

   The JADE Elector Sensor frames -- JUNO_JADE_E060, JUNO_JADE_E180, and
   JUNO_JADE_E300 -- are fixed w.r.t. to the spacecraft and defined as
   follows:

      -  +Z axis is normal to the plane between upper and lower
         entrance deflectors ("principal" plane) and points away from
         the sensor base

      -  +X axis is in the "principal" plane nominally points towards the
         center of the sensor FOV

      -  +Y axis completes the right-handed frame

      -  the origin of the frame is at the intersection of the "principal"
         plane and the sensor symmetry axis.

   This diagram illustrates the JADE Electron sensor frames:

      Spacecraft +Z side view:
      ------------------------

            Solar Array 3
           ~ ~ ~ ~ ~ ~ ~ ~
            \   .-'        \      +Xe060
             \-'         .-'\           ^    <-. Spin Direction
              \       .-'              /        `.
               \   .-'        <.      /
                \-'     +Ye060  `-.  /
                 \       .-'       `o.+Ze060
                  \   .-'    ----- .  `-.          Solar Array 1
                   .-'    +Ysc ^    `.   `-.--------------------.
                   |    /      |      \    |      |      |      |
                               |       \   |      |      |      |``--..
         +Xe180     +Ze180     |    +Xsc   |      |      |      |      `--..
            <------o           o------> |  |      |      |      |           |
                   |  .      +Zsc       ,  |      |      |      |     ..--''
                   |   \               /   |      |      |      |..--'
                   |    \ HGA         /           |      |      | Magnetometer
                   V .   `.         .'   .>  -------------------'     Boom
             +Ye180   `-.  ` ----- '  .-' +Ye300
                 /       `-  +Ze300 o'
                /           `-. .-'  \
               /`-.           /'      \
              /    `-.       /         \
             /        `-.   /           v
            /`-.         `-/      +Xe300
           /~ ~ ~ ~ ~ ~ ~ ~                       +Zsc, +Zje060, +Zje180,
            Solar Array 2                          +Zje300 are out of
                                                         the page.

   As seen on the diagram the JUNO_JADE_E060, JUNO_JADE_E180, and
   JUNO_JADE_E300 frames are nominally rotated from the spacecraft
   frame by +60, 180 and -60 degrees about +Z axis correspondingly.

   Since the frame definitions below contains the reverse
   transformations -- from the JADE Electron Sensor frames to the
   spacecraft frame -- the order of rotations is reversed and the signs
   of rotation angles are changed to the opposite ones compared to the
   description above.

   \begindata

      FRAME_JUNO_JADE_E060         = -61201
      FRAME_-61201_NAME            = 'JUNO_JADE_E060'
      FRAME_-61201_CLASS           = 4
      FRAME_-61201_CLASS_ID        = -61201
      FRAME_-61201_CENTER          = -61
      TKFRAME_-61201_SPEC          = 'ANGLES'
      TKFRAME_-61201_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61201_ANGLES        = ( -60.0, 0.0, 0.0 )
      TKFRAME_-61201_AXES          = (   3,   2,   1   )
      TKFRAME_-61201_UNITS         = 'DEGREES'

      FRAME_JUNO_JADE_E180         = -61202
      FRAME_-61202_NAME            = 'JUNO_JADE_E180'
      FRAME_-61202_CLASS           = 4
      FRAME_-61202_CLASS_ID        = -61202
      FRAME_-61202_CENTER          = -61
      TKFRAME_-61202_SPEC          = 'ANGLES'
      TKFRAME_-61202_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61202_ANGLES        = ( 180.0, 0.0, 0.0 )
      TKFRAME_-61202_AXES          = (   3,   2,   1   )
      TKFRAME_-61202_UNITS         = 'DEGREES'

      FRAME_JUNO_JADE_E300         = -61203
      FRAME_-61203_NAME            = 'JUNO_JADE_E300'
      FRAME_-61203_CLASS           = 4
      FRAME_-61203_CLASS_ID        = -61203
      FRAME_-61203_CENTER          = -61
      TKFRAME_-61203_SPEC          = 'ANGLES'
      TKFRAME_-61203_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61203_ANGLES        = (  60.0, 0.0, 0.0 )
      TKFRAME_-61203_AXES          = (   3,   2,   1   )
      TKFRAME_-61203_UNITS         = 'DEGREES'

   \begintext

   The JADE Ion Sensor frame -- JUNO_JADE_I -- is fixed w.r.t. to the
   spacecraft and defined as follows:

      -  +Z axis is normal to the plane between upper and lower
         entrance deflectors ("principal" plane) and points away from
         the anode

      -  +X axis is in the "principal" plane nominally points towards the
         center of the sensor FOV

      -  +Y axis completes the right-handed frame

      -  the origin of the frame is at the intersection of the "principal"
         plane and the sensor symmetry axis.

   This diagram illustrates the JADE Ion sensor frame:


      Spacecraft +Z side view:
      ------------------------

                Solar Array 3             <-. Spin Direction
               ~ ~ ~ ~ ~ ~ ~ ~                `.
               \   .-'        \.
                \-'         .-' `-.
                 \       .-'       `-.
    (45 deg above \   .-'    ----- .  `-.      Solar Array 1
      the page)    .-'    +Ysc ^    `.   `-.--------------------.
          +Xi    ..@    /      |      \    |      |      |      |
             <-''  |\          |       \   |      |      |      |``--..
          +Yi      | \         |    +Xsc   |      |      |      |      `--..
    (45 deg below  |15\        o------> |  |      |      |      |           |
      the page)    |   v     +Zsc       ,  |      |      |      |     ..--''
                   |  +Zi              /   |      |      |      |..--'
                   |             HGA  /    |      |      |      | Magnetometer
                   `-.   `.         .'   .-'--------------------'     Boom
                  /   `-.  ` ----- '  .-'
                 /       `-.       .-'
                /           `-. .-'
               /`-.           /'
               ~ ~ ~ ~ ~ ~ ~ ~                         +Zsc is out of
               Solar Array 2                              the page.


   As seen on the diagram the JUNO_JADE_I frame is nominally rotated
   from the spacecraft first by -75 degrees about +Z, then by +90
   degrees about +Y, then by -135 degrees about +Z.

   Since the frame definitions below contains the reverse
   transformation -- from the JADE Ion Sensor frame to the spacecraft
   frame -- the order of rotations is reversed and the signs of
   rotation angles are changed to the opposite ones compared to the
   description above.

   \begindata

      FRAME_JUNO_JADE_I            = -61204
      FRAME_-61204_NAME            = 'JUNO_JADE_I'
      FRAME_-61204_CLASS           = 4
      FRAME_-61204_CLASS_ID        = -61204
      FRAME_-61204_CENTER          = -61
      TKFRAME_-61204_SPEC          = 'ANGLES'
      TKFRAME_-61204_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61204_ANGLES        = ( 75.0, -90.0, 135.0 )
      TKFRAME_-61204_AXES          = (  3,     2,     3   )
      TKFRAME_-61204_UNITS         = 'DEGREES'

   \begintext


JEDI Frames
-------------------------------------------------------------------------------

   The set of frames for the JEDI experiment includes three JEDI Sensor
   frames -- JUNO_JEDI_090, JUNO_JEDI_A180, and JUNO_JEDI_270, -- fixed
   w.r.t. to the spacecraft and defined as follows:

      -  +Z axis is along the sensor head symmetry axis, pointing away
         from the sensor electronics box

      -  +X axis is in the FOV center plane, nominally pointing towards
         the center of the full (160 x 12) sensor FOV

      -  +Y axis completes the right-handed frame

      -  the origin of the frame is at the intersection of the FOV
         center plane and the sensor head symmetry axis.

   Note that for the JEDI/090 and JEDI/270 sensors the frame is as
   defined in the JEDI MICD. For the JEDI/A180 sensor the frame is not
   as defined in the JEDI MICD: it is rotated by -90 degrees about +X
   to align the +Z axis with the sensor's symmetry axis.

   This diagram illustrates the JEDI sensor frames:

      Spacecraft +Z side view:
      ------------------------

           Solar Array 3
          ~ ~ ~ ~ ~ ~ ~ ~
           \       .-'    \       +X090
            \   .-'        \    ^
             \-'         .-'\   |         <-. Spin Direction
              \              \  |            `.
               \   .  +Y090   \ |
                \-'      <------o +Z090
                 \       .-        `-.
                  \   .-'    ----- .  `-.      Solar Array 1
                   .-'    +Ysc ^    `.   `-.--------------------.
                   |    /      |      \    |      |      |      |
                   |   /       |       \   |      |      |      |``--..
                   |  '        |    +Xsc   |      |      |      |      `--..
                               o------> |  |      |      |      |           |
         +Xa180   +Ya180     +Zsc       ,  |      |      |      |     ..--''
            <------x                   /   |      |      |      |..--'
                   |    \ HGA         /    |      |      |      | Magnetometer
                   | .   `.         .'   .-'--------------------'     Boom
                   |  `-.  ` ----- '  .-'
                   V       +Z270   .-'
             +Za180          -. o------>         +X090 and +X270 are out
                              / |     +Y270      of the page, 10 degrees
              /    `-.       /  |                above the s/c XY plane.
             /        `-.   /   |
            /`-.         `-/    V                +Z090 and +Z270 are out
           /    `-.       /      +X270          of the page, tilted by ~12
           ~ ~ ~ ~ ~ ~ ~ ~                    degrees towards the s/c +Z axis.
            Solar Array 2
                                                 +Y090 is out of the page,
                                             ~7.3 deg above the s/c XY plane.

                                                 +Y270 is into the page,
                                             ~7.3 deg below the s/c XY plane.

                                                 +Yja180 is into the page.

                                                 +Zsc is out of the page.

   The JUNO_JEDI_090 frame is nominally rotated from the spacecraft
   frame first by +90 degrees about +Z, then by -10 degrees about +Y,
   then by +8 degrees about +X.

   The JUNO_JEDI_A180 frame is nominally rotated from the spacecraft
   frame first by 180 degrees about +Z, then by -90 degrees about +X.

   The JUNO_JEDI_270 frame is nominally rotated from the spacecraft
   frame first by -90 degrees about +Z, then by -10 degrees about +Y,
   then by -8 degrees about +X.

   Since the frame definitions below contains the reverse
   transformations -- from the JEDI Sensor frames to the spacecraft
   frame -- the order of rotations is reversed and the signs of
   rotation angles are changed to the opposite ones compared to the
   description above.

   \begindata

      FRAME_JUNO_JEDI_090          = -61301
      FRAME_-61301_NAME            = 'JUNO_JEDI_090'
      FRAME_-61301_CLASS           = 4
      FRAME_-61301_CLASS_ID        = -61301
      FRAME_-61301_CENTER          = -61
      TKFRAME_-61301_SPEC          = 'ANGLES'
      TKFRAME_-61301_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61301_ANGLES        = ( -90.0, 10.0, -8.0 )
      TKFRAME_-61301_AXES          = (   3,    2,    1   )
      TKFRAME_-61301_UNITS         = 'DEGREES'

      FRAME_JUNO_JEDI_A180         = -61302
      FRAME_-61302_NAME            = 'JUNO_JEDI_A180'
      FRAME_-61302_CLASS           = 4
      FRAME_-61302_CLASS_ID        = -61302
      FRAME_-61302_CENTER          = -61
      TKFRAME_-61302_SPEC          = 'ANGLES'
      TKFRAME_-61302_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61302_ANGLES        = ( 180.0, 0.0, 90.0 )
      TKFRAME_-61302_AXES          = (   3,   2,    1   )
      TKFRAME_-61302_UNITS         = 'DEGREES'

      FRAME_JUNO_JEDI_270          = -61303
      FRAME_-61303_NAME            = 'JUNO_JEDI_270'
      FRAME_-61303_CLASS           = 4
      FRAME_-61303_CLASS_ID        = -61303
      FRAME_-61303_CENTER          = -61
      TKFRAME_-61303_SPEC          = 'ANGLES'
      TKFRAME_-61303_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61303_ANGLES        = ( 90.0, 10.0, 8.0 )
      TKFRAME_-61303_AXES          = (  3,    2,   1   )
      TKFRAME_-61303_UNITS         = 'DEGREES'

   \begintext


JIRAM Frames:
-------------------------------------------------------------------------------

   The set of frames for the JIRAM experiment includes the unit
   reference frame (URF) -- JUNO_JIRAM_URF, -- the imager and
   spectrometer frames -- JUNO_JIRAM_I and JUNO_JIRAM_S, -- and the
   imager L-band and M-band channel frames -- JUNO_JIRAM_I_LBAND and
   JUNO_JIRAM_I_MBAND. This set of frames does not attempt to account
   for the de-spinning mirror motion and assumes that the de-spinning
   compensation results in effectively inertially fixed instrument
   pointing for a given observation.

   The JIRAM unit reference frame -- JUNO_JIRAM_URF -- is the JIRAM
   "hardware" frame. It is fixed w.r.t. to the spacecraft and is
   defined as follows:

      -  +Z axis is normal to the JIRAM optical head base, points from
         the base towards the spacecraft, and is nominally co-aligned
         with the spacecraft +Z axis;

      -  +X axis is along the nominal FOV center axis

      -  +Y axis completes the right-handed frame

      -  the origin of the frame is at center of the JIRAM optical
         head reference mounting hole.

   This diagram illustrates the JIRAM unit reference frame:

      Spacecraft +Z side view:
      ------------------------

                Solar Array 3             <-. Spin Direction
               ~ ~ ~ ~ ~ ~ ~ ~               `.
               \   .-'        \.
      -.        \-'         .-' `-.
        ` +Xurf  \       .-'       `-.
      22    <-.   \   .-'    ----- .  `-.      Solar Array 1
      deg      `-. .-'    +Ysc ^    `.   `-.--------------------.
      ---         `o    /      |      \    |      |      |      |
                  /|+Zurf      |       \   |      |      |      |``--..
                 / |  '        |    +Xsc   |      |      |      |      `--..
                /  |  |        o------> |  |      |      |      |           |
               V   |  .      +Zsc       ,  |      |      |      |     ..--''
          +Yurf    |   \               /   |      |      |      |..--'
                   |    \ HGA         /    |      |      |      | Magnetometer
                   `-.   `.         .'   .-'--------------------'     Boom
                  /   `-.  ` ----- '  .-'
                 /       `-.       .-'
                /           `-. .-'
               /`-.           /'
               ~ ~ ~ ~ ~ ~ ~ ~
               Solar Array 2                  +Zurf and +Zsc are out of
                                                     the page.

   As seen on the diagram the JUNO_JIRAM_URF frame is nominally rotated
   from the spacecraft frame by +158 degrees about +Z.

   Since the frame definition below contain the reverse transformation
   -- from the JIRAM unit reference frame to the spacecraft frame --
   the order of rotations is reversed and the signs of rotation angles
   are changed to the opposite ones compared to the description above.

   \begindata

      FRAME_JUNO_JIRAM_URF         = -61401
      FRAME_-61401_NAME            = 'JUNO_JIRAM_URF'
      FRAME_-61401_CLASS           = 4
      FRAME_-61401_CLASS_ID        = -61401
      FRAME_-61401_CENTER          = -61
      TKFRAME_-61401_SPEC          = 'ANGLES'
      TKFRAME_-61401_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61401_ANGLES        = ( -158.0, 0.0, 0.0 )
      TKFRAME_-61401_AXES          = (    3,   2,   1   )
      TKFRAME_-61401_UNITS         = 'DEGREES'

   \begintext

   The JIRAM imager and spectrometer frames -- JUNO_JIRAM_I and
   JUNO_JIRAM_S, -- and the imager L-band and M-band channel frames --
   JUNO_JIRAM_I_LBAND and JUNO_JIRAM_I_MBAND -- are the "image" frames
   defined as follows:

      -  +Z axis is along the boresight (view direction of the center
         pixel of the spectrometer line, combined imager CCD or individual
         L-band and M-band CCDs);

      -  +X axis is along the CCD columns (spectral direction of the
         spectrometer), pointing in the "along-track" direction resulting
         from the spacecraft rotation

      -  +Y axis completes the right-handed frame, pointing along the
         spatial spectrometer direction.

      -  the origin of the frame is the instrument's focal point.

   This diagram illustrates the spectrometer and images frames:

      Spacecraft +Z side view:
      ------------------------

                Solar Array 3             <-. Spin Direction
               ~ ~ ~ ~ ~ ~ ~ ~               `.
               \   .-'        \.
                  '         .-' `-.
          +Zs/i/m/l      .-'       `-.
            <-.       .-'    ----- .  `-.      Solar Array 1
               `-. .-'    +Ysc ^    `.   `-.--------------------.
                  `o    /      |      \    |      |      |      |
                  /|+Ys/i/m/l  |       \   |      |      |      |``--..
                 / |  '        |    +Xsc   |      |      |      |      `--..
                /  |  |        o------> |  |      |      |      |           |
               V   |  .      +Zsc       ,  |      |      |      |     ..--''
      +Xs/i/m/l    |   \               /   |      |      |      |..--'
                   |    \ HGA         /    |      |      |      | Magnetometer
                   `-.   `.         .'   .-'--------------------'     Boom
                  /   `-.  ` ----- '  .-'
                 /       `-.       .-'
                /           `-. .-'
               /`-.           /'
               ~ ~ ~ ~ ~ ~ ~ ~
               Solar Array 2                  +Ys/i/m/l and +Zsc are out of
                                                      the page.

   The spectrometer frame is defined w.r.t. to the unit reference
   frame; the imager frame is defined w.r.t. to the spectrometer frame;
   the imager L-band and M-band channel frames are defined w.r.t. to
   the imager frame.

   Nominally the JIRAM spectrometer frame is rotated from the unit reference
   frame first by +90 degrees about +Y, then by +90 degrees about +Z, then
   by +7 degrees about +Y.

   Nominally the JIRAM imager frame is rotated from the spectrometer
   frame by TBD degrees about +Y. (Placeholder value is +0.88 degrees
   assuming that the slit is in the middle of the M-band CCD; this
   values was picked abritrarily because various materials in [4] provide
   contradicting information.)

   Nominally the JIRAM imager L-band frame is rotated from the imager frame
   by +0.88 degrees (1/2 of L-band CCD) about +Y.

   Nominally the JIRAM imager M-band frame is rotated from the imager frame
   by -0.88 degrees (1/2 of M-band CCD) about +Y.

   Since the frame definitions below contain the reverse
   transformations, the order of rotations is reversed and the signs of
   rotation angles are changed to the opposite ones compared to the
   description above.

   \begindata

      FRAME_JUNO_JIRAM_S           = -61420
      FRAME_-61420_NAME            = 'JUNO_JIRAM_S'
      FRAME_-61420_CLASS           = 4
      FRAME_-61420_CLASS_ID        = -61420
      FRAME_-61420_CENTER          = -61
      TKFRAME_-61420_SPEC          = 'ANGLES'
      TKFRAME_-61420_RELATIVE      = 'JUNO_JIRAM_URF'
      TKFRAME_-61420_ANGLES        = ( -90.0, -90.0, -7.0 )
      TKFRAME_-61420_AXES          = (   2,     3,    2   )
      TKFRAME_-61420_UNITS         = 'DEGREES'

      FRAME_JUNO_JIRAM_I           = -61410
      FRAME_-61410_NAME            = 'JUNO_JIRAM_I'
      FRAME_-61410_CLASS           = 4
      FRAME_-61410_CLASS_ID        = -61410
      FRAME_-61410_CENTER          = -61
      TKFRAME_-61410_SPEC          = 'ANGLES'
      TKFRAME_-61410_RELATIVE      = 'JUNO_JIRAM_S'
      TKFRAME_-61410_ANGLES        = ( 0.0, -0.88, 0.0 )
      TKFRAME_-61410_AXES          = ( 3,    2,    1   )
      TKFRAME_-61410_UNITS         = 'DEGREES'

      FRAME_JUNO_JIRAM_I_LBAND     = -61411
      FRAME_-61411_NAME            = 'JUNO_JIRAM_I_LBAND'
      FRAME_-61411_CLASS           = 4
      FRAME_-61411_CLASS_ID        = -61411
      FRAME_-61411_CENTER          = -61
      TKFRAME_-61411_SPEC          = 'ANGLES'
      TKFRAME_-61411_RELATIVE      = 'JUNO_JIRAM_I'
      TKFRAME_-61411_ANGLES        = ( 0.0, -0.88, 0.0 )
      TKFRAME_-61411_AXES          = ( 3,    2 ,   1   )
      TKFRAME_-61411_UNITS         = 'DEGREES'

      FRAME_JUNO_JIRAM_I_MBAND     = -61412
      FRAME_-61412_NAME            = 'JUNO_JIRAM_I_MBAND'
      FRAME_-61412_CLASS           = 4
      FRAME_-61412_CLASS_ID        = -61412
      FRAME_-61412_CENTER          = -61
      TKFRAME_-61412_SPEC          = 'ANGLES'
      TKFRAME_-61412_RELATIVE      = 'JUNO_JIRAM_I'
      TKFRAME_-61412_ANGLES        = ( 0.0, +0.88, 0.0 )
      TKFRAME_-61412_AXES          = ( 3,    2,    1   )
      TKFRAME_-61412_UNITS         = 'DEGREES'

   \begintext


JUNOCAM Frames
-------------------------------------------------------------------------------

   The JUNOCAM frame -- JUNO_JUNOCAM -- is fixed w.r.t. to the
   spacecraft and defined as follows:

      -  +Z axis is along the camera boresight;

      -  +X axis is along the CCD lines, pointing in the increasing
         pixel direction

      -  +Y axis completes the right-handed frame

      -  the origin of the frame is at the camera focal point.

   This diagram illustrates the JUNOCAM frame:

      Spacecraft +Z side view:
      ------------------------

                Solar Array 3             <-. Spin Direction
               ~ ~ ~ ~ ~ ~ ~ ~               `.
               \   .-'        \.
                \-'         .-' `-.
                 \       .-'       `-.
                  \   .-'    ----- .  `-.      Solar Array 1
                   .-'    +Ysc ^    `.   `-.--------------------.
                   |    /      |      \    |      |      |      |
                   |   /       |       \   |      |      |      |``--..
                      '        |    +Xsc   |      |      |      |      `--..
                 +Xjc |        o------> |  |      |      |      |           |
            <------x  .      +Zsc       ,  |      |      |      |     ..--''
          +Zjc     |   \               /   |      |      |      |..--'
                   |    \ HGA         /    |      |      |      | Magnetometer
                   | .   `.         .'   .-'--------------------'     Boom
                   V  `-.  ` ----- '  .-'
                 /  +Yjc `-.       .-'
                /           `-. .-'                +Xjc is into
               /`-.           /'                     the page.
               ~ ~ ~ ~ ~ ~ ~ ~
               Solar Array 2                       +Zsc is out of
                                                     the page.

   As seen on the diagram the JUNO_JUNOCAM frame is nominally rotated
   from the spacecraft frame first by 180 degrees about +Z, then by +90
   degrees about +Y.

   Since the frame definition below contain the reverse transformation
   -- from the JUNOCAM frame to the spacecraft frame -- the order of
   rotations is reversed and the signs of rotation angles are changed
   to the opposite ones compared to the description above.

   \begindata

      FRAME_JUNO_JUNOCAM           = -61500
      FRAME_-61500_NAME            = 'JUNO_JUNOCAM'
      FRAME_-61500_CLASS           = 4
      FRAME_-61500_CLASS_ID        = -61500
      FRAME_-61500_CENTER          = -61
      TKFRAME_-61500_SPEC          = 'ANGLES'
      TKFRAME_-61500_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61500_ANGLES        = ( 180.0, -90.0, 0.0 )
      TKFRAME_-61500_AXES          = (   3,     2,   1   )
      TKFRAME_-61500_UNITS         = 'DEGREES'

   \begintext


MWR Frames:
-------------------------------------------------------------------------------

   The set of frames for the MWR experiment includes six MWR antenna
   frames -- JUNO_MWR_A1, JUNO_MWR_A2, JUNO_MWR_A3, JUNO_MWR_A4,
   JUNO_MWR_A5, and JUNO_MWR_A6, -- fixed w.r.t. to the spacecraft and
   defined as follows:

      -  +Z axis is along the antenna boresight

      -  +Y axis is nominally along the spacecraft +Z axis

      -  +X axis completes the right-handed frame

      -  the origin of the frame is at the geometric center of the
         antenna patch or outer rim.

   This diagram illustrates the MWR antenna frames:

      Spacecraft +Z side view:
      ------------------------

              Solar Array 3              ^        <-. Spin Direction
               ~ ~ ~ ~ ~ ~ ~   +Xa1     / +Za1       `.
               \   .-'        <.       /
                \-'         .   `-.   /
                 \       .-'       `-o +Ya1
                  \   .-'    ----- .   -.      Solar Array 1
                   .-'    +Ysc ^    `.   `-.--------------------.
                   |    /      |      \    |      |      |      |
                   |   /       |       \   |      |      |      |``--..
                   |  '        |    +Xsc   |      |      |      |      `--..
                   |  |        o------> |  |      |      |      |           |
                   |  .      +Zsc       ,  |      |      |      |     ..--''
                   |   \               /                 |      |..--'
                   |    \ HGA         /     +Xa2/3/4/5/6 |      | Magnetometer
                   `-.   `.         .'   .->   -----------------'     Boom
                  /   `-.  ` ----- '  .-'
                 /       `-.         o +Ya2/3/4/5/6
                /           `-. .-'   \
               /`-.           /'       \
               ~ ~ ~ ~ ~ ~ ~ ~          \ +Za2/3/4/5/6
               Solar Array 2             V
                                                   +Ya* and +Zsc are
                                                    out of the page.


   The JUNO_MWR_A1 frame is nominally rotated from the spacecraft frame
   first by +150 degrees about +Z, then by +90 degrees about +X.

   The JUNO_MWR_A2..A6 frames are nominally rotated from the spacecraft
   frame first by +30 degrees about +Z, then by +90 degrees about +X.

   Since the frame definitions below contain the reverse
   transformations, the order of rotations is reversed and the signs of
   rotation angles are changed to the opposite ones compared to the
   description above.

   \begindata

      FRAME_JUNO_MWR_A1            = -61601
      FRAME_-61601_NAME            = 'JUNO_MWR_A1'
      FRAME_-61601_CLASS           = 4
      FRAME_-61601_CLASS_ID        = -61601
      FRAME_-61601_CENTER          = -61
      TKFRAME_-61601_SPEC          = 'ANGLES'
      TKFRAME_-61601_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61601_ANGLES        = ( -150.0, 0.0, -90.0 )
      TKFRAME_-61601_AXES          = (    3,   2,     1   )
      TKFRAME_-61601_UNITS         = 'DEGREES'

      FRAME_JUNO_MWR_A2            = -61602
      FRAME_-61602_NAME            = 'JUNO_MWR_A2'
      FRAME_-61602_CLASS           = 4
      FRAME_-61602_CLASS_ID        = -61602
      FRAME_-61602_CENTER          = -61
      TKFRAME_-61602_SPEC          = 'ANGLES'
      TKFRAME_-61602_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61602_ANGLES        = ( -30.0, 0.0, -90.0 )
      TKFRAME_-61602_AXES          = (   3,   2,     1   )
      TKFRAME_-61602_UNITS         = 'DEGREES'

      FRAME_JUNO_MWR_A3            = -61603
      FRAME_-61603_NAME            = 'JUNO_MWR_A3'
      FRAME_-61603_CLASS           = 4
      FRAME_-61603_CLASS_ID        = -61603
      FRAME_-61603_CENTER          = -61
      TKFRAME_-61603_SPEC          = 'ANGLES'
      TKFRAME_-61603_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61603_ANGLES        = ( -30.0, 0.0, -90.0 )
      TKFRAME_-61603_AXES          = (   3,   2,     1   )
      TKFRAME_-61603_UNITS         = 'DEGREES'

      FRAME_JUNO_MWR_A4            = -61604
      FRAME_-61604_NAME            = 'JUNO_MWR_A4'
      FRAME_-61604_CLASS           = 4
      FRAME_-61604_CLASS_ID        = -61604
      FRAME_-61604_CENTER          = -61
      TKFRAME_-61604_SPEC          = 'ANGLES'
      TKFRAME_-61604_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61604_ANGLES        = ( -30.0, 0.0, -90.0 )
      TKFRAME_-61604_AXES          =   ( 3,   2,     1   )
      TKFRAME_-61604_UNITS         = 'DEGREES'

      FRAME_JUNO_MWR_A5            = -61605
      FRAME_-61605_NAME            = 'JUNO_MWR_A5'
      FRAME_-61605_CLASS           = 4
      FRAME_-61605_CLASS_ID        = -61605
      FRAME_-61605_CENTER          = -61
      TKFRAME_-61605_SPEC          = 'ANGLES'
      TKFRAME_-61605_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61605_ANGLES        = ( -30.0, 0.0, -90.0 )
      TKFRAME_-61605_AXES          = (   3,   2,     1   )
      TKFRAME_-61605_UNITS         = 'DEGREES'

      FRAME_JUNO_MWR_A6            = -61606
      FRAME_-61606_NAME            = 'JUNO_MWR_A6'
      FRAME_-61606_CLASS           = 4
      FRAME_-61606_CLASS_ID        = -61606
      FRAME_-61606_CENTER          = -61
      TKFRAME_-61606_SPEC          = 'ANGLES'
      TKFRAME_-61606_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61606_ANGLES        = ( -30.0, 0.0, -90.0 )
      TKFRAME_-61606_AXES          = (   3,   2,     1   )
      TKFRAME_-61606_UNITS         = 'DEGREES'

   \begintext



UVS Frames
-------------------------------------------------------------------------------

   The set of frames for the UVS experiment includes two frames
   -- JUNO_UVS_BASE and JUNO_UVS.

   The UVS "hardware" frame, JUNO_UVS_BASE, is fixed w.r.t. to the
   spacecraft and defined as follows:

      -  +Z axis is normal to the sensor mounting plane and points
         into the sensor; it is nominally along the slit

      -  +X axis is parallel to the scan mirror rotation axis and points
         from the sensor electronics towards the entrance baffle

      -  +Y axis completes the right-handed frame

      -  the origin of the frame is at the center of the reference
         mounting hole.

   The UVS "observation" frame, JUNO_UVS, is a CK-based frame defined
   as follows:

      -  +X axis is the instrument boresight

      -  +Z axis is along the slit and for the "zero" scan mirror position
         points in the same direction as the +Z axis of the JUNO_UVS_BASE
         frame

      -  +Y axis completes the right-handed frame

      -  the origin of the frame is at the intersection of the
         reflected boresight and the scan mirror axis.

   This diagram illustrates the UVS frames (the JUNO_UVS frame is shown
   in the "zero" scan mirror position):

      Spacecraft +Z side view:
      ------------------------

                Solar Array 3             <-. Spin Direction
               ~ ~ ~ ~ ~ ~ ~ ~               `.
               \   .-'        \.
                \-'         .-' `-.
                 \       .-'       `-.
                      .-'    ----- .  `-.      Solar Array 1
                +Yu  '    +Ysc ^    `.   `-.--------------------.
                   ^    /      |      \    |      |      |      |
                   | +Xub      |       \   |      |      |      |``--..
                   |^          |    +Xsc   |      |      |      |      `--..
         +Xu       || |        o------> |  |      |      |      |           |
            <------x| .      +Zsc       ,  |      |      |      |     ..--''
                +Zu |  \               /   |      |      |      |..--'
                    x------>          /    |      |      |      | Magnetometer
                 +Zub    +Yub   HGA .'   .-'--------------------'     Boom
                  /   `-.    ----- '  .-'
                 /       `-.       .-'
                /           `-. .-'               +Zub and +Zu are
               /`-.           /'                    into the page.
               ~ ~ ~ ~ ~ ~ ~ ~
               Solar Array 2                       +Zsc is out of
                                                     the page.


      Scan Mirror Plane and Axis (Spacecraft +Z side view:):
      ------------------------------------------------------

                     |
                     | Scan Mirror Axis
                     |

                     ^ +Yu
                .    |
                 `.  |
            +Xu    `.|
              <------x.
    Reflected      +Zu `.    Scan Mirror plane
    boresight            `  in "zero" position

                     ^ +Xub                             ^ +Ysc
                     |                                  |
                     |                                  |
                     |                                  |
                     x------> Yub                       o------>
                   +Zub                              +Zsc       +Xsc


   As seen on the diagram the JUNO_UVS_BASE frame is nominally rotated
   from the spacecraft frame first by +90 degrees about +Z, then by 180
   degrees about +X.

   For a perfect nominal alignment of the boresight and scan mirror
   axis and a perfect nominal 45 degrees position of the mirror plane,
   at the "zero" mirror position the JUNO_UVS frame is simply rotated
   by -90 degrees about +Z of the JUNO_UVS_BASE frame. For any other
   mirror position within the +30/-30 degrees range the two additional
   rotations are needed: first by the "scan angle" about +Y, then by
   the "scan angle" about +X. (TBD: this needs to be further
   analyzed/confirmed.) These rotations will be stored in CK files.

   Since the frame JUNO_UVS_BASE definition below contain the reverse
   transformation -- from the UVS_BASE frame to the spacecraft frame --
   the order of rotations is reversed and the signs of rotation angles
   are changed to the opposite ones compared to the description above.

   \begindata

      FRAME_JUNO_UVS_BASE          = -61700
      FRAME_-61700_NAME            = 'JUNO_UVS_BASE'
      FRAME_-61700_CLASS           = 4
      FRAME_-61700_CLASS_ID        = -61700
      FRAME_-61700_CENTER          = -61
      TKFRAME_-61700_SPEC          = 'ANGLES'
      TKFRAME_-61700_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61700_ANGLES        = ( -90.0, 0.0, 180.0 )
      TKFRAME_-61700_AXES          = (   3,   2,     1   )
      TKFRAME_-61700_UNITS         = 'DEGREES'

      FRAME_JUNO_UVS               = -61701
      FRAME_-61701_NAME            = 'JUNO_UVS'
      FRAME_-61701_CLASS           = 3
      FRAME_-61701_CLASS_ID        = -61701
      FRAME_-61701_CENTER          = -61
      CK_-61701_SCLK               = -61
      CK_-61701_SPK                = -61

   \begintext


WAVES Frames
-------------------------------------------------------------------------------

   The set of frames for the WAVES experiment includes two frames
   -- JUNO_WAVES_MSC and  JUNO_WAVES_ANTENNA.

   The WAVES MSC frame, JUNO_WAVES_MSC, is fixed w.r.t. to the
   spacecraft and defined as follows:

      -  +Z axis is along the MSC center axis and points in the same
         direction as the spacecraft +Z axis

      -  +Y axis is in the mounting plate plane and points away from
         the spacecraft

      -  +X axis completes the right-handed frame

      -  the origin of the frame is at the geometric center of the  MSC
         center axis.

   The WAVES electrical antenna frame, JUNO_WAVES_ANTENNA, is fixed
   w.r.t. to the spacecraft and defined as follows:

      -  +Z axis is normal to the antenna mounting plane and points
         away from the spacecraft; it is nominally co-aligned with the
         spacecraft -Z axis

      -  +Y axis is in the mounting plate plane and points between the
         two antennas is stowed position

      -  +X axis completes the right-handed frame

      -  the origin of the frame is at the geometric center of the
         antenna mounting plate.

   This diagram illustrates the WAVES frames:

      Spacecraft +Z side view:
      ------------------------

                Solar Array 3             <-. Spin Direction
               ~ ~ ~ ~ ~ ~ ~ ~               `.
               \   .-'        \.
                \-'         .-' `-.
                 \       .-'       `-.
                  \   .-'    ----- .  `-.      Solar Array 1
                   .-'    +Ysc ^    `.   `-.--------------------.
                   |    /      |      \    |      |      |      |
                   |   /       |           |      |      |      |``--..
                   |  '        |     +Yant               |      |      `--..
                   |  |        o----> <----x +Zant       |      |           |
                   |  .    +Zsc   +Xsc  ,  |             |      |     ..--''
                   |   \               /   |      |      |      |..--'
                   |    \ HGA         /    |      |      |      | Magnetometer
                   `-.   `.         .'   . V -------------------'     Boom
                  /   `-.  ` ----- '  .-'   +Xant
        Solar    /       `-.         '
       Array 2  /           `  .o +Zmsc
               /`-.         .-'  \
               ~ ~ ~ ~   <-'      \
                       +Xmsc       \                +Zsc is out of
                                    V +Ymsc            the page.

   The JUNO_WAVES_MSC frame is nominally rotated from the spacecraft
   frame by -150 degrees about +Z.

   The JUNO_WAVES_ANTENNA frame is nominally rotated from the spacecraft
   frame first by -90 degrees about +Z, then by 180 degrees about +X.

   Since the frame definitions below contain the reverse
   transformations, the order of rotations is reversed and the signs of
   rotation angles are changed to the opposite ones compared to the
   description above.

   \begindata

      FRAME_JUNO_WAVES_MSC         = -61810
      FRAME_-61810_NAME            = 'JUNO_WAVES_MSC'
      FRAME_-61810_CLASS           = 4
      FRAME_-61810_CLASS_ID        = -61810
      FRAME_-61810_CENTER          = -61
      TKFRAME_-61810_SPEC          = 'ANGLES'
      TKFRAME_-61810_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61810_ANGLES        = ( 150.0, 0.0, 0.0 )
      TKFRAME_-61810_AXES          = (   3,   2,   1   )
      TKFRAME_-61810_UNITS         = 'DEGREES'

      FRAME_JUNO_WAVES_ANTENNA     = -61820
      FRAME_-61820_NAME            = 'JUNO_WAVES_ANTENNA'
      FRAME_-61820_CLASS           = 4
      FRAME_-61820_CLASS_ID        = -61820
      FRAME_-61820_CENTER          = -61
      TKFRAME_-61820_SPEC          = 'ANGLES'
      TKFRAME_-61820_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61820_ANGLES        = ( 90.0, 0.0, 180.0 )
      TKFRAME_-61820_AXES          = (  3,   2,     1   )
      TKFRAME_-61820_UNITS         = 'DEGREES'

   \begintext


Solar Array Frames
-------------------------------------------------------------------------------

   Two frames are defined for each of the three solar arrays.

   The first frame -- a fixed-offset frame named JUNO_SA#_HINGE (where
   # is 1, 2, or 3) -- is fixed w.r.t. to the spacecraft and is defined
   as follows:

      -  +Z axis is co-aligned with the s/c +Z axis

      -  +X axis is along the solar array symmetry axis and points
         from the hinge to the outer side of the array

      -  +Y axis is along the hinge axis and points to complete the
         right-handed frame

      -  the origin of the frame is in the middle of the hinge axis

   The second frame -- a CK-based frame named JUNO_SA# (where # is 1,
   2, or 3) -- rotates about the hinge (+Y) with respect to the
   corresponding JUNO_SA#_HINGE frame and is defined as follows:

      -  +Z axis is along the normal to the array surface on the solar
         cell side

      -  +X axis is along the solar array symmetry axis and points
         from the hinge towards the outer side of the array

      -  +Y axis is along the hinge axis and points to complete the
         right-handed frame

      -  the origin of the frame is in the middle of between two center
         sections of the array

   In the non-articulated ("zero") position the two frames for each of the
   arrays are co-aligned, as shown on this diagram:

      Spacecraft +Z side view:
      ------------------------

                .-\
             .-'   \
          .-'       \ Solar Array 3
       .-'           \
       \           .-'\
        \      ^ +Xsa3
         \   ,  \       \
          \-'    \    .-'\
           \      o +Zsa3 \
        +Ysa3   .-'        \
             <-'         .-'\             <-. Spin Direction
                     ^ +Xsa3h                `.
               \   .  \       \.
                \-'    \    .-' `-.
                 \      o +Zsa3h   `-.
             +Ysa3h   .-'    ----- .  `-. +Ysa1h       +Ysa1    Solar Array 1
                  <.-'    +Ysc ^    `.   ` ^  ---------  ^  ----.
                        /      |      \    |      |      |      |
                   |   /       |       \   |      |      |      |``--..
                   |  '        |    +Xsc   |   +Xsa1h    |    +Xsa1    `--..
                   |  |        o------> |  o----->       o----->            |
                   |  .      +Zsc       , +Zsa1h       +Zsa1    |     ..--''
                   |   \               /   |      |      |      |..--'
                   |    \ HGA         /    |      |      |      | Magnetometer
                   `-.   `.         .'   .-'--------------------'     Boom
                  /   +Zsa2h ----- '  .-'
                 /      o`-.       .-'
                /      /    `->
               +Xsa2h /        +Ysa2h
              /      V       /
             /         -.   /
            /`-. +Zsa2   `-/
           /      o       /
          /      / `-.
         +Xsa2  /     `-> +Ysa2
        /      V
       /         -.   /
      /.           `-/
        `-.         / Solar Array 2              All +Z axes are out of
           `-.     /                                    the page.
              `-. /
                 `


   The keywords below define the solar array frames.

   \begindata

      FRAME_JUNO_SA1_HINGE         = -61010
      FRAME_-61010_NAME            = 'JUNO_SA1_HINGE'
      FRAME_-61010_CLASS           = 4
      FRAME_-61010_CLASS_ID        = -61010
      FRAME_-61010_CENTER          = -61
      TKFRAME_-61010_SPEC          = 'ANGLES'
      TKFRAME_-61010_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61010_ANGLES        = ( 0.0, 0.0, 0.0 )
      TKFRAME_-61010_AXES          = ( 1,   2,   3   )
      TKFRAME_-61010_UNITS         = 'DEGREES'

      FRAME_JUNO_SA1               = -61011
      FRAME_-61011_NAME            = 'JUNO_SA1'
      FRAME_-61011_CLASS           = 3
      FRAME_-61011_CLASS_ID        = -61011
      FRAME_-61011_CENTER          = -61
      CK_-61011_SCLK               = -61
      CK_-61011_SPK                = -61

      FRAME_JUNO_SA2_HINGE         = -61020
      FRAME_-61020_NAME            = 'JUNO_SA2_HINGE'
      FRAME_-61020_CLASS           = 4
      FRAME_-61020_CLASS_ID        = -61020
      FRAME_-61020_CENTER          = -61
      TKFRAME_-61020_SPEC          = 'ANGLES'
      TKFRAME_-61020_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61020_ANGLES        = ( 0.0, 0.0, 0.0 )
      TKFRAME_-61020_AXES          = ( 1,   2,   3   )
      TKFRAME_-61020_UNITS         = 'DEGREES'

      FRAME_JUNO_SA2               = -61021
      FRAME_-61021_NAME            = 'JUNO_SA2'
      FRAME_-61021_CLASS           = 3
      FRAME_-61021_CLASS_ID        = -61021
      FRAME_-61021_CENTER          = -61
      CK_-61021_SCLK               = -61
      CK_-61021_SPK                = -61

      FRAME_JUNO_SA3_HINGE         = -61030
      FRAME_-61030_NAME            = 'JUNO_SA3_HINGE'
      FRAME_-61030_CLASS           = 4
      FRAME_-61030_CLASS_ID        = -61030
      FRAME_-61030_CENTER          = -61
      TKFRAME_-61030_SPEC          = 'ANGLES'
      TKFRAME_-61030_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61030_ANGLES        = ( 0.0, 0.0, 0.0 )
      TKFRAME_-61030_AXES          = ( 1,   2,   3   )
      TKFRAME_-61030_UNITS         = 'DEGREES'

      FRAME_JUNO_SA3               = -61031
      FRAME_-61031_NAME            = 'JUNO_SA3'
      FRAME_-61031_CLASS           = 3
      FRAME_-61031_CLASS_ID        = -61031
      FRAME_-61031_CENTER          = -61
      CK_-61031_SCLK               = -61
      CK_-61031_SPK                = -61

   \begintext


Antenna Frames
-------------------------------------------------------------------------------

   The JUNO HGA, MGA, and "forward" and "aft" LGA antenna frames --
   JUNO_HGA, JUNO_MGA, JUNO_LGA_FORWARD, and JUNO_LGA_AFT -- are
   defined as follows:

      -  +Z axis is along the antenna boresight

      -  +X axis is along the clock reference direction of the antenna
         pattern

      -  +Y axis completes the right-handed frame

      -  the origin of the frame is in the geometric center of the
         antenna's outer rim or patch

   The JUNO "toroid" LGA frame -- JUNO_LGA_TOROID -- is defined to be
   co-aligned with the spacecraft frame.

   All antenna frames are defined as fixed-offset frames with respect
   to the spacecraft frame.

   Nominally the all antenna frames (except for JUNO_LGA_AFT) are
   co-aligned with the spacecraft frame. The JUNO_LGA_AFT frame is
   rotated from the spacecraft frame by 180 degrees about +X.

   This diagram illustrates the antenna frames:

      Spacecraft -Y side view:
      ------------------------

                         +Zhga
                               ^
                               | +Zmga,+Zlgaf
                               |    ^ ^
                               |    | |
                         +Yhga x------> +Xhga
                              / \   | |
                  HGA .-------------x-x---->-> +Xmga,+Xlgaf
                       \      +Ymga,+Ylgaf
                        `.           .'
                           `-------'
                           |       |                            Magnetometer
                           |       |                                Boom
      ================o==o==o==o-----------o======o======o======o===========*
          Solar    |           |           |   Solar Array 1
         Array 2   |           |           |
                   |                       |
                   |                       |
                   |      +Zsc ^           |
                   |    +Zlgat |           |
                   |           |           |
                   |           |           |          +Ysc, +Yhga, Ylgaf,
                   `----- +Ysc x------>   -'          and +Ylgat are into
            +Ylgaa o------>  /_____\  +Xsc                  the page.
                   |    +Xlgaa       +Xlgat
                   |                                   +Ylgaa is out of
                   |                                      the page.
                   V +Zlgaa


   The keywords below define the antenna frames.

   \begindata

      FRAME_JUNO_HGA               = -61040
      FRAME_-61040_NAME            = 'JUNO_HGA'
      FRAME_-61040_CLASS           = 4
      FRAME_-61040_CLASS_ID        = -61040
      FRAME_-61040_CENTER          = -61
      TKFRAME_-61040_SPEC          = 'ANGLES'
      TKFRAME_-61040_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61040_ANGLES        = ( 0.0, 0.0, 0.0 )
      TKFRAME_-61040_AXES          = ( 1,   2,   3   )
      TKFRAME_-61040_UNITS         = 'DEGREES'

      FRAME_JUNO_MGA               = -61050
      FRAME_-61050_NAME            = 'JUNO_MGA'
      FRAME_-61050_CLASS           = 4
      FRAME_-61050_CLASS_ID        = -61050
      FRAME_-61050_CENTER          = -61
      TKFRAME_-61050_SPEC          = 'ANGLES'
      TKFRAME_-61050_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61050_ANGLES        = ( 0.0, 0.0, 0.0 )
      TKFRAME_-61050_AXES          = ( 1,   2,   3   )
      TKFRAME_-61050_UNITS         = 'DEGREES'

      FRAME_JUNO_LGA_FORWARD       = -61061
      FRAME_-61061_NAME            = 'JUNO_LGA_FORWARD'
      FRAME_-61061_CLASS           = 4
      FRAME_-61061_CLASS_ID        = -61061
      FRAME_-61061_CENTER          = -61
      TKFRAME_-61061_SPEC          = 'ANGLES'
      TKFRAME_-61061_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61061_ANGLES        = ( 0.0, 0.0, 0.0 )
      TKFRAME_-61061_AXES          = ( 1,   2,   3   )
      TKFRAME_-61061_UNITS         = 'DEGREES'

      FRAME_JUNO_LGA_AFT           = -61062
      FRAME_-61062_NAME            = 'JUNO_LGA_AFT'
      FRAME_-61062_CLASS           = 4
      FRAME_-61062_CLASS_ID        = -61062
      FRAME_-61062_CENTER          = -61
      TKFRAME_-61062_SPEC          = 'ANGLES'
      TKFRAME_-61062_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61062_ANGLES        = ( 180.0, 0.0, 0.0 )
      TKFRAME_-61062_AXES          = (   1,   2,   3   )
      TKFRAME_-61062_UNITS         = 'DEGREES'

      FRAME_JUNO_LGA_TOROID        = -61063
      FRAME_-61063_NAME            = 'JUNO_LGA_TOROID'
      FRAME_-61063_CLASS           = 4
      FRAME_-61063_CLASS_ID        = -61063
      FRAME_-61063_CENTER          = -61
      TKFRAME_-61063_SPEC          = 'ANGLES'
      TKFRAME_-61063_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61063_ANGLES        = ( 0.0, 0.0, 0.0 )
      TKFRAME_-61063_AXES          = ( 1,   2,   3   )
      TKFRAME_-61063_UNITS         = 'DEGREES'

   \begintext


ACS Sensor Frames
-------------------------------------------------------------------------------

   This section defined frames for ACS sensors -- SRUs and SSSs.


SRU Frames

   The JUNO SRU frames -- JUNO_SRU1 and JUNO_SRU2 -- are defined as
   follows:

      -  +Z axis is along the SRU boresight

      -  +X axis is nominally along the spacecraft -Z axis

      -  +Y axis completes the right-handed frame

      -  the origin of the frame is at the SRU focal point

   Nominally the SRU1 frame is rotated from the spacecraft frame first
   by +90 degrees about Y, then by -50 degrees about X.

   Nominally the SRU2 frame is rotated from the spacecraft frame first
   by +90 degrees about Y, then by -60 degrees about X.

   This diagram illustrates the SRU frames:

      Spacecraft +Z side view:
      ------------------------
                                        +Zsru2
             Solar Array 3                ^            <-. Spin Direction
                                  +Ysru1 /  10 deg        `.
               ~ ~ ~ ~ ~ +Ysru2 <. <.   /
                \-'               `-.`./      .> +Zsru1
                 \       .-'   +Xsru2`x.   .-'
                  \   .-'    ---      `-`x'     Solar Array 1
                   .-'    +Ysc ^       +Xsru1  -----------------.
                   |    /      |      \           |      |      |
                   |   /       |       \   |      |      |      |``--..
                   |  '        |    +Xsc   |      |      |      |      `--..
                   |  |        o------> |  |      |      |      |           |
                   |  .      +Zsc       ,  |      |      |      |     ..--''
                   |   \               /   |      |      |      |..--'
                   |    \ HGA         /    |      |      |      | Magnetometer
                   `-.   `.         .'   .-'--------------------'     Boom
                  /   `-.  ` ----- '  .-'
                 /       `-.       .-'
                /           `-. .-'              +Xsru1 and +Xsru2 are
               ~ ~ ~ ~ ~ ~ ~ ~ '                    into the page.

            Solar Array 2                            +Zsc is out of
                                                        the page.

   Since the frame definitions below contains the reverse
   transformations -- from the SRU frames to the spacecraft frame --
   the order of rotations is reversed and the signs of rotation angles
   are changed to the opposite ones compared to the description above.

   \begindata

      FRAME_JUNO_SRU1              = -61071
      FRAME_-61071_NAME            = 'JUNO_SRU1'
      FRAME_-61071_CLASS           = 4
      FRAME_-61071_CLASS_ID        = -61071
      FRAME_-61071_CENTER          = -61
      TKFRAME_-61071_SPEC          = 'ANGLES'
      TKFRAME_-61071_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61071_ANGLES        = ( 0.0, -90.0, 50.0 )
      TKFRAME_-61071_AXES          = ( 3,     2,    1   )
      TKFRAME_-61071_UNITS         = 'DEGREES'

      FRAME_JUNO_SRU2              = -61072
      FRAME_-61072_NAME            = 'JUNO_SRU2'
      FRAME_-61072_CLASS           = 4
      FRAME_-61072_CLASS_ID        = -61072
      FRAME_-61072_CENTER          = -61
      TKFRAME_-61072_SPEC          = 'ANGLES'
      TKFRAME_-61072_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61072_ANGLES        = ( 0.0, -90.0, 60.0 )
      TKFRAME_-61072_AXES          = ( 3,     2,    1   )
      TKFRAME_-61072_UNITS         = 'DEGREES'

   \begintext


SSS Frames

   The JUNO SSS frames -- JUNO_SSS1 and JUNO_SSS2 -- are defined as
   follows:

      -  +Z axis is along the SSS boresight and is nominally along the
         spacecraft -X axis.

      -  +X axis is nominally along the spacecraft -Z axis

      -  +Y axis completes the right-handed frame

      -  the origin of the frame is at the SSS geometric center

   Nominally the SSS frames are rotated from the spacecraft frame first
   by +90 degrees about Y, then by 180 degrees about X.

   This diagram illustrates the SSS frames:

      Spacecraft +Z side view:
      ------------------------

             Solar Array 3                <-. Spin Direction
                                             `.
               ~ ~ ~ ~ ~ ~ ~ ~\.
                \-'         .-' `-.
                 \       .-'       `-.
                  \   .-'    ----- .  `-.      Solar Array 1
                   .-'    +Ysc ^    `.   `-.--------------------.
     +Zss1                     |      \    |      |      |      |
           <------x +Xsss1     |       \   |      |      |      |``--..
           <------x +Xsss2     |    +Xsc   |      |      |      |      `--..
     +Zsss2       |            o------> |  |      |      |      |           |
                  ||  .      +Zsc       ,  |      |      |      |     ..--''
           +Ysss1 V|   \               /   |      |      |      |..--'
           +Ysss2 V|    \ HGA         /    |      |      |      | Magnetometer
                   `-.   `.         .'   .-'--------------------'     Boom
                  /   `-.  ` ----- '  .-'
                 /       `-.       .-'
                /           `-. .-'             +Xsss1 and +Xsss2 are
               ~ ~ ~ ~ ~ ~ ~ ~/'                    into the page.

             Solar Array 2                          +Zsc is out of
                                                      the page.

   Since the frame definitions below contains the reverse
   transformations -- from the SSS frames to the spacecraft frame --
   the order of rotations is reversed and the signs of rotation angles
   are changed to the opposite ones compared to the description above.

   \begindata

      FRAME_JUNO_SSS1              = -61073
      FRAME_-61073_NAME            = 'JUNO_SSS1'
      FRAME_-61073_CLASS           = 4
      FRAME_-61073_CLASS_ID        = -61073
      FRAME_-61073_CENTER          = -61
      TKFRAME_-61073_SPEC          = 'ANGLES'
      TKFRAME_-61073_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61073_ANGLES        = ( 0.0, -90.0, 180.0 )
      TKFRAME_-61073_AXES          = ( 3,     2,     1   )
      TKFRAME_-61073_UNITS         = 'DEGREES'

      FRAME_JUNO_SSS2              = -61074
      FRAME_-61074_NAME            = 'JUNO_SSS2'
      FRAME_-61074_CLASS           = 4
      FRAME_-61074_CLASS_ID        = -61074
      FRAME_-61074_CENTER          = -61
      TKFRAME_-61074_SPEC          = 'ANGLES'
      TKFRAME_-61074_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61074_ANGLES        = ( 0.0, -90.0, 180.0 )
      TKFRAME_-61074_AXES          = ( 3,     2,     1   )
      TKFRAME_-61074_UNITS         = 'DEGREES'

   \begintext


Truster Frames
-------------------------------------------------------------------------------

   The JUNO REM thruster frames -- JUNO_REM_[FL1,2,3,4] [FA1,2]
   [RL1,2,3,4] [RA1,2] -- are defined as follows:

      -  +Z axis is along the thrust vector.

      -  +X axis is in the plane containing the thrust vector and the
         spacecraft +Z axis and points in the direction of the
         spacecraft +Z axis

      -  +Y axis completes the right-handed frame

      -  the origin of the frame is center of the nozzle outer edge.

   These diagrams approximately illustrate the REM thruster vector
   directions -- +Z axes of the REM frames, -- other axes are not
   shown:

      Spacecraft +Z side view:
      ------------------------

             Solar Array 3                <-. Spin Direction
                               ^ +Zfa1        `.
               ~ ~ ~ ~ ~ ~ ~ ~\|
                 +Zfl4 <------@@@------> +Zfl1
                 \        FL4 FA1 FL1
                  \   .-'    ----- .  `-.      Solar Array 1
                   .-'    +Ysc ^    `.   `-.--------------------.
                   |    /      |      \    |      |      |      |
                   |   /       |       \   |      |      |      |``--..
                   |  '        |    +Xsc   |      |      |      |      `--..
                   |  |        o------> |  |      |      |      |           |
                   |  .      +Zsc       ,  |      |      |      |     ..--''
                   |   \               /   |      |      |      |..--'
                   |    \ HGA         /    |      |      |      | Magnetometer
                   `-.   `.         .'   .-'--------------------'     Boom
                  /   `-.  ` ----- '  .-'
                 /        FL3 FA2 FL2
                /+Zfl3 <------@@@------> +Zfl2
               ~ ~ ~ ~ ~ ~ ~ ~/|
                               v +Zfa2
             Solar Array 2                           +Zsc is out of
                                                      the page.

      Spacecraft -Z side view:
      ------------------------

             Solar Array 2                 -. Spin Direction
                               ^ +Zra2       `.
               ~ ~ ~ ~ ~ ~ ~ ~\|               v
                 +Zrl3 <------@@@------> +Zrl2
                 \        RL3 RA2 RL2
                  \   .-'             `-.      Solar Array 1
                   .-'                   `-.--------------------.
                   |                       |      |      |      |
                   |                       |      |      |      |``--..
                   |        +Zsc    +Xsc   |      |      |      |      `--..
                   |           o------>    |      |      |      |           |
                   |           |           |      |      |      |     ..--''
                   |           |           |      |      |      |..--'
                   |           |           |      |      |      | Magnetometer
                   `-.    +Ysc V         .-'--------------------'     Boom
                  /   `-.             .-'
                 /        RL4 RA1 RL1
                 +Zrl4 <------@@@------> +Zrl1
               ~ ~ ~ ~ ~ ~ ~ ~/|
                               v +Zra1
             Solar Array 3                           +Zsc is into
                                                      the page.

   The angles in the REM frame definitions below are based the
   information from [4].

   \begindata

      FRAME_JUNO_REM_FL1           = -61081
      FRAME_-61081_NAME            = 'JUNO_REM_FL1'
      FRAME_-61081_CLASS           = 4
      FRAME_-61081_CLASS_ID        = -61081
      FRAME_-61081_CENTER          = -61
      TKFRAME_-61081_SPEC          = 'ANGLES'
      TKFRAME_-61081_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61081_ANGLES        = (   22.009651,  -76.551858,  157.431346 )
      TKFRAME_-61081_AXES          = ( 1,   2,   3   )
      TKFRAME_-61081_UNITS         = 'DEGREES'

      FRAME_JUNO_REM_FL2           = -61082
      FRAME_-61082_NAME            = 'JUNO_REM_FL2'
      FRAME_-61082_CLASS           = 4
      FRAME_-61082_CLASS_ID        = -61082
      FRAME_-61082_CENTER          = -61
      TKFRAME_-61082_SPEC          = 'ANGLES'
      TKFRAME_-61082_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61082_ANGLES        = (  -22.009640,  -76.551859, -157.431357 )
      TKFRAME_-61082_AXES          = ( 1,   2,   3   )
      TKFRAME_-61082_UNITS         = 'DEGREES'

      FRAME_JUNO_REM_FL3           = -61083
      FRAME_-61083_NAME            = 'JUNO_REM_FL3'
      FRAME_-61083_CLASS           = 4
      FRAME_-61083_CLASS_ID        = -61083
      FRAME_-61083_CENTER          = -61
      TKFRAME_-61083_SPEC          = 'ANGLES'
      TKFRAME_-61083_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61083_ANGLES        = (  -22.009651,   76.551858,  -22.568654 )
      TKFRAME_-61083_AXES          = ( 1,   2,   3   )
      TKFRAME_-61083_UNITS         = 'DEGREES'

      FRAME_JUNO_REM_FL4           = -61084
      FRAME_-61084_NAME            = 'JUNO_REM_FL4'
      FRAME_-61084_CLASS           = 4
      FRAME_-61084_CLASS_ID        = -61084
      FRAME_-61084_CENTER          = -61
      TKFRAME_-61084_SPEC          = 'ANGLES'
      TKFRAME_-61084_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61084_ANGLES        = (   22.009640,   76.551859,   22.568643 )
      TKFRAME_-61084_AXES          = ( 1,   2,   3   )
      TKFRAME_-61084_UNITS         = 'DEGREES'

      FRAME_JUNO_REM_FA1           = -61085
      FRAME_-61085_NAME            = 'JUNO_REM_FA1'
      FRAME_-61085_CLASS           = 4
      FRAME_-61085_CLASS_ID        = -61085
      FRAME_-61085_CENTER          = -61
      TKFRAME_-61085_SPEC          = 'ANGLES'
      TKFRAME_-61085_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61085_ANGLES        = (   10.000059,    0.000000,   90.000000 )
      TKFRAME_-61085_AXES          = ( 1,   2,   3   )
      TKFRAME_-61085_UNITS         = 'DEGREES'

      FRAME_JUNO_REM_FA2           = -61086
      FRAME_-61086_NAME            = 'JUNO_REM_FA2'
      FRAME_-61086_CLASS           = 4
      FRAME_-61086_CLASS_ID        = -61086
      FRAME_-61086_CENTER          = -61
      TKFRAME_-61086_SPEC          = 'ANGLES'
      TKFRAME_-61086_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61086_ANGLES        = (  -10.000059,    0.000000,  -90.000000 )
      TKFRAME_-61086_AXES          = ( 1,   2,   3   )
      TKFRAME_-61086_UNITS         = 'DEGREES'

      FRAME_JUNO_REM_RL1           = -61091
      FRAME_-61091_NAME            = 'JUNO_REM_RL1'
      FRAME_-61091_CLASS           = 4
      FRAME_-61091_CLASS_ID        = -61091
      FRAME_-61091_CENTER          = -61
      TKFRAME_-61091_SPEC          = 'ANGLES'
      TKFRAME_-61091_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61091_ANGLES        = (  157.990360,  -76.551859,   22.568643 )
      TKFRAME_-61091_AXES          = ( 1,   2,   3   )
      TKFRAME_-61091_UNITS         = 'DEGREES'

      FRAME_JUNO_REM_RL2           = -61092
      FRAME_-61092_NAME            = 'JUNO_REM_RL2'
      FRAME_-61092_CLASS           = 4
      FRAME_-61092_CLASS_ID        = -61092
      FRAME_-61092_CENTER          = -61
      TKFRAME_-61092_SPEC          = 'ANGLES'
      TKFRAME_-61092_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61092_ANGLES        = ( -157.990349,  -76.551858,  -22.568654 )
      TKFRAME_-61092_AXES          = ( 1,   2,   3   )
      TKFRAME_-61092_UNITS         = 'DEGREES'

      FRAME_JUNO_REM_RL3           = -61093
      FRAME_-61093_NAME            = 'JUNO_REM_RL3'
      FRAME_-61093_CLASS           = 4
      FRAME_-61093_CLASS_ID        = -61093
      FRAME_-61093_CENTER          = -61
      TKFRAME_-61093_SPEC          = 'ANGLES'
      TKFRAME_-61093_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61093_ANGLES        = ( -157.990360,   76.551859, -157.431357 )
      TKFRAME_-61093_AXES          = ( 1,   2,   3   )
      TKFRAME_-61093_UNITS         = 'DEGREES'

      FRAME_JUNO_REM_RL4           = -61094
      FRAME_-61094_NAME            = 'JUNO_REM_RL4'
      FRAME_-61094_CLASS           = 4
      FRAME_-61094_CLASS_ID        = -61094
      FRAME_-61094_CENTER          = -61
      TKFRAME_-61094_SPEC          = 'ANGLES'
      TKFRAME_-61094_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61094_ANGLES        = (  157.990349,   76.551858,  157.431346 )
      TKFRAME_-61094_AXES          = ( 1,   2,   3   )
      TKFRAME_-61094_UNITS         = 'DEGREES'

      FRAME_JUNO_REM_RA1           = -61095
      FRAME_-61095_NAME            = 'JUNO_REM_RA1'
      FRAME_-61095_CLASS           = 4
      FRAME_-61095_CLASS_ID        = -61095
      FRAME_-61095_CENTER          = -61
      TKFRAME_-61095_SPEC          = 'ANGLES'
      TKFRAME_-61095_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61095_ANGLES        = (  169.999941,    0.000000,   90.000000 )
      TKFRAME_-61095_AXES          = ( 1,   2,   3   )
      TKFRAME_-61095_UNITS         = 'DEGREES'

      FRAME_JUNO_REM_RA2           = -61096
      FRAME_-61096_NAME            = 'JUNO_REM_RA2'
      FRAME_-61096_CLASS           = 4
      FRAME_-61096_CLASS_ID        = -61096
      FRAME_-61096_CENTER          = -61
      TKFRAME_-61096_SPEC          = 'ANGLES'
      TKFRAME_-61096_RELATIVE      = 'JUNO_SPACECRAFT'
      TKFRAME_-61096_ANGLES        = ( -169.999941,    0.000000,  -90.000000 )
      TKFRAME_-61096_AXES          = ( 1,   2,   3   )
      TKFRAME_-61096_UNITS         = 'DEGREES'

   \begintext


Juno NAIF ID Codes -- Definitions
========================================================================

   This section contains name to NAIF ID mappings for the JUNO mission.
   Once the contents of this file is loaded into the KERNEL POOL, these
   mappings become available within SPICE, making it possible to use
   names instead of ID code in the high level SPICE routine calls.

   Spacecraft:
   -----------

      JUNO                           -61
      JUNO                           -61
      JUNO_SPACECRAFT                -61000
      JUNO_SPACECRAFT_BUS            -61000
      JUNO_SC_BUS                    -61000

   Magnetometers and ASCs:
   -----------------------

      JUNO_ASC1                      -61111
      JUNO_ASC2                      -61112
      JUNO_FGM_IB                    -61114
      JUNO_ASC3                      -61121
      JUNO_ASC4                      -61122
      JUNO_FGM_OB                    -61124

   JADE:
   -----

      JUNO_JADE_E060                 -61201
      JUNO_JADE_E180                 -61202
      JUNO_JADE_E300                 -61203
      JUNO_JADE_I                    -61204

   JEDI:
   -----

      JUNO_JEDI_090                  -61301
      JUNO_JEDI_A180                 -61302
      JUNO_JEDI_270                  -61303

   JIRAM:
   ------

      JUNO_JIRAM_I                   -61410
      JUNO_JIRAM_I_LBAND             -61411
      JUNO_JIRAM_I_MBAND             -61412
      JUNO_JIRAM_S                   -61420

   JUNOCAM:
   --------

      JUNO_JUNOCAM                   -61500
      JUNO_JUNOCAM_BLUE              -61501
      JUNO_JUNOCAM_GREEN             -61502
      JUNO_JUNOCAM_RED               -61503
      JUNO_JUNOCAM_METHANE           -61504

   MWR:
   ----

      JUNO_MWR_A1                    -61601
      JUNO_MWR_A2                    -61602
      JUNO_MWR_A3                    -61603
      JUNO_MWR_A4                    -61604
      JUNO_MWR_A5                    -61605
      JUNO_MWR_A6                    -61606

   UVS:
   ----

      JUNO_UVS_BASE                  -61700
      JUNO_UVS                       -61701

   WAVES:
   ------

      JUNO_WAVES_MSC                 -61810
      JUNO_WAVES_ANTENNA             -61820

   Solar Arrays:
   -------------

      JUNO_SA1_HINGE                 -61010
      JUNO_SA1                       -61011
      JUNO_SA2_HINGE                 -61020
      JUNO_SA2                       -61021
      JUNO_SA3_HINGE                 -61030
      JUNO_SA3                       -61031

   Antennas:
   ---------

      JUNO_HGA                       -61040
      JUNO_MGA                       -61050
      JUNO_LGA_FORWARD               -61061
      JUNO_LGA_AFT                   -61062
      JUNO_LGA_TOROID                -61063

   ACS Sensors:
   ------------

      JUNO_SRU1                      -61071
      JUNO_SRU2                      -61072

      JUNO_SSS1                      -61073
      JUNO_SSS2                      -61074

   Thrusters:
   ----------

      JUNO_REM_FL1                   -61081
      JUNO_REM_FL2                   -61082
      JUNO_REM_FL3                   -61083
      JUNO_REM_FL4                   -61084
      JUNO_REM_FA1                   -61085
      JUNO_REM_FA2                   -61086

      JUNO_REM_RL1                   -61091
      JUNO_REM_RL2                   -61092
      JUNO_REM_RL3                   -61093
      JUNO_REM_RL4                   -61094
      JUNO_REM_RA1                   -61095
      JUNO_REM_RA2                   -61096

   The mappings summarized in this table are implemented by the keywords
   below.

   \begindata

      NAIF_BODY_NAME += ( 'JUNO'                        )
      NAIF_BODY_CODE += ( -61                           )

      NAIF_BODY_NAME += ( 'JUNO'                        )
      NAIF_BODY_CODE += ( -61                           )

      NAIF_BODY_NAME += ( 'JUNO_SPACECRAFT'             )
      NAIF_BODY_CODE += ( -61000                        )

      NAIF_BODY_NAME += ( 'JUNO_SPACECRAFT_BUS'         )
      NAIF_BODY_CODE += ( -61000                        )

      NAIF_BODY_NAME += ( 'JUNO_SC_BUS'                 )
      NAIF_BODY_CODE += ( -61000                        )

      NAIF_BODY_NAME += ( 'JUNO_ASC1'                   )
      NAIF_BODY_CODE += ( -61111                        )

      NAIF_BODY_NAME += ( 'JUNO_ASC2'                   )
      NAIF_BODY_CODE += ( -61112                        )

      NAIF_BODY_NAME += ( 'JUNO_FGM_IB'                 )
      NAIF_BODY_CODE += ( -61114                        )

      NAIF_BODY_NAME += ( 'JUNO_ASC3'                   )
      NAIF_BODY_CODE += ( -61121                        )

      NAIF_BODY_NAME += ( 'JUNO_ASC4'                   )
      NAIF_BODY_CODE += ( -61122                        )

      NAIF_BODY_NAME += ( 'JUNO_FGM_OB'                 )
      NAIF_BODY_CODE += ( -61124                        )

      NAIF_BODY_NAME += ( 'JUNO_JADE_E060'              )
      NAIF_BODY_CODE += ( -61201                        )

      NAIF_BODY_NAME += ( 'JUNO_JADE_E180'              )
      NAIF_BODY_CODE += ( -61202                        )

      NAIF_BODY_NAME += ( 'JUNO_JADE_E300'              )
      NAIF_BODY_CODE += ( -61203                        )

      NAIF_BODY_NAME += ( 'JUNO_JADE_I'                 )
      NAIF_BODY_CODE += ( -61204                        )

      NAIF_BODY_NAME += ( 'JUNO_JEDI_090'               )
      NAIF_BODY_CODE += ( -61301                        )

      NAIF_BODY_NAME += ( 'JUNO_JEDI_A180'              )
      NAIF_BODY_CODE += ( -61302                        )

      NAIF_BODY_NAME += ( 'JUNO_JEDI_270'               )
      NAIF_BODY_CODE += ( -61303                        )

      NAIF_BODY_NAME += ( 'JUNO_JIRAM_I'                )
      NAIF_BODY_CODE += ( -61410                        )

      NAIF_BODY_NAME += ( 'JUNO_JIRAM_I_LBAND'          )
      NAIF_BODY_CODE += ( -61411                        )

      NAIF_BODY_NAME += ( 'JUNO_JIRAM_I_MBAND'          )
      NAIF_BODY_CODE += ( -61412                        )

      NAIF_BODY_NAME += ( 'JUNO_JIRAM_S'                )
      NAIF_BODY_CODE += ( -61420                        )

      NAIF_BODY_NAME += ( 'JUNO_JUNOCAM'                )
      NAIF_BODY_CODE += ( -61500                        )

      NAIF_BODY_NAME += ( 'JUNO_JUNOCAM_BLUE'           )
      NAIF_BODY_CODE += ( -61501                        )

      NAIF_BODY_NAME += ( 'JUNO_JUNOCAM_GREEN'          )
      NAIF_BODY_CODE += ( -61502                        )

      NAIF_BODY_NAME += ( 'JUNO_JUNOCAM_RED'            )
      NAIF_BODY_CODE += ( -61503                        )

      NAIF_BODY_NAME += ( 'JUNO_JUNOCAM_METHANE'        )
      NAIF_BODY_CODE += ( -61504                        )

      NAIF_BODY_NAME += ( 'JUNO_MWR_A1'                 )
      NAIF_BODY_CODE += ( -61601                        )

      NAIF_BODY_NAME += ( 'JUNO_MWR_A2'                 )
      NAIF_BODY_CODE += ( -61602                        )

      NAIF_BODY_NAME += ( 'JUNO_MWR_A3'                 )
      NAIF_BODY_CODE += ( -61603                        )

      NAIF_BODY_NAME += ( 'JUNO_MWR_A4'                 )
      NAIF_BODY_CODE += ( -61604                        )

      NAIF_BODY_NAME += ( 'JUNO_MWR_A5'                 )
      NAIF_BODY_CODE += ( -61605                        )

      NAIF_BODY_NAME += ( 'JUNO_MWR_A6'                 )
      NAIF_BODY_CODE += ( -61606                        )

      NAIF_BODY_NAME += ( 'JUNO_UVS_BASE'               )
      NAIF_BODY_CODE += ( -61700                        )

      NAIF_BODY_NAME += ( 'JUNO_UVS'                    )
      NAIF_BODY_CODE += ( -61701                        )

      NAIF_BODY_NAME += ( 'JUNO_WAVES_MSC'              )
      NAIF_BODY_CODE += ( -61810                        )

      NAIF_BODY_NAME += ( 'JUNO_WAVES_ANTENNA'          )
      NAIF_BODY_CODE += ( -61820                        )

      NAIF_BODY_NAME += ( 'JUNO_SA1_HINGE'              )
      NAIF_BODY_CODE += ( -61010                        )

      NAIF_BODY_NAME += ( 'JUNO_SA1'                    )
      NAIF_BODY_CODE += ( -61011                        )

      NAIF_BODY_NAME += ( 'JUNO_SA2_HINGE'              )
      NAIF_BODY_CODE += ( -61020                        )

      NAIF_BODY_NAME += ( 'JUNO_SA2'                    )
      NAIF_BODY_CODE += ( -61021                        )

      NAIF_BODY_NAME += ( 'JUNO_SA3_HINGE'              )
      NAIF_BODY_CODE += ( -61030                        )

      NAIF_BODY_NAME += ( 'JUNO_SA3'                    )
      NAIF_BODY_CODE += ( -61031                        )

      NAIF_BODY_NAME += ( 'JUNO_HGA'                    )
      NAIF_BODY_CODE += ( -61040                        )

      NAIF_BODY_NAME += ( 'JUNO_MGA'                    )
      NAIF_BODY_CODE += ( -61050                        )

      NAIF_BODY_NAME += ( 'JUNO_LGA_FORWARD'            )
      NAIF_BODY_CODE += ( -61061                        )

      NAIF_BODY_NAME += ( 'JUNO_LGA_AFT'                )
      NAIF_BODY_CODE += ( -61062                        )

      NAIF_BODY_NAME += ( 'JUNO_LGA_TOROID'             )
      NAIF_BODY_CODE += ( -61063                        )

      NAIF_BODY_NAME += ( 'JUNO_SRU1'                   )
      NAIF_BODY_CODE += ( -61071                        )

      NAIF_BODY_NAME += ( 'JUNO_SRU2'                   )
      NAIF_BODY_CODE += ( -61072                        )

      NAIF_BODY_NAME += ( 'JUNO_SSS1'                   )
      NAIF_BODY_CODE += ( -61073                        )

      NAIF_BODY_NAME += ( 'JUNO_SSS2'                   )
      NAIF_BODY_CODE += ( -61074                        )

      NAIF_BODY_NAME += ( 'JUNO_REM_FL1'                )
      NAIF_BODY_CODE += ( -61081                        )

      NAIF_BODY_NAME += ( 'JUNO_REM_FL2'                )
      NAIF_BODY_CODE += ( -61082                        )

      NAIF_BODY_NAME += ( 'JUNO_REM_FL3'                )
      NAIF_BODY_CODE += ( -61083                        )

      NAIF_BODY_NAME += ( 'JUNO_REM_FL4'                )
      NAIF_BODY_CODE += ( -61084                        )

      NAIF_BODY_NAME += ( 'JUNO_REM_FA1'                )
      NAIF_BODY_CODE += ( -61085                        )

      NAIF_BODY_NAME += ( 'JUNO_REM_FA2'                )
      NAIF_BODY_CODE += ( -61086                        )

      NAIF_BODY_NAME += ( 'JUNO_REM_RL1'                )
      NAIF_BODY_CODE += ( -61091                        )

      NAIF_BODY_NAME += ( 'JUNO_REM_RL2'                )
      NAIF_BODY_CODE += ( -61092                        )

      NAIF_BODY_NAME += ( 'JUNO_REM_RL3'                )
      NAIF_BODY_CODE += ( -61093                        )

      NAIF_BODY_NAME += ( 'JUNO_REM_RL4'                )
      NAIF_BODY_CODE += ( -61094                        )

      NAIF_BODY_NAME += ( 'JUNO_REM_RA1'                )
      NAIF_BODY_CODE += ( -61095                        )

      NAIF_BODY_NAME += ( 'JUNO_REM_RA2'                )
      NAIF_BODY_CODE += ( -61096                        )

   \begintext
