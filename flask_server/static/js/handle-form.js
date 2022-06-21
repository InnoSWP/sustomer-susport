import * as core from "./core.js";
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
        onError: function (arg0) {
            throw new Error("Function not implemented.");
        },
        request: Object.assign(Object.assign({}, core.defaultRequest), { method: "POST", body: JSON.stringify(msg) }),
    };
    core.basicFetch(parameters);
    console.log("undefined");
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
        onError: function (arg0) {
            console.log("Error while request fetching");
            console.log(arg0);
        },
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
    let newButton = document.createElement("button");
    newButton.type = "button";
    newButton.textContent = "get responses";
    let container = document.createElement("div");
    document.body.appendChild(container);
    newButton.onclick = () => getUpdatesForMessages(container);
    form.appendChild(newButton);
}
setup();
//# sourceMappingURL=handle-form.js.map