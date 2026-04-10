---
blurb: Calendar tool
date: 2026-01-19 06:35
type: project
extra_images:
- /static/images/calendifier-ha.png
image: /static/images/calendifier.png
one_liner: A calendar app with full iCalendar (RFC5545) support and deep internationalisation
  across languages and locales.
social_image: /static/images/calendifier.png
tags:
- cat:Desktop Apps
- calendar
- event
- events
- RFC5545
- notes
- internationalisation
- clock
- python
title: Calendifier
---

# Calendifier  📅

## Problem → Solution → Impact

**Problem:** Implementing RFC-compliant calendars manually is tedious and error-prone.

**Solution:** Calendifier parses and generates RFC5545 calendar formats for event management.

**Impact:** Scheduling features stopped drifting out of sync with real dates and edge cases, so shipping calendar-dependent behaviour became predictable.

# Rationale
I wanted a fun project that created a next-gen calendar for both desktop and Home Assistant.
I then wanted to make it fully featured with an NTP synchronised digital/analogue clock, with full and effective 
support for eventing.  Then I fancied adding in some additional features so for extra fun and defiance I wrote in 
functionality for locale specific holidays.  As a final coup de grace, I made it fully internationlised for a large 
number of locales around the world in foreign languages/numbering standards; that, by the way, was freaking HARD! 


# Challenges along the way
A standards-compliant calendar backend. RFC5545? I *hardly* knew her.
The main app was HARD due to internationalisation; this was my first foray into internationalising an app and I did it 
for BOTH a browser AND home assistant dashboard cards.

Another really difficult thing for me was not only identifying holidays for locales which aren't British but making them 
appear correctly on the UI depending on the locale selected.
However, aside from the aforementioned internationalisation support challenges, I really struggled through writing code to support
RFC5545 which is basically the official canonical way to support Eventing in a Calendar application.  I got there in the end though
and I feel the UI is relatively intuitive for this purpose.

[Releases](https://github.com/oernster/Calendifier/releases)

## 🌟 Overview

**Calendifier** is a sophisticated calendar system available in two deployment modes:

1. **🖥️ Desktop Application** - Cross-platform desktop calendar built with Python and PySide6
2. **🏠 Home Assistant Integration** - Web-based dashboard cards for Home Assistant with beautiful UI

Both versions feature comprehensive internationalisation supporting **40 languages** and **40 countries**, making it a truly global calendar solution.
One huge takeaway I had from this piece of work was that internationalisation is an incredibly HARD thing to implement!

### ✨ Key Features

- 📅 **Full Calendar Management** - Monthly view with intuitive navigation
- 🌍 **40-Language Support** - Complete localisation with runtime language switching
- 🏳️ **40-Country Holiday Support** - Intelligent holiday detection with native translations
- 🕐 **Real-time Analog Clock** - NTP synchronisation for accurate timekeeping
- 📝 **Comprehensive Event Management** - Create, edit, delete with categories and recurring events
- 🎨 **Dynamic Theming** - Dark/Light mode with instant switching
- 📝 **Integrated Notes** - Built-in note-taking functionality
- 📤📥 **Import/Export** - Support for iCalendar, CSV and JSON formats
- ⚙️ **Extensive Configuration** - Customisable settings for all preferences

## 🌍 International Support

### 🗣️ Supported Languages

| Code | Language | Notes |
|---:|---|---|
| usgb | 🇺🇸🇬🇧 English | US & UK variants |
| ca | 🇨🇦 Français (Québec) | Quebec French |
| es | 🇪🇸 Català | Catalan |
| es | 🇪🇸 Español | Spanish |
| fr | 🇫🇷 Français | French |
| de | 🇩🇪 Deutsch | German |
| it | 🇮🇹 Italiano | Italian |
| br | 🇧🇷 Português | Brazilian Portuguese |
| pt | 🇵🇹 Português | Portuguese |
| ru | 🇷🇺 Русский | Russian |
| cn | 🇨🇳 简体中文 | Simplified Chinese |
| tw | 🇹🇼 繁體中文 | Traditional Chinese |
| jp | 🇯🇵 日本語 | Japanese |
| kr | 🇰🇷 한국어 | Korean |
| in | 🇮🇳 हिन्दी | Hindi |
| sa | 🇸🇦 العربية | Arabic |
| cz | 🇨🇿 Čeština | Czech |
| se | 🇸🇪 Svenska | Swedish |
| no | 🇳🇴 Norsk | Norwegian |
| dk | 🇩🇰 Dansk | Danish |
| fi | 🇫🇮 Suomi | Finnish |
| nl | 🇳🇱 Nederlands | Dutch |
| pl | 🇵🇱 Polski | Polish |
| tr | 🇹🇷 Türkçe | Turkish |
| ua | 🇺🇦 Українська | Ukrainian |
| gr | 🇬🇷 Ελληνικά | Greek |
| id | 🇮🇩 Bahasa Indonesia | Indonesian |
| vn | 🇻🇳 Tiếng Việt | Vietnamese |
| th | 🇹🇭 ไทย | Thai |
| bg | 🇧🇬 Български | Bulgarian |
| sk | 🇸🇰 Slovenčina | Slovak |
| si | 🇸🇮 Slovenščina | Slovenian |
| hr | 🇭🇷 Hrvatski | Croatian |
| hu | 🇭🇺 Magyar | Hungarian |
| ro | 🇷🇴 Română | Romanian |
| il | 🇮🇱 עברית | Hebrew |
| ee | 🇪🇪 Eesti | Estonian |
| lv | 🇱🇻 Latviešu | Latvian |
| lt | 🇱🇹 Lietuvių | Lithuanian |

### 🏳️ Holiday Support
The application automatically detects and displays holidays for 40 countries with intelligent cultural filtering:

| Code | Country | Holiday set | Supported |
|---:|---|---|:---:|
| us | 🇺🇸 United States | Federal holidays | ✅ |
| ca | 🇨🇦 Canada | Jours fériés / Holidays | ✅ |
| gb | 🇬🇧 United Kingdom | Bank holidays | ✅ |
| es | 🇪🇸 Spain | National holidays | ✅ |
| fr | 🇫🇷 France | Jours fériés | ✅ |
| de | 🇩🇪 Germany | Feiertage | ✅ |
| it | 🇮🇹 Italy | Giorni festivi | ✅ |
| br | 🇧🇷 Brazil | Feriados nacionais | ✅ |
| pt | 🇵🇹 Portugal | Feriados nacionais | ✅ |
| ru | 🇷🇺 Russia | Праздничные дни | ✅ |
| cn | 🇨🇳 China | 法定节假日 | ✅ |
| tw | 🇹🇼 Taiwan | 國定假日 | ✅ |
| jp | 🇯🇵 Japan | 祝日 | ✅ |
| kr | 🇰🇷 South Korea | 공휴일 | ✅ |
| in | 🇮🇳 India | राष्ट्रीय अवकाश | ✅ |
| sa | 🇸🇦 Saudi Arabia | الأعياد الوطنية | ✅ |
| cz | 🇨🇿 Czech Republic | Státní svátky | ✅ |
| se | 🇸🇪 Sweden | Helgdagar | ✅ |
| no | 🇳🇴 Norway | Helligdager | ✅ |
| dk | 🇩🇰 Denmark | Helligdage | ✅ |
| fi | 🇫🇮 Finland | Juhlapäivät | ✅ |
| nl | 🇳🇱 Netherlands | Feestdagen | ✅ |
| pl | 🇵🇱 Poland | Święta państwowe | ✅ |
| tr | 🇹🇷 Turkey | Resmi tatiller | ✅ |
| ua | 🇺🇦 Ukraine | Державні свята | ✅ |
| gr | 🇬🇷 Greece | Εθνικές γιορτές | ✅ |
| id | 🇮🇩 Indonesia | Hari libur nasional | ✅ |
| vn | 🇻🇳 Vietnam | Ngày lễ quốc gia | ✅ |
| th | 🇹🇭 Thailand | วันหยุดราชการ | ✅ |
| bg | 🇧🇬 Bulgaria | Национални praznici | ✅ |
| sk | 🇸🇰 Slovakia | Štátne sviatky | ✅ |
| si | 🇸🇮 Slovenia | Državni prazniki | ✅ |
| hr | 🇭🇷 Croatia | Državni blagdani | ✅ |
| hu | 🇭🇺 Hungary | Nemzeti ünnepek | ✅ |
| ro | 🇷🇴 Romania | Sărbători naționale | ✅ |
| il | 🇮🇱 Israel | חגים לאומיים | ✅ |
| ee | 🇪🇪 Estonia | Riigipühad | ✅ |
| lv | 🇱🇻 Latvia | Valsts svētki | ✅ |
| lt | 🇱🇹 Lithuania | Valstybės šventės | ✅ |

## ✨ Home Assistant Features
- 🎨 **Beautiful Dashboard Cards** - Clock, Calendar, Events, Notes, Settings, Data Management
- 📱 **Responsive Design** - Works on desktop, tablet and mobile
- 🌐 **Web Access** - Access from anywhere on your network
- 🔄 **Auto-Updates** - Cards refresh automatically
- 🎯 **Optimised Layout** - No overlapping, proper spacing

---

## 🖥️ Desktop Application

Traditional desktop application for local use.

### 🎯 First Launch

On first launch, the application will:
- 🔍 **Auto-detect your system locale** and set the appropriate language

- 🏳️ **Match your country** to display relevant holidays

- 🎨 **Apply your system theme** (dark/light mode)

- 📁 **Create user data directory** at `~/.calendar_app/`

### 🌙 Dark Theme

### ☀️ Light Theme

### 🌍 Language Switching

### 📝 Event Management



## 📦 Building & Distribution

Calendifier supports multiple build targets for maximum compatibility across platforms:



### 🖥️ Cross-Platform Executable (Nuitka)

Build a single executable file for Windows, macOS and Linux:



## ⚙️ Configuration



### 🏠 User Data Location

The application stores user data in:
- **Windows:** `%USERPROFILE%\.calendar_app\`
- **macOS:** `~/.calendar_app/`
- **Linux:** `~/.calendar_app/`



### 📁 Configuration Files

- **`settings.json`** - Application preferences
- **`data/calendar.db`** - SQLite database
- **`logs/`** - Application logs
- **`exports/`** - Exported calendar files
- **`backups/`** - Database backups


**Made with ❤️ for the global community**

*Supporting 40 languages and 40 countries worldwide*
