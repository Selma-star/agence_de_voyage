'use strict';

$(function() {
  // Area chart
  if ($('#apexcharts-area').length) {
    var dataUrl = '/chart-data/';
    var chart = new ApexCharts(
      document.querySelector('#apexcharts-area'),
      {
        chart: { height: 350, type: 'area', toolbar: { show: false } },
        dataLabels: { enabled: false },
        stroke: { curve: 'smooth' },
        series: [
          { name: 'Flight Only',  data: [] },
          { name: 'Hotel Only',   data: [], color: '#00CFE8' },
          { name: 'Full Package', data: [], color: '#003366' }
        ],
        xaxis: { categories: [], tickPlacement: 'on' }
      }
    );
    chart.render();

    function fetchAndUpdate() {
      $.getJSON(dataUrl)
        .done(function(d) {
          chart.updateOptions({ xaxis: { categories: d.categories } });
          chart.updateSeries([
            { name: 'Flight Only',  data: d.flight_only  },
            { name: 'Hotel Only',   data: d.hotel_only   },
            { name: 'Full Package', data: d.full_package }
          ]);
        })
        .fail(function(err) {
          console.error('Error fetching chart data:', err);
        });
    }

    // Initial load + poll every 24 hours (86400000 ms)
    fetchAndUpdate();
    setInterval(fetchAndUpdate, 86400000);
  }

  if (!$('#bar').length) return;

  var dataUrl = '/client-chart-data/';

  // 1) Create an empty bar chart with one series (“Clients”)
  var optionsBar = {
    chart: {
      type: 'bar',
      height: 350,
      width: '100%',
      toolbar: { show: false }
    },
    dataLabels: { enabled: false },
    plotOptions: {
      bar: { columnWidth: '45%' }
    },
    series: [
      { name: 'Clients', data: [] }
    ],
    xaxis: {
      categories: [],      // will be set dynamically
      labels: { show: true },
      axisBorder: { show: false },
      axisTicks:  { show: false }
    },
    yaxis: {
      labels: { style: { colors: '#777' } },
      axisBorder: { show: false },
      axisTicks:  { show: false }
    },
    title: {
      text: '',
      align: '',
      style: { fontSize: '18px' }
    }
  };

  var chartBar = new ApexCharts(document.querySelector('#bar'), optionsBar);
  chartBar.render();

  // 2) Function to fetch data and update the chart
  function updateClients() {
    $.getJSON(dataUrl)
      .done(function(d) {
        chartBar.updateOptions({ xaxis: { categories: d.categories } });
        chartBar.updateSeries([
          { name: 'Clients', data: d.data }
        ]);
      })
      .fail(function(err) {
        console.error('Error fetching client chart data:', err);
      });
  }

  // 3) Initial load + refresh every 24 hours (86400000 ms)
  updateClients();
  setInterval(updateClients, 86400000);

});
