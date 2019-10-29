function change_hour(x) {
   hour = x;
   replot_scalar(Sprop);
   replot_vector(Vprop);
   plot_title.innerHTML = dw+' '+d+' '+title_prop[Sprop]+' '+hour+':00';
   document.getElementById('clouds_layer').src =  folder+'/'+domain+'/'+sc+'/'+hour+'00_blcloudpct.png';
   document.getElementById('press_layer').src =  folder+'/'+domain+'/'+sc+'/'+hour+'00_mslpress.png';
}

function change_domain(x) {
   domain = x
   replot_scalar(Sprop);
   replot_vector(Vprop);
   document.getElementById('terrain_layer').src = folder+'/'+domain+'/'+sc+'/terrain.png';
   document.getElementById('gnd_layer').src = folder+'/'+domain+'/'+sc+'/terrain1.png';
   document.getElementById('ccaa_layer').src = folder+'/'+domain+'/'+sc+'/ccaa.png';
   document.getElementById('rivers_layer').src = folder+'/'+domain+'/'+sc+'/rivers.png';
   document.getElementById('roads_layer').src = folder+'/'+domain+'/'+sc+'/roads.png';
   document.getElementById('takeoffs_layer').src = folder+'/'+domain+'/'+sc+'/takeoffs.png';
   document.getElementById('clouds_layer').src =  folder+'/'+domain+'/'+sc+'/'+hour+'00_blcloudpct.png';
   document.getElementById('press_layer').src =  folder+'/'+domain+'/'+sc+'/'+hour+'00_mslpress.png';
}

function change_day(x) {
   sc = SCs[x];
   dw = days[(( today.getDay() + x )%7)];
   var newDate = new Date(Date.now() + x*24*60*60*1000);
   d = newDate.getDate();
   replot_scalar(Sprop);
   replot_vector(Vprop);
   document.getElementById('terrain_layer').src = folder+'/'+domain+'/'+sc+'/terrain.png';
   document.getElementById('gnd_layer').src = folder+'/'+domain+'/'+sc+'/terrain1.png';
   document.getElementById('ccaa_layer').src = folder+'/'+domain+'/'+sc+'/ccaa.png';
   document.getElementById('rivers_layer').src = folder+'/'+domain+'/'+sc+'/rivers.png';
   document.getElementById('roads_layer').src = folder+'/'+domain+'/'+sc+'/roads.png';
   document.getElementById('takeoffs_layer').src = folder+'/'+domain+'/'+sc+'/takeoffs.png';
   document.getElementById('clouds_layer').src =  folder+'/'+domain+'/'+sc+'/'+hour+'00_blcloudpct.png';
   document.getElementById('press_layer').src =  folder+'/'+domain+'/'+sc+'/'+hour+'00_mslpress.png';
   plot_title.innerHTML = dw+' '+d+' '+title_prop[Sprop]+' '+hour+':00';
}


function replot_cloud(x){
   Oprop = x
   var OL = document.getElementById('overall_layer')
   if (Oprop != null){
      document.getElementById('overall_layer').src= folder+'/'+domain+'/'+sc+'/'+hour+'00_'+Oprop+'.png';
      document.getElementById('gnd_layer').src = folder+'/'+domain+'/'+sc+'/terrain1.png';
      if (OL.style.visibility=="hidden") {
          OL.style.visibility="visible";}
   }
}

function replot_vector(x){
   Vprop = x
   var VL = document.getElementById('vector_layer')
   VL.src= folder+'/'+domain+'/'+sc+'/'+hour+'00_'+Vprop+'_vec.png';
   if (VL.style.visibility=="hidden") {
      VL.style.visibility="visible";}
}

function replot_scalar(x){
   Sprop = x
   document.getElementById('scalar_layer').src= folder+'/'+domain+'/'+sc+'/'+hour+'00_'+Sprop+'.png';
   plot_title.innerHTML = dw+' '+d+' '+title_prop[Sprop]+' '+hour+':00';
}

function toggleVisibility(id) {
  var el = document.getElementById(id);
  if (el.style.visibility=="visible") {
     el.style.visibility="hidden";}
  else {
     el.style.visibility="visible";}
}
//
// ------------ Slider ------------
function set_opacity(x,layers) {
   var layersLength = layers.length;
   for (var i = 0; i < layersLength; i++) {
      document.getElementById(layers[i]).style.opacity = x/100;
   }
   replot_scalar(Sprop);
}
