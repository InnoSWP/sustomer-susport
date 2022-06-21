import * as core from "./core.js";

function requestFailure(error: any): void {
  console.log("Error during request performing");
  console.log(error);
}
function form2text(form: HTMLElement): string {
  const el = form.querySelector("#question_text") as HTMLInputElement;
  return core.html2text(el);
}

function submitForm(form: HTMLElement, container: HTMLElement): void {
  const value: string = form2text(form);
  console.log(value);
  sendMessage({
    text: value,
    user_id: 1337,
  });
  const history = getLocalChat();
  const newHistory = addMessage(history, {
    author: userIsAuthor,
    text: value,
  });
  displayChat(newHistory, container);
  storeChat(newHistory);
}

function sendMessage(msg: core.MessageRequestBody) {
  const parameters: core.FetchParameters = {
    url: "/messages",
    onSuccess: function (value: Response): void {
      // throw new Error("Function not implemented.");
      console.log(value.ok);
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

function displayMessage(message: ChatEntry): HTMLElement {
  const messageContainer = document.createElement("div");
  if (message.author == userIsAuthor) {
    messageContainer.setAttribute("class", "user-message");
  } else {
    messageContainer.setAttribute("class", "others-message");
  }
  messageContainer.textContent = message.text;
  return messageContainer;
}

function deleteChildren(container: HTMLElement) {
  for (let i = container.children.length; i > 0 ; i--) {
    container.removeChild(container.children[0]);
  }
}
function addChildren(container: HTMLElement, children: HTMLElement[]) {
  children.map((child) => container.appendChild(child));
}
function displayChat(chat: ChatHistory, container: HTMLElement): void {
  const chatElementsHtml = chat.map((value: ChatEntry) => {
    return displayMessage(value);
  });
	console.log(container.children.length)
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
    form.querySelector("button[value=refresh")
  );
  let container = <HTMLElement>document.querySelector("div#message-history");
  document.body.appendChild(container);
  refreshButton.onclick = () => getUpdatesForMessages(container);
}

setup();
