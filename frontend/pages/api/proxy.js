// frontend/pages/api/proxy.js
import formidable from 'formidable';
import fs from 'fs';
import path from 'path';

export const config = {
  api: {
    bodyParser: false, // Important: we're parsing the form manually
  },
};

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).send('Method not allowed');
  }

  const form = formidable({ multiples: false });

  form.parse(req, async (err, fields, files) => {
    if (err) {
      console.error('Upload error:', err);
      return res.status(500).json({ error: 'Failed to parse upload' });
    }

    const file = files.file;
    if (!file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    try {
      // Forward the PDF to your backend service (replace port as needed)
      const backendRes = await fetch('http://orchestrator:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/pdf',
        },
        body: fs.createReadStream(file.filepath),
      });

      const data = await backendRes.json();
      res.status(200).json(data);
    } catch (e) {
      console.error('Failed to contact backend:', e);
      res.status(500).json({ error: 'Failed to contact backend' });
    }
  });
}

  