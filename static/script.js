document.getElementById("uploadForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const formData = new FormData();
  const fileInput = document.querySelector('input[name="file"]');
  if (!fileInput.files.length) {
    alert("Please select a file.");
    return;
  }
  const file = fileInput.files[0];
  formData.append("file", file);

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
    a.click();
    window.URL.revokeObjectURL(url); // clean up
  })
  .catch(err => {
    document.getElementById("result").textContent = err.message || "Upload failed.";
  });
});

    .catch((err) => {
      document.getElementById("result").textContent = err.message || "Upload failed.";
    });
});

