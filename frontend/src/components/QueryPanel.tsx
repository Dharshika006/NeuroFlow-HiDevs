"use client";

import { useState } from "react";

type Props = {

  onSubmit: (
    query: string
  ) => void;
};

export default function QueryPanel({

  onSubmit

}: Props) {

  const [

    query,

    setQuery

  ] = useState("");

  return (

    <div>

      <textarea

        rows={5}

        value={query}

        onChange={(e) =>
          setQuery(
            e.target.value
          )
        }

        className="
        border
        p-2
        w-full"
      />

      <p>

        {
          query.length
        }
        {" "}
        characters

      </p>

      <button

        onClick={() =>
          onSubmit(query)
        }

        className="
        border
        px-4
        py-2"
      >

        Submit

      </button>

    </div>
  );
}