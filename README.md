# GipsyX_Wrapper
A python wrapper around JPL's GipsyX for efficient processing of multi station and multi year datasets. Supports GPS-only, GLONASS-only and GPS+GLONASS PPP modes. The wrapper can use arbitrary number of threads to convert RINEX to datarecord format, process and gather the data. GipsyX solution files are extracted into pandas DataFrames and saved as a serialized ZSTD container files. Finally, the solutions are analysed with Eterna software.

It has all the necessary modules needed for products and data preparation such as: IONEX files merging, tropnominals generation, orbit and clock products conversion and merging etc. All multithreaded.

Additionally, a pbs-script based submission method is added to efficiently utilize PBS clusters.
