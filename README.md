# Visualization of AMR simulations with a high spatial dynamic range
Sample codes for visualization of nested uniform grids, which are extracted from an AMR hierarchical grid. 
Nested grids with different resolutions are transited seamlessly in a produced movie. 

## Making PNG files with uniform grids
### zoomseries.py
A Python command regulating a process for making PNG files. The calling sequence is following:

    ./zoomseries.py

This command produces a directory of png_zoom_1080p, which contains PNG files.

### pvscript.py
Paraview script that is used in a process of zoomseries.py

### compsite_series.py
This command composites two files with different resolutions in each movie frame. The calling sequence is following:

    ./compsite_series.py

This command produces a directory of png_zoom_composite_1080p, which contains composed PNG files.

## Making a movie with PNG files.
### dir2mp4.sh

The calling sequence is following:

    ./dir2mp4.sh png_zoom_composite_1080p
    
This command produces a movie of zoom_composite_1080.mp4.

### png2mp4.sh

This is a back end of dir2mp4.sh This command a mp4 file by PNG files.

  
