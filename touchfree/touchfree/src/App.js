import logo from "./logo.svg";
import "./App.css";
import React, { useRef, useEffect } from "react";
import * as handTrack from "handtrackjs";

function App() {
  const tempRef = useRef(false);
	const videoRef = useRef();
	const canvasRef = useRef();
	useEffect(() => {
    if (tempRef.current) return;
    tempRef.current = true;
		const runHandDetection = async () => {
			const video = videoRef.current;
			const canvas = canvasRef.current;
			const model = await handTrack.load();

			// Function to start gesture detection
			const startGestureDetection = () => {
				const detectGesture = async () => {
					const predictions = await model.detect(video);
					// Process the predictions here (e.g., check for specific gestures)
					// Access the bounding box coordinates using predictions[0].bbox
					// Draw the bounding box on the canvas using drawRect() function
					// ...
          console.log(predictions);
					requestAnimationFrame(detectGesture);
				};

				// Start gesture detection
				detectGesture();
			};

			// Event listener to detect when the video has loaded
			video.addEventListener("loadeddata", startGestureDetection);

			// Start video stream
			navigator.mediaDevices
				.getUserMedia({ video: true })
				.then((stream) => {
					video.srcObject = stream;
					video.play();
				})
				.catch((error) => console.error("Error accessing video stream:", error));

			// Cleanup function to remove the event listener
			return () => {
				video.removeEventListener("loadeddata", startGestureDetection);
			};
		};

		runHandDetection();
	}, []);
	return (
		<div>
			<video ref={videoRef} width="640" height="480" />
			<canvas ref={canvasRef} width="640" height="480" />
		</div>
	);
}

export default App;
