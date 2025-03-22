document.addEventListener("DOMContentLoaded", function () {
  const analyzeButton = document.getElementById("analyzeBtn");
  const resultContainer = document.getElementById("result");

  analyzeButton.addEventListener("click", async function () {
    chrome.tabs.query(
      { active: true, currentWindow: true },
      async function (tabs) {
        let url = tabs[0].url;
        let videoId = extractVideoID(url);

        if (!videoId) {
          resultContainer.innerHTML =
            "<p style='color: red;'>Invalid YouTube URL</p>";
          return;
        }

        resultContainer.innerHTML = "<p>Analyzing comments...</p>";

        try {
          let response = await fetch("http://localhost:5000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ video_id: videoId }),
          });

          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }

          let data = await response.json();
          console.log(data);

          if (data.status === "success") {
            resultContainer.innerHTML = `<h2>Sentiment Analysis</h2>`;

            // 🎯 **1️⃣ Show Sentiment Grid First**
            let sentimentGrid = document.createElement("div");
            sentimentGrid.className = "sentiment-grid";
            sentimentGrid.innerHTML = `
            <div class="sentiment-box positive">Positive<br>${data.sentiment_counts.positive}</div>
            <div class="sentiment-box neutral">Neutral<br>${data.sentiment_counts.neutral}</div>
            <div class="sentiment-box negative">Negative<br>${data.sentiment_counts.negative}</div>
          `;
            resultContainer.appendChild(sentimentGrid);

            // 🎯 **2️⃣ Display Pie Chart Below**
            let pieChartContainer = document.createElement("div");
            pieChartContainer.id = "pie-chart";
            resultContainer.appendChild(pieChartContainer);

            let pieChartData = [
              {
                values: [
                  data.pie_chart_data.positive,
                  data.pie_chart_data.neutral,
                  data.pie_chart_data.negative,
                ],
                labels: ["Positive", "Neutral", "Negative"],
                type: "pie",
              },
            ];
            let pieChartLayout = { title: "Sentiment Distribution" };
            Plotly.newPlot("pie-chart", pieChartData, pieChartLayout);

            // 🎯 **3️⃣ Show Top Words Below**
            let topWordsContainer = document.createElement("div");
            topWordsContainer.innerHTML = `
            <h2>Top Words:</h2>
            <p>${data.top_sentiment_phrases.join(", ")}</p>
          `;
            resultContainer.appendChild(topWordsContainer);

            // 🎯 **4️⃣ Show Word Cloud Last**
            let wordCloudContainer = document.createElement("div");
            wordCloudContainer.innerHTML = `<img src="${data.word_cloud_url}" alt="Word Cloud" />`;
            resultContainer.appendChild(wordCloudContainer);
          } else {
            resultContainer.innerHTML =
              "<p style='color: red;'>Error analyzing comments.</p>";
          }
        } catch (error) {
          console.error("Error:", error);
          resultContainer.innerHTML = `<p style='color: red;'>Server not responding: ${error.message}</p>`;
        }
      }
    );
  });
});

function extractVideoID(url) {
  let match = url.match(/[?&]v=([^&]+)/);
  console.log(match[1]);
  return match ? match[1] : null;
}
