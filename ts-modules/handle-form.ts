function html2text(htmlElement: HTMLInputElement | null): string {
  // if (htmlElement == null || htmlElement.textContent == undefined)
  if (htmlElement == null) {
    return "";
  }
  return htmlElement.value;
}

function form2text(form: HTMLElement): string {
  const el = form.querySelector("#question_text") as HTMLInputElement;
  return html2text(el);
}

function submitForm(form: HTMLElement): void {
  const value: string = form2text(form);
  console.log(value);
  sendMessage({
    text: value,
    user_id: 1337,
  });
}

interface messageRequestBody {
  text: string;
  user_id: number;
}

function sendData(data: string) {
  const request: RequestInit = {
    method: "POST",
    headers: { "content-type": "application/json;charset=UTF-8" },
    body: data,
  };

  const promise = window.fetch("/messages", request);
  promise.then((value: Response) => {
    console.log(value.ok);
  });
  promise.catch((error) => console.log(error));
}

function sendMessage(msg: messageRequestBody) {
  sendData(JSON.stringify(msg));
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
}

setup();
