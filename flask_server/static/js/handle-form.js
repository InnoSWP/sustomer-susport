import * as core from "./core.js";
function requestFailure(error) {
    console.log("Error during request performing");
    console.log(error);
}
function form2text(form) {
    const el = form.querySelector("#question_text");
    return core.html2text(el);
}
function sendMessage(msg, handleSimilarQuestions) {
    const parameters = {
        url: "/messages",
        onSuccess: function (value) {
            value.text().then((text) => {
                if (value.ok) {
                    handleSimilarQuestions(text);
                }
            });
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
function addMessage(chat, message) {
    chat.push(message);
    return chat;
}
const userIsAuthor = " ";
const similarQuestionLabel = "similar-question";
function displayMessage(message) {
    const messageContainer = document.createElement("div");
    switch (message.author) {
        case userIsAuthor:
            messageContainer.setAttribute("class", "user-message");
            break;
        case similarQuestionLabel:
            messageContainer.setAttribute("class", "similar-question");
            break;
        default:
            messageContainer.setAttribute("class", "others-message");
    }
    messageContainer.textContent = message.text;
    return messageContainer;
}
function deleteChildren(container) {
    for (let i = container.children.length; i > 0; i--) {
        container.removeChild(container.children[0]);
    }
}
function addChildren(container, children) {
    children.forEach((child) => container.appendChild(child));
}
function displayChat(chat, container) {
    const chatElementsHtml = chat.map((value) => {
        return displayMessage(value);
    });
    deleteChildren(container);
    addChildren(container, chatElementsHtml);
}
export { deleteChildren, addChildren, displayChat, requestFailure, form2text, sendMessage, addMessage, similarQuestionLabel, userIsAuthor, };
//# sourceMappingURL=handle-form.js.map