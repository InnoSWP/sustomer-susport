function html2text(htmlElement) {
    if (htmlElement == null) {
        return "";
    }
    return htmlElement.value;
}
function form2text(form) {
    const el = form.querySelector("#question_text");
    return html2text(el);
}
function submitForm(form) {
    const value = form2text(form);
    console.log(value);
    sendMessage({
        text: value,
        user_id: 1337,
    });
}
function sendData(data) {
    const request = {
        method: "POST",
        headers: { "content-type": "application/json;charset=UTF-8" },
        body: data,
    };
    const promise = window.fetch("/messages", request);
    promise.then((value) => {
        console.log(value.ok);
    });
    promise.catch((error) => console.log(error));
}
function sendMessage(msg) {
    sendData(JSON.stringify(msg));
}
function setup() {
    const form = document.querySelector("#ask_question_form");
    if (form == null) {
        alert("form not found");
        return;
    }
    const button = form.querySelector("button[value=submit]");
    button.onclick = () => submitForm(form);
}
setup();
//# sourceMappingURL=handle-form.js.map