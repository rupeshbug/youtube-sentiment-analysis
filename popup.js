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
            resultContainer.innerHTML = `
              <h3>Sentiment Analysis</h3>
              <p>Positive: ${data.sentiment_counts.positive}</p>
              <p>Neutral: ${data.sentiment_counts.neutral}</p>
              <p>Negative: ${data.sentiment_counts.negative}</p>
              <h4>Top Words:</h4>
              <p>${data.top_sentiment_phrases.join(", ")}</p>
            `;
          } else {
            resultContainer.innerHTML =
              "<p style='color: red;'>Error analyzing comments.</p>";
          }
        } catch (error) {
          console.error("Error:", error);
          resultContainer.innerHTML =
            "<p style='color: red;'>Server not responding: ${error.message}</p>";
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
