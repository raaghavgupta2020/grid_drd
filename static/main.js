//========================================================================
// Drag and drop image handling
//========================================================================

var fileDrag = document.getElementById("file-drag");
var fileSelect = document.getElementById("file-upload");

// Add event listeners
fileDrag.addEventListener("dragover", fileDragHover, false);
fileDrag.addEventListener("dragleave", fileDragHover, false);
fileDrag.addEventListener("drop", fileSelectHandler, false);
fileSelect.addEventListener("change", fileSelectHandler, false);

function fileDragHover(e) {
  // prevent default behaviour
  e.preventDefault();
  e.stopPropagation();

  fileDrag.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
}

function fileSelectHandler(e) {
  // handle file selecting
  var files = e.target.files || e.dataTransfer.files;
  fileDragHover(e);
  for (var i = 0, f; (f = files[i]); i++) {
    // previewFile(f);
  }
}

//========================================================================
// Web page elements for functions to use
//========================================================================

var imagePreview = document.getElementById("image-preview");
var imageDisplay = document.getElementById("image-display");
var uploadCaption = document.getElementById("upload-caption");
var predResult = document.getElementById("pred-result");
var loader = document.getElementById("loader");
var predResult2 = document.getElementById("pred-result-2");

//========================================================================
// Main button events
//========================================================================

async function loadImageData(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = function(event) {
      resolve(event.target.result);
    };

    reader.onerror = function(event) {
      reject(event.error);
    };

    reader.readAsDataURL(file);
  });
}

async function submitImage() {
  console.log("submit");
  const selectedFiles = fileSelect.files;
  console.log(selectedFiles);
  
  if (!selectedFiles || selectedFiles.length === 0) {
    window.alert("Please select one or more images before submit.");
    return;
  }

  loader.classList.remove("hidden");
  imageDisplay.classList.add("loading");

  const imagesArray = [];
  console.log(typeof(imagesArray));

  for (let i = 0; i < selectedFiles.length; i++) {
    try {
      const imageData = await loadImageData(selectedFiles[i]);
      console.log("here1");
      imagesArray.push(imageData);
    } catch (error) {
      console.error("Error loading image:", error);
    }
    console.log("here2");
  }

  console.log("here3");
  console.log(typeof(imagesArray));
  console.log(imagesArray[0]);

  for (let i = 0; i < imagesArray.length; i++) {
    predictImage(imagesArray[i],selectedFiles[i]);
  }

  generateImageGrid(imagesArray, selectedFiles);

}
// Call the async function when needed, for example, on a button click

function clearImage() {
  // reset selected files
  fileSelect.value = "";

  // remove image sources and hide them
  imagePreview.src = "";
  imageDisplay.src = "";
  predResult.innerHTML = "";
  predResult2.innerHTML = "";

  hide(imagePreview);
  hide(imageDisplay);
  hide(loader);
  hide(predResult);
  hide(predResult2);
  show(uploadCaption);

  imageDisplay.classList.remove("loading");
}

function previewFile(file) {
  // show the preview of the image
  console.log(file.name);
  var fileName = encodeURI(file.name);

  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = () => {
    imagePreview.src = URL.createObjectURL(file);

    show(imagePreview);
    hide(uploadCaption);

    // reset
    predResult.innerHTML = "";
    predResult2.innerHTML = "";
    imageDisplay.classList.remove("loading");

    displayImage(reader.result, "image-display");
  };
}

//========================================================================
// Helper functions
//========================================================================

function predictImage(image,file) {
  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(image)
  })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
          console.log("here1");
          console.log(data);
          // displayResult(data);
          hide(loader);
          console.log("here2");
          saveToDatabase(data, file.name);
        });
    })
    .catch(err => {
      console.log("An error occured", err.message);
      window.alert("Oops! Something went wrong.");
    });
}

function saveToDatabase(data, filename) {
  fetch("/save_to_database", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({ data, filename })
  })
  .catch(err => {
      console.log("An error occurred while saving to the database", err.message);
  });
}

function displayImage(image, id) {
  // display image on given id <img> element
  let display = document.getElementById(id);
  display.src = image;
  show(display);
}

function displayResult(data) {
  // display the result
  // imageDisplay.classList.remove("loading");
  hide(loader);
  predResult.innerHTML = data.result;
  predResult2.innerHTML = data.probability;
  show(predResult);
  show(predResult2);
}

function hide(el) {
  // hide an element
  el.classList.add("hidden");
}

function show(el) {
  // show an element
  el.classList.remove("hidden");
}

function processRow(button) {
  var row = button.closest("tr");
  var existingResult = row.getAttribute("data-existing-result");
  var existingProbability = row.getAttribute("data-existing-probability");
  var inputFields = row.querySelectorAll(".input-field");
  var input1Value = inputFields[0].value;
  var input2Value = inputFields[1].value;
  // console.log("hey1 = "+input1Value);
  // console.log("hey2 = "+input2Value);
  // console.log("hey3 = "+existingProbability);
  // console.log("hey4 = "+existingResult);
  remediate(input1Value, input2Value, existingResult, existingProbability);
}

async function remediate(input1Value, input2Value, existingResult, existingProbability) {
  // console.log("hey1 = "+input1Value);
  // console.log("hey2 = "+input2Value);
  // console.log("hey3 = "+existingProbability);
  // console.log("hey4 = "+existingResult);

  var inputText = "There is a patient "+input1Value+" whose age is "+input2Value+" ,his eye image is uploaded in a ML model which detects if the person has diabetic retinopathy, the severity comes out to be "+existingResult+" with a probability of correctness of ML model equals to "+existingProbability+" ,now generate remediation steps in 80-100 words";
  // var inputText = "raghav gupta";
  // console.log(inputText);

  const response = await fetch('/generate_response', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ input_text: inputText }),
  });

  if (!response.ok) {
    throw new Error(`API request failed with status: ${response.status}`);
  }

  const data = await response.json();
  console.log("data");
  console.log(data.body);

  // Create a dialog box
  const dialog = document.createElement('dialog');
  dialog.innerHTML = `
    <div>
      <p style="color:#000000">${data.body}</p>
      <button id="closeDialog">Close</button>
    </div>
  `;
  
  // Append the dialog box to the body
  document.body.appendChild(dialog);

  // Open the dialog
  dialog.showModal();
  
  // Close the dialog when the close button is clicked
  const closeButton = dialog.querySelector('#closeDialog');
  closeButton.addEventListener('click', () => {
    dialog.close();
    // You can also remove the dialog element from the DOM if needed
    dialog.remove();
  });
}


async function generateImageGrid(imagesArray, selectedFiles) {
  console.log("heyyy");
  const imageGrid = document.getElementById("image-grid");
  imageGrid.innerHTML = ''; // Clear the grid before adding images

  for (let i = 0; i < imagesArray.length; i++) {
    const imageDiv = document.createElement("div");
    imageDiv.className = "image-item";

    const imageName = document.createElement("p");
    imageName.textContent = selectedFiles[i].name;

    // const predictionResult = document.createElement("p");
    // predictionResult.textContent = "Prediction: " + predictions[i].label;

    // const predictionProbability = document.createElement("p");
    // predictionProbability.textContent = "Probability: " + predictions[i].probability.toFixed(3);
    
    const imageElement = document.createElement("img");
    imageElement.src = imagesArray[i];
    imageElement.className = "grid-image";

    imageDiv.appendChild(imageName);
    imageDiv.appendChild(imageElement);
    // imageDiv.appendChild(predictionResult);
    // imageDiv.appendChild(predictionProbability);
    imageGrid.appendChild(imageDiv);

    // clearImage();
  }
}