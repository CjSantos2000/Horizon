const business_id = document.querySelector("#business_id");
// Sample data for the line chart
const data = {
  labels: ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"],
  datasets: [
    {
      label: "Income",
      data: [10, 15, 7, 25, 18],
      fill: false,
      borderColor: "rgba(60, 179, 113, 1)",
      borderWidth: 2,
    },
    {
      label: "Expense",
      data: [2000, 1500, 4000, 3500, 1800],
      fill: false,
      borderColor: "rgba(250, 0, 0, 1)",
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

const getChartAllData = () => {
  fetch(
    "business-chart-data?" +
      new URLSearchParams({
        period: "all",
      }),
    {
      method: "GET",
    }
  )
    .then((response) => response.json())
    .then((results) => {
      const [income_data, income_labels, expense_data, expense_labels] = [
        results.income.data,
        results.income.labels,
        results.expense.data,
        results.expense.labels,
      ];

      myChart.data.labels = income_labels;
      myChart.data.datasets[0].data = income_data;
      myChart.data.datasets[1].data = expense_data;
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
      const [income_data, income_labels, expense_data, expense_labels] = [
        results.income.data,
        results.income.labels,
        results.expense.data,
        results.expense.labels,
      ];

      myChart.data.labels = income_labels;
      myChart.data.datasets[0].data = income_data;
      myChart.data.datasets[1].data = expense_data;
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
      const [income_data, income_labels, expense_data, expense_labels] = [
        results.income.data,
        results.income.labels,
        results.expense.data,
        results.expense.labels,
      ];

      myChart.data.labels = income_labels;
      myChart.data.datasets[0].data = income_data;
      myChart.data.datasets[1].data = expense_data;
      myChart.update();
    });
};
const getChartYearlyData = () => {
  fetch(
    "business-chart-data?" +
      new URLSearchParams({
        period: "yearly",
      }),
    {
      method: "GET",
    }
  )
    .then((response) => response.json())
    .then((results) => {
      const [income_data, income_labels, expense_data, expense_labels] = [
        results.income.data,
        results.income.labels,
        results.expense.data,
        results.expense.labels,
      ];

      myChart.data.labels = income_labels;
      myChart.data.datasets[0].data = income_data;
      myChart.data.datasets[1].data = expense_data;
      myChart.update();
    });
};

document.getElementById("allButton").addEventListener("click", () => {
  getChartAllData();
});

document.getElementById("weeklyButton").addEventListener("click", () => {
  getChartWeeklyData();
});

document.getElementById("monthlyButton").addEventListener("click", () => {
  getChartMonthlyData();
});

document.getElementById("yearlyButton").addEventListener("click", () => {
  getChartYearlyData();
});

$(document).ready(function () {
  // Add a class to the initially selected button
  $("#allButton").addClass("btn-selected");

  // Add the click event listeners for the buttons
  $("#allButton").click(function () {
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

  $("#yearlyButton").click(function () {
    $(".btn-secondary").removeClass("btn-selected");
    $(this).addClass("btn-selected");
  });
});

document.onload = getChartAllData();
