#!/bin/bash

# Converts all .md files in outputs/soap_notes/ to .pdf using pandoc

echo "📄 Converting Markdown files to PDF..."
for file in outputs/soap_notes/*.md; do
  pdf="${file%.md}.pdf"
  pandoc "$file" -o "$pdf"
  echo "✅ Created: $pdf"
done
echo "✅ All Markdown files have been converted to PDF."