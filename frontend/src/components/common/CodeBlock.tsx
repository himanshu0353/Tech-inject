import React from 'react';
import { CopyButton } from './CopyButton';
import './CodeBlock.css';

export interface CodeBlockProps {
  code: string;
  filename?: string;
  language?: string;
}

export const CodeBlock: React.FC<CodeBlockProps> = ({ code, filename, language = 'tsx' }) => {
  return (
    <div className="tech-codeblock">
      <div className="tech-codeblock__header">
        <div className="tech-codeblock__title">
          <span className="tech-codeblock__dot" />
          <span className="tech-codeblock__filename">{filename || language}</span>
        </div>
        <CopyButton textToCopy={code} label="Copy Code" />
      </div>
      <pre className="tech-codeblock__content">
        <code>{code}</code>
      </pre>
    </div>
  );
};
