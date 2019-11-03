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
   C_layer.src= get_filename(folder,domain,sc,hour,UTCshift,'blcloudpct',false);
   R_layer.src= get_filename(folder,domain,sc,hour,UTCshift,'rain1',false);
   P_layer.src= get_filename(folder,domain,sc,hour,UTCshift,'mslpress',false);
}

function change_domain(x) {
   domain = x
   replot_scalar(Sprop);
   replot_vector(Vprop);
   TER_layer.src = get_folder(folder,domain,sc)+'/terrain.png';
   GND_layer.src = get_folder(folder,domain,sc)+'/terrain1.png';
   CCA_layer.src = get_folder(folder,domain,sc)+'/ccaa.png';
   RIV_layer.src = get_folder(folder,domain,sc)+'/rivers.png';
   ROA_layer.src = get_folder(folder,domain,sc)+'/roads.png';
   TAK_layer.src = get_folder(folder,domain,sc)+'/takeoffs.png';
   C_layer.src= get_filename(folder,domain,sc,hour,UTCshift,'blcloudpct',false);
   R_layer.src= get_filename(folder,domain,sc,hour,UTCshift,'rain1',false);
   P_layer.src= get_filename(folder,domain,sc,hour,UTCshift,'mslpress',false);
   document.getElementById("days").innerHTML = generate_days();
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
   //plot_title.innerHTML = dw+' '+d+' '+title_prop[Sprop]+' '+hour+':00';
   update_plot_title(dw,d,Sprop,hour)
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
   var checks = {'sfcwind': 'VchkSFCwind', 'blwind':'VchkBLwind',
                 'bltopwind': 'VchkBLTOPwind'}
   var VL = document.getElementById('vector_layer')
   Vprop = x
   var fname = get_filename(folder,domain,sc,hour,UTCshift,Vprop,true);
   VL.src = fname;
   check(checks[x]);
}

function replot_scalar(x){
   var Slayer = document.getElementById('scalar_layer')
   var CBlayer = document.getElementById('cbar_layer')
   Sprop = x
   var fname = get_filename(folder,domain,sc,hour,UTCshift,Sprop,false);
   Slayer.src = fname;
   CBlayer.src= folder+'/'+Sprop+'.png';
   if ( ["sfcwind", "blwind", "bltopwind"].includes(x) ){
      replot_vector(x)
   }

   // plot_title.innerHTML = dw+' '+d+' '+title_prop[Sprop]+' '+hour+':00';
   update_plot_title(dw,d,Sprop,hour)
   return fname;
}

function toggleVisibility(ids) {
   var ids_length = ids.length;
   for (var i = 0; i < ids_length; i++) {
      var id = ids[i];
      var el = document.getElementById(ids[i]);
      if (el.style.visibility=="visible") {
         el.style.visibility="hidden";
         if (id == 'rain_layer'){
            var rain = document.getElementById('rain_cbar_layer');
            rain.style.visibility="hidden";
         }
      }
      else {
         el.style.visibility="visible";
         if (id == 'rain_layer'){
            var rain = document.getElementById('rain_cbar_layer');
            rain.style.visibility="visible";
         }
      }
      if (ids[i] == 'gnd_layer'){
         set_opacity(0,['scalar_layer']);
      }
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

function update_plot_title(dw,d,Sprop,hour){
   var Vdate = valid_dates[sc][domain];
   var day_num = Vdate.getDate();
   var day_week = days[Vdate.getDay()];
   plot_title.innerHTML = day_week+' '+day_num+' '+title_prop[Sprop]+' '+hour+':00';
}

function generate_days(){
   // Generate days
   var text = "";
   var Vdate;
   var i = 0;
   for (var key_sc in valid_dates) {
      var Vdate = valid_dates[key_sc][domain];
      text += '<button type="button" class="button_inactive" '
      text += 'id="button_day_'+i+'" ';
      text += 'onclick="javascript:change_day('+i+');">';
      text += days[Vdate.getDay()];
      if (i===0){
         text += ' '+Vdate.getDate()
      }
      text += '</button>   ';
      i += 1;
   }
   return text.slice(0, -2);
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

// Collapsable button
function toggle_opts_menu() {
   if (Opts_menu == true){
      closeNav();
      Opts_menu = false;
   }
   else if (Opts_menu == false){
      openNav();
      Opts_menu = true;
   }
}

function openNav() {
   document.getElementById("options_button").style.width = "250px";
   document.getElementById("opts_box").style.width = "250px";
}

function closeNav() {
   Opts_minx=1000;
   var foo = Opts_minx.toString()+'px';
   alert(foo);
   document.getElementById("options_button").style.width = foo;
   alert('button')
   document.getElementById("opts_box").style.height = foo;
   alert('box')
}

function check(id) {
    document.getElementById(id).checked = true;
}

function uncheck(id) {
    document.getElementById(id).checked = false;
}
