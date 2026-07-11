// Chart.js
let mediaRecorder;
let audioChunks = [];

const recordBtn = document.getElementById("recordBtn");

if (recordBtn) {
    recordBtn.addEventListener("click", async () => {

        if (recordBtn.innerText === "Start Recording") {

            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.start();
            recordBtn.innerText = "Stop Recording";

            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {

                const audioBlob = new Blob(audioChunks, { type: "audio/wav" });

                const formData = new FormData();
                formData.append("audio", audioBlob, "record.wav");

                const response = await fetch("/record", {
                    method: "POST",
                    body: formData
                });

                const result = await response.json();

                document.getElementById("prediction").innerHTML =
                    "<h2>Predicted Emotion: " + result.emotion + "</h2>";
            };

        } else {

            mediaRecorder.stop();
            recordBtn.innerText = "Start Recording";

        }

    });
}


             