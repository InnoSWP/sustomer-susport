import * as core from "./core.js";
import * as handler from "./handle-form.js";
function getLocalChat() {
    const chat = window.localStorage.getItem("ChatHistory");
    if (chat == null)
        return [];
    return JSON.parse(chat);
}
function storeChat(chat) {
    window.localStorage.setItem("ChatHistory", JSON.stringify(chat));
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
        onError: handler.requestFailure,
        request: Object.assign(Object.assign({}, core.defaultRequest), { method: "POST", body: JSON.stringify(msg) }),
    };
    core.basicFetch(parameters);
}
function updateChatComposition(message, container) {
    const history = getLocalChat();
    const newHistory = handler.addMessage(history, message);
    handler.displayChat(newHistory, container);
    storeChat(newHistory);
}
function submitForm(form, container) {
    const value = handler.form2text(form);
    sendMessage({
        text: value,
        user_id: 1337,
    }, (text) => {
        console.log(text);
        const body = JSON.parse(text);
        body.forEach((similarQuestion) => {
            return updateChatComposition({
                author: handler.similarQuestionLabel,
                text: `${similarQuestion.question}:\t\t${similarQuestion.answer}`,
            }, container);
        });
    });
    updateChatComposition({
        author: handler.userIsAuthor,
        text: value,
    }, container);
}
function appendAnswer(container, text) {
    const div = document.createElement("div");
    div.textContent = text;
    container.appendChild(div);
}
function getUpdatesForMessages(container) {
    function onSuccess(response) {
        response.text().then((value) => {
            const data = JSON.parse(value);
            if (data.length == 0) {
                handler.displayChat(getLocalChat(), container);
                return;
            }
            const newMessages = data.map((text) => {
                return { author: "support", text: text };
            });
            const chatHistory = getLocalChat().concat(newMessages);
            storeChat(chatHistory);
            handler.displayChat(chatHistory, container);
        });
    }
    core.basicFetch({
        url: "/messages",
        onSuccess: onSuccess,
        onError: handler.requestFailure,
        request: core.defaultRequest,
    });
}
function setup() {
    const form = document.querySelector("#ask_question_form");
    if (form == null) {
        return;
    }
    const button = form.querySelector("button[value=submit]");
    button.onclick = () => submitForm(form, container);
    const refreshButton = (form.querySelector("button[value=refresh]"));
    const container = document.querySelector("div#message-history");
    document.body.appendChild(container);
    refreshButton.onclick = () => getUpdatesForMessages(container);
    getUpdatesForMessages(container);
    const clearButton = document.querySelector("button[value=clear]");
    clearButton.onclick = () => {
        localStorage.clear();
        handler.deleteChildren(container);
    };
}
function pollingUpdates(container) {
    getUpdatesForMessages(container);
    setTimeout(() => pollingUpdates(container), 1000);
}
setup();
//# sourceMappingURL=setup-form.js.map