
var title_prop = {'blwind':'BL Wind', 'bltopwind':'BL Top Wind', 'sfcwind':'Surface Wind',
                  'cape': 'CAPE', 'wstar':'Thermal Updraft Velocity', 'hbl':'Height of BL Top',
                  'bsratio':'Buoyancy/Shear Ratio', 'blcloudpct': '1h Accumulated Rain',
                  'mslpress':'Mean Sea Level Pressure'}
//var days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
var days = ['Domingo','Lunes','Martes','Miércoles','Jueves','Viernes','Sábado'];
var months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
var SCs = ['SC2', 'SC2+1', 'SC4+2', 'SC4+3']

var today = new Date()
var UTCshift = today.getTimezoneOffset() / 60;
var d = today.getDate();
var dw = days[ today.getDay() ];
var m = today.getMonth() + 1;
var my = months[ today.getMonth() ];
var y = today.getFullYear();
//var folder = '/var/www/html/RASP/data/PLOTS';
var folder = 'data/PLOTS';

/* Global variables */
var sc = 'SC2';
var domain = 'w2';
var Oprop = null;
var Sprop = 'sfcwind';
var Vprop = 'sfcwind';
var Ndays = 4;
var Nhours = 12;
var hour0 = 8;
var hour = 12;

/* State variables */
var Opts_menu = false;
var Opts_minx = 100;

// Useful aliases
var plot_title = document.getElementById("Title");
var TER_layer = document.getElementById('terrain_layer')
var GND_layer = document.getElementById('gnd_layer')
var CCA_layer = document.getElementById('ccaa_layer')
var RIV_layer = document.getElementById('rivers_layer')
var ROA_layer = document.getElementById('roads_layer')
var TAK_layer = document.getElementById('takeoffs_layer')
// data
var S_layer = document.getElementById('scalar_layer')
var V_layer = document.getElementById('vector_layer')
var C_layer = document.getElementById('clouds_layer')
var R_layer = document.getElementById('rain_layer')
var P_layer = document.getElementById('press_layer')
var CB_layer = document.getElementById('cbar_layer')
var CB_R_layer = document.getElementById('rain_cbar_layer')

// ----  Default values for initial load ----
update_plot_title(dw,d,Sprop,hour)
TER_layer.src = get_folder(folder,domain,sc)+'/terrain.png';
GND_layer.src = get_folder(folder,domain,sc)+'/terrain1.png';
CCA_layer.src = get_folder(folder,domain,sc)+'/ccaa.png';
RIV_layer.src = get_folder(folder,domain,sc)+'/rivers.png';
ROA_layer.src = get_folder(folder,domain,sc)+'/roads.png';
TAK_layer.src = get_folder(folder,domain,sc)+'/takeoffs.png';
// meteo
S_layer.src = get_filename(folder,domain,sc,hour,UTCshift,Sprop,false);
V_layer.src = get_filename(folder,domain,sc,hour,UTCshift,Vprop,true);
// special layers
C_layer.src  = get_filename(folder,domain,sc,hour,UTCshift,'blcloudpct',false);
R_layer.src  = get_filename(folder,domain,sc,hour,UTCshift,'rain1',false);
P_layer.src  = get_filename(folder,domain,sc,hour,UTCshift,'mslpress',false);
CB_layer.src = folder+'/'+Sprop+'.png';
CB_R_layer.src = folder+'/'+'rain1.png';

document.getElementById("days").innerHTML = generate_days();

// Generate hours in local time
var text = "";
var i;
var j;
for (i = 0; i < Nhours; i++) {
   j = i + hour0;
   text += '<button type="button" class="button_inactive" '
   text += 'id="button_hour_'+i.toString()+'" ';
   text += 'onclick="javascript:change_hour('+i+');">';
   text += j + ":00";
   text += '</button>   ';
}
document.getElementById("hours").innerHTML = text.slice(0, -2);
