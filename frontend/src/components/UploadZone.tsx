"use client";

import { useState } from "react";

export default function UploadZone() {

  const [

    uploading,

    setUploading

  ] = useState(false);

  async function upload(

    files: FileList | null

  ) {

    if (!files) return;

    setUploading(true);

    const formData =
      new FormData();

    Array.from(files)
      .forEach(

        (file) => {

          formData.append(
            "files",
            file
          );
        }
      );

    await fetch(

      "http://127.0.0.1:8000/ingest",

      {

        method: "POST",

        body: formData
      }
    );

    setUploading(false);
  }

  return (

 <div

  className="
  border-2
  border-dashed
  rounded
  p-10
  text-center"
 >

  <h3>

   Drag files here

  </h3>

  <input

   type="file"

   multiple

   onChange={(e) =>
    upload(
     e.target.files
    )
   }
  />

  {
   uploading && (

    <div>

     Uploading...

    </div>
   )
  }

 </div>
  );
}
