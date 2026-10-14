# Aatlas Replay — site

Página única, sem dependências de build.

- `index.html` — o site completo (HTML + CSS + JS inline; personagens e ilustrações de produto em SVG embutidos, estáticos, com zoom ao passar o mouse; fontes Geist, Geist Mono e Instrument Serif via Google Fonts).
- `design-system.md` — manual visual do site (cores, tipografia, botões, cards, SVGs, personagens). Ao mudar o visual, atualize junto.
- Ícones: [Lucide](https://lucide.dev) 1.55.0 (licença ISC) nos cartões, botões e na seta "clique no vídeo" (`corner-right-down`); [Tabler](https://tabler.io/icons) (MIT) nos números dos passos; [Simple Icons](https://simpleicons.org) 16.34.0 (CC0) no botão de WhatsApp. Faixa de esportes: Material Design Icons (Apache 2.0: `mdi:volleyball`, `mdi:soccer`, `mdi:soccer-field`, `mdi:skateboarding`), Material Symbols (Apache 2.0: `pickleball` no beach tennis, `padel`), Maki (CC0: `soccer` no futsal) e IconOven (MIT: `martial-arts`). Ficam embutidos no HTML, porque a CSP não libera CDN; para trocar um, copie o SVG do site da biblioteca.
- `assets/aatlas-replay.mp4` — vídeo narrado com música (37 s). Não toca sozinho: começa com som quando a pessoa clica.
- `assets/poster.jpg` — capa do vídeo.
- `assets/p-*.webp` — personagens e o celular do story (fundo transparente). Os originais ficam em `personagens/` (não vai para o Vercel); para refazer os recortes: `python personagens/recortar.py .` (precisa de `pip install pillow numpy`). Os recortes de cada imagem estão no começo do script.
- `chars.py` (opcional) — gera os personagens desenhados (`python3 chars.py chars.json`) caso queira ajustar poses ou criar novos.

## Publicação
Domínio oficial: https://www.aatlascompany.com.br/replay/ (Hostinger). Cópia de teste no Vercel: https://aatlas-replay-quadras.vercel.app. Para montar a `dist`, no PowerShell:

```
Copy-Item *.html,paginas.css,vercel.json,.htaccess,favicon.png dist -Force; Copy-Item assets dist -Recurse -Force
```

- `404.html`: página de endereço inexistente. Usa `<base href="/replay/">` e o `.htaccess` aponta `ErrorDocument 404 /replay/404.html`; se a pasta mudar, mude os dois.
- Hostinger: envie o conteúdo da `dist` (menos a pasta `.vercel`) para `public_html/replay/`. O `.htaccess` faz o papel do `vercel.json`.
- Vercel: `npx vercel deploy dist --prod`.

- WhatsApp: `const WHATSAPP` no fim do `index.html` e o `href` dos botões `.cta-link` (DDI+DDD+número).
- `vercel.json`: cabeçalhos de segurança (CSP etc.) e cache dos `assets/` (7 dias — ao trocar um arquivo, mude o nome dele). Ao adicionar script/fonte/pixel de terceiros, libere o domínio na CSP.
- Tema: claro fixo (off-white), pensado para um público pouco digital. Não há modo escuro de propósito.

## Para evoluir no Claude Code
- Separar CSS/JS em arquivos, adicionar formulário real de contato (WhatsApp/CRM), domínio e analytics (Meta Pixel / GA4).
- Trocar as telas ilustrativas por fotos/vídeos reais da primeira arena instalada.
