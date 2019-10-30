function change_hour(x) {
   hour = x+hour0;
   var XXX = replot_scalar(Sprop);
   replot_vector(Vprop);
   var i;
   var id;
   for (i = 0; i < Nhours; i++) {
      id = 'button_hour_' + i;
      document.getElementById(id).className = "button_inactive";
   }
   id = 'button_hour_' + x;
   var Button = document.getElementById(id);
   Button.className = "button_active";
   //plot_title.innerHTML = dw+' '+d+' '+title_prop[Sprop]+' '+hour+':00';
   //document.getElementById('clouds_layer').src =  folder+'/'+domain+'/'+sc+'/'+hour-UTCshift+'00_blcloudpct.png';
   //document.getElementById('press_layer').src =  folder+'/'+domain+'/'+sc+'/'+hour-UTCshift+'00_mslpress.png';
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

function set_all(folder,domain,sc){
}

function change_day(x) {
   sc = SCs[x];
   dw = days[(( today.getDay() + x )%7)];
   var newDate = new Date(Date.now() + x*24*60*60*1000);
   d = newDate.getDate();
   var i;
   var id;
   for (i = 0; i < Ndays; i++) {
      id = 'button_day_' + i;
      document.getElementById(id).className = "button_inactive";
   }
   id = 'button_day_' + x;
   var Button = document.getElementById(id);
   Button.className = "button_active";
   replot_scalar(Sprop);
   replot_vector(Vprop);
   replot_general();
}

function replot_general(){
   // Default values for initial load
   TER_layer.src = get_folder(folder,domain,sc)+'/terrain.png';
   GND_layer.src = get_folder(folder,domain,sc)+'/terrain1.png';
   CCA_layer.src = get_folder(folder,domain,sc)+'/ccaa.png';
   RIV_layer.src = get_folder(folder,domain,sc)+'/rivers.png';
   ROA_layer.src = get_folder(folder,domain,sc)+'/roads.png';
   TAK_layer.src = get_folder(folder,domain,sc)+'/takeoffs.png';
   // special layers
   C_layer.src  = get_filename(folder,domain,sc,hour,UTCshift,'blcloudpct',false);
   P_layer.src  = get_filename(folder,domain,sc,hour,UTCshift,'mslpress',false);
   CB_layer.src = folder+'/'+Sprop+'.png';
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
   var VL = document.getElementById('vector_layer')
   Vprop = x
   var fname = get_filename(folder,domain,sc,hour,UTCshift,Vprop,true);
   VL.src = fname;
   // To reverse the action of None
   if (VL.style.visibility=="hidden") {
      VL.style.visibility="visible";}
}

function replot_scalar(x){
   var Slayer = document.getElementById('scalar_layer')
   var CBlayer = document.getElementById('cbar_layer')
   Sprop = x
   var fname = get_filename(folder,domain,sc,hour,UTCshift,Sprop,false);
   Slayer.src = fname;
   CBlayer.src= folder+'/'+Sprop+'.png';
   plot_title.innerHTML = dw+' '+d+' '+title_prop[Sprop]+' '+hour+':00';
   return fname;
}

function toggleVisibility(id) {
  var el = document.getElementById(id);
  if (el.style.visibility=="visible") {
     el.style.visibility="hidden";
  }
  else {
     el.style.visibility="visible";}
  if (id == 'gnd_layer'){
     set_opacity(0,['scalar_layer']);
  }
}

function get_folder(fol,dom,sc){
   return fol+'/'+dom+'/'+sc
}

function get_filename(fol,dom,sc,hour,UTCshift,prop,isvec){
   var utc_hour = (hour+UTCshift).toString().padStart(2, '0');
   var fname = fol+'/'+dom+'/'+sc+'/'+ utc_hour +'00_'+prop;
   if (isvec===true){
      fname += '_vec';
   }
   fname += '.png'
   return fname
}

// ------------ Slider ------------
function set_opacity(x,layers) {
   var layersLength = layers.length;
   for (var i = 0; i < layersLength; i++) {
      document.getElementById(layers[i]).style.opacity = x/100;
   }
   replot_scalar(Sprop);
}

function toggle_domain(){
   var old = domain
   if (domain == 'w2') {
      domain = "d2";}
   else if (domain == 'd2') {
      domain = "w2";}
   else {
      domain = "w2";}
   change_domain(domain)
}
