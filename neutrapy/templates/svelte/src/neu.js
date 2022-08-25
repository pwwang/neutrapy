// This is just a sample app. You can structure your Neutralinojs app code as you wish.
// This example app is written with vanilla JavaScript and HTML.
// Feel free to use any frontend framework you like :)
// See more details: https://neutralino.js.org/docs/how-to/use-a-frontend-library

const extensionId = "js.neutralino.${slug_name}.python";

Neutralino.init();

Neutralino.events.on("windowClose", (e) => Neutralino.app.exit() );

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
