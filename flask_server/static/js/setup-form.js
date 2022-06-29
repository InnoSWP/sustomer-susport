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
function updateChatComposition(message, container) {
    const history = getLocalChat();
    const newHistory = handler.addMessage(history, message);
    handler.displayChat(newHistory, container);
    storeChat(newHistory);
}
function submitForm(form, container) {
    const value = handler.form2text(form);
    handler.sendMessage({
        text: value,
        user_id: 1337,
    }, (text) => {
        const body = JSON.parse(text);
        body.forEach((similarQuestion) => {
            return updateChatComposition({
                author: handler.similarQuestionLabel,
                text: `${similarQuestion.question}   ?=>  ${similarQuestion.answer}`,
            }, container);
        });
    });
    updateChatComposition({
        author: handler.userIsAuthor,
        text: value,
    }, container);
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
    let container = document.querySelector("div#message-history");
    document.body.appendChild(container);
    refreshButton.onclick = () => getUpdatesForMessages(container);
}
setup();
//# sourceMappingURL=setup-form.js.map