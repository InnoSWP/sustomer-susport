import * as core from "./core.js";

function requestFailure(error: any): void {
  console.log("Error during request performing");
  console.log(error);
}
function form2text(form: HTMLElement): string {
  const el = form.querySelector("#question_text") as HTMLInputElement;
  return core.html2text(el);
}

function sendMessage(
  msg: core.MessageRequestBody,
  handleSimilarQuestions: (text: string) => void
) {
  const parameters: core.FetchParameters = {
    url: "/messages",
    onSuccess: function (value: Response): void {
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

function addMessage(chat: ChatHistory, message: ChatEntry): ChatHistory {
  chat.push(message);
  return chat;
}
const userIsAuthor: string = " ";
const similarQuestionLabel: string = "similar-question";

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

// for test purposes
export {
  deleteChildren,
  addChildren,
  ChatHistory,
  ChatEntry,
  displayChat,
  requestFailure,
  form2text,
  sendMessage,
  addMessage,
  similarQuestionLabel,
	userIsAuthor,
};
