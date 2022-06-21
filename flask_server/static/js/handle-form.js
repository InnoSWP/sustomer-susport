import * as core from "./core.js";
function requestFailure(error) {
    console.log("Error during request performing");
    console.log(error);
}
function form2text(form) {
    const el = form.querySelector("#question_text");
    return core.html2text(el);
}
function submitForm(form) {
    const value = form2text(form);
    console.log(value);
    sendMessage({
        text: value,
        user_id: 1337,
    });
}
function sendMessage(msg) {
    const parameters = {
        url: "/messages",
        onSuccess: function (value) {
            console.log(value.ok);
        },
        onError: requestFailure,
        request: Object.assign(Object.assign({}, core.defaultRequest), { method: "POST", body: JSON.stringify(msg) }),
    };
    core.basicFetch(parameters);
}
function appendAnswer(container, text) {
    const div = document.createElement("div");
    div.textContent = text;
    container.appendChild(div);
}
function getUpdatesForMessages(container) {
    function onSuccess(response) {
        response.text().then((value) => {
            appendAnswer(container, value);
        });
    }
    core.basicFetch({
        url: "/messages",
        onSuccess: onSuccess,
        onError: requestFailure,
        request: core.defaultRequest,
    });
}
function setup() {
    const form = document.querySelector("#ask_question_form");
    if (form == null) {
        alert("form not found");
        return;
    }
    const button = form.querySelector("button[value=submit]");
    button.onclick = () => submitForm(form);
    const refreshButton = (form.querySelector("button[value=refresh"));
    let container = document.querySelector("div#message-history");
    document.body.appendChild(container);
    refreshButton.onclick = () => getUpdatesForMessages(container);
}
setup();
//# sourceMappingURL=handle-form.js.map