import { useState } from "react";

export default function ImageForm() {
  const [filebase64, setFileBase64] = useState<string>("");
  const [baseurl, setBaseURL] = useState<string>("");
  const [disabler, setDisable] = useState<boolean>(false);

  function formSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.toString();
    console.log({ filebase64 });
    console.log({ baseurl });
    alert("file submitted");
  }

  function convertFile(files: FileList | null) {
    if (files) {
      const fileRef = files[0] || "";
      const fileType: string = fileRef.type || "";
      console.log("File type:", fileType);
      console.log("File content:", fileRef.arrayBuffer);
      const reader = new FileReader();
      reader.readAsArrayBuffer(fileRef);
      reader.onload = (ev: ProgressEvent<FileReader>) => {
        const result = ev.target?.result as ArrayBuffer;
        setFileBase64(
          `data:${fileType};base64,${btoa(String.fromCharCode(...new Uint8Array(result)))}`
        );
      };
    }
  }

  function extractURL(e: string) {
    setBaseURL(e);
  }

  function submit() {
    void setDisable(true);
  }

  return (
    <form encType="multipart/form-data" onSubmit={formSubmit}>
      <input
        type="file"
        disabled={disabler}
        onChange={(e) => convertFile(e.target.files)}
      />
      <input
        type="url"
        disabled={disabler}
        onChange={(e) => {
          extractURL(e.target.value);
        }}
      />
      <hr />
      {filebase64 && (
        <>
          <p>
            Here is your image
            <br />
          </p>
          {/*filebase64.indexOf("image/") > -1 && (
            <img src={filebase64} width={300} />
          )*/}
          <hr />
          <button type="submit" onClick={submit}>
            {" "}
            Submit and check the console
          </button>
        </>
      )}
    </form>
  );
}
