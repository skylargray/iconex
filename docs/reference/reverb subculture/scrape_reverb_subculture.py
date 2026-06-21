#!/usr/bin/env python3
"""
Scrape the Gearspace "Reverb Subculture" thread and convert to markdown.

Usage:
    pip install requests beautifulsoup4
    python3 scrape_reverb_subculture.py

Output: reverb-subculture-full.md (or chunked into 5-page files)

This fetches all 36 pages, extracts posts, and writes clean markdown.
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import sys
import os

BASE_URL = "https://gearspace.com/board/geekzone/380233-reverb-subculture"
TOTAL_PAGES = 36
CHUNK_SIZE = 5  # pages per output file
DELAY_BETWEEN_PAGES = 2  # seconds, be polite

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}


def get_page_url(page_num):
    if page_num == 1:
        return f"{BASE_URL}.html"
    return f"{BASE_URL}-{page_num}.html"


def fetch_page(page_num, session):
    """Fetch a single page and return BeautifulSoup object."""
    url = get_page_url(page_num)
    print(f"  Fetching page {page_num}: {url}")
    resp = session.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, 'html.parser')


def extract_posts(soup, page_num):
    """Extract all posts from a page's HTML."""
    posts = []

    # Find all post containers - they're in table rows with id="post_NNNN"
    post_divs = soup.find_all('div', id=re.compile(r'^post_\d+'))

    # Alternative: look for the post table structure
    if not post_divs:
        post_divs = soup.find_all('div', id=re.compile(r'^post_message_\d+'))

    # Try yet another approach - find post count links
    post_links = soup.find_all('a', href=re.compile(r'postcount=\d+'))

    # Build posts from the page structure
    # The page has posts in <table> elements with specific classes
    # Let's look for post content more carefully

    # Find all elements with id starting with "post_message_"
    post_messages = soup.find_all('div', id=re.compile(r'^post_message_\d+'))

    if not post_messages:
        # Try finding posts by the post number links
        # Each post has a link like showpost.php?p=NNNNN&postcount=NN
        pass

    # Let's try a more robust approach using the page structure
    # Posts are typically in <li> or <div> elements with post-related IDs

    # Look for the main content area
    posts_area = soup.find('div', id='posts') or soup.find('ol', id='posts')

    if posts_area:
        # Find individual post containers
        post_containers = posts_area.find_all(['li', 'div', 'table'],
                                               recursive=False)
    else:
        # Fallback: find all elements with post IDs
        post_containers = soup.find_all(
            lambda tag: tag.get('id', '').startswith('post_') and
                       not tag.get('id', '').startswith('post_message_')
        )

    for container in post_containers:
        post = extract_single_post(container, page_num)
        if post:
            posts.append(post)

    # If we still don't have posts, try the post_message approach
    if not posts:
        posts = extract_posts_fallback(soup, page_num)

    return posts


def extract_single_post(container, page_num):
    """Extract data from a single post container."""
    post = {}

    # Get post number
    post_link = container.find('a', href=re.compile(r'postcount=(\d+)'))
    if post_link:
        match = re.search(r'postcount=(\d+)', post_link['href'])
        if match:
            post['num'] = int(match.group(1))
    else:
        return None

    post['page'] = page_num

    # Get post ID for the link
    post_id_match = re.search(r'p=(\d+)', post_link.get('href', ''))
    post['link'] = post_link['href'] if post_link else ''
    if post_id_match:
        post['link'] = f"https://gearspace.com/board/showpost.php?p={post_id_match.group(1)}&postcount={post['num']}"

    # Get username
    username_elem = container.find('a', class_='bigusername') or \
                    container.find('a', href=re.compile(r'member\.php'))
    if username_elem:
        post['username'] = username_elem.get_text(strip=True)
    else:
        # Try finding username in other ways
        user_info = container.find('div', class_=re.compile(r'user'))
        post['username'] = user_info.get_text(strip=True)[:50] if user_info else 'Unknown'

    # Get user title/role
    user_title = container.find('div', class_='usertitle') or \
                 container.find('span', class_='usertitle')
    post['role'] = user_title.get_text(strip=True) if user_title else ''

    # Get date
    date_elem = container.find('td', class_='thead') or \
                container.find('span', class_='date') or \
                container.find('div', class_='postdate')
    if date_elem:
        date_text = date_elem.get_text(strip=True)
        # Clean up date text
        date_text = re.sub(r'#\d+', '', date_text).strip()
        date_text = re.sub(r'\s+', ' ', date_text)
        post['date'] = date_text
    else:
        post['date'] = 'Unknown'

    # Get user join info
    join_info = container.find(string=re.compile(r'Joined:'))
    post['joined'] = ''
    if join_info:
        parent = join_info.parent
        if parent:
            post['joined'] = parent.get_text(strip=True)

    posts_info = container.find(string=re.compile(r'Posts:'))
    post['posts_count'] = ''
    if posts_info:
        parent = posts_info.parent
        if parent:
            post['posts_count'] = parent.get_text(strip=True)

    # Get post content
    msg_div = container.find('div', id=re.compile(r'^post_message_'))
    if msg_div:
        post['content'] = html_to_markdown(msg_div)
    else:
        # Try blockquote or other content containers
        content_area = container.find('div', class_=re.compile(r'content|message'))
        post['content'] = html_to_markdown(content_area) if content_area else ''

    return post if post.get('content') else None


def extract_posts_fallback(soup, page_num):
    """Fallback post extraction using text patterns."""
    posts = []

    # Find all post message divs
    msg_divs = soup.find_all('div', id=re.compile(r'^post_message_'))

    for msg_div in msg_divs:
        post_id_match = re.search(r'post_message_(\d+)', msg_div.get('id', ''))
        if not post_id_match:
            continue

        post_id = post_id_match.group(1)
        post = {'page': page_num}

        # Find the post count
        count_link = soup.find('a', href=re.compile(f'p={post_id}&postcount='))
        if count_link:
            count_match = re.search(r'postcount=(\d+)', count_link['href'])
            post['num'] = int(count_match.group(1)) if count_match else 0
        else:
            # Try to find it nearby
            count_link = soup.find('a', id=f'postcount{post_id}')
            if count_link:
                post['num'] = int(count_link.get_text(strip=True))
            else:
                continue

        post['link'] = f"https://gearspace.com/board/showpost.php?p={post_id}&postcount={post['num']}"

        # Walk up to find the parent post container
        parent = msg_div
        for _ in range(10):
            parent = parent.parent
            if parent is None:
                break
            if parent.get('id', '').startswith('post_'):
                break

        # Username
        if parent:
            user_link = parent.find('a', class_='bigusername')
            if not user_link:
                user_link = parent.find('a', href=re.compile(r'member\.php\?u='))
            post['username'] = user_link.get_text(strip=True) if user_link else 'Unknown'

            # Role
            user_title = parent.find('div', class_='usertitle')
            post['role'] = user_title.get_text(strip=True) if user_title else ''

            # Date - look for date in the post header
            date_cell = parent.find('td', class_='thead')
            if date_cell:
                date_text = date_cell.get_text(strip=True)
                date_text = re.sub(r'#\d+.*$', '', date_text).strip()
                post['date'] = date_text
            else:
                post['date'] = 'Unknown'

            # Join info
            join_elem = parent.find(string=re.compile(r'Joined:'))
            post['joined'] = join_elem.parent.get_text(strip=True) if join_elem and join_elem.parent else ''

            posts_elem = parent.find(string=re.compile(r'Posts:\s*[\d,]+'))
            post['posts_count'] = posts_elem.parent.get_text(strip=True) if posts_elem and posts_elem.parent else ''
        else:
            post['username'] = 'Unknown'
            post['role'] = ''
            post['date'] = 'Unknown'
            post['joined'] = ''
            post['posts_count'] = ''

        # Content
        post['content'] = html_to_markdown(msg_div)

        posts.append(post)

    # Sort by post number
    posts.sort(key=lambda p: p.get('num', 0))
    return posts


def html_to_markdown(elem):
    """Convert an HTML element to clean markdown."""
    if elem is None:
        return ''

    result = []

    for child in elem.children:
        if isinstance(child, str):
            text = child
            # Don't strip internal whitespace completely
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
                # Clean up relative URLs
                if href.startswith('/'):
                    href = f'https://gearspace.com{href}'
                result.append(f'[{text}]({href})')
            elif text:
                result.append(text)

        elif tag == 'img':
            src = child.get('src', '')
            alt = child.get('alt', '')
            title = child.get('title', '')
            # Skip smileys
            if 'smilies' in src or 'smiley' in (alt + title).lower():
                continue
            if src:
                if src.startswith('/'):
                    src = f'https://gearspace.com{src}'
                result.append(f'![{alt or title}]({src})')

        elif tag == 'div':
            classes = ' '.join(child.get('class', []))
            if 'quote' in classes or 'bbcode_container' in classes:
                # Handle quotes
                quote_text = child.get_text(strip=True)
                # Try to extract the "Originally Posted by" header
                quote_header = child.find('div', class_=re.compile(r'quote_container|bbcode_postedby'))
                if quote_header:
                    header_text = quote_header.get_text(strip=True)
                    # Remove header from quote text
                    body = child.find('div', class_=re.compile(r'message|quote_container'))
                    if body:
                        quote_text = body.get_text(strip=True)
                    result.append(f'\n> {header_text}\n')
                    for line in quote_text.split('\n'):
                        line = line.strip()
                        if line:
                            result.append(f'> {line}\n')
                else:
                    for line in quote_text.split('\n'):
                        line = line.strip()
                        if line:
                            result.append(f'> {line}\n')
                result.append('\n')
            else:
                result.append(html_to_markdown(child))

        elif tag == 'table':
            # Quotes are sometimes in tables
            result.append(html_to_markdown(child))

        elif tag == 'td':
            result.append(html_to_markdown(child))

        elif tag == 'tr':
            result.append(html_to_markdown(child))

        elif tag in ('p', 'blockquote'):
            text = html_to_markdown(child)
            if text.strip():
                result.append(f'\n{text}\n')

        elif tag == 'pre' or tag == 'code':
            text = child.get_text()
            result.append(f'\n```\n{text}\n```\n')

        elif tag in ('ul', 'ol'):
            for li in child.find_all('li'):
                text = li.get_text(strip=True)
                result.append(f'- {text}\n')

        elif tag == 'hr':
            result.append('\n---\n')

        else:
            # For other tags, recurse
            result.append(html_to_markdown(child))

    text = ''.join(result)
    # Clean up excessive newlines
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    return text.strip()


def post_to_markdown(post):
    """Convert a single post dict to markdown string."""
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
    """Write the file header."""
    return """# Reverb Subculture -- Gearspace GeekZone Thread

**Thread URL:** https://gearspace.com/board/geekzone/380233-reverb-subculture.html
**Forum:** GeekZone @ Gearspace
**Total Pages:** 36 (~1,059 posts)
**Started:** 8th April 2009

A legendary technical thread on algorithmic reverb design, DSP implementation,
and digital audio effects. Features contributions from professional reverb
designers including Casey (Bricasti), Sean Costello (ValhallaDSP), and many
DIY builders.

"""


def main():
    # Parse command line args
    start_page = 1
    end_page = TOTAL_PAGES
    output_mode = 'chunked'  # 'single' or 'chunked'

    if '--single' in sys.argv:
        output_mode = 'single'
    if '--start' in sys.argv:
        idx = sys.argv.index('--start')
        start_page = int(sys.argv[idx + 1])
    if '--end' in sys.argv:
        idx = sys.argv.index('--end')
        end_page = int(sys.argv[idx + 1])

    print(f"Scraping Reverb Subculture thread, pages {start_page}-{end_page}")
    print(f"Output mode: {output_mode}")
    print()

    session = requests.Session()
    all_posts = []

    for page_num in range(start_page, end_page + 1):
        print(f"Processing page {page_num}/{end_page}...")

        try:
            soup = fetch_page(page_num, session)
            posts = extract_posts(soup, page_num)

            if not posts:
                print(f"  WARNING: No posts found on page {page_num}, trying fallback...")
                posts = extract_posts_fallback(soup, page_num)

            print(f"  Found {len(posts)} posts")
            all_posts.extend(posts)

        except Exception as e:
            print(f"  ERROR on page {page_num}: {e}")
            continue

        # Be polite
        if page_num < end_page:
            time.sleep(DELAY_BETWEEN_PAGES)

    print(f"\nTotal posts extracted: {len(all_posts)}")

    # Write output
    if output_mode == 'single':
        output_file = 'reverb-subculture-full.md'
        print(f"Writing to {output_file}...")

        with open(output_file, 'w') as f:
            f.write(write_header())

            current_page = None
            for post in all_posts:
                if post['page'] != current_page:
                    current_page = post['page']
                    f.write(f"\n---\n\n## Page {current_page}\n\n")
                f.write(post_to_markdown(post))
                f.write('\n')

        size = os.path.getsize(output_file)
        print(f"Done! {output_file} ({size:,} bytes)")

    else:
        # Chunked output
        chunk_start = start_page
        while chunk_start <= end_page:
            chunk_end = min(chunk_start + CHUNK_SIZE - 1, end_page)
            chunk_posts = [p for p in all_posts
                          if chunk_start <= p['page'] <= chunk_end]

            if not chunk_posts:
                chunk_start = chunk_end + 1
                continue

            output_file = f'reverb-subculture-pages-{chunk_start:02d}-{chunk_end:02d}.md'
            print(f"Writing {output_file} ({len(chunk_posts)} posts)...")

            with open(output_file, 'w') as f:
                if chunk_start == start_page:
                    f.write(write_header())

                current_page = None
                for post in chunk_posts:
                    if post['page'] != current_page:
                        current_page = post['page']
                        f.write(f"\n---\n\n## Page {current_page}\n\n")
                    f.write(post_to_markdown(post))
                    f.write('\n')

            size = os.path.getsize(output_file)
            print(f"  {output_file} ({size:,} bytes)")

            chunk_start = chunk_end + 1

    print("\nComplete!")


if __name__ == '__main__':
    main()
