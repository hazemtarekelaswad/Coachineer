let startButton = document.getElementById("startButton");
let stopButton = document.getElementById("stopButton");
// let saveButton = document.getElementById("saveButton");
let evaluateButton = document.getElementById("evaluateButton");

stopButton.disabled = true;
evaluateButton.classList.add("disabled");
// evaluateButton.disabled = true;

startButton.onclick = () => {
    startButton.disabled = true;
    stopButton.disabled = false;

    // saveButton.href = "";
    evaluateButton.classList.add("disabled");
    // evaluateButton.disabled = true;

    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // alert(xhr.responseText);
        }
    }
    xhr.open("POST", "/record_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ status: "true" }));
}

stopButton.onclick = () => {
    startButton.disabled = false;
    stopButton.disabled = true;


    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            evaluateButton.classList.remove("disabled");
            // saveButton.href = "/static/videos/original/video.mp4";
            // evaluateButton.disabled = false;
        }
    }
    xhr.open("POST", "/record_status");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify({ status: "false" }));
}

// evaluateButton.onclick = () => {
//     let xhr = new XMLHttpRequest();
//     xhr.onreadystatechange = function () {
//         if (xhr.readyState == 4 && xhr.status == 200) { }
//     }
//     xhr.open("POST", window.location.href);
//     xhr.send();
// }
