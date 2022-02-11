# ************************************************************************************************************
# 
# ...generate my(!) weather charts
# --------------------------------
#        Uwe Berger, 2021
#
# ...see variables/parameters at the beginning :-)
#
# example: gnuplot  -e "days='30'" -e "path='results/'" graph_arg.gp
#
# ---------
# Have fun!
#
# ************************************************************************************************************

# parameters
if (!exists("days")) days='1'
if (!exists("path")) path=''
#print "day=".days
#print "path=".path

# for all graphs
set terminal png font arial 8 size 1200, 400
set datafile separator ";"
set xdata time
set timefmt "%d.%m.%Y %H:%M:%S"
set key outside bottom horizontal
set xlabel "Date/Time"
set grid ytics lc rgb "#bbbbbb" lw 1 lt 0
set grid xtics lc rgb "#bbbbbb" lw 1 lt 0
xend=system("date '+%d.%m.%Y %H:%M:00'")
xstart=system("date '+%d.%m.%Y %H:%M:00' --date='-".days." day'")
set xrange[xstart:xend]
ts=system("date '+%d.%m.%Y, %H:%M:%S'")
l_w = 2

# temperature
set ylabel "Temperature in °C"
set yrange [-20:+50]
set ytics 5
set output path.'temperature_'.days.'d.png'
set title "Temperature last ".days."d (created ".ts.")"
plot path."temperature_BME280_".days."d.csv" using 1:2 title 'BME280' with lines lw l_w, path."temperature_SHT15_".days."d.csv" using 1:2 title 'SHT15' with lines lw l_w, path."temperature_TMP36_".days."d.csv" using 1:2 title 'TMP36' with lines lw l_w

# humidity
set ylabel "Humidity in %"
set yrange [0:100]
set ytics 10
set output path.'humidity_'.days.'d.png'
set title "Humidity last ".days."d (created ".ts.")"
plot path."humidity_BME280_".days."d.csv" using 1:2 title 'BME280' with lines lw l_w, path."humidity_SHT15_".days."d.csv" using 1:2 title 'SHT15' with lines lw l_w

# pressure_rel
set ylabel "Pressure (rel.) in hPa"
set yrange [950:1050]
set ytics 10
set output path.'pressure_rel_'.days.'d.png'
set title "Pressure (rel.) last ".days."d (created ".ts.")"
plot path."pressure_rel_BME280_".days."d.csv" using 1:2 title 'BME280' with lines lw l_w

# Vbat (ESP)
set ylabel "Vbat (ESP) in V"
set yrange [2.8:4.5]
set ytics 0.2
set output path.'vbat_'.days.'d.png'
set title "Vbat (ESP) last ".days."d (created ".ts.")"
plot path."vbat_ESP_".days."d.csv" using 1:2 title 'ESP' with lines lw l_w

# awake_time (ESP)
set ylabel "Awake time (ESP) in ms"
set yrange [1800:3000]
set ytics 100
set output path.'awake_time_'.days.'d.png'
set title "Awake time (ESP) last ".days."d (created ".ts.")"
plot path."awake_time_ESP_".days."d.csv" using 1:2 title 'ESP' with lines lw l_w

# luminosity
set ylabel "Luminosity in lux"
set yrange [1:100000]
set logscale y 10
set output path.'luminosity_'.days.'d.png'
set title "Luminosity last ".days."d (created ".ts.")"
plot path."luminosity_BH1750_".days."d.csv" using 1:2 title 'BH1750' with lines lw l_w

