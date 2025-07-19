document.getElementById("uploadForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const formData = new FormData();
  const file = document.getElementById("imageFile").files[0];
  formData.append("file", file);

  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then(response => {
      if (response.ok) {
        return response.blob();
      } else {
        return response.json().then(err => { throw err; });
      }
    })
    .then(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "flag.txt";
      a.click();
    })
    .catch(err => {
      document.getElementById("result").textContent = err.message || "Upload failed.";
    });
});

    .catch((err) => {
      document.getElementById("result").textContent = err.message || "Upload failed.";
    });
});

