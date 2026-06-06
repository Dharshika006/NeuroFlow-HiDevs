"use client";

export default function DocumentStatusBadge({

  status

}: {

  status: string;

}) {

  const colors: any = {

    processing:
      "bg-blue-500",

    completed:
      "bg-green-500",

    failed:
      "bg-red-500"
  };

  return (

    <span

      className={`
      inline-flex
      items-center
      gap-2
      px-2
      py-1
      rounded
      text-white
      ${colors[status]}
      `}
    >

      {

        status ===
          "processing" && (

          <span
            className="
            animate-pulse"
          >

            ●

          </span>
        )
      }

      {status}

    </span>
  );
}