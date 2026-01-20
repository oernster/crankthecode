---
title: "Stellody"
date: "2026-01-19 13:45"
tags: ["Stellody", "stellar", "melody", "curated", "Sub-Genres", "music", "playlists", "music library", "spotify", "python"]
blurb: "Music playlists"
one_liner: "A cross-platform app that analyses your library (or Spotify) and generates genre-sorted playlists."

# Used by the site as the cover image AND by the RSS feed thumbnail.
# It will NOT be duplicated in the post body (the renderer strips a matching standalone image paragraph).
image: /static/images/stellody.png
thumb_image: /static/images/stellody-icon.png

extra_images:
  - /static/images/stellody-installer.png
  - /static/images/stellody-options.png
  - /static/images/stellody-playlists.png
  - /static/images/stellody-formats.png
---

[Stellody live site](https://www.stellody.com)

## Problem → Solution → Impact

**Problem:** Music playlist generators often lack emotional logic and harmonic context, resulting in disjointed or bland playback experiences.

**Solution:** Stellody uses sentiment-aware sequencing and custom logic to generate harmonically coherent playlists with smoother transitions and thematic flow.

**Impact:** Delivers a more immersive listening experience and demonstrates the intersection of music theory, emotional modeling, and automation.

# Rationale
I wanted to discover new music based on my local 5k track library of FLAC music.  However, I wanted it to be curated to my personal tastes rather than the 
generic categorisations that Spotify chucks at you.  So this was initially a personal project that I ended up productizing and publishing on the internet.
It is fully featured now and even allows you to use existing playlists you've created rather than your local library to discover new music.

I spent just over a year writing Stellody.
It's the piece of work I'm most proud of and my crowning glory of a fully deployed app!

# Challenges along the way
Creating an app this large took time and perseverance and a LOT of caffeine and patience.
Related artists curated from the musicbrainz API using multiple lookup techniques was NOT straightforward!
Then creating alphabetically sorted custom curated sub-genre labelled playlists on top of that with sufficient artists 
in each playlist pool was another fight altogether.
The UI, since I'm not really a UI developer, I'm more of a backend dev, is something of which I'm particularly proud.
That took a lot of time and effort to curate and make appear like a beautiful professional app.
Then there was the installer with a custom curated UI; I even added light and dark modes to the installer AS WELL as Stellody as a subtle flex!!!
Then there was licensing so all my hard work can't be stolen by the average noob; I think I got that down pat or at least *I hope so*.
I think I've priced it reasonably for all license tiers and capabilities; not expensive, not free. 

# Overview
Stellody is a play on words; Stellar and Melody.

Start with a local music folder or your Spotify playlists.
Stellody analyses your artists, finds similar ones, and works out the genres they belong to.
Then it generates ready-made playlists directly in Spotify — neatly sorted by genre (works with Spotify Free or Premium).

Spotify playlist mode: your playlists are retrieved automatically — no manual importing.

Deezer support is built, but currently disabled due to Deezer API restrictions.
When it’s finished, just check Spotify for your new playlists. Not on Spotify? The in-app guide explains how to transfer playlists to other services.

Runs locally — your music files never leave your computer. We only create playlists in Spotify.

It runs on Windows, Linux and MacOS.

# Why Stellody? 🌟🎶

<div class="stellody-competition">
  <style>
    .stellody-competition {
      background-color: #083c9c;
      color: #fdf5c4;
      font-family: Helvetica, sans-serif;
      line-height: 1.6;
      padding: 2rem;
      border-radius: 12px;
      margin-top: 1.5rem;
    }
    .stellody-competition h1,
    .stellody-competition h2,
    .stellody-competition h3 {
      color: #fdf5c4;
      font-weight: 700;
      margin: 0;
    }
    .stellody-competition h1 {
      font-size: 2.5rem;
      margin-bottom: 1em;
    }
    .stellody-competition h2 {
      font-size: 2rem;
      margin-top: 2em;
      display: flex;
      align-items: center;
      gap: 0.5em;
    }
    .stellody-competition .content-wrapper {
      display: flex;
      flex-wrap: wrap;
      gap: 2rem;
    }
    .stellody-competition .features-list,
    .stellody-competition .intro-text {
      flex: 1 1 45%;
      min-width: 300px;
    }
    .stellody-competition ul.feature-list {
      list-style: square;
      padding-left: 1.5em;
      color: #fff;
    }
    .stellody-competition ul.feature-list li {
      margin-bottom: 1em;
    }
    .stellody-competition blockquote {
      border-left: 4px solid #ffc875;
      padding-left: 1em;
      font-style: italic;
      margin: 2em 0;
      color: #a6f6c1 !important; /* FORCE light green */
    }
    .stellody-competition blockquote strong {
      color: #ffc875 !important; /* FORCE orange for strong */
    }
    .stellody-competition footer {
      margin-top: 3em;
      font-size: 0.9rem;
      color: #ddd;
    }
    .stellody-competition a {
      color: #8be9fd;
      text-decoration: none;
    }
    .stellody-competition a:hover {
      text-decoration: underline;
    }
  </style>

  <main>
    <h1>🎧 Stellody vs The Competition</h1>
    <div class="intro-text">
      <p>
        There’s no shortage of so-called “AI playlist generators” online. Most of them offer a mash of buzzwords,
        vague mood sliders, and surface-level Spotify integration.
      </p>
      <p>
        Let’s stroll through the actual landscape of <strong>Stellody’s competition</strong> — and why Stellody isn’t just
        better. It’s in a <strong>category of its own</strong>.
      </p>
    </div>

    <h2>✨ Stellody’s Capabilities</h2>
    <ul class="feature-list">
      <li><strong>Dual Source Support:</strong> Start with either your local music folder or your existing Spotify playlists.</li>
      <li><strong>Genre Filtering:</strong> Pick exactly which genre families to include — from Metal and Jazz to Pop, Hip Hop, and Ambient.</li>
      <li><strong>Goal Year Range Control:</strong> Specify a target minimum and maximum year. Stellody aims to prioritise that range while keeping playlists diverse.</li>
      <li><strong>Subgenre Awareness:</strong> Stellody understands real music taxonomy — from <em>Cloud Rap</em> to <em>Nu Metal</em> to <em>Baroque Pop</em>.</li>
      <li><strong>Privacy First:</strong> Your files never leave your machine. Stellody runs locally, using Spotify only for playlist creation.</li>
      <li><strong>Spotify + MusicBrainz Integration:</strong> Enriches classification using artist metadata — not guesswork.</li>
      <li><strong>Cross-Platform:</strong> Available for Windows, macOS, and Linux — with proper installers and versioning.</li>
      <li><strong>Professional Licensing:</strong> Demo, Standard, and Pro tiers — all built into the app with no online account required.</li>
    </ul>

    <h2>💀 The Competitor Roast</h2>
    <ul class="feature-list">
      <li>
        <strong>Musely / Spotify Playlist Maker:</strong> You type in a theme like “Summer Vibes.”
        <br><em>Roast:</em> "Musely: Because who doesn’t want a sponsored mood mixtape when they could have precise genre control?"
      </li>
      <li>
        <strong>Playlistable.io:</strong> AI playlist building based on your listening history.
        <br><em>Roast:</em> "Playlistable: Perfect if you want Spotify to echo your existing taste — again."
      </li>
      <li>
        <strong>Chosic & Similar:</strong> Artist or keyword input gets you genre soup.
        <br><em>Roast:</em> "Chosic: For when AI guesses genres like a confused game show host."
      </li>
      <li>
        <strong>Spotivibly, SpotiPlay, Vondy:</strong> Pick a mood, get a playlist.
        <br><em>Roast:</em> "Spotivibly: Fast playlists with the emotional depth of a fortune cookie."
      </li>
      <li>
        <strong>Mixider:</strong> Mixes songs from multiple platforms.
        <br><em>Roast:</em> "Mixider: A DJ simulator for people who think drag-and-drop fixes metadata."
      </li>
    </ul>

    <h2>🏆 Final Summary</h2>
    <blockquote style="color:lightgreen;">
      <strong>"Most playlist generators:"</strong> Tell users what they vaguely want, hit Spotify’s API, and hope no one notices they’ve heard it all before.<br>
      <strong>"Stellody:"</strong> Classifies local music with precision. Builds genre-separated playlists. Keeps data private. Respects taste.
    </blockquote>

    <footer>
      Still not convinced?
      <strong><a href="https://www.stellody.com/change-log">See the changelog</a></strong> or explore
      <strong><a href="https://www.stellody.com/">Stellody’s homepage</a></strong> to try it yourself.<br>
      Built by someone who actually listens — and owns a 5k library of musical tracks.
    </footer>
  </main>
</div>

