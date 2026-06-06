"use client";

type Props = {

  citation: any;

  onClose: () => void;
};

export default function CitationDrawer({

  citation,

  onClose

}: Props) {

  if (!citation)
    return null;

  return (

    <div

      className="
      fixed
      top-0
      right-0
      h-full
      w-96
      bg-white
      border-l
      shadow-lg
      p-4
      overflow-auto"
    >

      <button
        onClick={onClose}
      >
        Close
      </button>

      <h2>
        Citation
      </h2>

      <p>
        <strong>
          Document:
        </strong>

        {" "}

        {
          citation.document_name
        }
      </p>

      <p>
        <strong>
          Page:
        </strong>

        {" "}

        {
          citation.page_number
        }
      </p>

      <hr />

      <pre>

        {
          citation.content_preview
        }

      </pre>

    </div>
  );
}