import React from "react";
import "../global.css";
import { startRecording, stopRecording } from "../recordFunctions.js";

const Record = () => {
  const startRecordingHandler = () => {
    startRecording();
  };

  const stopRecordingHandler = () => {
    stopRecording();
  };

  return (
    <div>
      <h1>Record Yourself</h1>
      <h2>
        <video id="videoElement" autoPlay></video>
		<div>
			<button onClick={startRecordingHandler}>Start Recording</button>
			<button onClick={stopRecordingHandler}>Stop Recording and Send</button>
		</div>
	</h2>
      <script src="recordFunctions.js"></script>
    </div>
  );
};

export default Record;
