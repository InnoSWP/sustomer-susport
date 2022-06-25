import * as core from "./core.js";

function requestFailure(error: any): void {
  console.log("Error during request performing");
  console.log(error);
}
function form2text(form: HTMLElement): string {
  const el = form.querySelector("#question_text") as HTMLInputElement;
  return core.html2text(el);
}

function updateChatComposition(
  message: ChatEntry,
  container: HTMLElement
): void {
  const history = getLocalChat();
  const newHistory = addMessage(history, message);
  displayChat(newHistory, container);
  storeChat(newHistory);
}

function submitForm(form: HTMLElement, container: HTMLElement): void {
  const value: string = form2text(form);
  sendMessage(
    {
      text: value,
      user_id: 1337,
    },
    (text: string) => {
      const body: Array<{answer: string, question: string}> = JSON.parse(text);
      body.forEach((similarQuestion) => {
        return updateChatComposition(
          {
            author: similarQuestionLabel,
            text: `${similarQuestion.question}   ?=>  ${similarQuestion.answer}`,
          },
          container
        );
      });
    }
  );
  updateChatComposition(
    {
      author: userIsAuthor,
      text: value,
    },
    container
  );
}

function sendMessage(
  msg: core.MessageRequestBody,
  handleSimilarQuestions: (text: string) => void
) {
  const parameters: core.FetchParameters = {
    url: "/messages",
    onSuccess: function (value: Response): void {
      // throw new Error("Function not implemented.");
      value.text().then((text) => {
        if (value.ok) {
          handleSimilarQuestions(text);
        }
      });
    },
    onError: requestFailure,
    request: {
      ...core.defaultRequest,
      method: "POST",
      body: JSON.stringify(msg),
    },
  };
  core.basicFetch(parameters);
}

function appendAnswer(container: HTMLElement, text: string): void {
  const div = document.createElement("div");
  div.textContent = text;
  container.appendChild(div);
}

interface ChatEntry {
  author: string;
  text: string;
}
type ChatHistory = ChatEntry[];

function getLocalChat(): ChatHistory {
  const chat = window.localStorage.getItem("ChatHistory");
  if (chat == null) return [];
  return JSON.parse(chat);
}

function storeChat(chat: ChatHistory) {
  window.localStorage.setItem("ChatHistory", JSON.stringify(chat));
}

function addMessage(chat: ChatHistory, message: ChatEntry): ChatHistory {
  chat.push(message);
  return chat;
}
const userIsAuthor: string = " ";
const similarQuestionLabel : string = "similar-question"

function displayMessage(message: ChatEntry): HTMLElement {
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

function deleteChildren(container: HTMLElement) {
  for (let i = container.children.length; i > 0; i--) {
    container.removeChild(container.children[0]);
  }
}
function addChildren(container: HTMLElement, children: HTMLElement[]) {
  children.forEach((child) => container.appendChild(child));
}
function displayChat(chat: ChatHistory, container: HTMLElement): void {
  const chatElementsHtml = chat.map((value: ChatEntry) => {
    return displayMessage(value);
  });
  deleteChildren(container);
  addChildren(container, chatElementsHtml);
}

function getUpdatesForMessages(container: HTMLElement) {
  function onSuccess(response: Response): void {
    response.text().then((value: string) => {
      const data: string[] = JSON.parse(value);
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

      // appendAnswer(container, value);
    });
  }
  core.basicFetch({
    url: "/messages",
    onSuccess: onSuccess,
    onError: requestFailure,
    request: core.defaultRequest,
  });
}

function setup(): void {
  const form = <HTMLElement | null>document.querySelector("#ask_question_form");
  if (form == null) {
    alert("form not found");
    return;
  }
  const button = <HTMLElement>form.querySelector("button[value=submit]");
  button.onclick = () => submitForm(form, container);
  // button.onclick = () => sendJson(JSON.stringify({ abba: "hah" }));
  const refreshButton = <HTMLButtonElement>(
    form.querySelector("button[value=refresh]")
  );
  let container = <HTMLElement>document.querySelector("div#message-history");
  document.body.appendChild(container);
  refreshButton.onclick = () => getUpdatesForMessages(container);
}

setup();
