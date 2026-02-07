---
date: 2026-02-07 14:30
emoji: "\U0001F9E9"
one_liner: Effective management of the crankthecode website.
tags:
- cat:Blog
- tag
- fastapi
- tagging
- organisation
title: Automating tagging in crankthecode for menu organisation
---

# Tag to menu item organisation automation

This was a simple change to the crankthecode website. It is a backend change but it makes my life easier.

Basically, to summarise, I have made the code use the tags in blog and non-blog posts to automatically match their menu item counterparts in the UI.

To do this I created a tagging system, slightly enhancing what I had already with a prefix of 'cat:' for a category.  e.g. 'cat:blog' or 'cat:Tools'
which is case insensitive; though the left menu items on the front page of the UI remain correctly cased.

This means I can simply post new markdown files as I choose without any additional coding friction going forward.

The 'All posts' menu item still excludes blog posts by default but I have added a specific blog posts toggle button in case a viewer wants full visibility.

Lastly, I have added a UI enhancement that only displays the 1st five posts by default once you click through from any menu item on the landing page.  There is a 'More...' button to expand for more posts.

No more hassle updating HTML files.

JOY!

*-A nice tidy refactoring upgrade.*