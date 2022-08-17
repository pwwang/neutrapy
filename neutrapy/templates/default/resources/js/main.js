// This is just a sample app. You can structure your Neutralinojs app code as you wish.
// This example app is written with vanilla JavaScript and HTML.
// Feel free to use any frontend framework you like :)
// See more details: https://neutralino.js.org/docs/how-to/use-a-frontend-library

const extensionId = "js.neutralino.${name}.python";

async function evaluate_python_code() {
    this.disabled = true;
    document.getElementById("output").innerHTML = "Running ...";
    try {
        await Neutralino.extensions.dispatch(
            extensionId,
            "fromAppToExtension",
            document.getElementById("code").value
        )
    } catch {
        document.getElementById("output").innerHTML = "Error: Extension isn't loaded!";
    }
}

function ext_ready() {
    let btn = document.getElementById("evaluate");
    btn.innerHTML = "Evaluate";
    btn.disabled = false;
    btn.removeEventListener("click", evaluate_python_code);
    btn.addEventListener("click", evaluate_python_code);
}

Neutralino.init();

Neutralino.events.on("windowClose", (evt) => Neutralino.app.exit() );
Neutralino.events.on("fromExtensionToApp", (evt) => {
    document.getElementById("output").innerHTML = evt.detail;
    document.getElementById("evaluate").disabled = false;
});

Neutralino.events.on("extensionReady", (evt) => {
    if (evt.detail === extensionId) {
        ext_ready();
    }
});
Neutralino.events.on("extClientConnect", (evt) => {
    if (evt.detail === extensionId) {
        ext_ready();
    }
});

window.onerror = async function(message, source, lineno, colno, error) {
    console.error(message, source, lineno, colno, error);
    try {
        await Neutralino.extensions.dispatch(
            extensionId,
            "windowClose"
        )
    } catch {}
    return false;
};
