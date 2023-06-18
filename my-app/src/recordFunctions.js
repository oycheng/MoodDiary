let mediaRecorder;
let recordedChunks = [];
let terminateFunction;
setUpAudio();

// Video
navigator.mediaDevices
  .getUserMedia({ video: true })
  .then((stream) => {
    // Set the video source to the stream
    const videoElement = document.getElementById("videoElement");
    if (videoElement) {
      videoElement.srcObject = stream;
    }
  })
  .catch((error) => {
    console.error("Error accessing the camera: ", error);
  });

function startStream() {
  mediaRecorder.start();
  console.log(mediaRecorder.state);
  console.log("recorder started");

  terminateFunction = startCaptureFrame();
}

function notifyServer() {
  // tell server to start
  const sendData = {
    start: "start",
  };
  fetch("http://localhost:5000/start", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(sendData),
  })
    .then((response) => response.json())
    .then((responseData) => {
      // do nothing
    })
    .catch((error) => {
      // Handle any errors that occur during the request
      console.error("Error:", error);
    });
}

function startRecording() {
  startStream();
  notifyServer();
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    // Stop recording
    mediaRecorder.stop();
    console.log(mediaRecorder.state);

    terminateFunction();
    console.log("Recording stopped.");
  } else {
    console.warn("No recording found.");
  }
}

function startCaptureFrame() {
  const interval = setInterval(() => {
    const canvasElement = document.createElement("canvas"); // Create a temporary canvas element
    const videoElement = document.getElementById("videoElement");
    const newWidth = videoElement.videoWidth;
    const newHeight = videoElement.videoHeight;
    canvasElement.width = newWidth;
    canvasElement.height = newHeight;
    const context = canvasElement.getContext("2d");

    context.drawImage(videoElement, 0, 0, newWidth, newHeight);
    const dataURL = canvasElement.toDataURL("image/jpeg");
    const blob = dataURLToBlob(dataURL);

    const formData = new FormData();
    formData.append("frame_jpg", blob, "frame.jpg");

    fetch("http://localhost:5000/process-frame-result", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.ok) {
          console.log("Frame sent successfully!");
        } else {
          console.error(
            "Failed to send frame:",
            response.status,
            response.statusText
          );
        }
      })
      .catch((error) => {
        console.error("Error sending frame:", error);
      });
  }, 2000);

  return function () {
    clearInterval(interval);
    console.log("Interval ended");
  };
}

function dataURLToBlob(dataURL) {
  const parts = dataURL.split(",");
  const contentType = parts[0].split(":")[1].split(";")[0];
  const base64 = atob(parts[1]);
  const arrayBuffer = new ArrayBuffer(base64.length);
  const uint8Array = new Uint8Array(arrayBuffer);
  for (let i = 0; i < base64.length; i++) {
    uint8Array[i] = base64.charCodeAt(i);
  }
  return new Blob([arrayBuffer], { type: contentType });
}

function setUpAudio() {
  if (navigator.mediaDevices.getUserMedia) {
    console.log("getUserMedia supported.");

    const constraints = { audio: true };

    let onSuccess = function (stream) {
      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.onstop = function (e) {
        console.log("data available after MediaRecorder.stop() called.");
        const blob = new Blob(recordedChunks, {
          type: "audio/mp3; codecs=opus",
        });

        sendAudio(blob);

        recordedChunks = [];
        console.log("download");
      };

      mediaRecorder.ondataavailable = function (e) {
        recordedChunks.push(e.data);
        console.log("recordedChunks pushed");
      };
    };

    let onError = function (err) {
      console.log("The following error occured: " + err);
    };

    navigator.mediaDevices.getUserMedia(constraints).then(onSuccess, onError);
  } else {
    console.log("getUserMedia not supported on your browser!");
  }
}

function sendAudio(audioBlob) {
  // Create FormData to send the audio file
  const formData = new FormData();
  formData.append("audio", audioBlob, "recording.mp3");

  // Send the HTTP request
  fetch("http://localhost:5000/transcription", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((message) => {
      // Handle the response from the server
      console.log(message.response);
    })
    .catch((error) => {
      // Handle any errors that occurred during the request
      console.error(error);
    });
}

export { startRecording, stopRecording };