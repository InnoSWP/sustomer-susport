import * as core from "./core.js";
function requestFailure(error) {
    console.log("Error during request performing");
    console.log(error);
}
function form2text(form) {
    const el = form.querySelector("#question_text");
    if (el == null) {
        return "";
    }
    return core.html2text(el);
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
    return container;
}
function addChildren(container, children) {
    children.forEach((child) => container.appendChild(child));
    return container;
}
function displayChat(chat, container) {
    const chatElementsHtml = chat.map((value) => {
        return displayMessage(value);
    });
    deleteChildren(container);
    addChildren(container, chatElementsHtml);
    return container;
}
export { deleteChildren, addChildren, displayChat, requestFailure, form2text, addMessage, displayMessage, similarQuestionLabel, userIsAuthor, };
//# sourceMappingURL=handle-form.js.map