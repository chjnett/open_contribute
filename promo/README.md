# Promo kit

Draft copy and assets for publicizing `open_contribute`. These are **untracked drafts**
— use them, then delete or commit as you like. They are not part of the product.

| File | What it is | Where to post |
| :--- | :--- | :--- |
| `show-hn-post.md` | Show HN title + top comment | https://news.ycombinator.com (Submit → "Show HN") |
| `blog-post.md` | ~1,100-word long-form article | dev.to / personal blog / GeekNews-en |
| `directory-submissions.md` | skills.sh + awesome-list copy, PR template, order of operations | skills.sh, GitHub awesome lists |
| `community-posts.md` | Reddit, GeekNews(한국어), 디스콰이엇 drafts | reddit.com/r/ClaudeAI, news.hada.io, disquiet.io |
| `social-preview.png` | 1280×640 OG image | GitHub repo Settings → General → Social preview; dev.to cover; HN/Twitter og:image |
| `make_og_image.py` | Regenerates `social-preview.png` | — |

## Suggested order

1. Upload `social-preview.png` as the GitHub **Social preview** image
   (repo → Settings → General → Social preview → Edit).
2. Post **Show HN** (`show-hn-post.md`).
3. Same day, publish **dev.to** article (`blog-post.md`).
4. Within the week: submit to **skills.sh** + open **awesome-list PRs**
   (`directory-submissions.md`).
5. Post **community threads** (`community-posts.md`), linking the blog (not the repo)
   to avoid link-spam flags.

> Social preview image and demo GIF are the two things that can only be set from the
> GitHub **web UI** (no API), so I generated the image but you'll upload it yourself.
