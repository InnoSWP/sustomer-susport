import * as core from "./core.js"
import * as handler from "./handle-form.js"


function getLocalChat(): handler.ChatHistory {
  const chat = window.localStorage.getItem("ChatHistory");
  if (chat == null) return [];
  return JSON.parse(chat);
}

function storeChat(chat: handler.ChatHistory) {
  window.localStorage.setItem("ChatHistory", JSON.stringify(chat));
}

function updateChatComposition(
  message: handler.ChatEntry,
  container: HTMLElement
): void {
  const history = getLocalChat();
  const newHistory = handler.addMessage(history, message);
  handler.displayChat(newHistory, container);
  storeChat(newHistory);
}

function submitForm(form: HTMLElement, container: HTMLElement): void {
  const value: string = handler.form2text(form);
  handler.sendMessage(
    {
      text: value,
      user_id: 1337,
    },
    (text: string) => {
      const body: Array<{ answer: string; question: string }> =
        JSON.parse(text);
      body.forEach((similarQuestion) => {
        return updateChatComposition(
          {
            author: handler.similarQuestionLabel,
            text: `${similarQuestion.question}   ?=>  ${similarQuestion.answer}`,
          },
          container
        );
      });
    }
  );
  updateChatComposition(
    {
      author: handler.userIsAuthor,
      text: value,
    },
    container
  );
}

function getUpdatesForMessages(container: HTMLElement) {
  function onSuccess(response: Response): void {
    response.text().then((value: string) => {
      const data: string[] = JSON.parse(value);
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

function setup(): void {
  const form = document.querySelector("#ask_question_form");
  if (form == null) {
    return;
  }
  const button = <HTMLElement>form.querySelector("button[value=submit]");
  button.onclick = () => submitForm(<HTMLElement>form, container);
  const refreshButton = <HTMLButtonElement>(
    form.querySelector("button[value=refresh]")
  );
  let container = <HTMLElement>document.querySelector("div#message-history");
  document.body.appendChild(container);
  refreshButton.onclick = () => getUpdatesForMessages(container);
}

setup();
