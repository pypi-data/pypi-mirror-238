=====
Usage
=====

To use Explain the DQ in a project::

    import explaintheDQ
    explaintheDQ(32769)

What you get is a table explaining the flags for this DQ value:


	     Name        Flag Bit                 Description                
	---------------- ----- --- -------------------------------------------
	      DO_NOT_USE  True   0                      Bad pixel. Do not use.
	       SATURATED False   1             Pixel saturated during exposure
	        JUMP_DET False   2               Jump detected during exposure
	         DROPOUT False   3                   Data lost in transmission
	         OUTLIER False   4                Flagged by outlier detection
	     PERSISTENCE False   5                            High persistence
	        AD_FLOOR False   6                             Below A/D floor
	      CHARGELOSS False   7                            Charge Migration
	UNRELIABLE_ERROR False   8            Uncertainty exceeds quoted error
	     NON_SCIENCE False   9    Pixel not on science portion of detector
	            DEAD False  10                                  Dead pixel
	             HOT False  11                                   Hot pixel
	            WARM False  12                                  Warm pixel
	          LOW_QE False  13                      Low quantum efficiency
	              RC False  14                                    RC pixel
	       TELEGRAPH  True  15                             Telegraph pixel
	       NONLINEAR False  16                      Pixel highly nonlinear
	   BAD_REF_PIXEL False  17              Reference pixel cannot be used
	   NO_FLAT_FIELD False  18               Flat field cannot be measured
	   NO_GAIN_VALUE False  19                     Gain cannot be measured
	     NO_LIN_CORR False  20          Linearity correction not available
	    NO_SAT_CHECK False  21              Saturation check not available
	 UNRELIABLE_BIAS False  22                         Bias variance large
	 UNRELIABLE_DARK False  23                         Dark variance large
	UNRELIABLE_SLOPE False  24    Slope variance large (i.e., noisy pixel)
	 UNRELIABLE_FLAT False  25                         Flat variance large
	            OPEN False  26 Open pixel (counts move to adjacent pixels)
	        ADJ_OPEN False  27                      Adjacent to open pixel
	UNRELIABLE_RESET False  28                  Sensitive to reset anomaly
	 MSA_FAILED_OPEN False  29   Pixel sees light from failed-open shutter
	 OTHER_BAD_PIXEL False  30                            A catch-all flag
	 REFERENCE_PIXEL False  31                  Pixel is a reference pixel

So this pixel was marked as DO_NO_USE because it is known to have random telegraph noise.
