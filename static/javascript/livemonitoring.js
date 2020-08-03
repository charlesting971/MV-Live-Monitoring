//<script type="text/javascript" charset="utf-8"> 
$(document).ready(function() {
  var count = 0;
  var P = [];
  var Q = [];
  var V = [];
  var IE_display = [];
  var RR_display = [];
  var VE_display = [];
  var PEEP_display = [];
  var PIP_display = [];
  var Vtidal_display = [];  
  var Ers_display = [];
  var Rrs_display = [];  
  var P_display = [];
  var Q_display = [];
  var V_display = [];
  var T_display = []; 
  var sprt = 0;
  var layout_display = {
    xaxis : {
      tickvals : [],
      ticktext : []
    }        
  }  
  var lyt_height = 400;
  var lyt_width = 1050;
  var newtickvals = [];
  var newticktext = [];
  var disp_length = 800;
  var ini_tickvals = [];
  var ini_ticktext = [];

  for (i = 0; i < disp_length; i++) {
    ini_tickvals.push(i*0.02);
    ini_ticktext.push("");
  }

  for (var i = 0; i < 901; i++) {
    P_display.push(NaN);
    Q_display.push(NaN);
    V_display.push(NaN);
  }  

  plot_time = 0.00;
  for (var i = 0; i < disp_length; i++) {
    T_display.push(plot_time);        
    plot_time += 0.02;
  }

  // *Graph layout for P,Q,V
  var pressure_layout = {
    autosize: true,
    //width: lyt_width,
    height: lyt_height,
    paper_bgcolor: "#333333",
    plot_bgcolor: "#333333",
    title: "Pressure",
    xaxis: {
      //title: "Time (s)",
      //type: "date",
      color: "white",
      showgrid: false,
      showline: true,
      fixedrange: true,
      zeroline: false,
      tickmode:"array",
      tickvals: ini_tickvals,
      ticktext: ini_ticktext
    },
    yaxis: {
      title: "cmH20",
      color: "white",
      fixedrange: true,
      showline: true
    },
    font: {
      family: "Fjalla One, sans-serif",
      size: 16,
      color: "white"
    }
  };

  var flow_layout = {
    autosize: true,
    //width: lyt_width,
    height: lyt_height-25,
    paper_bgcolor: "#333333",
    plot_bgcolor: "#333333",
    title: "Flow",
    xaxis: {
      //title: "Time (s)",
      //type: "date",
      color: "white",
      showgrid: false,
      zeroline: false,
      fixedrange: true,
      tickmode:"array",
      tickvals: ini_tickvals,
      ticktext: ini_ticktext
    },
    yaxis: {
      title: "L/min",
      color: "white",
      fixedrange: true,
      showline: true
    },
    font: {
      family: "Fjalla One, sans-serif",
      size: 16,
      color: "white"
    }
  };

  var volume_layout = {
    autosize: true,
    //width: lyt_width,
    height: lyt_height-35,
    paper_bgcolor: "#333333",
    plot_bgcolor: "#333333",
    title: "Volume",
    xaxis: {
      //title: "Time (s)",
      //type: "date",
      color: "white",
      showgrid: false,
      zeroline: false,
      fixedrange: true,
      tickmode:"array",
      tickvals: ini_tickvals,
      ticktext: ini_ticktext
    },
    yaxis: {
      title: "L",
      color: "white",
      fixedrange: true,
      showline: true
    },
    font: {
      family: "Fjalla One, sans-serif",
      size: 16,
      color: "white"
    }
  };

  // *Initial empty array for P,Q,V data
  var pressure_data = [
    {
      x: T_display,
      y: [],
      type: "line",
      line: {
        color: "rgb(55, 128, 191)",
        width: 3
      }
    }
  ];

  var flow_data = [
    {
      x: T_display,
      y: [],
      type: "line",
      line: {
        color: "rgb(55, 128, 191)",
        width: 3
      }
    }
  ];

  var volume_data = [
    {
      x: T_display,
      y: [],
      type: "line",
      line: {
        color: "rgb(55, 128, 191)",
        width: 3
      }
    }
  ];

  // *Plot P,Q,V graph
  Plotly.plot("pressure_chart", pressure_data, pressure_layout, { responsive: true });
  Plotly.plot("flow_chart", flow_data, flow_layout, { responsive: true });
  Plotly.plot("volume_chart", volume_data, volume_layout, { responsive: true });





  
  // update the display array
  setInterval(function() {
    var t0 = performance.now();
    if (P.length > 0) {
      console.log('start to plot graph with data');
      P_display[count] = P.shift();
      Q_display[count] = Q.shift();
      V_display[count] = V.shift();  

      for (i = count + 1; i < count + 5; i++) {
        P_display[i] = NaN;
        Q_display[i] = NaN;
        V_display[i] = NaN; 

        if ((0.02*count).toFixed(2) == layout_display.xaxis.tickvals[0])  {
          layout_display.xaxis.tickvals.shift();
          layout_display.xaxis.ticktext.shift();
        }       
      }

      if ((0.02*count).toFixed(2) == newtickvals[0]) {
        layout_display.xaxis.tickvals.push(newtickvals[0]);
        layout_display.xaxis.ticktext.push(newticktext[0]);
        newtickvals.shift();
        newticktext.shift();

        document.getElementById('IE_val').innerHTML =  IE_display[0];
        document.getElementById('RR_val').innerHTML = RR_display[0].toFixed(2).toString();
        document.getElementById('VE_val').innerHTML = VE_display[0].toFixed(2).toString();
        document.getElementById('PEEP_val').innerHTML = PEEP_display[0].toFixed(2).toString();
        document.getElementById('PIP_val').innerHTML = PIP_display[0].toFixed(2).toString();
        document.getElementById('Vtidal_val').innerHTML = Vtidal_display[0].toFixed(2).toString();
        document.getElementById('Ers_val').innerHTML =  Ers_display[0].toFixed(2).toString();
        document.getElementById('Rrs_val').innerHTML = Rrs_display[0].toFixed(2).toString();

        IE_display.shift();
        RR_display.shift();
        VE_display.shift();
        PEEP_display.shift();
        PIP_display.shift();
        Vtidal_display.shift();
        Ers_display.shift();
        Rrs_display.shift();

      }

      count += 1;          

      if (P[0] == 'end') {
        // remove previous tailing data if new display array is shorter
        if (count < disp_length) {
          for (c = count; c < disp_length; c++){
            P_display[c] = NaN;
            Q_display[c] = NaN;
            V_display[c] = NaN; 
          }                 
        }
        P.shift();
        Q.shift();
        V.shift();
        count = 0;
        console.log('count has reseted to 0 ///////////////////////////////')       
      }
    }
    var t1=performance.now();
    if (t1-t0 >= 20){
      console.log('Data Update exceeds the time interval 0.02s');
      console.log(t1-t0);
    }
  }, 20);
  
  // update the plot
  setInterval(function() {
    var t0=performance.now();    
    if (P.length > 0) {
      Plotly.update("pressure_chart",{ y: [P_display] }, layout_display);
      Plotly.update("flow_chart", {y: [Q_display] }, layout_display);
      Plotly.update("volume_chart", {y: [V_display] }, layout_display);        
    }
    var t1=performance.now();
    if (t1-t0 >= 500){
      console.log(' Plot Update exceeds the time interval 0.02s');
      console.log(t1-t0);      
    }    
  }, 20);    


  // verify our websocket connection is established
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  socket.on('connect', function() {
      console.log('Websocket connected!');
  });

  // arranging the incoming data
  socket.on('send2Client', function(JSONfile) {
      var t0 = performance.now();
      var jsonReceived = JSON.parse(JSONfile); // dataPoints
      // get time in 24 hours format at start of every breath
      var now = new Date();

      var t1 = performance.now();
      // checks if the incoming data length will make the current array exceed 900 data
      // if exceeds, populate the current array space with 'end' and start a new array
      if (sprt+jsonReceived.Pressure.length>disp_length){
        P.push('end');
        Q.push('end');
        V.push('end');
        sprt = 0;
      }

      newtickvals.push((0.02*sprt).toFixed(2));
      newticktext.push([('0'+now.getHours()).slice(-2),':',('0'+now.getMinutes()).slice(-2),':',('0'+now.getSeconds()).slice(-2)].join(''));

      var t2 = performance.now();
      for (i = 0; i < jsonReceived.Pressure.length; i++) {

          P.push(jsonReceived.Pressure[i]);
          Q.push(jsonReceived.FlowRate[i]);
          V.push(jsonReceived.Volume[i]); 
          sprt += 1;
      } 
      var t3 = performance.now();
      // updates the calculated data
      IE_display.push(jsonReceived.IE);
      RR_display.push(jsonReceived.RR);
      VE_display.push(jsonReceived.VE);
      PEEP_display.push(jsonReceived.PEEP);
      PIP_display.push(jsonReceived.PIP);
      Vtidal_display.push(jsonReceived.Vtidal);
      Ers_display.push(jsonReceived.Ers);
      Rrs_display.push(jsonReceived.Rrs);
      //console.log(P.length);
      var t4 = performance.now();

      var t5 = performance.now();      
      console.log('Parse jsonFILE Time:');
      console.log(t1-t0);
      console.log('Check Exceed Length Time:');
      console.log(t2-t1);
      console.log('Update Array Time:');
      console.log(t3-t2);
      console.log('Update Calc Array Time:');
      console.log(t4-t3);
      console.log('Get Current Time Time:');
      console.log(t5-t4);
  });

})
//</script>