import * as core from "./core.js";
function requestFailure(error) {
    console.log("Error during request performing");
    console.log(error);
}
function form2text(form) {
    const el = form.querySelector("#question_text");
    return core.html2text(el);
}
function updateChatComposition(message, container) {
    const history = getLocalChat();
    const newHistory = addMessage(history, message);
    displayChat(newHistory, container);
    storeChat(newHistory);
}
function submitForm(form, container) {
    const value = form2text(form);
    sendMessage({
        text: value,
        user_id: 1337,
    }, (text) => {
        const body = JSON.parse(text);
        body.map((similarQuestion) => {
            return updateChatComposition({
                author: similarQuestionLabel,
                text: `${similarQuestion.question}   ?=>  ${similarQuestion.answer}`,
            }, container);
        });
    });
    updateChatComposition({
        author: userIsAuthor,
        text: value,
    }, container);
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
    if (message.author == userIsAuthor) {
    }
    else {
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
    children.map((child) => container.appendChild(child));
}
function displayChat(chat, container) {
    const chatElementsHtml = chat.map((value) => {
        return displayMessage(value);
    });
    deleteChildren(container);
    addChildren(container, chatElementsHtml);
}
function getUpdatesForMessages(container) {
    function onSuccess(response) {
        response.text().then((value) => {
            const data = JSON.parse(value);
            if (data.length == 0) {
                displayChat(getLocalChat(), container);
                return;
            }
            {
                const newMessages = data.map((value) => {
                    return { author: "support", text: value };
                });
                const chatHistory = getLocalChat().concat(newMessages);
                storeChat(chatHistory);
                displayChat(chatHistory, container);
            }
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
    button.onclick = () => submitForm(form, container);
    const refreshButton = (form.querySelector("button[value=refresh"));
    let container = document.querySelector("div#message-history");
    document.body.appendChild(container);
    refreshButton.onclick = () => getUpdatesForMessages(container);
}
setup();
//# sourceMappingURL=handle-form.js.map