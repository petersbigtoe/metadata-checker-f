async function uploadFile() {
  const input = document.getElementById("fileInput");
  const file = input.files[0];
  if (!file) {
    alert("Please select a file.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  document.getElementById("result").textContent = "Uploading...";

  try {
    const response = await fetch("https://your-backend-url.com/check", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      document.getElementById("result").textContent = "Flag: " + data.flag;
    } else {
      document.getElementById("result").textContent = "Error: " + data.message;
    }
  } catch (err) {
    document.getElementById("result").textContent = "Request failed: " + err;
  }
}
