import { useState } from "react";

import { API_BASE_URL } from "@/api_url.ts";

export default function ImageForm() {
  const [file, setFile] = useState<string>("");
  const [disabler, setDisable] = useState<boolean>(false);
  const [error, setError] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [desc, setDesc] = useState<string>("");

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");

    try {
      const formdata = new FormData();
      formdata.append("logo", file);
      formdata.append("name", name);
      formdata.append("description", desc);
      console.table(formdata);

      const response = await fetch(`${API_BASE_URL}/api/projects/${2}`, {
        method: "POST",
        body: formdata,
      });

      if (!response.ok) {
        throw new Error("Invalid credentials");
      }

      const data = await response.json();

      localStorage.setItem("token", data.token);
    } catch (err) {
      setError(err?.message);
    }
  };

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
        setFile(
          `data:${fileType};base64,${btoa(String.fromCharCode(...new Uint8Array(result)))}`
        );
      };
    }
  }

  function submit() {
    void setDisable(true);
  }

  return (
    <form encType="multipart/form-data" onSubmit={handleSubmit}>
      <div className="project-register">
        <label htmlFor="Picture as File">Picture as File</label>
        <input
          name="Picture as File"
          type="file"
          disabled={disabler}
          onChange={(e) => convertFile(e.target.files)}
        />
      </div>
      <div className="project-register">
        <label htmlFor="Picture as Link">Picture as Link</label>
        <input
          name="Picture as Link"
          type="url"
          disabled={disabler}
          onChange={(e) => setFile(e.target.value)}
        />
      </div>
      <div className="project-register">
        <label htmlFor="Name">Name</label>
        <input
          name="Name"
          type="text"
          disabled={disabler}
          onChange={(e) => setName(e.target.value)}
        />
      </div>
      <div className="project-register">
        <label htmlFor="Description">Description</label>
        <input
          name="Description"
          type="text"
          disabled={disabler}
          onChange={(e) => setDesc(e.target.value)}
        />
      </div>
      <hr />
      {file && (
        <>
          <p>
            Here is your image
            <br />
          </p>
          {/*filebase64.indexOf("image/") > -1 && (
            <img src={filebase64} width={300} />
          )*/}
          <hr />
          {error && <p className="error">{error}</p>}
          <button type="submit" onClick={submit}>
            {" "}
            Submit and check the console
          </button>
        </>
      )}
    </form>
  );
}
