#!/usr/bin/env python3
"""
Scrape locally saved HTML pages of the Gearspace "Lexicon Reverbs: A Brief Bestiary"
thread and convert to markdown.

Usage:
    pip install beautifulsoup4

    1. In your browser, open each page of the thread and save as "Webpage, HTML Only"
       (not "Complete" -- you only need the .html file, not the folder of assets).

       Name the files:
           page01.html   <-- https://gearspace.com/board/high-end/362930-lexicon-reverbs-brief-bestiary.html
           page02.html   <-- https://gearspace.com/board/high-end/362930-lexicon-reverbs-brief-bestiary-2.html
           ...
           page14.html

    2. Put all .html files in the same directory as this script (or pass --dir).

    3. Run:
           python3 scrape_lexicon_bestiary_local.py
           python3 scrape_lexicon_bestiary_local.py --dir C:\\path\\to\\pages
           python3 scrape_lexicon_bestiary_local.py --single
           python3 scrape_lexicon_bestiary_local.py --start 3 --end 7

Output: lexicon-bestiary-pages-NN-NN.md  (chunked, 5 pages per file)
        lexicon-bestiary-full.md          (with --single)
"""

import sys
import os
import re
from bs4 import BeautifulSoup

TOTAL_PAGES = 14
CHUNK_SIZE = 5


# ---------------------------------------------------------------------------
# File loading
# ---------------------------------------------------------------------------

def get_html_path(page_num, html_dir):
    """Return the path to the saved HTML file for a given page number."""
    filename = f"page{page_num:02d}.html"
    return os.path.join(html_dir, filename)


def load_page(page_num, html_dir):
    """Load a saved HTML file and return a BeautifulSoup object."""
    path = get_html_path(page_num, html_dir)
    if not os.path.exists(path):
        raise FileNotFoundError(f"HTML file not found: {path}")
    print(f"  Loading {path}")
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return BeautifulSoup(f.read(), 'html.parser')


# ---------------------------------------------------------------------------
# Post extraction  (identical logic to the live scraper)
# ---------------------------------------------------------------------------

def extract_posts(soup, page_num):
    """Extract all posts from a parsed page."""
    posts = []

    posts_area = soup.find('div', id='posts') or soup.find('ol', id='posts')

    if posts_area:
        post_containers = posts_area.find_all(['li', 'div', 'table'], recursive=False)
    else:
        post_containers = soup.find_all(
            lambda tag: tag.get('id', '').startswith('post_') and
                        not tag.get('id', '').startswith('post_message_')
        )

    for container in post_containers:
        post = extract_single_post(container, page_num)
        if post:
            posts.append(post)

    if not posts:
        posts = extract_posts_fallback(soup, page_num)

    return posts


def extract_single_post(container, page_num):
    """Extract data from a single post container element."""
    post = {}

    post_link = container.find('a', href=re.compile(r'postcount=(\d+)'))
    if post_link:
        match = re.search(r'postcount=(\d+)', post_link['href'])
        if match:
            post['num'] = int(match.group(1))
    else:
        return None

    post['page'] = page_num

    post_id_match = re.search(r'p=(\d+)', post_link.get('href', ''))
    post['link'] = post_link['href'] if post_link else ''
    if post_id_match:
        post['link'] = (
            f"https://gearspace.com/board/showpost.php"
            f"?p={post_id_match.group(1)}&postcount={post['num']}"
        )

    username_elem = (
        container.find('a', class_='bigusername') or
        container.find('a', href=re.compile(r'member\.php'))
    )
    if username_elem:
        post['username'] = username_elem.get_text(strip=True)
    else:
        user_info = container.find('div', class_=re.compile(r'user'))
        post['username'] = user_info.get_text(strip=True)[:50] if user_info else 'Unknown'

    user_title = (
        container.find('div', class_='usertitle') or
        container.find('span', class_='usertitle')
    )
    post['role'] = user_title.get_text(strip=True) if user_title else ''

    date_elem = (
        container.find('td', class_='thead') or
        container.find('span', class_='date') or
        container.find('div', class_='postdate')
    )
    if date_elem:
        date_text = date_elem.get_text(strip=True)
        date_text = re.sub(r'#\d+', '', date_text).strip()
        date_text = re.sub(r'\s+', ' ', date_text)
        post['date'] = date_text
    else:
        post['date'] = 'Unknown'

    join_info = container.find(string=re.compile(r'Joined:'))
    post['joined'] = ''
    if join_info and join_info.parent:
        post['joined'] = join_info.parent.get_text(strip=True)

    posts_info = container.find(string=re.compile(r'Posts:'))
    post['posts_count'] = ''
    if posts_info and posts_info.parent:
        post['posts_count'] = posts_info.parent.get_text(strip=True)

    msg_div = container.find('div', id=re.compile(r'^post_message_'))
    if msg_div:
        post['content'] = html_to_markdown(msg_div)
    else:
        content_area = container.find('div', class_=re.compile(r'content|message'))
        post['content'] = html_to_markdown(content_area) if content_area else ''

    return post if post.get('content') else None


def extract_posts_fallback(soup, page_num):
    """Fallback: find posts by post_message_ divs and walk up to parent."""
    posts = []

    msg_divs = soup.find_all('div', id=re.compile(r'^post_message_'))

    for msg_div in msg_divs:
        post_id_match = re.search(r'post_message_(\d+)', msg_div.get('id', ''))
        if not post_id_match:
            continue

        post_id = post_id_match.group(1)
        post = {'page': page_num}

        count_link = soup.find('a', href=re.compile(f'p={post_id}&postcount='))
        if count_link:
            count_match = re.search(r'postcount=(\d+)', count_link['href'])
            post['num'] = int(count_match.group(1)) if count_match else 0
        else:
            count_link = soup.find('a', id=f'postcount{post_id}')
            if count_link:
                try:
                    post['num'] = int(count_link.get_text(strip=True))
                except ValueError:
                    continue
            else:
                continue

        post['link'] = (
            f"https://gearspace.com/board/showpost.php"
            f"?p={post_id}&postcount={post['num']}"
        )

        parent = msg_div
        for _ in range(10):
            parent = parent.parent
            if parent is None:
                break
            if parent.get('id', '').startswith('post_'):
                break

        if parent:
            user_link = parent.find('a', class_='bigusername')
            if not user_link:
                user_link = parent.find('a', href=re.compile(r'member\.php\?u='))
            post['username'] = user_link.get_text(strip=True) if user_link else 'Unknown'

            user_title = parent.find('div', class_='usertitle')
            post['role'] = user_title.get_text(strip=True) if user_title else ''

            date_cell = parent.find('td', class_='thead')
            if date_cell:
                date_text = date_cell.get_text(strip=True)
                date_text = re.sub(r'#\d+.*$', '', date_text).strip()
                post['date'] = date_text
            else:
                post['date'] = 'Unknown'

            join_elem = parent.find(string=re.compile(r'Joined:'))
            post['joined'] = (
                join_elem.parent.get_text(strip=True)
                if join_elem and join_elem.parent else ''
            )

            posts_elem = parent.find(string=re.compile(r'Posts:\s*[\d,]+'))
            post['posts_count'] = (
                posts_elem.parent.get_text(strip=True)
                if posts_elem and posts_elem.parent else ''
            )
        else:
            post['username'] = 'Unknown'
            post['role'] = ''
            post['date'] = 'Unknown'
            post['joined'] = ''
            post['posts_count'] = ''

        post['content'] = html_to_markdown(msg_div)
        posts.append(post)

    posts.sort(key=lambda p: p.get('num', 0))
    return posts


# ---------------------------------------------------------------------------
# HTML → Markdown converter
# ---------------------------------------------------------------------------

def html_to_markdown(elem):
    """Recursively convert an HTML element tree to clean markdown text."""
    if elem is None:
        return ''

    result = []

    for child in elem.children:
        if isinstance(child, str):
            text = child
            if text.strip():
                result.append(text)
            elif result and result[-1] != '\n':
                result.append(' ')
            continue

        tag = child.name if hasattr(child, 'name') else None
        if tag is None:
            continue

        if tag == 'br':
            result.append('\n')

        elif tag in ('b', 'strong'):
            text = child.get_text()
            result.append(f'**{text}**')

        elif tag in ('i', 'em'):
            text = child.get_text()
            result.append(f'*{text}*')

        elif tag == 'a':
            href = child.get('href', '')
            text = child.get_text(strip=True)
            if href and text:
                if href.startswith('/'):
                    href = f'https://gearspace.com{href}'
                result.append(f'[{text}]({href})')
            elif text:
                result.append(text)

        elif tag == 'img':
            src = child.get('src', '')
            alt = child.get('alt', '')
            title = child.get('title', '')
            if 'smilies' in src or 'smiley' in (alt + title).lower():
                continue
            if src:
                if src.startswith('/'):
                    src = f'https://gearspace.com{src}'
                result.append(f'![{alt or title}]({src})')

        elif tag == 'div':
            classes = ' '.join(child.get('class', []))
            if 'quote' in classes or 'bbcode_container' in classes:
                quote_header = child.find('div', class_=re.compile(r'quote_container|bbcode_postedby'))
                if quote_header:
                    header_text = quote_header.get_text(strip=True)
                    body = child.find('div', class_=re.compile(r'message|quote_container'))
                    quote_text = body.get_text(strip=True) if body else child.get_text(strip=True)
                    result.append(f'\n> {header_text}\n')
                    for line in quote_text.split('\n'):
                        line = line.strip()
                        if line:
                            result.append(f'> {line}\n')
                else:
                    quote_text = child.get_text(strip=True)
                    for line in quote_text.split('\n'):
                        line = line.strip()
                        if line:
                            result.append(f'> {line}\n')
                result.append('\n')
            else:
                result.append(html_to_markdown(child))

        elif tag in ('table', 'td', 'tr'):
            result.append(html_to_markdown(child))

        elif tag in ('p', 'blockquote'):
            text = html_to_markdown(child)
            if text.strip():
                result.append(f'\n{text}\n')

        elif tag in ('pre', 'code'):
            text = child.get_text()
            result.append(f'\n```\n{text}\n```\n')

        elif tag in ('ul', 'ol'):
            for li in child.find_all('li'):
                text = li.get_text(strip=True)
                result.append(f'- {text}\n')

        elif tag == 'hr':
            result.append('\n---\n')

        else:
            result.append(html_to_markdown(child))

    text = ''.join(result)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    return text.strip()


# ---------------------------------------------------------------------------
# Markdown formatting
# ---------------------------------------------------------------------------

def post_to_markdown(post):
    lines = []
    lines.append('---\n')
    lines.append(f"### Post #{post['num']} -- Page {post['page']}")
    lines.append(f"**User:** {post['username']}")

    meta = []
    if post.get('role'):
        meta.append(post['role'])
    if post.get('joined'):
        meta.append(post['joined'])
    if post.get('posts_count'):
        meta.append(post['posts_count'])
    if meta:
        lines.append(f"**Info:** {' | '.join(meta)}")

    lines.append(f"**Date:** {post['date']}")
    lines.append(f"**Link:** <{post['link']}>")
    lines.append('')
    lines.append(post['content'])
    lines.append('')

    return '\n'.join(lines)


def write_header():
    return (
        "# Lexicon Reverbs: A Brief Bestiary -- Gearspace High End Thread\n\n"
        "**Thread URL:** https://gearspace.com/board/high-end/362930-lexicon-reverbs-brief-bestiary.html\n"
        "**Forum:** High End @ Gearspace\n"
        "**Total Pages:** 14\n\n"
        "A technical thread covering the Lexicon reverb hardware family: architecture,\n"
        "algorithms, and the lineage from early ARU-based units through the 480L and beyond.\n\n"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    start_page = 1
    end_page = TOTAL_PAGES
    output_mode = 'chunked'
    html_dir = '.'

    if '--single' in sys.argv:
        output_mode = 'single'
    if '--start' in sys.argv:
        idx = sys.argv.index('--start')
        start_page = int(sys.argv[idx + 1])
    if '--end' in sys.argv:
        idx = sys.argv.index('--end')
        end_page = int(sys.argv[idx + 1])
    if '--dir' in sys.argv:
        idx = sys.argv.index('--dir')
        html_dir = sys.argv[idx + 1]

    print(f"Reading local HTML files from: {os.path.abspath(html_dir)}")
    print(f"Pages: {start_page}–{end_page}  |  Output: {output_mode}")
    print()

    # Warn about missing files before we start
    missing = []
    for n in range(start_page, end_page + 1):
        p = get_html_path(n, html_dir)
        if not os.path.exists(p):
            missing.append(p)
    if missing:
        print("WARNING: the following expected files are missing:")
        for m in missing:
            print(f"  {m}")
        print()

    all_posts = []

    for page_num in range(start_page, end_page + 1):
        print(f"Processing page {page_num}/{end_page}...")
        try:
            soup = load_page(page_num, html_dir)
            posts = extract_posts(soup, page_num)

            if not posts:
                print(f"  WARNING: No posts found on page {page_num}, trying fallback...")
                posts = extract_posts_fallback(soup, page_num)

            print(f"  Found {len(posts)} posts")
            all_posts.extend(posts)

        except FileNotFoundError as e:
            print(f"  SKIP: {e}")
            continue
        except Exception as e:
            print(f"  ERROR on page {page_num}: {e}")
            continue

    print(f"\nTotal posts extracted: {len(all_posts)}")

    if not all_posts:
        print("No posts extracted — check that your HTML files are named page01.html … page14.html")
        sys.exit(1)

    # Write output
    if output_mode == 'single':
        output_file = 'lexicon-bestiary-full.md'
        print(f"Writing {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(write_header())
            current_page = None
            for post in all_posts:
                if post['page'] != current_page:
                    current_page = post['page']
                    f.write(f"\n---\n\n## Page {current_page}\n\n")
                f.write(post_to_markdown(post))
                f.write('\n')
        print(f"Done! {output_file} ({os.path.getsize(output_file):,} bytes)")

    else:
        chunk_start = start_page
        while chunk_start <= end_page:
            chunk_end = min(chunk_start + CHUNK_SIZE - 1, end_page)
            chunk_posts = [p for p in all_posts
                           if chunk_start <= p['page'] <= chunk_end]

            if not chunk_posts:
                chunk_start = chunk_end + 1
                continue

            output_file = f'lexicon-bestiary-pages-{chunk_start:02d}-{chunk_end:02d}.md'
            print(f"Writing {output_file} ({len(chunk_posts)} posts)...")
            with open(output_file, 'w', encoding='utf-8') as f:
                if chunk_start == start_page:
                    f.write(write_header())
                current_page = None
                for post in chunk_posts:
                    if post['page'] != current_page:
                        current_page = post['page']
                        f.write(f"\n---\n\n## Page {current_page}\n\n")
                    f.write(post_to_markdown(post))
                    f.write('\n')
            print(f"  {output_file} ({os.path.getsize(output_file):,} bytes)")
            chunk_start = chunk_end + 1

    print("\nComplete!")


if __name__ == '__main__':
    main()
