# ************************************************************************************************************
# 
# generate my(!) heatmaps
# -----------------------
#    Uwe Berger, 2021
#
# ...see variables/parameters at the beginning :-)
#
# example: gnuplot  -e "year='2021'" -e "path='results/'" heatmap_arg.gp
#
# ---------
# Have fun!
#
# ************************************************************************************************************

# parameters
if (!exists("year")) year='42'
if (!exists("path")) path=''
#print "year=".year
#print "path=".path

# for all heatmaps
unset key
set terminal png font arial 8 size 1200, 400
set view map
set xdata time
set timefmt "%Y-%m-%d"
set format x "%d.%m.\n%Y"
set yrange [0:24]
set ytics 1
set ylabel "Day hour"
set xlabel "Date"
set tics out
set xrange [year."-01-01":year."-12-31"]
set colorbox size 10, 300
ts=system("date '+%d.%m.%Y, %H:%M:%S'")

# temperatur
set output path.'heatmap_temperature_'.year.'.png'
set title "Temperature ".year." (created: ".ts.")"
set cblabel "°C"
set cbrange [-25.0:55.0]
set palette defined (0 "blue",17 "#00ffff",33 "white",55 "yellow",\
    70 "red",100 "#990000", 101 "grey")
plot path.'heatmap_temperature_'.year.'.csv' using 1:2:3 with image

# pressure_rel
set output path.'heatmap_pressure_rel_'.year.'.png'
set title "Pressure (rel.) ".year." (created: ".ts.")"
set cblabel 'hPa'
set cbrange [950:1050]
set palette defined (0 'blue', 17 '#00ffff', 33 'white', 50 'yellow', 85 'red', 100 '#990000', 101 'grey')
plot path.'heatmap_pressure_rel_'.year.'.csv' using 1:2:3 with image

# humidity
set output path.'heatmap_humidity_'.year.'.png'
set title "Humidity ".year." (created: ".ts.")"
set cblabel '%'
set cbrange [0:100]
set palette defined (0 'white', 100 'blue', 101 'grey')
plot path.'heatmap_humidity_'.year.'.csv' using 1:2:3 with image

# Vbat (ESP)
set output path.'heatmap_vbat_'.year.'.png'
set title "Vbat (ESP) ".year." (created: ".ts.")"
set cblabel 'V'
set cbrange [3.3:4.2]
set palette defined (0 '#990000', 25 'red', 50 'yellow', 66 'white', 77 '#00ffff', 100 'blue', 101 'grey')
plot path.'heatmap_vbat_'.year.'.csv' using 1:2:3 with image

set output path.'heatmap_awake_time_'.year.'.png'
set title "Awake time (ESP) ".year." (created: ".ts.")"
set cblabel 'ms'
set logscale cb 10
set cbrange [1000:10000]
set palette defined (0 'blue', 28 '#00ffff', 30 'white', 33 'yellow', 90 'red', 100 '#990000', 101 'grey')
plot path.'heatmap_awake_time_'.year.'.csv' using 1:2:3 with image

# luminosity
set output path.'heatmap_luminosity_'.year.'.png'
set title "Luminosity ".year." (created: ".ts.")"
set cblabel 'lux'
set logscale cb 10
set cbrange [1:100000]
set palette defined (0 'black', 100 'white')
plot path.'heatmap_luminosity_'.year.'.csv' using 1:2:3 with image

