"use client";

import UploadZone
from "@/components/UploadZone";

import DocumentStatusBadge
from "@/components/DocumentStatusBadge";

export default function DocumentsPage() {

  const documents = [

    {

      filename:
        "paper.pdf",

      type:
        "pdf",

      status:
        "completed",

      chunks:
        42,

      created:
        "2026-06-04"
    },

    {

      filename:
        "report.docx",

      type:
        "docx",

      status:
        "processing",

      chunks:
        0,

      created:
        "2026-06-04"
    }
  ];

  return (

    <div className="p-6">

      <h1
        className="
        text-3xl
        mb-4"
      >

        Documents

      </h1>

      <UploadZone />

      <table
        className="
        mt-6
        w-full
        border"
      >

        <thead>

          <tr>

            <th>
              Filename
            </th>

            <th>
              Type
            </th>

            <th>
              Status
            </th>

            <th>
              Chunks
            </th>

            <th>
              Created
            </th>

          </tr>

        </thead>

        <tbody>

          {documents.map(

            (d, i) => (

              <tr
                key={i}
              >

                <td>
                  {d.filename}
                </td>

                <td>
                  {d.type}
                </td>

                <td>

                  <DocumentStatusBadge

                    status={
                      d.status
                    }
                  />

                </td>

                <td>
                  {d.chunks}
                </td>

                <td>
                  {d.created}
                </td>

              </tr>
            )
          )}

        </tbody>

      </table>

    </div>
  );
}