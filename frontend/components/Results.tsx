
import React from "react";

interface Props {
  data: {
    summary: string;
    sections: { [key: string]: string };
  };
}

const Results: React.FC<Props> = ({ data }) => {
  return (
    <div className="mt-6">
      <h2 className="text-xl font-semibold mb-2">Summary</h2>
      <p className="mb-4">{data.summary}</p>

      <h2 className="text-xl font-semibold mb-2">Sections</h2>
      {Object.entries(data.sections).map(([title, content]) => (
        <div key={title} className="mb-4">
          <h3 className="font-bold">{title}</h3>
          <p className="text-sm text-gray-700">{content}</p>
        </div>
      ))}
    </div>
  );
};

export default Results;
