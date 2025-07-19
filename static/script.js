document.getElementById("uploadForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const formData = new FormData(this);

  fetch("/upload", {
    method: "POST",
    body: formData,
  })
  .then(response => {
    if (response.ok) {
      return response.blob();
    } else {
      return response.text().then(text => { throw new Error(text); });
    }
  })
  .then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "flag.txt";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
    document.getElementById("result").textContent = "✅ Congrats! Flag downloaded.";
  })
  .catch(err => {
    document.getElementById("result").textContent = err.message || "Upload failed.";
  });
});


