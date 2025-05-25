const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = 3001;

const fileMap = {
  log: 'X:/Dev/Watch/Relay/relay.log',
  results: 'X:/Dev/SphereX/output/results.json',
  core: 'X:/Dev/SphereX/output/core_src_lib.rs',
  parse: 'X:/Dev/SphereX/output/parse_pdf.rs'
};

app.get('/api/file/:type', (req, res) => {
  const filePath = fileMap[req.params.type];
  if (!filePath) return res.status(404).send('Unknown file type');
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) return res.status(500).send('Failed to read file');
    res.send(data);
  });
});

app.listen(PORT, () => {
  console.log(`Relay UI server running at http://localhost:${PORT}`);
});