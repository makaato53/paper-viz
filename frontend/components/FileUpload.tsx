import React, { useCallback, useState } from "react";

interface Props {
  onFileSelect: (file: File) => void;
}

const FileUpload: React.FC<Props> = ({ onFileSelect }) => {
  const [dragging, setDragging] = useState(false);

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  }, [onFileSelect]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onFileSelect(e.target.files[0]);
    }
  };

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      className={`border-2 border-dashed p-4 rounded text-center transition-all ${
        dragging ? "border-blue-500 bg-blue-50" : "border-gray-400"
      }`}
    >
      <p className="text-sm mb-2">Drag & drop your PDF here or click to upload</p>
      <input
        type="file"
        accept=".pdf"
        onChange={handleChange}
        className="mx-auto block"
      />
    </div>
  );
};

export default FileUpload;

