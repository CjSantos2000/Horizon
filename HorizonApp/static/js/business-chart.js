const business_id = document.querySelector("#business_id");
// Sample data for the line chart
const data = {
  labels: ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"],
  datasets: [
    {
      label: "Sales Amount",
      data: [10, 15, 7, 25, 18],
      fill: false,
      borderColor: "rgba(75, 192, 192, 1)",
      borderWidth: 2,
    },
  ],
};

// Create a Chart.js line chart
const ctx = document.getElementById("myChart").getContext("2d");
const myChart = new Chart(ctx, {
  type: "line", // Set the chart type to "line"
  data: data,
  options: {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
    plugins: {
      title: {
        display: true,
        text: "Sales Performance", // Chart title
        font: {
          size: 24,
        },
      },
    },
  },
});

const getChartDailyData = () => {
  fetch(
    "business-chart-data?" +
      new URLSearchParams({
        period: "daily",
      }),
    {
      method: "GET",
    }
  )
    .then((response) => response.json())
    .then((results) => {
      const [data, labels] = [results.data, results.labels];
      myChart.data.labels = labels;
      myChart.data.datasets[0].data = data;
      myChart.update();
    });
};
const getChartWeeklyData = () => {
  fetch(
    "business-chart-data?" +
      new URLSearchParams({
        period: "weekly",
      }),
    {
      method: "GET",
    }
  )
    .then((response) => response.json())
    .then((results) => {
      const [data, labels] = [results.data, results.labels];
      myChart.data.labels = labels;
      myChart.data.datasets[0].data = data;
      myChart.update();
    });
};
const getChartMonthlyData = () => {
  fetch(
    "business-chart-data?" +
      new URLSearchParams({
        period: "monthly",
      }),
    {
      method: "GET",
    }
  )
    .then((response) => response.json())
    .then((results) => {
      const [data, labels] = [results.data, results.labels];
      myChart.data.labels = labels;
      myChart.data.datasets[0].data = data;
      myChart.update();
    });
};

document.getElementById("dailyButton").addEventListener("click", () => {
  getChartDailyData();
});

document.getElementById("weeklyButton").addEventListener("click", () => {
  getChartWeeklyData();
});

document.getElementById("monthlyButton").addEventListener("click", () => {
  getChartMonthlyData();
});

$(document).ready(function () {
  // Add a class to the initially selected button
  $("#dailyButton").addClass("btn-selected");

  // Add the click event listeners for the buttons
  $("#dailyButton").click(function () {
    $(".btn-secondary").removeClass("btn-selected");
    $(this).addClass("btn-selected");
  });

  $("#weeklyButton").click(function () {
    $(".btn-secondary").removeClass("btn-selected");
    $(this).addClass("btn-selected");
  });

  $("#monthlyButton").click(function () {
    $(".btn-secondary").removeClass("btn-selected");
    $(this).addClass("btn-selected");
  });
});

document.onload = getChartDailyData();
