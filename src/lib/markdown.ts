import { createMarkdownProcessor } from '@astrojs/markdown-remark';

let processor: Awaited<ReturnType<typeof createMarkdownProcessor>> | undefined;

function slugifyPath(path: string) {
  return path
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

export function rewriteCodeLinks(markdown: string, anchorPrefix?: string) {
  if (!anchorPrefix) return markdown;
  return markdown.replace(/\]\((?:\.\/)?codigo\/aula-\d+\/([^\s)]+)\)/gi, (_match, path) => {
    return `](#${anchorPrefix}-arquivo-${slugifyPath(path)})`;
  });
}

export async function renderMarkdown(markdown: string, anchorPrefix?: string) {
  processor ??= await createMarkdownProcessor({ gfm: true, smartypants: false, syntaxHighlight: false });
  const result = await processor.render(rewriteCodeLinks(markdown, anchorPrefix));
  return result.code;
}

export function markdownToPlainText(markdown: string) {
  let text = markdown.replace(/\r\n?/g, '\n');
  text = text.replace(/```[^\n]*\n([\s\S]*?)```/g, (_match, code) => code.trimEnd());
  text = text.replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1');
  text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '$1');
  text = text.replace(/^\s{0,3}#{1,6}\s+/gm, '');
  text = text.replace(/^\s*[-*+]\s+/gm, '- ');
  text = text.replace(/^\s*(\d+)\.\s+/gm, '$1. ');
  text = text.replace(/^\s*>\s?/gm, '');
  text = text.replace(/(`+)([^`]+)\1/g, '$2');
  text = text.replace(/(\*\*|__)(.*?)\1/g, '$2');
  text = text.replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '$1');
  text = text.replace(/(?<!_)_([^_]+)_(?!_)/g, '$1');
  text = text.replace(/^\s*[-*_]{3,}\s*$/gm, '');
  return text.replace(/\n{3,}/g, '\n\n').trim();
}
