document.getElementById("predictBtn").addEventListener("click", function () {
  const riskLevels = ["Low", "Medium", "High"];
  const randomRisk = riskLevels[Math.floor(Math.random() * riskLevels.length)];
  const riskBox = document.getElementById("riskLevel");
  const recList = document.getElementById("recommendations");

  recList.innerHTML = "";

  if (randomRisk === "Low") {
    riskBox.style.background = "green";
    recList.innerHTML = `
      <li>Maintain a balanced diet.</li>
      <li>Keep regular health checkups.</li>`;
  } else if (randomRisk === "Medium") {
    riskBox.style.background = "orange";
    recList.innerHTML = `
      <li>Reduce salt and sugar intake.</li>
      <li>Consult a physician for risk management.</li>`;
  } else {
    riskBox.style.background = "red";
    recList.innerHTML = `
      <li>Avoid smoking and alcohol completely.</li>
      <li>Follow a strict low-fat diet.</li>
      <li>Immediate medical consultation recommended.</li>`;
  }

  riskBox.textContent = randomRisk;
});

document.getElementById("resetBtn").addEventListener("click", function () {
  document.getElementById("riskLevel").textContent = "—";
  document.getElementById("recommendations").innerHTML = "";
});
