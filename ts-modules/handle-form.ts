import * as core from "./core.js";

function form2text(form: HTMLElement): string {
  const el = form.querySelector("#question_text") as HTMLInputElement;
  return core.html2text(el);
}

function submitForm(form: HTMLElement): void {
  const value: string = form2text(form);
  console.log(value);
  sendMessage({
    text: value,
    user_id: 1337,
  });
}

function sendMessage(msg: core.MessageRequestBody) {
  const parameters: core.FetchParameters = {
    url: "/messages",
    onSuccess: function (value: Response): void {
      // throw new Error("Function not implemented.");
      console.log(value.ok);
    },
    onError: function (arg0: any): void {
      throw new Error("Function not implemented.");
    },
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

function getUpdatesForMessages(container: HTMLElement) {
  function onSuccess(response: Response): void {
    response.text().then((value: string) => {
      appendAnswer(container, value);
    });
  }
  core.basicFetch({
    url: "/messages",
    onSuccess: onSuccess,
    onError: function (arg0: any): void {
      console.log("Error while request fetching");
      console.log(arg0);
    },
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
  button.onclick = () => submitForm(form);
  // button.onclick = () => sendJson(JSON.stringify({ abba: "hah" }));
  const refreshButton = <HTMLButtonElement>(
    form.querySelector("button[value=refresh")
  );
  let container = <HTMLElement>document.querySelector("div#message-history");
  document.body.appendChild(container);
  refreshButton.onclick = () => getUpdatesForMessages(container);
}

setup();
