##  GT_prep_0.4.py
#### used for adding 6 CC_layers and a CC_layer-7 with the correct LUT based on AVID luts copied to the * REEL comment.

#### Usage:  
##### **python3 GT_prep_0.4.py -i or --inEDL (source EDL) -o or --outEDL (output EDL) -v or --verbose -q or --quiet**

##### example line of an EDL:
003  A001C001 V     C        02:47:25:20 02:47:49:04 01:00:20:01 01:00:43:09 
* FROM CLIP NAME:  A001C001_200303_F701.NEW.01 
* LOC: 01:00:25:10 RED     THIS IS A MARKER 
* REEL: GT_COTERIE_NIGHT_02_LC_SDR_V2_3 

##### would result in:
003  A001C001 V     C        02:47:25:20 02:47:49:04 01:00:20:01 01:00:43:09
* FROM CLIP NAME:  A001C001_200303_F701.NEW.01
* LOC: 01:00:25:10 RED     THIS IS A MARKER
* REEL: GT_COTERIE_NIGHT_02_LC_SDR_V2_3
* SOURCE FILE: A001C001_200303_F701
* NUCODA_LAYER Log
* NUCODA_LAYER Log2
* NUCODA_LAYER Log3
* NUCODA_LAYER Log4
* NUCODA_LAYER Log5
* NUCODA_LAYER Log6
* NUCODA_LAYER GT_LUT -effect NucodaCMSPath -lut T:\luts\GoodTrouble\GT_COTERIE_NIGHT_02_LC_SDR_V2_3.cube


Note:
Need to add a function to auto conform titles.
1. strip dissolves
2. remove black events
3. extend head and tail of each clip to cover dissolve.
4. Insert title names

I wish there was a way to choose in Nucoda EDL whether to interp source as single frame or sequence.
