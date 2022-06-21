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
    const history = getLocalChat();
    storeChat(addMessage(history, {
        author: userIsAuthor,
        text: value,
    }));
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
function getLocalChat() {
    const chat = window.localStorage.getItem("ChatHistory");
    if (chat == null)
        return [];
    return JSON.parse(chat);
}
function storeChat(chat) {
    window.localStorage.setItem("ChatHistory", JSON.stringify(chat));
}
function addMessage(chat, message) {
    chat.push(message);
    return chat;
}
const userIsAuthor = " ";
function displayMessage(message) {
    const messageContainer = document.createElement("div");
    if (message.author == userIsAuthor) {
        messageContainer.setAttribute("class", "user-message");
    }
    else {
        messageContainer.setAttribute("class", "others-message");
    }
    messageContainer.textContent = message.text;
    return messageContainer;
}
function deleteChildren(container) {
    for (let i = 0; i < container.children.length; i++) {
        container.removeChild(container.children[0]);
    }
}
function addChildren(container, children) {
    children.map((child) => container.appendChild(child));
}
function getUpdatesForMessages(container) {
    function onSuccess(response) {
        response.text().then((value) => {
            const data = JSON.parse(value);
            if (data.length == 0)
                return;
            {
                const newMessages = data.map((value) => {
                    return { author: "support", text: value };
                });
                const chatHistory = getLocalChat().concat(newMessages);
                storeChat(chatHistory);
                const chatElementsHtml = chatHistory.map((value) => {
                    return displayMessage(value);
                });
                deleteChildren(container);
                addChildren(container, chatElementsHtml);
            }
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