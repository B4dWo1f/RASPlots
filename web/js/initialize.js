var title_prop = {'blwind':'BL Wind', 'bltopwind':'BL Top Wind', 'sfcwind':'Surface Wind',
                  'cape': 'CAPE', 'wstar':'Thermal Updraft Velocity', 'hbl':'Height of BL Top',
                  'bsratio':'Buoyancy/Shear Ratio', 'blcloudpct': '1h Accumulated Rain',
                  'mslpress':'Mean Sea Level Pressure'}
var days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
var months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
var SCs = ['SC2', 'SC2+1', 'SC4+2', 'SC4+3']

var today = new Date()
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
var hour = '12';

var plot_title = document.getElementById("Title");

// Default values for initial load
document.getElementById('terrain_layer').src = folder+'/'+domain+'/'+sc+'/terrain.png';
document.getElementById('gnd_layer').src = folder+'/'+domain+'/'+sc+'/terrain1.png';
document.getElementById('ccaa_layer').src = folder+'/'+domain+'/'+sc+'/ccaa.png';
document.getElementById('rivers_layer').src = folder+'/'+domain+'/'+sc+'/rivers.png';
document.getElementById('roads_layer').src = folder+'/'+domain+'/'+sc+'/roads.png';
document.getElementById('takeoffs_layer').src = folder+'/'+domain+'/'+sc+'/takeoffs.png';
// meteo
document.getElementById('scalar_layer').src =  folder+'/'+domain+'/'+sc+'/'+hour+'00_'+Sprop+'.png';
document.getElementById('vector_layer').src =  folder+'/'+domain+'/'+sc+'/'+hour+'00_'+Vprop+'_vec.png';
plot_title.innerHTML = dw+' '+d+' '+title_prop[Sprop]+' '+hour+':00';
// special layers
document.getElementById('clouds_layer').src =  folder+'/'+domain+'/'+sc+'/'+hour+'00_blcloudpct.png';
document.getElementById('press_layer').src =  folder+'/'+domain+'/'+sc+'/'+hour+'00_mslpress.png';

// Generate days
var text = "";
var i;
for (i = 0; i <= 3; i++) {
   text += '<a href="javascript:change_day(' + i.toString() + ');">' 
   text += days[(( today.getDay() + i )%7)] + "</a> | ";
}
document.getElementById("days").innerHTML = text.slice(0, -2);

// Generate hours
var text = "";
var i;
for (i = 8; i <= 20; i++) {
   text += '<a href="javascript:change_hour('+i.toString()+');">' + i.toString() + ":00</a> | ";
}
document.getElementById("hours").innerHTML = text.slice(0, -2);
