import * as core from "./core.js";

function requestFailure(error: any): void {
  console.log("Error during request performing");
  console.log(error);
}
function form2text(form: HTMLElement): string {
  const el = form.querySelector("#question_text") as HTMLInputElement | null;
  if (el == null) {
    return "";
  }
  return core.html2text(el);
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
  return container;
}

function addChildren(container: HTMLElement, children: HTMLElement[]) {
  children.forEach((child) => container.appendChild(child));
  return container;
}
function displayChat(chat: ChatHistory, container: HTMLElement): HTMLElement {
  const chatElementsHtml = chat.map((value: ChatEntry) => {
    return displayMessage(value);
  });
  deleteChildren(container);
  addChildren(container, chatElementsHtml);
  return container;
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
  addMessage,
  displayMessage,
  similarQuestionLabel,
  userIsAuthor,
};
